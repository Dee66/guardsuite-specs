#!/usr/bin/env python3
"""Stricter YAML/content validator for PIL contracts.

Performs additional semantic checks beyond syntax:
- scoring_kpis: version format, gates present in score_weights, task_type_weights numeric
- project_map: task_id format, required fields present, confidence values allowed,
  implementation_files syntactic checks and optional existence checks (warn by default)
- task_contract: presence of done_contract and ambiguity_flags
- repo_contract: presence of sanity_checks/required_structure/complexity_profile_metrics

Usage:
  python3 scripts/validate_yaml_strict.py [--fail-missing-files]

Exit codes:
  0 OK
  2 Validation failures
  3 Missing dependency (pyyaml)
"""
from pathlib import Path
import sys
import re

try:
    import yaml
except Exception:
    yaml = None

ALLOWED_CONF = {"STATIC", "DYNAMIC", "AI_REVIEW"}
TASK_ID_RE = re.compile(r"^[A-Z]+-\d{3}$")

if yaml is None:
    print("ERROR: PyYAML not installed. Install pyyaml to run strict checks.")
    sys.exit(3)

fail_missing_files = "--fail-missing-files" in sys.argv

errors = []
warnings = []

# Load helper
def load_yaml(path: str):
    p = Path(path)
    if not p.exists():
        errors.append(f"Missing file: {path}")
        return None
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"YAML parse error in {path}: {e}")
        return None

# scoring_kpis checks
sk = load_yaml("scoring_kpis.yml")
if isinstance(sk, dict):
    ver = sk.get("version")
    if not ver or not re.match(r"^\d+\.\d+(?:\.\d+)?$", str(ver)):
        errors.append("scoring_kpis.yml: 'version' missing or not semver-like (e.g. '1.0')")
    sw = sk.get("score_weights")
    if not isinstance(sw, dict):
        errors.append("scoring_kpis.yml: 'score_weights' must be a mapping")
    else:
        total = 0
        bad_keys = []
        for k, v in sw.items():
            try:
                vi = int(v)
            except Exception:
                bad_keys.append(k)
                continue
            total += vi
        if bad_keys:
            errors.append(f"scoring_kpis.yml: score_weights values must be integers for keys: {bad_keys}")
        if total != 100:
            errors.append(f"scoring_kpis.yml: score_weights sum to {total}, expected 100")
    gates = sk.get("gates") or []
    for g in gates:
        if not (isinstance(sw, dict) and g in sw):
            errors.append(f"scoring_kpis.yml: gate '{g}' not present in score_weights keys")
    ttw = sk.get("task_type_weights")
    if not isinstance(ttw, dict):
        errors.append("scoring_kpis.yml: 'task_type_weights' must be a mapping")
    else:
        for k, v in ttw.items():
            try:
                _ = float(v)
            except Exception:
                errors.append(f"scoring_kpis.yml: task_type_weights '{k}' must be numeric")

# project_map checks
pm = load_yaml("project_map.yml")
if pm is None:
    pass
elif not isinstance(pm, dict):
    errors.append("project_map.yml: top-level must be a mapping of task_id -> entry")
else:
    for tid, entry in pm.items():
        if not TASK_ID_RE.match(str(tid)):
            warnings.append(f"project_map.yml: task id '{tid}' does not match expected pattern 'AAA-000'")
        if not isinstance(entry, dict):
            errors.append(f"project_map.yml: entry for {tid} must be a mapping")
            continue
        if "implementation_files" not in entry:
            errors.append(f"project_map.yml: {tid} missing 'implementation_files' field")
        else:
            impl = entry.get("implementation_files")
            if not isinstance(impl, list):
                errors.append(f"project_map.yml: {tid} implementation_files must be a list")
            else:
                for path in impl:
                    if not isinstance(path, str):
                        errors.append(f"project_map.yml: {tid} implementation_files contains non-string: {path}")
                    # warn on placeholders like <pillar_name>
                    if "<" in path or ">" in path:
                        warnings.append(f"project_map.yml: {tid} implementation_files contains placeholder: {path}")
                    # check existence
                    p = Path(path)
                    if not p.exists():
                        msg = f"project_map.yml: {tid} implementation file missing: {path}"
                        if fail_missing_files:
                            errors.append(msg)
                        else:
                            warnings.append(msg)
        cr = entry.get("confidence_requirements")
        if cr is None:
            warnings.append(f"project_map.yml: {tid} missing 'confidence_requirements' field")
        else:
            if isinstance(cr, str):
                if cr not in ALLOWED_CONF:
                    errors.append(f"project_map.yml: {tid} confidence_requirements '{cr}' not in {sorted(ALLOWED_CONF)}")
            else:
                errors.append(f"project_map.yml: {tid} confidence_requirements must be a string")

# task_contract checks
tc = load_yaml("task_contract.yml")
if isinstance(tc, dict):
    if "done_contract" not in tc:
        errors.append("task_contract.yml: missing 'done_contract' key")
    if "ambiguity_flags" not in tc:
        errors.append("task_contract.yml: missing 'ambiguity_flags' key")

# repo_contract checks
rc = load_yaml("repo_contract.yml")
if isinstance(rc, dict):
    for k in ("sanity_checks", "required_structure", "complexity_profile_metrics"):
        if k not in rc:
            errors.append(f"repo_contract.yml: missing '{k}' key")

# Summarize
if errors:
    print("STRICT VALIDATION FAILED:")
    for e in errors:
        print(" -", e)
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(" -", w)
    sys.exit(2)

print("STRICT VALIDATION OK")
if warnings:
    print("Warnings:")
    for w in warnings:
        print(" -", w)
sys.exit(0)
