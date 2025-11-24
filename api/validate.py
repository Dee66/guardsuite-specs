"""Product validation helpers leveraging canonical schemas."""

from __future__ import annotations

from typing import Any, Dict, List

from api.db import load_db
from validation.validator import (
    BOOTSTRAP_SCHEMA,
    CHECKLIST_SCHEMA,
    PRODUCT_SCHEMA,
    validate_yaml_text,
)


def validate_product(pid: str) -> Dict[str, Any]:
    db = load_db()
    product = db.get(pid)
    if not product:
        return {"valid": False, "errors": ["Product not found"]}

    results: List[str] = []

    spec_ok, spec_errors = validate_yaml_text(product.get("spec_yaml", ""), PRODUCT_SCHEMA)
    if not spec_ok:
        results.extend(f"spec: {err}" for err in spec_errors)

    checklist_ok, checklist_errors = validate_yaml_text(
        product.get("checklist_yaml", ""), CHECKLIST_SCHEMA
    )
    if not checklist_ok:
        results.extend(f"checklist: {err}" for err in checklist_errors)

    instructions_ok, inst_errors = validate_yaml_text(
        product.get("gpt_instructions_yaml", ""), BOOTSTRAP_SCHEMA
    )
    if not instructions_ok:
        results.extend(f"gpt_instructions: {err}" for err in inst_errors)

    return {"valid": not results, "errors": results}
