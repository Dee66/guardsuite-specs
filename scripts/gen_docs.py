#!/usr/bin/env python3
# COPILOT: Maintain strict YAML → Markdown determinism. Never reorder fields arbitrarily.
# COPILOT: When adding validation rules, ensure backward-compatibility with all product YAML.
# scripts/gen_docs.py
"""Generate Markdown docs from products/*.yml using templates/*.j2."""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"
TEMPLATES = ROOT / "templates"
OUTDIR = ROOT / "docs" / "products"

env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def get_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def iter_product_files() -> List[Path]:
    return sorted(
        p
        for p in PRODUCTS.glob("*.yml")
        if not p.name.endswith("_worksheet.yml") and p.name != "guardsuite_master_spec.yml"
    )


def list_product_ids() -> List[str]:
    return [p.stem for p in iter_product_files()]


def validate_product(product: dict, product_id: str) -> None:
    required_keys = ("id", "name", "version", "features")
    for key in required_keys:
        if key not in product:
            raise ValueError(f"Product '{product_id}' missing required key: {key}")
        if product[key] in (None, ""):
            raise ValueError(f"Product '{product_id}' has empty value for: {key}")
    if not isinstance(product["features"], list):
        raise ValueError(f"Product '{product_id}' features must be a list")


def render_product(product_id: str, outdir: Path, snippets: dict) -> Path:
    product_file = PRODUCTS / f"{product_id}.yml"
    if not product_file.exists():
        raise FileNotFoundError(f"Product file {product_file} missing")
    product = load_yaml(product_file)
    validate_product(product, product_id)
    tpl = env.get_template("product_page.md.j2")
    iso_timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    meta = {"commit": get_git_commit(), "timestamp": iso_timestamp}
    rendered = tpl.render(
        product=product,
        snippets=snippets,
        meta=meta,
        product_raw=yaml.safe_dump(product, sort_keys=False),
    )
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"{product_id}.md"
    outpath.write_text(rendered, encoding="utf-8")
    return outpath


def resolve_targets(product: str | None, generate_all: bool) -> List[str]:
    targets: List[str] = []
    if generate_all:
        targets.extend(list_product_ids())
    if product:
        targets.append(product)
    # Deduplicate while preserving order
    seen = set()
    ordered: List[str] = []
    for pid in targets:
        if pid in seen:
            continue
        seen.add(pid)
        ordered.append(pid)
    if not ordered:
        raise ValueError("No products selected. Use --product <id> or --all.")
    return ordered


def main() -> None:
    parser = argparse.ArgumentParser(description="Render GuardSuite product docs")
    parser.add_argument("--product", help="single product id to render")
    parser.add_argument("--all", action="store_true", help="render docs for every product spec")
    parser.add_argument("--out", default=str(OUTDIR), help="output directory for generated docs")
    args = parser.parse_args()

    targets = resolve_targets(args.product, args.all)
    snippets = load_yaml(ROOT / "snippets" / "marketing.yml")
    outdir = Path(args.out)
    for pid in targets:
        outpath = render_product(pid, outdir, snippets)
        print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
