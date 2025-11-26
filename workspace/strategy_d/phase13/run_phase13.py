#!/usr/bin/env python3
"""Phase 13 canonical alignment script.

Performs deterministic canonicalization of product metadata files:
- enforce canonical field ordering from `schemas/product_schema.yml`
- insert missing required fields with placeholders
- normalize `related_products` (filter to valid products and sort)
- move invalid related references into `x_legacy.invalid_related_products`
- write per-product unified diffs into `workspace/strategy_d/phase13/diffs/`
- write `workspace/strategy_d/phase13/canonical_alignment_log.md`

This script is deterministic and idempotent.
"""
import os
import sys
import yaml
from pathlib import Path
from difflib import unified_diff

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "schemas" / "product_schema.yml"
PHASE13_DIR = ROOT / "workspace" / "strategy_d" / "phase13"
DIFFS_DIR = PHASE13_DIR / "diffs"
LOG_PATH = PHASE13_DIR / "canonical_alignment_log.md"

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def dump_yaml(data):
    # stable dump without sorting keys beyond insertion order
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)

def main():
    PHASE13_DIR.mkdir(parents=True, exist_ok=True)
    DIFFS_DIR.mkdir(parents=True, exist_ok=True)

    schema = load_yaml(SCHEMA_PATH)
    schema_props = list(schema.get("properties", {}).keys())
    required = list(schema.get("required", []))

    # discover product metadata files
    product_files = sorted(Path("products").glob("*/metadata/product.yml"))
    valid_ids = []
    products = {}
    for p in product_files:
        data = load_yaml(p)
        pid = data.get("id")
        if pid:
            valid_ids.append(pid)
            products[pid] = p

    log_lines = ["# Phase 13: Canonical Alignment Log", "", f"Processed {len(product_files)} product metadata files.", ""]

    for p in product_files:
        old_text = p.read_text(encoding="utf-8")
        data = load_yaml(p)
        pid = data.get("id") or p.parent.parent.name

        new = {}
        # 1) place schema properties in canonical order
        for key in schema_props:
            if key in data:
                new[key] = data[key]
            else:
                # insert placeholder for required fields
                if key in required:
                    if key == "owner":
                        new[key] = "TBD"
                    elif key == "version":
                        new[key] = "0.0.0"
                    elif key == "spec_yaml":
                        new[key] = f"products/{pid}.yml"
                    elif key == "checklist_yaml":
                        new[key] = f"checklists/{pid}.yml"
                    elif key == "gpt_instructions_yaml":
                        new[key] = f"templates/{pid}_instructions.yml"
                    else:
                        new[key] = ""

        # 2) canonicalize related_products if present
        rp = data.get("related_products")
        invalid_rp = []
        if isinstance(rp, list):
            filtered = [r for r in rp if r in valid_ids]
            invalid_rp = [r for r in rp if r not in valid_ids]
            filtered = sorted(set(filtered))
            if filtered:
                new["related_products"] = filtered

        # 3) preserve or normalize pillar/product_type if present
        if "pillar" in data:
            new["pillar"] = str(data["pillar"]).strip().lower()
        if "product_type" in data:
            new["product_type"] = str(data["product_type"]).strip().lower()

        # 4) copy remaining keys in deterministic order (sorted) except ones handled
        handled = set(schema_props) | {"related_products", "pillar", "product_type"}
        remaining = [k for k in data.keys() if k not in handled]
        for k in sorted(remaining):
            new[k] = data[k]

        # 5) if invalid related products existed, ensure x_legacy exists and record them
        if invalid_rp:
            xl = new.get("x_legacy", {})
            xl.setdefault("invalid_related_products", []).extend(sorted(invalid_rp))
            new["x_legacy"] = xl

        new_text = dump_yaml(new)

        if new_text != old_text:
            # write back canonical file
            p.write_text(new_text, encoding="utf-8")
            # write unified diff
            ud = unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True), fromfile=str(p), tofile=str(p))
            diff_path = DIFFS_DIR / f"{pid}.phase13.diff"
            diff_path.write_text("".join(ud), encoding="utf-8")
            log_lines.append(f"- Updated `{p}`; diff -> `{diff_path.relative_to(ROOT)}`")
        else:
            log_lines.append(f"- No changes for `{p}`")

    # write log
    LOG_PATH.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print("WROTE", LOG_PATH)

if __name__ == '__main__':
    main()
