#!/usr/bin/env python3
import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
AI = os.path.join(ROOT, "ai_reports")
MAP_PATH = os.path.join(AI, "checklist_evidence_map.json")
SUMMARY_PATH = os.path.join(AI, "evidence_summary.json")

with open(MAP_PATH, "r", encoding="utf-8") as f:
    cmap = json.load(f)
with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
    summary = json.load(f)

# Read adapter pytest summary
adapter_pytest = os.path.join(AI, "adapter_pytest_summary.txt")
adapter_pytest_exists = os.path.exists(adapter_pytest)
adapter_pytest_excerpt = None
if adapter_pytest_exists:
    with open(adapter_pytest, "r", encoding="utf-8") as f:
        s = f.read()
    adapter_pytest_excerpt = s.strip().splitlines()[-20:]

# Read adapters flake8
adapters_flake = os.path.join(AI, "adapters_flake8.txt")
adapters_flake_exists = os.path.exists(adapters_flake)
adapters_flake_excerpt = None
if adapters_flake_exists:
    with open(adapters_flake, "r", encoding="utf-8") as f:
        s = f.read()
    adapters_flake_excerpt = s.strip().splitlines()[:50]

# Read file commits
file_commits = os.path.join(AI, "file_commits.txt")
file_commits_exists = os.path.exists(file_commits)
file_commits_lines = []
if file_commits_exists:
    with open(file_commits, "r", encoding="utf-8") as f:
        file_commits_lines = [l.strip() for l in f.readlines() if l.strip()]

# Update cmap mappings with targeted info
m = cmap.get("mappings", {})
# update adapters scaffolding status if adapter tests passed
if adapter_pytest_exists:
    passed = False
    # heuristics: look for 'passed' or '0 failed' in last lines
    tail = "\n".join(adapter_pytest_excerpt or [])
    if "passed" in tail and "failed" not in tail:
        passed = True
    # update mapping
    if "ADAPTERS_SCAFFOLDED" not in m:
        m["ADAPTERS_SCAFFOLDED"] = {"evidence": [], "status": "partial"}
    m["ADAPTERS_SCAFFOLDED"]["evidence"].append({"type": "pytest", "path": os.path.relpath(adapter_pytest, ROOT), "passed": passed})
    if passed:
        m["ADAPTERS_SCAFFOLDED"]["status"] = "done"

# attach flake8 excerpt
if adapters_flake_exists:
    if "ADAPTERS_SCAFFOLDED" not in m:
        m["ADAPTERS_SCAFFOLDED"] = {"evidence": [], "status": "partial"}
    m["ADAPTERS_SCAFFOLDED"]["evidence"].append({"type": "flake8", "path": os.path.relpath(adapters_flake, ROOT)})

# attach commit lines
if file_commits_exists:
    # parse lines like: <file>: <commit info>
    for line in file_commits_lines:
        if ":" in line:
            filep, info = line.split(":", 1)
            key = None
            if "schema.yml" in filep:
                key = "PROMOTED_SCHEMA"
            elif "00_base_rule.yml" in filep:
                key = "BASE_RULE_UPDATED"
            elif "computeguard_adapter.py" in filep or "pipeline_adapter.py" in filep:
                key = "ADAPTERS_SCAFFOLDED"
            if key:
                if key not in m:
                    m[key] = {"evidence": [], "status": "partial"}
                m[key]["evidence"].append({"type": "git_last_commit", "file": filep, "info": info.strip()})

# write back
cmap["mappings"] = m
cmap["updated_at"] = datetime.utcnow().isoformat() + "Z"
with open(MAP_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(cmap, f, indent=2, sort_keys=True)

# update evidence_summary with adapter test info
summary["adapter_tests"] = {
    "path": os.path.relpath(adapter_pytest, ROOT) if adapter_pytest_exists else None,
    "exists": adapter_pytest_exists,
    "excerpt_lines": adapter_pytest_excerpt or []
}
summary["adapters_flake8"] = {
    "path": os.path.relpath(adapters_flake, ROOT) if adapters_flake_exists else None,
    "exists": adapters_flake_exists,
    "excerpt_lines": adapters_flake_excerpt or []
}
summary["file_commits_path"] = os.path.relpath(file_commits, ROOT) if file_commits_exists else None
summary["updated_at"] = datetime.utcnow().isoformat() + "Z"
with open(SUMMARY_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(summary, f, indent=2, sort_keys=True)

print("Updated checklist_evidence_map.json and evidence_summary.json with targeted results")
