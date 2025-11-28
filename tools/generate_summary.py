#!/usr/bin/env python3
"""Generate a human-friendly summary `ai_reports/summary.md` from ai_reports artifacts."""
from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "ai_reports"
OUT = AI / "summary.md"

summary = ["# Audit Summary\n"]

# header
summary.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}\n")

# load checklist update log
logp = AI / "checklist_update_log.json"
if logp.exists():
    log = json.loads(logp.read_text(encoding='utf-8'))
    summary.append("## Checklist Update Log\n")
    summary.append(f"Applied IDs: {log.get('applied_ids')}\n")
    summary.append(f"Skipped IDs: {list(log.get('skipped_ids', {}).keys())}\n")

# evidence map
emap = AI / "checklist_evidence_map.json"
if emap.exists():
    em = json.loads(emap.read_text(encoding='utf-8'))
    summary.append("## Evidence Map Snapshot\n")
    for k,v in em.get('mappings', {}).items():
        summary.append(f"- {k}: {v.get('status')} — {v.get('rationale')}\n")

# perf results
perf = AI / "perf_results.json"
if perf.exists():
    p = json.loads(perf.read_text(encoding='utf-8'))
    summary.append("## Performance Results\n")
    summary.append(f"Command: {p.get('command')}\n")
    if p.get('mean_seconds'):
        summary.append(f"Mean time: {p.get('mean_seconds'):.6f}s (stdev {p.get('stdev_seconds'):.6f})\n")

# pytest results
junit = AI / "pytest_full_results.xml"
if junit.exists():
    summary.append("## Tests\n")
    # rely on previous junit reading by rule engine; include quick note
    summary.append("Full test results available in `ai_reports/pytest_full_results.xml`.\n")

# determinism
det = AI / "determinism_hashes.txt"
if det.exists():
    summary.append("## Determinism\n")
    summary.append(det.read_text(encoding='utf-8'))

# add pointer to dry run patch
patch = AI / "checklist_patch_dryrun.patch"
if patch.exists():
    summary.append("## Proposed Checklist Patch\n")
    summary.append("See `ai_reports/checklist_patch_dryrun.patch`.\n")

OUT.write_text("\n".join(summary), encoding='utf-8', newline='\n')
print("Wrote", OUT)
