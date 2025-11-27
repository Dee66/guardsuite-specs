from strategy_e.pipeline.results.diff_utils import generate_unified_diff
from strategy_e.pipeline.results.backup_utils import write_backup


def run_pipeline_on_text(
    text: str,
    rules,
    path: str = None,
    dry_run: bool = False,
    backup_dir: str = None,
):
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
    iterable_rules = None
    if isinstance(rules, dict):
        iterable_rules = [(None, rules)]
    else:
        iterable_rules = rules

    for _path, rule in iterable_rules:
        for step in rule.get("normalization", {}).get("steps", []):
            if step.get("operation") == "trim_trailing_whitespace":
                normalized = "\n".join(
                    [ln.rstrip() for ln in normalized.splitlines()]
                )

    # VALIDATION (dummy, to be extended later)
    for _path, rule in iterable_rules:
        for check in rule.get("validation", {}).get("checks", []):
            if check.get("type") == "line_length":
                max_len = check.get("max", 120)
                for idx, line in enumerate(normalized.splitlines(), start=1):
                    if len(line) > max_len:
                        errors.append(
                            f"Line {idx}: exceeds {max_len} characters"
                        )

    # APPLY REPAIR STEPS
    # rules may be a mapping (from tests) or an iterable of (path, rule) tuples
    if isinstance(rules, dict):
        steps = rules.get("repair", {}).get("steps", [])
    else:
        steps = []
        for _p, r in rules:
            steps.extend(r.get("repair", {}).get("steps", []))

    # apply_repair_steps may be integrated later; placeholder kept if missing
    try:
        from strategy_e.pipeline.executor.repair_steps import (
            apply_repair_steps,
        )

        repaired = apply_repair_steps(normalized, steps)
    except Exception:
        repaired = normalized

    # WRITE BACKUP BEFORE REPAIR (only when not dry_run)
    backup_path = None
    if path is not None and not dry_run:
        try:
            backup_path = write_backup(path, text, backup_dir=backup_dir)
        except Exception:
            backup_path = None

    # DIFF GENERATION
    diff_output = generate_unified_diff(
        text, repaired, before_label="original", after_label="repaired"
    )

    # WRITE REPAIRED TEXT BACK TO FILE IF path PROVIDED (only when not dry_run)
    if path is not None and not dry_run:
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(repaired)
        except Exception:
            pass

    return {
        "normalized_text": normalized,
        "validation_errors": errors,
        "repaired_text": repaired,
        "diff": diff_output,
        "backup_path": backup_path,
        "dry_run": dry_run,
    }
