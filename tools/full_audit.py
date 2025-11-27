#!/usr/bin/env python3
"""Full audit orchestrator.

Stages:
- run collector
- run pytest full suite and adapter tests (capture outputs)
- run pytest 3 times for determinism (normalize outputs and compare)
- run flake8 on adapters
- run rule engine (dry-run) to produce suggestions
- produce a dry-run patch for checklist updates (do not apply)

Outputs:
- ai_reports/* (evidence_summary.json, checklist_evidence_map.json, pytest outputs, adapter outputs, determinism results)
- ai_reports/checklist_update_dryrun.json
- ai_reports/checklist_patch_dryrun.patch
"""
import subprocess
import shutil
import sys
from pathlib import Path
import difflib

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "ai_reports"
TOOLS = ROOT / "tools"

AI.mkdir(parents=True, exist_ok=True)

def run(cmd, cwd=ROOT):
    print("RUN:", cmd)
    p = subprocess.run(cmd, cwd=str(cwd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout

# 1. collector
print("Step 1: running evidence collector")
run(f"{sys.executable} tools/collect_evidence.py")

# 2. run full pytest once (capture fresh) and produce JUnit XML
print("Step 2: running full pytest (with junit xml)")
rc, out = run(f"pytest -q --junitxml={AI / 'pytest_full_results.xml'}")
with open(AI / "pytest_full_run.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write(out)

# If junit xml produced, note it
if (AI / "pytest_full_results.xml").exists():
    print("Wrote JUnit results to ai_reports/pytest_full_results.xml")

# 3. run adapter tests and capture
print("Step 3: running adapter tests (with junit xml)")
rc_a, out_a = run(f"pytest -q strategy_e/adapters/tests -q --junitxml={AI / 'adapter_pytest_results.xml'}")
with open(AI / "adapter_pytest_summary.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write(out_a)
if (AI / "adapter_pytest_results.xml").exists():
    print("Wrote adapter JUnit results to ai_reports/adapter_pytest_results.xml")

# 4. run flake8 on adapters
print("Step 4: running flake8 on adapters")
rc_f, out_f = run("flake8 strategy_e/adapters --max-line-length 88")
with open(AI / "adapters_flake8.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write(out_f)

# 5. determinism: run pytest 3 times and normalize outputs
print("Step 5: determinism runs (pytest x3)")
det_dir = AI / "determinism_runs"
det_dir.mkdir(parents=True, exist_ok=True)
outs = []
for i in range(1,4):
    rc_i, out_i = run("pytest -q")
    p = det_dir / f"pytest_run_{i}.txt"
    p.write_text(out_i, encoding="utf-8", newline="\n")
    outs.append(out_i)

# naive normalization: strip absolute paths and timestamps (very conservative)
def normalize(text):
    import re
    # remove ISO timestamps
    text = re.sub(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", "<TS>", text)
    # remove datetime with timezone
    text = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \+[0-9]{4}", "<TS>", text)
    # collapse long whitespace
    text = re.sub(r"\s+", " ", text)
    # remove file paths (naive: segments containing / and .py)
    text = re.sub(r"[\w\-/.]+\.py", "<FILE>.py", text)
    return text.strip()

norms = [normalize(t) for t in outs]
import hashlib

def hashlib_sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

hashes = [hashlib_sha(n) for n in norms]
with open(AI / "determinism_hashes.txt", "w", encoding="utf-8", newline="\n") as f:
    for i,h in enumerate(hashes, start=1):
        f.write(f"run{i}: {h}\n")

# 6a. run perf harness to capture basic performance numbers
print("Step 6a: running perf harness")
run(f"{sys.executable} tools/perf_harness.py")

# 6. run rule engine (which updates checklist_evidence_map.json and suggestions)
print("Step 6: running rule engine")
run(f"{sys.executable} tools/rule_engine.py")

# 7. create dry-run patch: apply suggested IDs to a copy of checklist.md and diff
print("Step 7: creating dry-run checklist patch")
from pathlib import Path
import json

with open(AI / "checklist_update_suggestions.json", "r", encoding="utf-8") as f:
    suggestions = json.load(f)

cl_path = ROOT / "products" / "computeguard" / "checklist" / "checklist.md"
orig = cl_path.read_text(encoding="utf-8")
new = orig
for cid in suggestions.get("suggested_mark_done", []):
    # naive replace: find line starting with '- [ ] CID' and replace with '- [x] CID'
    import re
    pattern = rf"^- \[ \] {re.escape(cid)}\b.*$"
    repl = lambda m: m.group(0).replace("- [ ]", "- [x]")
    new, n = re.subn(pattern, repl, new, flags=re.MULTILINE)

# write proposed new file to temp
temp_path = AI / "checklist_proposed.md"
temp_path.write_text(new, encoding="utf-8", newline="\n")

# produce unified diff
ud = difflib.unified_diff(orig.splitlines(keepends=True), new.splitlines(keepends=True), fromfile=str(cl_path), tofile=str(cl_path) + ".proposed")
patch = "".join(ud)
with open(AI / "checklist_patch_dryrun.patch", "w", encoding="utf-8", newline="\n") as f:
    f.write(patch)

# write dry-run log
dryrun_log = {
    "generated_at": None,
    "suggestions": suggestions,
    "patch_path": str(AI / "checklist_patch_dryrun.patch")
}
from datetime import datetime
dryrun_log["generated_at"] = datetime.utcnow().isoformat() + "Z"
with open(AI / "checklist_update_dryrun.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(dryrun_log, f, indent=2, sort_keys=True)

print("Full audit (dry-run) complete. See ai_reports/checklist_update_dryrun.json and ai_reports/checklist_patch_dryrun.patch")
