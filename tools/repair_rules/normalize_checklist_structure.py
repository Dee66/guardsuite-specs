"""
Rule: normalize_checklist_structure
Purpose:
  Enforce Strategy-D canonical ordering for checklist.yml files.
"""

import yaml


def normalize(text: str) -> str:
    # Placeholder for Phase 3 deeper logic
    try:
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            return text
        # Move unknown keys into x_legacy
        known = [
            "metadata",
            "structure_requirements",
            "documentation_requirements",
            "schema_requirements",
            "evaluator_requirements",
            "fixpack_requirements",
            "testing_requirements",
            "artifacts",
            "acceptance",
            "dependencies",
            "provenance",
            "phases",
            "items",
        ]
        cleaned = {}
        legacy = {}
        for k, v in data.items():
            if k in known:
                cleaned[k] = v
            else:
                legacy[k] = v
        if legacy:
            cleaned["x_legacy"] = legacy
        return yaml.safe_dump(cleaned, sort_keys=False)
    except Exception:
        return text
