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


def validate_rule_spec(path: Path):
    errors = []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as e:
        return [f"YAML parse error: {e}"]

    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "rule_id" in data and not isinstance(data["rule_id"], str):
        errors.append("rule_id must be a string.")

    if "file_patterns" in data and not isinstance(data["file_patterns"], list):
        errors.append("file_patterns must be a list.")

    return errors


def validate_all_under(base: Path):
    results = {}
    for path in sorted(base.rglob("*.yml")):
        results[str(path)] = validate_rule_spec(path)
    return results
