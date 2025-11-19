#!/usr/bin/env python3
# COPILOT: Snapshots must be safe for direct paste into AI chats.
# COPILOT: Strip any unnecessary whitespace and ensure stable YAML ordering.
# scripts/export_for_ai.py
"""Export single-file spec snapshots for AI workflows."""

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
OUTDIR = ROOT / "ai_snapshots"

env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)


def get_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def list_product_ids() -> List[str]:
    return sorted(
        p.stem
        for p in PRODUCTS.glob("*.yml")
        if not p.name.endswith("_worksheet.yml") and p.name != "guardsuite_master_spec.yml"
    )


def resolve_targets(product: str | None, export_all: bool) -> List[str]:
    targets: List[str] = []
    if export_all:
        targets.extend(list_product_ids())
    if product:
        targets.append(product)
    ordered: List[str] = []
    seen = set()
    for pid in targets:
        if pid in seen:
            continue
        seen.add(pid)
        ordered.append(pid)
    if not ordered:
        raise ValueError("No products selected. Use --product <id> or --all.")
    return ordered


def export(product_id: str, outdir: Path) -> Path:
    product_file = PRODUCTS / f"{product_id}.yml"
    if not product_file.exists():
        raise FileNotFoundError(f"{product_file} missing")
    product = load_yaml(product_file)
    tpl = env.get_template("spec_snapshot.md.j2")
    ts = datetime.now(timezone.utc)
    iso_timestamp = ts.isoformat().replace("+00:00", "Z")
    meta = {"commit": get_git_commit(), "timestamp": iso_timestamp}
    product_raw = yaml.safe_dump(product, sort_keys=False).strip()
    rendered = tpl.render(product=product, meta=meta, product_raw=product_raw).strip() + "\n"
    outdir.mkdir(parents=True, exist_ok=True)
    fname = f"{product_id}_snapshot_{ts.strftime('%Y%m%dT%H%M%SZ')}".strip()
    outpath = outdir / f"{fname}.md"
    outpath.write_text(rendered, encoding="utf-8")
    print(f"AI snapshot written to {outpath}")
    return outpath


def main() -> None:
    parser = argparse.ArgumentParser(description="Export AI-friendly GuardSuite specs")
    parser.add_argument("--product", help="single product id to export")
    parser.add_argument("--all", action="store_true", help="export snapshots for every product")
    parser.add_argument("--out", default=str(OUTDIR), help="output directory for snapshots")
    args = parser.parse_args()

    targets = resolve_targets(args.product, args.all)
    outdir = Path(args.out)
    for pid in targets:
        export(pid, outdir)


if __name__ == "__main__":
    main()
