#!/usr/bin/env python3
"""Validate that validation_artifacts referenced in project_map.yml exist.

- For pytest node ids like `tests/test_x.py::test_name`, check the file exists.
- For paths, check the file exists.

Exit 0 on success, 2 on missing artifacts.
"""
from pathlib import Path
import sys

try:
    import yaml
except Exception:
    yaml = None

if yaml is None:
    print("ERROR: PyYAML not installed")
    sys.exit(3)

pm = yaml.safe_load(Path("project_map.yml").read_text(encoding="utf-8"))
missing = []
for tid, entry in (pm or {}).items():
    vas = entry.get("validation_artifacts", []) or []
    for va in vas:
        if isinstance(va, str):
            if "::" in va:
                fname = va.split("::", 1)[0]
                p = Path(fname)
                if not p.exists():
                    missing.append(f"{tid}: validation artifact test file missing: {fname}")
            else:
                p = Path(va)
                if not p.exists():
                    missing.append(f"{tid}: validation artifact file missing: {va}")
        else:
            missing.append(f"{tid}: validation_artifact entry not a string: {va}")

if missing:
    print("Validation artifacts check FAILED:")
    for m in missing:
        print(" -", m)
    sys.exit(2)

print("Validation artifacts check OK")
sys.exit(0)
