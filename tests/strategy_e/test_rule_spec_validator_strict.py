import re
from pathlib import Path
from strategy_e.validators.rule_spec_validator import validate_rule_spec


def test_strict_valid_spec_passes():
    path = Path("rule_specs/vectorscan/00_base_rule.yml")
    errors = validate_rule_spec(path)
    assert errors == [], f"Unexpected errors: {errors}"


def test_invalid_rule_id_fails(tmp_path):
    p = tmp_path / "bad.yml"
    p.write_text("rule_id: BAD RULE\napplies_to: x\nversion: 1\n", encoding="utf-8")
    errors = validate_rule_spec(p)
    assert any("rule_id" in e for e in errors)


def test_missing_outputs_fields(tmp_path):
    p = tmp_path / "bad2.yml"
    p.write_text("rule_id: test-rule\napplies_to: x\nversion: 1\noutputs: {}\n", encoding="utf-8")
    errors = validate_rule_spec(p)
    assert any("outputs" in e for e in errors)
