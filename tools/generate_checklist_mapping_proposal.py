#!/usr/bin/env python3
"""Generate a proposed mapping file for checklist updates.

Outputs:
- `tools/checklist_mapping_proposed.json`: mapping {suggestion_id: token}
- `ai_reports/checklist_mapping_proposal.json`: detailed proposals with matched lines and confidence

Uses conservative heuristics to find the best checklist line for each suggestion.
"""
import json
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "products" / "computeguard" / "checklist" / "checklist.md"
EVIDENCE_MAP = ROOT / "ai_reports" / "checklist_evidence_map.json"
DRYRUN = ROOT / "ai_reports" / "checklist_update_dryrun.json"
OUT_SIMPLE = ROOT / "tools" / "checklist_mapping_proposed.json"
OUT_DETAILED = ROOT / "ai_reports" / "checklist_mapping_proposal.json"


def load_suggestions():
    if DRYRUN.exists():
        j = json.loads(DRYRUN.read_text(encoding="utf-8"))
        return j.get("suggestions", {}).get("suggested_mark_done", [])
    if EVIDENCE_MAP.exists():
        em = json.loads(EVIDENCE_MAP.read_text(encoding="utf-8"))
        return list(em.get("mappings", {}).keys())
    return []


def load_checklist_entries():
    txt = CHECKLIST.read_text(encoding="utf-8")
    lines = txt.splitlines()
    pattern = re.compile(r"^- \[.\] (\w[\w\-]*\d*):?\s*(.*)$")
    entries = []
    for i, l in enumerate(lines):
        m = pattern.match(l)
        if m:
            cid = m.group(1)
            desc = m.group(2)
            entries.append({"index": i, "id": cid, "text": desc, "full": l})
    return entries


def keywords_from_rationale(rationale):
    if not rationale:
        return []
    parts = re.findall(r"[A-Za-z]{3,}", rationale)
    return list(dict.fromkeys(p.lower() for p in parts))


def main():
    suggestions = load_suggestions()
    entries = load_checklist_entries()
    em = json.loads(EVIDENCE_MAP.read_text(encoding="utf-8")) if EVIDENCE_MAP.exists() else {}

    simple = {}
    detailed = {"generated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), "proposals": {}}

    for sid in suggestions:
        info = em.get("mappings", {}).get(sid, {})
        rationale = info.get("rationale", "")
        status = info.get("status")

        candidates = []

        # 1) exact checklist id match
        for e in entries:
            if e["id"].lower() == sid.lower():
                candidates.append((e, 0.99))

        # 2) suggestion id appears in line text
        for e in entries:
            if sid.lower() in e["full"].lower() or sid.lower() in e["text"].lower():
                candidates.append((e, 0.95))

        # 3) keywords from rationale and evidence paths
        kws = keywords_from_rationale(rationale)
        for ev in info.get("evidence", []) if info else []:
            p = ev.get("path")
            if isinstance(p, str):
                # include filename stems
                stem = Path(p).stem
                if stem:
                    kws.append(stem.lower())

        for kw in kws:
            for e in entries:
                if kw in e["full"].lower() or kw in e["text"].lower():
                    candidates.append((e, 0.7))

        # dedupe by id, keep best score
        best = {}
        for e, score in candidates:
            cid = e["id"]
            if cid not in best or score > best[cid][1]:
                best[cid] = (e, score)

        if best:
            chosen, conf = max(best.values(), key=lambda t: t[1])
            token = chosen["id"]
            simple[sid] = token
            detailed["proposals"][sid] = {
                "token": token,
                "confidence": float(conf),
                "matched_line": chosen["full"],
                "status": status,
            }
        else:
            # fallback: use sid itself
            simple[sid] = sid
            detailed["proposals"][sid] = {
                "token": None,
                "confidence": 0.0,
                "matched_line": None,
                "status": status,
            }

    OUT_SIMPLE.write_text(json.dumps(simple, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    OUT_DETAILED.write_text(json.dumps(detailed, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    print("Wrote mapping proposal:", OUT_SIMPLE)
    print("Wrote detailed proposal:", OUT_DETAILED)


if __name__ == "__main__":
    main()
