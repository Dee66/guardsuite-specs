"""YAML validation helpers for GuardSpecs."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Tuple

import yaml
from jsonschema import ValidationError, validate

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def load_schema(name: str) -> Any:
    path = SCHEMA_DIR / name
    return yaml.safe_load(path.read_text(encoding="utf-8"))


PRODUCT_SCHEMA = load_schema("product_schema.yml")
CHECKLIST_SCHEMA = load_schema("checklist_schema.yml")
BOOTSTRAP_SCHEMA = load_schema("bootstrap_schema.yml")


def _ensure_yaml_text(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    if raw is None:
        return ""
    return yaml.safe_dump(raw)


def validate_yaml_text(yaml_text: Any, schema: Any) -> Tuple[bool, List[str]]:
    text = _ensure_yaml_text(yaml_text)
    try:
        data = yaml.safe_load(text) if text else {}
        validate(instance=data, schema=schema)
        return True, []
    except (yaml.YAMLError, ValidationError) as exc:
        return False, [str(exc)]
