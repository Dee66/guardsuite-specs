#!/usr/bin/env python3
"""
Drift alert engine.

Reads `canonical_state/drift_history.json` and applies configurable budgets
to produce alert reports in JSON and Markdown.

Write-only outputs:
 - canonical_state/drift_alerts.json
 - canonical_state/drift_alerts.md

All ordering deterministic (sorted keys, product ASC, file ASC).
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import sys


# Configurable budgets (defaults as requested)
DEFAULT_PER_PRODUCT = 5
DEFAULT_PER_FILE = 3
CONFIDENCE_REGRESSION_DROP = 0.15
DRIFT_SPIKE_THRESHOLD = 2


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def analyze(history, budgets=None):
    budgets = budgets or {}
    per_product_budget = budgets.get("per_product", DEFAULT_PER_PRODUCT)
    per_file_budget = budgets.get("per_file", DEFAULT_PER_FILE)
    conf_drop = budgets.get("confidence_regression_drop", CONFIDENCE_REGRESSION_DROP)
    spike_thr = budgets.get("drift_spike_threshold", DRIFT_SPIKE_THRESHOLD)

    timepoints = history.get("timepoints", [])
    per_file = history.get("per_file", {})
    per_product = history.get("per_product", {})

    # PRODUCT-LEVEL ALERTS: sum events across timeline for each product
    product_alerts = []
    for prod in sorted(per_product.keys()):
        timeline = per_product[prod].get("timeline", [])
        total_events = sum(
            (t.get("changed", 0) + t.get("added", 0) + t.get("removed", 0))
            for t in timeline
        )
        if total_events > per_product_budget:
            product_alerts.append(
                {
                    "product": prod,
                    "total_events": total_events,
                    "budget": per_product_budget,
                }
            )

    # FILE-LEVEL ALERTS: count events per file across timeline
    file_alerts = []
    for f in sorted(per_file.keys()):
        timeline = per_file[f].get("timeline", [])
        event_count = sum(
            1 for e in timeline if e.get("state") in ("changed", "added", "removed")
        )
        if event_count > per_file_budget:
            file_alerts.append(
                {"path": f, "event_count": event_count, "budget": per_file_budget}
            )

    # CONFIDENCE REGRESSION: detect drops between consecutive timeline entries per file
    confidence_regressions = []
    for f in sorted(per_file.keys()):
        entries = per_file[f].get("timeline", [])
        # gather numeric confidences in time order
        prev = None
        for e in entries:
            c = e.get("lineage_confidence")
            # skip None
            if c is None:
                prev = None
                continue
            try:
                c = float(c)
            except Exception:
                prev = None
                continue
            if prev is not None:
                if prev - c > conf_drop:
                    confidence_regressions.append(
                        {
                            "path": f,
                            "from": prev,
                            "to": c,
                            "drop": prev - c,
                            "timestamp": e.get("timestamp"),
                        }
                    )
            prev = c

    # DRIFT SPIKES: compute total events per timepoint across all files and find spikes
    # First collect ordered timestamps
    timestamps = []
    for tp in timepoints:
        ts = tp.get("timestamp")
        if ts:
            timestamps.append(ts)
    timestamps = sorted(list(dict.fromkeys(timestamps)))

    events_by_ts = {ts: 0 for ts in timestamps}
    # iterate files and their events
    for f, v in per_file.items():
        for e in v.get("timeline", []):
            ts = e.get("timestamp")
            if ts and e.get("state") in ("changed", "added", "removed"):
                events_by_ts[ts] = events_by_ts.get(ts, 0) + 1

    spike_alerts = []
    if timestamps:
        prev_count = None
        for ts in timestamps:
            cnt = events_by_ts.get(ts, 0)
            if prev_count is not None:
                delta = cnt - prev_count
                if delta >= spike_thr:
                    spike_alerts.append(
                        {
                            "timestamp": ts,
                            "events": cnt,
                            "previous_events": prev_count,
                            "delta": delta,
                            "threshold": spike_thr,
                        }
                    )
            prev_count = cnt

    out = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "budgets": {
            "per_product": per_product_budget,
            "per_file": per_file_budget,
            "confidence_regression_drop": conf_drop,
            "drift_spike_threshold": spike_thr,
        },
        "summary": {
            "product_alerts": len(product_alerts),
            "file_alerts": len(file_alerts),
            "confidence_regressions": len(confidence_regressions),
            "spike_alerts": len(spike_alerts),
        },
        "product_alerts": sorted(product_alerts, key=lambda x: x["product"]),
        "file_alerts": sorted(file_alerts, key=lambda x: x["path"]),
        "confidence_regressions": sorted(
            confidence_regressions,
            key=lambda x: (x.get("path"), x.get("timestamp") or ""),
        ),
        "spike_alerts": sorted(spike_alerts, key=lambda x: x["timestamp"]),
    }
    return out


def write_md(path: Path, report):
    ts = report.get("generated")
    lines = [
        "# GuardSuite Drift Alert Report",
        f"**Generated:** {ts}",
        "",
        "## Summary",
        f"- Product alerts: {report['summary']['product_alerts']}",
        f"- File alerts: {report['summary']['file_alerts']}",
        f"- Confidence regressions: {report['summary']['confidence_regressions']}",
        f"- Spike alerts: {report['summary']['spike_alerts']}",
        "",
        "## Product Alerts",
    ]
    for p in report["product_alerts"]:
        lines.append(
            f"- {p['product']}: {p['total_events']} events (budget {p['budget']})"
        )
    lines.append("")
    lines.append("## File Alerts")
    for f in report["file_alerts"]:
        lines.append(f"- {f['path']}: {f['event_count']} events (budget {f['budget']})")
    lines.append("")
    lines.append("## Confidence Regressions")
    for c in report["confidence_regressions"]:
        lines.append(
            f"- {c['path']}: {c['from']} -> {c['to']} (drop {c['drop']}) at {c.get('timestamp')}"
        )
    lines.append("")
    lines.append("## Spike Alerts")
    for s in report["spike_alerts"]:
        lines.append(
            f"- {s['timestamp']}: {s['events']} events (prev {s['previous_events']}, delta {s['delta']})"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def main(argv):
    root = Path("canonical_state")
    hist_path = root / "drift_history.json"
    if not hist_path.exists():
        print("drift_history.json not found in canonical_state/", file=sys.stderr)
        return 2
    history = load_json(hist_path)
    report = analyze(history)

    outjson = root / "drift_alerts.json"
    with outjson.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, sort_keys=True)

    outmd = root / "drift_alerts.md"
    write_md(outmd, report)
    print("WROTE", outjson, "and", outmd)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
