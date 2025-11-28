#!/usr/bin/env python3
"""Verify that expected files (exact filenames and paths) exist in the workspace.

This is a small deterministic checker to satisfy the checklist item
"Use exact filenames and folder paths provided in instructions." It prints a
simple summary and exits with non-zero on failure (so it can be used in CI).
"""
from pathlib import Path
import sys

EXPECTED = [
    "pil_checklist.md",
    "scoring_kpis.yml",
    "repo_contract.yml",
    "project_map.yml",
    "task_contract.yml",
    "repo-scanner.py",
    "scripts/update_pil_progress.py",
    "scripts/ai_consumer.py",
    "scripts/aggregate_and_analyze.py",
    "tests/test_ai_consumer.py",
    "AI_INPUT_CONTRACT.md",
    "AI_OUTPUT_CONTRACT.md",
]

missing = []
for p in EXPECTED:
    if not Path(p).exists():
        missing.append(p)

if missing:
    print("Missing expected files:")
    for m in missing:
        print(" - ", m)
    print(f"FAIL: {len(missing)} expected files missing.")
    sys.exit(2)

print("OK: all expected files present")
sys.exit(0)
