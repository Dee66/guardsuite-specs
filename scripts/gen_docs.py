#!/usr/bin/env python3
# COPILOT: Maintain strict YAML → Markdown determinism. Never reorder fields arbitrarily.
# COPILOT: When adding validation rules, ensure backward-compatibility with all product YAML.
# scripts/gen_docs.py
"""Generate Markdown docs from products/*.yml using templates/*.j2."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"
PRODUCT_SPECS = ROOT / "product_specs"
TEMPLATES = ROOT / "templates"
OUTDIR = ROOT / "docs" / "products"
PRODUCT_INDEX = PRODUCTS / "product_index.yml"
PRODUCTS_DOC_DIR = ROOT / "docs" / "products"
CANONICAL_SCHEMA_PATH = ROOT / "guardsuite-core" / "canonical_schema.json"
SCHEMA_DOC_DIR = ROOT / "docs" / "schema"

DEFAULT_TEMPLATE = "product_page.md.j2"
PRODUCT_TEMPLATE_OVERRIDES = {
    "playground": "spec_page.md.j2",
}
LEGACY_PRODUCT_IDS = {"pillar-template"}

env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)
_CANONICAL_SCHEMA_CACHE: dict | None = None
_CANONICAL_SCHEMA_TEXT: str | None = None


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def get_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def _product_candidate_paths(product_id: str) -> List[Path]:
    return [
        PRODUCTS / f"{product_id}.yml",
        PRODUCT_SPECS / f"{product_id}.yml",
    ]


def resolve_product_spec(product_id: str) -> Path:
    for path in _product_candidate_paths(product_id):
        if path.exists():
            return path
    raise FileNotFoundError(
        f"Product '{product_id}' spec missing under products/ or product_specs/."
    )


def find_product_spec(product_id: str) -> Path | None:
    for path in _product_candidate_paths(product_id):
        if path.exists():
            return path
    return None


def iter_product_files() -> List[Path]:
    files = [
        p
        for p in PRODUCTS.glob("*.yml")
        if not p.name.endswith("_worksheet.yml")
        and p.name not in {"guardsuite_master_spec.yml", "product_index.yml"}
    ]
    seen_ids = {p.stem for p in files}
    for legacy_id in sorted(LEGACY_PRODUCT_IDS):
        if legacy_id in seen_ids:
            continue
        legacy_path = PRODUCT_SPECS / f"{legacy_id}.yml"
        if legacy_path.exists():
            files.append(legacy_path)
            seen_ids.add(legacy_id)
    return sorted(files, key=lambda path: path.stem)


def list_product_ids() -> List[str]:
    return [p.stem for p in iter_product_files()]


def load_optional_yaml(relative_path: str | None) -> dict | None:
    if not relative_path:
        return None
    target = ROOT / relative_path
    if not target.exists():
        raise FileNotFoundError(f"Referenced snippet {relative_path} missing")
    return load_yaml(target)


def _load_canonical_schema() -> dict:
    global _CANONICAL_SCHEMA_CACHE, _CANONICAL_SCHEMA_TEXT
    if _CANONICAL_SCHEMA_CACHE is None:
        if not CANONICAL_SCHEMA_PATH.exists():
            raise FileNotFoundError(
                "guardsuite-core/canonical_schema.json missing; required for schema-linked products"
            )
        raw_text = CANONICAL_SCHEMA_PATH.read_text(encoding="utf-8")
        payload = json.loads(raw_text)
        _CANONICAL_SCHEMA_CACHE = payload
        _CANONICAL_SCHEMA_TEXT = json.dumps(payload, indent=2)
    return _CANONICAL_SCHEMA_CACHE


def _canonical_schema_text() -> str:
    _load_canonical_schema()
    return _CANONICAL_SCHEMA_TEXT or "{}"


def _canonical_schema_context(product: dict) -> dict | None:
    schema_source = (product.get("architecture") or {}).get("schema_source")
    if schema_source != "guardsuite-core/canonical_schema.json":
        return None
    payload = _load_canonical_schema()
    pretty = _canonical_schema_text()
    lines = pretty.splitlines()
    max_lines = 40
    excerpt_lines = lines[:max_lines]
    if len(lines) > max_lines:
        excerpt_lines.append("...")
    return {
        "path": CANONICAL_SCHEMA_PATH.relative_to(ROOT).as_posix(),
        "title": payload.get("title", "GuardSuite Canonical Plan"),
        "description": payload.get("description", ""),
        "required": payload.get("required", []),
        "properties": list((payload.get("properties") or {}).keys()),
        "excerpt": "\n".join(excerpt_lines),
    }


def _run_canonical_validator(failure_prefix: str) -> None:
    validator = ROOT / "scripts" / "validate_products.py"
    cmd = [sys.executable, str(validator), "--check-canonical"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        detail = (result.stderr or "").strip() or (result.stdout or "").strip()
        if not detail:
            detail = "validator reported an unknown failure"
        print(f"{failure_prefix}{detail}", file=sys.stderr)
        raise SystemExit(result.returncode)


def _canonical_preflight() -> None:
    _run_canonical_validator("Canonical schema docs build failed: ")


def resolve_related_products(product_ids: List[str]) -> List[dict]:
    related: List[dict] = []
    for pid in product_ids:
        display_name = pid
        spec_path = find_product_spec(pid)
        if spec_path:
            try:
                display_name = load_yaml(spec_path).get("name", pid)
            except Exception:
                display_name = pid
        related.append({
            "id": pid,
            "name": display_name,
            "doc_path": f"{pid}.md",
        })
    return related


def load_product_index_entries() -> List[dict]:
    if not PRODUCT_INDEX.exists():
        return []
    data = load_yaml(PRODUCT_INDEX) or {}
    entries = data.get("products", [])
    return sorted(entries, key=lambda entry: entry.get("product_id", ""))


def _product_display_name(product_id: str) -> str:
    spec_path = find_product_spec(product_id)
    if not spec_path:
        return product_id
    try:
        return load_yaml(spec_path).get("name", product_id)
    except Exception:
        return product_id


def validate_product(product: dict, product_id: str) -> None:
    required_keys = ("id", "name", "version", "features")
    for key in required_keys:
        if key not in product:
            raise ValueError(f"Product '{product_id}' missing required key: {key}")
        if product[key] in (None, ""):
            raise ValueError(f"Product '{product_id}' has empty value for: {key}")
    if not isinstance(product["features"], list):
        raise ValueError(f"Product '{product_id}' features must be a list")


def _template_for_product(product_id: str) -> str:
    return PRODUCT_TEMPLATE_OVERRIDES.get(product_id, DEFAULT_TEMPLATE)


def render_product(product_id: str, outdir: Path, snippets: dict) -> Path:
    product_file = resolve_product_spec(product_id)
    product = load_yaml(product_file)
    validate_product(product, product_id)
    tpl_name = _template_for_product(product_id)
    tpl = env.get_template(tpl_name)
    iso_timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    meta = {"commit": get_git_commit(), "timestamp": iso_timestamp}
    compliance_matrix = load_optional_yaml(product.get("compliance", {}).get("matrix_snippet"))
    contract_spec = load_optional_yaml(product.get("contract_ref"))
    contract_yaml = yaml.safe_dump(contract_spec, sort_keys=False) if contract_spec else None
    related_links = resolve_related_products(product.get("related_products", []))
    canonical_schema = _canonical_schema_context(product)
    rendered = tpl.render(
        product=product,
        snippets=snippets,
        meta=meta,
        product_raw=yaml.safe_dump(product, sort_keys=False),
        compliance_matrix=compliance_matrix,
        contract_spec=contract_spec,
        contract_yaml=contract_yaml,
        related_product_links=related_links,
        canonical_schema=canonical_schema,
    )
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"{product_id}.md"
    outpath.write_text(rendered, encoding="utf-8")
    return outpath


def render_ecosystem_overview(entries: List[dict]) -> Path:
    PRODUCTS_DOC_DIR.mkdir(parents=True, exist_ok=True)
    doc_path = PRODUCTS_DOC_DIR / "README.md"
    lines = [
        "# Spec Integrity Dashboard",
        "",
        "This overview is generated from `products/product_index.yml`.",
        "",
        "| Product | Version | Category | Contract | Related Products |",
        "|---------|---------|----------|----------|------------------|",
    ]
    for entry in entries:
        product_id = entry.get("product_id", "unknown")
        name = _product_display_name(product_id)
        contract = entry.get("contract_ref") or "none"
        related = ", ".join(entry.get("related_products", [])) or "none"
        lines.append(
            f"| [{name}]({product_id}.md) | {entry.get('version', 'n/a')} | {entry.get('category', 'n/a')} "
            f"| `{contract}` | {related} |"
        )
    doc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return doc_path


def render_canonical_schema_doc() -> Path:
    schema_payload = _load_canonical_schema()
    pretty = _canonical_schema_text()
    SCHEMA_DOC_DIR.mkdir(parents=True, exist_ok=True)
    doc_path = SCHEMA_DOC_DIR / "canonical_schema.md"
    lines = [
        "# GuardSuite Canonical Plan Schema",
        "",
        f"Source of truth: `{CANONICAL_SCHEMA_PATH.relative_to(ROOT).as_posix()}`",
        "",
        "## Summary",
        "",
        f"- Title: {schema_payload.get('title', 'n/a')}",
        f"- Description: {schema_payload.get('description', 'n/a')}",
        f"- Required properties: {', '.join(schema_payload.get('required', [])) or 'n/a'}",
        f"- Declared properties: {', '.join((schema_payload.get('properties') or {}).keys()) or 'n/a'}",
        "",
        "## JSON Schema",
        "",
        "```json",
        pretty,
        "```",
    ]
    doc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return doc_path


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

    _canonical_preflight()

    targets = resolve_targets(args.product, args.all)
    snippets = load_yaml(ROOT / "snippets" / "marketing.yml")
    outdir = Path(args.out)
    for pid in targets:
        outpath = render_product(pid, outdir, snippets)
        print(f"Wrote {outpath}")
    overview_entries = load_product_index_entries()
    if overview_entries:
        overview_path = render_ecosystem_overview(overview_entries)
        print(f"Updated ecosystem overview at {overview_path}")
    schema_doc = render_canonical_schema_doc()
    print(f"Wrote canonical schema reference at {schema_doc}")


if __name__ == "__main__":
    main()


def on_pre_build(config, **kwargs):  # pragma: no cover - invoked via mkdocs hooks
    _run_canonical_validator("Canonical schema mkdocs build failed: ")
