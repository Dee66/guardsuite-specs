"""CI-focused helpers for GuardSpecs automation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from api.bootstrap_api import regenerate_bootstrap
from api.db import load_db
from api.validate import validate_product
from validation.validator import BOOTSTRAP_SCHEMA, CHECKLIST_SCHEMA, PRODUCT_SCHEMA

PRODUCTS_DIR = Path("products")
STRUCTURAL_EXCLUDE = {
    "guardsuite-template.yml",
    "guardsuite_master_spec.yml",
}


def ci_validate_products() -> Dict[str, Any]:
    """Validate every product registered in the metadata store."""

    db = load_db()
    results: Dict[str, Any] = {}
    for pid in sorted(db.keys()):
        results[pid] = validate_product(pid)
    return {"results": results}


def ci_regenerate_all() -> Dict[str, Any]:
    """Regenerate bootstrap artifacts for every product and return outputs."""

    db = load_db()
    outputs: Dict[str, Any] = {}
    for pid in sorted(db.keys()):
        outputs[pid] = regenerate_bootstrap(pid)
    return {"bootstraps": outputs}


def _schema_signature(schema: Any, fallback: str) -> str:
    if isinstance(schema, dict):
        return schema.get("$id") or schema.get("title") or fallback
    return fallback


def ci_structural_check() -> Dict[str, Any]:
    """Perform lightweight YAML parsing checks across product specs."""

    problems = []
    for path in sorted(PRODUCTS_DIR.glob("*.yml")):
        if path.name in STRUCTURAL_EXCLUDE:
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - defensive logging only
            problems.append({"file": str(path), "error": str(exc)})
            continue

        if not isinstance(data, dict):
            problems.append({"file": str(path), "error": "root is not a mapping"})
            continue

        if not data.get("id"):
            problems.append({"file": str(path), "error": "missing id field"})

    schema_metadata = {
        "product_schema": _schema_signature(PRODUCT_SCHEMA, "product-schema"),
        "checklist_schema": _schema_signature(CHECKLIST_SCHEMA, "checklist-schema"),
        "bootstrap_schema": _schema_signature(BOOTSTRAP_SCHEMA, "bootstrap-schema"),
    }

    return {"problems": problems, "schema_metadata": schema_metadata}
