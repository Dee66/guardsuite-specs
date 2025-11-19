#!/usr/bin/env python3
# COPILOT: Do not add new required fields without updating all existing products.
"""Validate GuardSuite product YAML files for required keys and structure."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"

REQUIRED_FIELDS = [
    "id",
    "name",
    "short_description",
    "long_description",
    "version",
    "features",
]


def load_product(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_product(product: dict, path: Path) -> List[str]:
    errors: List[str] = []
    for field in REQUIRED_FIELDS:
        if field not in product:
            errors.append(f"{path}: missing required field '{field}'")
            continue
        if product[field] in (None, ""):
            errors.append(f"{path}: field '{field}' cannot be empty")
    features = product.get("features")
    if not isinstance(features, list):
        errors.append(f"{path}: 'features' must be a list")
    else:
        for idx, feature in enumerate(features):
            if not isinstance(feature, dict):
                errors.append(f"{path}: feature #{idx} must be an object")
    return errors


def main() -> None:
    product_files = sorted(
        p for p in PRODUCTS.glob("*.yml") if not p.name.endswith("_worksheet.yml")
    )
    if not product_files:
        print("No product specs found under products/", file=sys.stderr)
        sys.exit(1)
    problems: List[str] = []
    for file_path in product_files:
        product = load_product(file_path)
        problems.extend(validate_product(product, file_path))
    if problems:
        print("Product validation failed:")
        for issue in problems:
            print(f" - {issue}")
        sys.exit(1)
    print(f"Validated {len(product_files)} product spec(s).")


if __name__ == "__main__":
    main()
