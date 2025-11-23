#!/usr/bin/env python3
"""Validate product YAML files against the canonical JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"
PRODUCT_SPECS = ROOT / "product_specs"
SCHEMA_DIR = PRODUCTS / "schema"
SCHEMA_PATH = SCHEMA_DIR / "product.schema.json"
CANONICAL_SCHEMA_REL = "guardsuite-core/canonical_schema.json"
CANONICAL_SCHEMA_PATH = ROOT / CANONICAL_SCHEMA_REL
SCHEMA_EXTENSIONS = {".yml", ".yaml", ".json"}
PILLAR_TEMPLATE_ID = "pillar-template"
PILLAR_TEMPLATE_SCHEMA_PATH = SCHEMA_DIR / f"{PILLAR_TEMPLATE_ID}.schema.yml"
PILLAR_TEMPLATE_SCHEMA_PREFIX = "Pillar template YAML schema failed: "
PILLAR_TEMPLATE_SPEC_CANDIDATES = [
    PRODUCTS / f"{PILLAR_TEMPLATE_ID}.yml",
    PRODUCT_SPECS / f"{PILLAR_TEMPLATE_ID}.yml",
]


def load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml_file(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_canonical_schema() -> dict:
    if not CANONICAL_SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Canonical schema missing at {CANONICAL_SCHEMA_REL}; run canonical schema scaffolding"
        )
    try:
        return json.loads(CANONICAL_SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Canonical schema JSON invalid at {CANONICAL_SCHEMA_REL}: {exc}") from exc


def iter_schema_files() -> list[Path]:
    if not SCHEMA_DIR.exists():
        return []
    return sorted(
        p for p in SCHEMA_DIR.iterdir() if p.suffix.lower() in SCHEMA_EXTENSIONS and p.is_file()
    )


def _resolve_pillar_template_spec() -> Path | None:
    for candidate in PILLAR_TEMPLATE_SPEC_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def iter_product_files() -> list[Path]:
    files = [
        p
        for p in PRODUCTS.glob("*.yml")
        if not p.name.endswith("_worksheet.yml")
        and p.name not in {"guardsuite_master_spec.yml", "product_index.yml"}
    ]
    pillar_template = _resolve_pillar_template_spec()
    if pillar_template and pillar_template not in files:
        files.append(pillar_template)
    return sorted(files, key=lambda path: path.name)


def load_schema_document(path: Path) -> dict:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return load_yaml_file(path)


def validate_schema_canonical_references() -> list[str]:
    errors: list[str] = []
    for schema_path in iter_schema_files():
        document = load_schema_document(schema_path) or {}
        properties = document.get("properties")
        if not isinstance(properties, dict):
            continue
        references_block = properties.get("references")
        if not isinstance(references_block, dict):
            continue
        ref_properties = references_block.get("properties")
        if not isinstance(ref_properties, dict):
            errors.append(f"{schema_path}: references block must define properties for canonical schema checks")
            continue
        canonical_prop = ref_properties.get("canonical_schema")
        if not canonical_prop:
            continue
        if canonical_prop.get("type") != "string":
            errors.append(f"{schema_path}: references.canonical_schema.type must be 'string'")
        const_value = canonical_prop.get("const")
        if const_value != CANONICAL_SCHEMA_REL:
            errors.append(
                f"{schema_path}: references.canonical_schema.const must equal {CANONICAL_SCHEMA_REL}"
            )
        if "enum" in canonical_prop:
            errors.append(f"{schema_path}: references.canonical_schema must use const, not enum")
        required_refs = references_block.get("required", []) or []
        if "canonical_schema" not in required_refs:
            errors.append(f"{schema_path}: references block must require canonical_schema")
    return errors


def _pillar_template_schema_errors() -> list[str]:
    errors: list[str] = []
    if not PILLAR_TEMPLATE_SCHEMA_PATH.exists():
        errors.append("schema file missing under products/schema")
        return errors
    try:
        document = load_schema_document(PILLAR_TEMPLATE_SCHEMA_PATH) or {}
    except Exception as exc:  # pragma: no cover - yaml loader already covered elsewhere
        errors.append(f"unable to load schema: {exc}")
        return errors
    try:
        Draft202012Validator.check_schema(document)
    except Exception as exc:  # pragma: no cover - jsonschema internals
        errors.append(f"invalid Draft 2020-12 document: {exc}")
    properties = document.get("properties")
    if not isinstance(properties, dict):
        errors.append("properties block missing")
        return errors
    references = properties.get("references")
    if not isinstance(references, dict):
        errors.append("references block missing")
        return errors
    ref_properties = references.get("properties")
    if not isinstance(ref_properties, dict):
        errors.append("references.properties missing")
        return errors
    canonical_prop = ref_properties.get("canonical_schema")
    if not isinstance(canonical_prop, dict):
        errors.append("references.canonical_schema missing")
    else:
        const_value = canonical_prop.get("const")
        if const_value != CANONICAL_SCHEMA_REL:
            errors.append(
                f"references.canonical_schema.const must equal {CANONICAL_SCHEMA_REL}"
            )
        if canonical_prop.get("type") != "string":
            errors.append("references.canonical_schema.type must be 'string'")
    required_refs = references.get("required")
    if not isinstance(required_refs, list) or "canonical_schema" not in required_refs:
        errors.append("references block must require canonical_schema")
    return errors


def main() -> None:
    try:
        load_canonical_schema()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Canonical schema load failed: {exc}", file=sys.stderr)
        sys.exit(1)

    schema = load_schema()
    validator = Draft202012Validator(schema)
    product_files = iter_product_files()
    failures = []
    for product_file in product_files:
        data = load_yaml_file(product_file)
        errors = list(validator.iter_errors(data))
        for error in errors:
            failures.append(f"{product_file}: {error.message}")
    canonical_reference_errors = validate_schema_canonical_references()
    failures.extend(canonical_reference_errors)
    pillar_template_schema_errors = _pillar_template_schema_errors()
    failures.extend(
        f"{PILLAR_TEMPLATE_SCHEMA_PREFIX}{detail}" for detail in pillar_template_schema_errors
    )
    if failures:
        print("Schema validation failed:")
        for message in failures:
            print(f" - {message}")
        sys.exit(1)
    print(f"Schema validation passed for {len(product_files)} product spec(s).")


if __name__ == "__main__":
    main()
