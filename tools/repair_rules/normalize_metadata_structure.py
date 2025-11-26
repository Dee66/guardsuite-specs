"""
Rule: normalize_metadata_structure
Purpose:
  Enforce canonical ordering, remove empty keys, and relocate
  unknown fields into x_legacy.
"""
import yaml


def normalize(text: str) -> str:
    # Placeholder — implement real logic later
    try:
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            return text
        # Ensure stable ordering
        ordered = dict(sorted(data.items()))
        return yaml.safe_dump(ordered, sort_keys=False)
    except Exception:
        return text
