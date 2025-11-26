from pathlib import Path
from strategy_e.validators.rule_spec_validator import validate_rule_spec


def test_base_rule_spec_valid():
    # Use one actual base rule-spec (vectorscan) to ensure validator passes.
    path = Path("rule_specs/vectorscan/00_base_rule.yml")
    errors = validate_rule_spec(path)
    assert errors == [], f"Unexpected errors: {errors}"


def test_validator_detects_missing_fields(tmp_path):
    p = tmp_path / "bad.yml"
    p.write_text("rule_id: test\n", encoding="utf-8")

    errors = validate_rule_spec(p)
    assert "Missing required field: applies_to" in errors
