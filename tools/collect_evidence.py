#!/usr/bin/env python3
"""Collect deterministic evidence about repo state and write JSON summaries.

Writes:
- ai_reports/evidence_summary.json
- ai_reports/checklist_evidence_map.json

The script is conservative: it records file existence, last commit that touched the file, mtimes, pytest output path, flake8 output path, ai_reports artifacts list, and a short mapping for a few checklist IDs.
"""
import os
import subprocess
import json
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
AI_REPORTS = os.path.join(ROOT, "ai_reports")
os.makedirs(AI_REPORTS, exist_ok=True)

def run(cmd, cwd=ROOT):
    try:
        out = subprocess.check_output(cmd, cwd=cwd, shell=True, stderr=subprocess.STDOUT, text=True)
        return out
    except subprocess.CalledProcessError as e:
        return e.output

def git_branch():
    return run("git rev-parse --abbrev-ref HEAD").strip()

def git_recent_commits(n=50):
    out = run(f"git log -n {n} --pretty=format:'%h %ad %s' --date=iso")
    return out.strip().splitlines()

def file_last_commit(path):
    if not os.path.exists(path):
        return None
    out = run(f"git log -n1 --pretty=format:'%H|%h|%ad' --date=iso -- {path}")
    return out.strip() or None

def file_mtime_iso(path):
    if not os.path.exists(path):
        return None
    return datetime.utcfromtimestamp(os.path.getmtime(path)).isoformat()+"Z"

# Paths of interest
paths = [
    "products/computeguard/schema.yml",
    "products/computeguard/rules/00_base_rule.yml",
    "strategy_e/adapters/pipeline_adapter.py",
    "strategy_e/adapters/computeguard_adapter.py",
    "products/computeguard/checklist/checklist.md",
    "ai_reports/progress.json",
    "tools/update_checklist_from_progress.py",
]

files = {}
for p in paths:
    full = os.path.join(ROOT, p)
    files[p] = {
        "exists": os.path.exists(full),
        "last_commit": file_last_commit(p),
        "mtime": file_mtime_iso(full),
    }

# ai_reports files
ai_files = []
for root, dirs, filenames in os.walk(AI_REPORTS):
    for fn in filenames:
        ai_files.append(os.path.relpath(os.path.join(root, fn), ROOT))

# Run pytest and save summary
pytest_out_path = os.path.join(AI_REPORTS, "pytest_summary.txt")
pytest_cmd = "pytest -q"
try:
    with open(pytest_out_path, "w", encoding="utf-8") as f:
        p = subprocess.run(pytest_cmd, cwd=ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        f.write(p.stdout)
        pytest_exit = p.returncode
except Exception as e:
    with open(pytest_out_path, "w", encoding="utf-8") as f:
        f.write(str(e))
    pytest_exit = 2

# Flake8 output: always run and capture exit code and output
flake_path = os.path.join(AI_REPORTS, "phase5_flake8_raw_after.txt")
try:
    p = subprocess.run("flake8 . --exclude .venv", cwd=ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    with open(flake_path, "w", encoding="utf-8") as f:
        f.write(p.stdout)
    flake_exit = p.returncode
except FileNotFoundError as e:
    # flake8 not installed; record exit code 127 and message
    with open(flake_path, "w", encoding="utf-8") as f:
        f.write("flake8: command not found\n")
    flake_exit = 127
except subprocess.CalledProcessError as e:
    # subprocess.run shouldn't raise here, but handle defensively
    with open(flake_path, "w", encoding="utf-8") as f:
        f.write(e.output if hasattr(e, 'output') else str(e))
    flake_exit = getattr(e, 'returncode', 2)
except Exception as e:
    with open(flake_path, "w", encoding="utf-8") as f:
        f.write(str(e))
    flake_exit = 2

# Also run flake8 specifically on adapters directory and capture exit code
adapters_flake_path = os.path.join(AI_REPORTS, "adapters_flake8.txt")
try:
    p_ad = subprocess.run("flake8 strategy_e/adapters --max-line-length 88", cwd=ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    with open(adapters_flake_path, "w", encoding="utf-8") as f:
        f.write(p_ad.stdout)
    adapters_flake_exit = p_ad.returncode
except FileNotFoundError:
    with open(adapters_flake_path, "w", encoding="utf-8") as f:
        f.write("flake8: command not found\n")
    adapters_flake_exit = 127
except subprocess.CalledProcessError as e:
    with open(adapters_flake_path, "w", encoding="utf-8") as f:
        f.write(e.output if hasattr(e, 'output') else str(e))
    adapters_flake_exit = getattr(e, 'returncode', 2)
except Exception as e:
    with open(adapters_flake_path, "w", encoding="utf-8") as f:
        f.write(str(e))
    adapters_flake_exit = 2

summary = {
    "generated_at": datetime.utcnow().isoformat()+"Z",
    "branch": git_branch(),
    "recent_commits": git_recent_commits(50),
    "files": files,
    "ai_reports_files": sorted(ai_files),
    "pytest_summary": os.path.relpath(pytest_out_path, ROOT),
    "pytest_exit_code": pytest_exit,
    "flake8_summary": os.path.relpath(flake_path, ROOT),
    "flake8_exit_code": flake_exit,
    "adapters_flake8_summary": os.path.relpath(adapters_flake_path, ROOT),
    "adapters_flake8_exit_code": adapters_flake_exit,
}

with open(os.path.join(AI_REPORTS, "evidence_summary.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(summary, f, indent=2, sort_keys=True)

# Create a conservative checklist evidence map for a subset of items
map_out = {
    "generated_at": datetime.utcnow().isoformat()+"Z",
    "mappings": {
        "ACC-005": {
            "evidence": [
                {"type": "pytest", "path": summary["pytest_summary"], "exit_code": summary["pytest_exit_code"]}
            ],
            "status": "done" if summary["pytest_exit_code"] == 0 else "failed"
        },
        "PROMOTED_SCHEMA": {
            "evidence": [
                {"type": "file", "path": "products/computeguard/schema.yml", "exists": files.get("products/computeguard/schema.yml", {}).get("exists")}
            ],
            "status": "done" if files.get("products/computeguard/schema.yml", {}).get("exists") else "missing"
        },
        "BASE_RULE_UPDATED": {
            "evidence": [
                {"type": "file", "path": "products/computeguard/rules/00_base_rule.yml", "exists": files.get("products/computeguard/rules/00_base_rule.yml", {}).get("exists")}
            ],
            "status": "done" if files.get("products/computeguard/rules/00_base_rule.yml", {}).get("exists") else "missing"
        },
        "ADAPTERS_SCAFFOLDED": {
            "evidence": [
                {"type": "file", "path": "strategy_e/adapters/pipeline_adapter.py", "exists": files.get("strategy_e/adapters/pipeline_adapter.py", {}).get("exists")},
                {"type": "file", "path": "strategy_e/adapters/computeguard_adapter.py", "exists": files.get("strategy_e/adapters/computeguard_adapter.py", {}).get("exists")}
            ],
            "status": "partial"
        },
        "PROGRESS_JSON": {
            "evidence": [
                {"type": "file", "path": "ai_reports/progress.json", "exists": files.get("ai_reports/progress.json", {}).get("exists")}
            ],
            "status": "done" if files.get("ai_reports/progress.json", {}).get("exists") else "missing"
        }
    }
}

with open(os.path.join(AI_REPORTS, "checklist_evidence_map.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(map_out, f, indent=2, sort_keys=True)

print("Wrote ai_reports/evidence_summary.json and ai_reports/checklist_evidence_map.json")
