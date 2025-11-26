from typing import List, Dict, Any
from pathlib import Path

def run_pipeline_on_text(text: str, rules: List[Dict[str, Any]]):
    """
    Executes normalization, validation, and repair instructions in-order.
    - Normalization is optional.
    - Validation collects errors into a structured output.
    - Repair modifies the text if required.
    Returns a dict containing:
    {
      'normalized_text': <str>,
      'validation_errors': <list>,
      'repaired_text': <str>,
      'diff': <str>
    }
    """
    normalized = text
    errors = []

    # NORMALIZATION
    for (_path, rule) in rules:
        for step in rule.get("normalization", {}).get("steps", []):
            if step.get("operation") == "trim_trailing_whitespace":
                normalized = "\n".join([l.rstrip() for l in normalized.splitlines()])

    # VALIDATION (dummy, to be extended later)
    for (_path, rule) in rules:
        for check in rule.get("validation", {}).get("checks", []):
            if check.get("type") == "line_length":
                max_len = check.get("max", 120)
                for idx, line in enumerate(normalized.splitlines(), start=1):
                    if len(line) > max_len:
                        errors.append(f"Line {idx}: exceeds {max_len} characters")

    # REPAIR (dummy structural example)
    repaired = normalized

    return {
        "normalized_text": normalized,
        "validation_errors": errors,
        "repaired_text": repaired,
        "diff": "<pending>"
    }
