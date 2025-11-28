import re
import yaml
from pathlib import Path

REQUIRED_TOP_LEVEL = [
    "rule_id",
    "applies_to",
    "version",
    "description",
    "input_type",
    "file_patterns",
    "normalization",
    "validation",
    "repair",
    "outputs",
]


RULE_ID_RE = re.compile(r"^[a-z0-9_-]+(-base-\d+)?$")


def validate_rule_spec(path: Path):
    errors = []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as e:
        return [f"YAML parse error: {e}"]

    # Basic required fields
    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Type checks
    if "rule_id" in data and not isinstance(data["rule_id"], str):
        errors.append("rule_id must be a string.")

    # Strict rule_id format
    if "rule_id" in data and isinstance(data["rule_id"], str):
        if not RULE_ID_RE.match(data["rule_id"]):
            errors.append("rule_id must match regex: ^[a-z0-9_-]+(-base-\\d+)?$")

    # applies_to must match known product directories under rule_specs/
    if "applies_to" in data:
        applies = data["applies_to"]
        if isinstance(applies, str):
            products_dir = Path("rule_specs")
            try:
                known = sorted([p.name for p in products_dir.iterdir() if p.is_dir()])
            except Exception:
                known = []
            if applies not in known:
                errors.append(
                    f"applies_to must be one of the product directories under rule_specs/: {known}"
                )
        else:
            errors.append("applies_to must be a string")

    # description must be a non-empty multi-line string
    if "description" in data:
        desc = data["description"]
        if not isinstance(desc, str) or not desc.strip():
            errors.append("description must be a non-empty string")
        else:
            if "\n" not in desc:
                errors.append("description must be a multi-line string")

    # file_patterns must be a non-empty list of strings
    if "file_patterns" in data:
        fps = data["file_patterns"]
        if not isinstance(fps, list) or len(fps) == 0:
            errors.append("file_patterns must be a non-empty list of strings")
        else:
            for i, item in enumerate(fps):
                if not isinstance(item, str):
                    errors.append(f"file_patterns[{i}] must be a string")

    # normalization.steps checks
    norm = data.get("normalization") or {}
    steps = norm.get("steps") if isinstance(norm, dict) else None
    if steps is None:
        errors.append("normalization.steps must be a list (can be empty)")
    else:
        if not isinstance(steps, list):
            errors.append("normalization.steps must be a list")
        else:
            for idx, step in enumerate(steps):
                if not isinstance(step, dict):
                    errors.append(f"normalization.steps[{idx}] must be a mapping")
                else:
                    if "id" not in step or "operation" not in step:
                        errors.append(
                            f"normalization.steps[{idx}] must contain id and operation"
                        )

    # validation.checks checks
    val = data.get("validation") or {}
    checks = val.get("checks") if isinstance(val, dict) else None
    if checks is None:
        errors.append("validation.checks must be a list (can be empty)")
    else:
        if not isinstance(checks, list):
            errors.append("validation.checks must be a list")
        else:
            for idx, chk in enumerate(checks):
                if not isinstance(chk, dict):
                    errors.append(f"validation.checks[{idx}] must be a mapping")
                else:
                    if "id" not in chk or "description" not in chk:
                        errors.append(
                            f"validation.checks[{idx}] must contain id and description"
                        )

    # repair.steps checks
    rep = data.get("repair") or {}
    rsteps = rep.get("steps") if isinstance(rep, dict) else None
    if rsteps is None:
        errors.append("repair.steps must be a list (can be empty)")
    else:
        if not isinstance(rsteps, list):
            errors.append("repair.steps must be a list")
        else:
            for idx, rs in enumerate(rsteps):
                if not isinstance(rs, dict):
                    errors.append(f"repair.steps[{idx}] must be a mapping")
                else:
                    if "id" not in rs or "operation" not in rs:
                        errors.append(
                            f"repair.steps[{idx}] must contain id and operation"
                        )

    # outputs must contain produces_diff and produces_log as booleans
    out = data.get("outputs")
    if not isinstance(out, dict):
        errors.append(
            "outputs must be a mapping containing produces_diff and produces_log"
        )
    else:
        if "produces_diff" not in out or "produces_log" not in out:
            errors.append("outputs must contain produces_diff and produces_log")
        else:
            if not isinstance(out.get("produces_diff"), bool) or not isinstance(
                out.get("produces_log"), bool
            ):
                errors.append(
                    "outputs.produces_diff and outputs.produces_log must be booleans"
                )

    return errors


def validate_all_under(base: Path):
    results = {}
    for path in sorted(base.rglob("*.yml")):
        results[str(path)] = validate_rule_spec(path)
    return results
