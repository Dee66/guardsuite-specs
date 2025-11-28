#!/usr/bin/env python3
"""
Temporal drift history engine.

Scans `canonical_state/` for drift report and lineage snapshots, treats each
as a timepoint, and builds a deterministic temporal history.

Outputs `canonical_state/drift_history.json` and `canonical_state/drift_history.md`.
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import sys


def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def iso(ts):
    # normalize timestamps
    if not ts:
        return None
    return ts


def discover_snapshots(root: Path):
    cs = root.glob("drift_report*.json")
    reports = []
    for p in sorted(cs):
        try:
            j = load_json(p)
            t = j.get("timestamp") or j.get("generated")
            reports.append({"path": p, "data": j, "timestamp": t})
        except Exception:
            continue

    ls = root.glob("drift_lineage*.json")
    lineages = {}
    for p in sorted(ls):
        try:
            j = load_json(p)
            t = j.get("timestamp") or j.get("generated")
            if t:
                lineages[t] = {"path": p, "data": j}
            else:
                lineages[p.name] = {"path": p, "data": j}
        except Exception:
            continue

    # build timepoints: pair report with lineage when timestamps match
    timepoints = []
    for r in reports:
        t = r["timestamp"]
        lp = lineages.get(t)
        timepoints.append({"timestamp": t, "report": r, "lineage": lp})

    # sort by timestamp (asc) then by report path
    def keyfn(tp):
        return (tp["timestamp"] or "", str(tp["report"]["path"]))

    timepoints.sort(key=keyfn)
    return timepoints


def build_per_file_timeline(timepoints):
    files = {}
    for tp in timepoints:
        t = tp["timestamp"]
        rpt = tp["report"]["data"]
        details = rpt.get("details", {})
        for state in ("added", "removed", "changed", "unchanged"):
            for p in sorted(details.get(state, [])):
                ent = files.setdefault(p, {"timeline": []})
                lc = None
                if tp.get("lineage") and tp["lineage"]["data"].get("files", {}).get(p):
                    lc = (
                        tp["lineage"]["data"]["files"][p].get("lineage_confidence")
                        if isinstance(tp["lineage"]["data"]["files"][p], dict)
                        else None
                    )
                ent["timeline"].append(
                    {"timestamp": t, "state": state, "lineage_confidence": lc}
                )
    # sort timelines by timestamp
    for p in files:
        files[p]["timeline"].sort(key=lambda e: (e["timestamp"] or ""))
    return dict(sorted(files.items()))


def build_per_product_timeline(manifest, files_timeline):
    products = {p["id"]: {"timeline": []} for p in manifest.get("products", [])}
    # map file -> owners using manifest current view
    file_to_owners = {}
    for p in manifest.get("products", []):
        pid = p.get("id")
        root = p.get("paths", {}).get("root")
        for f in files_timeline:
            if root and f.startswith(root):
                file_to_owners.setdefault(f, []).append(pid)
        # also check explicit rule_spec paths
        for rs in p.get("rule_specs", []):
            rp = rs.get("path")
            if rp:
                file_to_owners.setdefault(rp, []).append(pid)

    # gather time-ordered list of timestamps
    timepoints = sorted(
        {
            e["timestamp"]
            for v in files_timeline.values()
            for e in v["timeline"]
            if e.get("timestamp")
        }
    )
    for ts in timepoints:
        per_prod_counts = {
            pid: {"changed": 0, "added": 0, "removed": 0} for pid in products
        }
        for f, v in files_timeline.items():
            for ev in v["timeline"]:
                if ev.get("timestamp") != ts:
                    continue
                owners = file_to_owners.get(f, [])
                for o in owners:
                    if ev["state"] == "changed":
                        per_prod_counts[o]["changed"] += 1
                    if ev["state"] == "added":
                        per_prod_counts[o]["added"] += 1
                    if ev["state"] == "removed":
                        per_prod_counts[o]["removed"] += 1
        for pid in products:
            products[pid]["timeline"].append(
                {
                    "timestamp": ts,
                    "changed": per_prod_counts[pid]["changed"],
                    "added": per_prod_counts[pid]["added"],
                    "removed": per_prod_counts[pid]["removed"],
                }
            )

    # sort products keys
    return dict(sorted(products.items()))


def main(argv):
    root = Path("canonical_state")
    timepoints = discover_snapshots(root)
    manifest = {}
    try:
        manifest = load_json(root / "guard_suite_state.json")
    except Exception:
        manifest = {}

    files_timeline = build_per_file_timeline(timepoints)
    per_product = build_per_product_timeline(manifest, files_timeline)

    out = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "timepoints": [
            {
                "timestamp": tp["timestamp"],
                "report_path": str(tp["report"]["path"]),
                "lineage_path": (
                    str(tp["lineage"]["path"]) if tp.get("lineage") else None
                ),
            }
            for tp in timepoints
        ],
        "per_file": files_timeline,
        "per_product": per_product,
    }

    outpath = root / "drift_history.json"
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, sort_keys=True)

    # markdown companion
    mdpath = root / "drift_history.md"
    ts = out["generated"]
    lines = [
        "# GuardSuite Temporal Drift History",
        f"**Generated:** {ts}",
        "",
        "This document summarizes long-range drift events across all known snapshots. See `drift_history.json` for full machine-readable details.",
    ]
    with mdpath.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    print("WROTE", outpath, "and", mdpath)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
