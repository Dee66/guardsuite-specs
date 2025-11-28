#!/usr/bin/env python3
"""Lightweight artifact validator against the local schemas.

This script does minimal structural validation (no external `jsonschema` dependency required).
It checks required top-level keys and types as defined in the simple schemas under `tools/schemas/`.

Usage: python3 tools/validate_artifacts.py [--repo <path>]

If no repo is provided it validates files under the current workspace.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "tools" / "schemas"
AI = ROOT / "ai_reports"

FILES_TO_VALIDATE = [
    (AI / "progress.json", SCHEMA_DIR / "progress_schema.json"),
    (AI / "evidence_summary.json", SCHEMA_DIR / "evidence_summary_schema.json"),
    (AI / "checklist_evidence_map.json", SCHEMA_DIR / "checklist_evidence_map_schema.json"),
]

errors = []

for data_path, schema_path in FILES_TO_VALIDATE:
    if not data_path.exists():
        print(f"SKIP: {data_path} (missing)")
        continue
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        errors.append((str(data_path), f"json_load_error: {e}"))
        continue
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except Exception as e:
        errors.append((str(schema_path), f"schema_load_error: {e}"))
        continue
    # Minimal checks: required keys
    req = schema.get("required", [])
    for k in req:
        if k not in data:
            errors.append((str(data_path), f"missing_required_key: {k}"))
    # Type hints: verify a couple of expected types
    props = schema.get("properties", {})
    for k, v in props.items():
        if k in data:
            expected = v.get("type")
            if expected:
                typ = type(data[k]).__name__
                # map python types to json schema types
                jtype = None
                if isinstance(data[k], str):
                    jtype = "string"
                elif isinstance(data[k], bool):
                    jtype = "boolean"
                elif isinstance(data[k], int):
                    jtype = "integer"
                elif isinstance(data[k], float):
                    jtype = "number"
                elif isinstance(data[k], list):
                    jtype = "array"
                elif isinstance(data[k], dict):
                    jtype = "object"
                if jtype and jtype != expected:
                    errors.append((str(data_path), f"type_mismatch: {k} expected {expected} got {jtype}"))

if errors:
    print("Validation completed: ERRORS found")
    for p, e in errors:
        print(f" - {p}: {e}")
    sys.exit(2)
else:
    print("Validation completed: no structural errors found (lightweight checks)")
    sys.exit(0)
