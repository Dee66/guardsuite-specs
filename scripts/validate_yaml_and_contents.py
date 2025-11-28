#!/usr/bin/env python3
"""Validate YAML syntax and basic content expectations for key contract files.

Exits with code 0 on success, non-zero on failure. Prints a concise report.
"""
from pathlib import Path
import sys
import json

try:
    import yaml
except Exception:
    yaml = None

KEY_FILES = {
    "scoring_kpis.yml": {
        "required_keys": ["version", "score_weights", "task_type_weights"],
    },
    "repo_contract.yml": {"required_keys": ["sanity_checks", "required_structure", "complexity_profile_metrics"]},
    "project_map.yml": {"required_keys": []},
    "task_contract.yml": {"required_keys": ["done_contract"]},
}

errors = []

if yaml is None:
    print("ERROR: PyYAML not available in environment. Install pyyaml to run YAML checks.")
    sys.exit(3)

for fname, meta in KEY_FILES.items():
    p = Path(fname)
    if not p.exists():
        errors.append(f"Missing file: {fname}")
        continue
    try:
        with p.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except Exception as e:
        errors.append(f"YAML parse error in {fname}: {e}")
        continue
    if data is None:
        errors.append(f"Empty YAML document: {fname}")
        continue

    # Basic required key checks
    for rk in meta.get("required_keys", []):
        if rk not in data:
            errors.append(f"{fname}: missing top-level key '{rk}'")

    # File-specific semantics
    if fname == "scoring_kpis.yml":
        sw = data.get("score_weights")
        if not isinstance(sw, dict):
            errors.append("scoring_kpis.yml: 'score_weights' must be a mapping")
        else:
            total = 0
            bad = []
            for k, v in sw.items():
                try:
                    vi = int(v)
                except Exception:
                    bad.append(k)
                    continue
                total += vi
            if bad:
                errors.append(f"scoring_kpis.yml: score_weights values must be integers for keys: {bad}")
            if total != 100:
                errors.append(f"scoring_kpis.yml: score_weights sum to {total}, expected 100")

    if fname == "project_map.yml":
        # Expect a mapping of tasks -> entries
        if not isinstance(data, dict):
            errors.append("project_map.yml: top-level document must be a mapping of task_id -> task_entry")
        else:
            for tid, entry in data.items():
                if not isinstance(entry, dict):
                    errors.append(f"project_map.yml: entry for {tid} must be a mapping")
                    continue
                if "implementation_files" not in entry:
                    errors.append(f"project_map.yml: {tid} missing 'implementation_files' field")
                if "confidence_requirements" not in entry:
                    errors.append(f"project_map.yml: {tid} missing 'confidence_requirements' field")

# Report
if errors:
    print("YAML/content validation FAILED with the following issues:")
    for e in errors:
        print(" -", e)
    sys.exit(2)

print("YAML/content validation OK: all checked files present and valid")
sys.exit(0)
