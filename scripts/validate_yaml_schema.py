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
SCHEMA_PATH = PRODUCTS / "schema" / "product.schema.json"


def load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml_file(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> None:
    schema = load_schema()
    validator = Draft202012Validator(schema)
    product_files = sorted(
        p for p in PRODUCTS.glob("*.yml") if not p.name.endswith("_worksheet.yml")
    )
    failures = []
    for product_file in product_files:
        data = load_yaml_file(product_file)
        errors = list(validator.iter_errors(data))
        for error in errors:
            failures.append(f"{product_file}: {error.message}")
    if failures:
        print("Schema validation failed:")
        for message in failures:
            print(f" - {message}")
        sys.exit(1)
    print(f"Schema validation passed for {len(product_files)} product spec(s).")


if __name__ == "__main__":
    main()
