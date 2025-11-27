#!/usr/bin/env python3
"""Run `tools/collect_evidence.py` in multiple repository paths and gather per-repo outputs.

Usage: python3 tools/multi_repo_audit.py <repo-path-1> [<repo-path-2> ...]

For each repo path this script will:
 - run `python3 tools/collect_evidence.py` in that repo (it will write to repo's `ai_reports/`)
 - copy the `ai_reports/evidence_summary.json` and `ai_reports/checklist_evidence_map.json` to
   `ai_reports/multi_repo/<repo-name>/` under the current workspace for aggregation.

This runner is intended as a smoke test and central orchestrator for multi-repo audits.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "ai_reports" / "multi_repo"
OUT_DIR.mkdir(parents=True, exist_ok=True)

if len(sys.argv) < 2:
    print("Usage: python3 tools/multi_repo_audit.py <repo-path-1> [<repo-path-2> ...]")
    sys.exit(1)

repos = sys.argv[1:]
for repo in repos:
    rpath = Path(repo).resolve()
    if not rpath.exists():
        print(f"SKIP {repo}: path does not exist")
        continue
    print(f"Running evidence collector in: {rpath}")
    # Ensure collector exists in repo
    collector = rpath / "tools" / "collect_evidence.py"
    if not collector.exists():
        print(f"Collector not found in {repo}: expected {collector}")
        continue
    # Run collector
    try:
        subprocess.run([sys.executable, str(collector)], cwd=str(rpath), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Collector failed in {repo}: {e}")
    # Copy outputs if present
    src_evidence = rpath / "ai_reports" / "evidence_summary.json"
    src_map = rpath / "ai_reports" / "checklist_evidence_map.json"
    dest = OUT_DIR / rpath.name
    dest.mkdir(parents=True, exist_ok=True)
    if src_evidence.exists():
        shutil.copy2(src_evidence, dest / "evidence_summary.json")
    if src_map.exists():
        shutil.copy2(src_map, dest / "checklist_evidence_map.json")
    # also copy progress if present
    src_prog = rpath / "ai_reports" / "progress.json"
    if src_prog.exists():
        shutil.copy2(src_prog, dest / "progress.json")
    print(f"Collected artifacts for {rpath.name} -> {dest}")

print("multi-repo audit completed")
