from typing import List, Dict, Any
from pathlib import Path
from strategy_e.pipeline.results.diff_utils import generate_unified_diff
from strategy_e.pipeline.results.backup_utils import write_backup

def run_pipeline_on_text(text: str, rules: List[Dict[str, Any]], path: str = None):
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

    # APPLY REPAIR STEPS (placeholder: identity transform)
    repaired = normalized

    # WRITE BACKUP BEFORE REPAIR
    backup_path = None
    if path is not None:
        try:
            backup_path = write_backup(path, text)
        except Exception:
            # Non-fatal: record but continue
            backup_path = None

    # DIFF GENERATION
    diff_output = generate_unified_diff(text, repaired, before_label="original", after_label="repaired")

    # WRITE REPAIRED TEXT BACK TO FILE IF path PROVIDED
    if path is not None:
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(repaired)
        except Exception:
            # Non-fatal: continue
            pass

    return {
        "normalized_text": normalized,
        "validation_errors": errors,
        "repaired_text": repaired,
        "diff": diff_output,
        "backup_path": backup_path
    }
