#!/usr/bin/env python3
# COPILOT: Snapshots must be safe for direct paste into AI chats.
# COPILOT: Strip any unnecessary whitespace and ensure stable YAML ordering.
# scripts/export_for_ai.py
"""Export single-file spec snapshots for AI workflows."""

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
TEMPLATES = ROOT / "templates"
OUTDIR = ROOT / "ai_snapshots"
PRODUCT_INDEX_PATH = PRODUCTS / "product_index.yml"
CANONICAL_SCHEMA_PATH = ROOT / "guardsuite-core" / "canonical_schema.json"
CANONICAL_REQUIRED_TOP_LEVEL = {"plan_id", "schema_version", "resources", "metadata"}
SNAPSHOT_PREFIX = "Canonical schema snapshot-export failed: "
CROSSMAP_PREFIX = "Canonical schema crossmap failed: "
REGISTRY_PREFIX = "Canonical schema registry failed: "
ROLLUP_PREFIX = "Canonical schema rollup failed: "
DISTRIBUTION_PREFIX = "Canonical schema distribution failed: "
PILLAR_TEMPLATE_PRODUCT_ID = "pillar-template"
PILLAR_TEMPLATE_SPEC_PATH = ROOT / "product_specs" / "pillar-template.yml"

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


def load_product_index() -> List[dict]:
    if not PRODUCT_INDEX_PATH.exists():
        return []
    data = load_yaml(PRODUCT_INDEX_PATH) or {}
    return data.get("products", [])


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


def export(
    product_id: str,
    outdir: Path,
    canonical_excerpt: dict | None,
    canonical_status: str,
    rollup_path: str | None = None,
    spec_path: Path | None = None,
) -> Path:
    product_file = spec_path or (PRODUCTS / f"{product_id}.yml")
    if not product_file.exists():
        raise FileNotFoundError(f"{product_file} missing")
    product = load_yaml(product_file)
    tpl = env.get_template("spec_snapshot.md.j2")
    ts = datetime.now(timezone.utc)
    iso_timestamp = ts.isoformat().replace("+00:00", "Z")
    meta = {
        "commit": get_git_commit(),
        "timestamp": iso_timestamp,
        "canonical_schema_status": canonical_status,
    }
    if rollup_path:
        meta["canonical_rollup"] = rollup_path
    product_raw = yaml.safe_dump(product, sort_keys=False).strip()
    rendered = tpl.render(
        product=product,
        meta=meta,
        product_raw=product_raw,
        canonical_excerpt=canonical_excerpt,
    ).strip() + "\n"
    outdir.mkdir(parents=True, exist_ok=True)
    fname = f"{product_id}_snapshot_{ts.strftime('%Y%m%dT%H%M%SZ')}".strip()
    outpath = outdir / f"{fname}.md"
    outpath.write_text(rendered, encoding="utf-8")
    print(f"AI snapshot written to {outpath}")
    return outpath


def _export_pillar_template(
    outdir: Path,
    canonical_excerpt: dict | None,
    canonical_status: str,
    rollup_path: str | None,
) -> Path:
    if not PILLAR_TEMPLATE_SPEC_PATH.exists():
        raise FileNotFoundError("product_specs/pillar-template.yml missing; bootstrap pillar template spec")
    return export(
        PILLAR_TEMPLATE_PRODUCT_ID,
        outdir,
        canonical_excerpt,
        canonical_status,
        rollup_path,
        spec_path=PILLAR_TEMPLATE_SPEC_PATH,
    )


def _index_map(entries: List[dict]) -> Dict[str, dict]:
    return {entry.get("product_id"): entry for entry in entries}


def export_product_index_snapshot(outdir: Path, canonical_status: str) -> Path:
    if not PRODUCT_INDEX_PATH.exists():
        raise FileNotFoundError("products/product_index.yml missing")
    ts = datetime.now(timezone.utc)
    iso_timestamp = ts.isoformat().replace("+00:00", "Z")
    registry_manifest = load_yaml(PRODUCT_INDEX_PATH) or {}
    registry_metadata = registry_manifest.get("metadata")
    if isinstance(registry_metadata, dict):
        registry_metadata["canonical_schema_status"] = canonical_status
    payload = {
        "meta": {
            "commit": get_git_commit(),
            "timestamp": iso_timestamp,
            "canonical_schema_status": canonical_status,
        },
        "index": registry_manifest,
    }
    serialized = yaml.safe_dump(payload, sort_keys=False).strip() + "\n"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"product_index_snapshot_{ts.strftime('%Y%m%dT%H%M%SZ')}.yml"
    outpath.write_text(serialized, encoding="utf-8")
    print(f"Product index snapshot written to {outpath}")
    return outpath


def export_products_bundle(
    product_ids: List[str], outdir: Path, index_entries: List[dict], canonical_status: str
) -> Path:
    index_lookup = _index_map(index_entries)
    ts = datetime.now(timezone.utc)
    iso_timestamp = ts.isoformat().replace("+00:00", "Z")
    bundle: List[dict] = []
    for pid in product_ids:
        spec_path = PRODUCTS / f"{pid}.yml"
        if not spec_path.exists():
            continue
        spec = load_yaml(spec_path)
        entry = index_lookup.get(pid, {})
        schema_path = entry.get("schema_path")
        schema = None
        if schema_path:
            schema_file = ROOT / schema_path
            if schema_file.exists():
                schema = load_yaml(schema_file)
        contract_ref = entry.get("contract_ref")
        contract = None
        if contract_ref:
            contract_file = ROOT / contract_ref
            if contract_file.exists():
                contract = load_yaml(contract_file)
        bundle.append(
            {
                "product_id": pid,
                "category": entry.get("category"),
                "spec": spec,
                "schema_path": schema_path,
                "schema": schema,
                "contract_ref": contract_ref,
                "contract": contract,
            }
        )
    payload = {
        "meta": {
            "commit": get_git_commit(),
            "timestamp": iso_timestamp,
            "canonical_schema_status": canonical_status,
        },
        "products": bundle,
    }
    serialized = yaml.safe_dump(payload, sort_keys=False).strip() + "\n"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"products_bundle_{ts.strftime('%Y%m%dT%H%M%SZ')}.yml"
    outpath.write_text(serialized, encoding="utf-8")
    print(f"Product bundle export written to {outpath}")
    return outpath


def export_contracts_bundle(
    index_entries: List[dict], outdir: Path, canonical_status: str
) -> Path | None:
    contracts = []
    for entry in index_entries:
        ref = entry.get("contract_ref")
        if not ref:
            continue
        target = ROOT / ref
        if not target.exists():
            continue
        contracts.append(
            {
                "product_id": entry.get("product_id"),
                "contract_ref": ref,
                "contract": load_yaml(target),
            }
        )
    if not contracts:
        return None
    ts = datetime.now(timezone.utc)
    payload = {
        "meta": {
            "commit": get_git_commit(),
            "timestamp": ts.isoformat().replace("+00:00", "Z"),
            "canonical_schema_status": canonical_status,
        },
        "contracts": contracts,
    }
    serialized = yaml.safe_dump(payload, sort_keys=False).strip() + "\n"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"contracts_bundle_{ts.strftime('%Y%m%dT%H%M%SZ')}.yml"
    outpath.write_text(serialized, encoding="utf-8")
    print(f"Contract bundle export written to {outpath}")
    return outpath


def export_playground_contract(outdir: Path | None = None, canonical_status: str | None = None) -> Path:
    """Write the Playground contract as a standalone YAML artifact for downstream AI tools."""
    contract_path = ROOT / "contracts" / "playground_contract.yml"
    if not contract_path.exists():
        raise FileNotFoundError(f"{contract_path} missing")
    contract = load_yaml(contract_path)
    ts = datetime.now(timezone.utc)
    iso_timestamp = ts.isoformat().replace("+00:00", "Z")
    meta = {
        "commit": get_git_commit(),
        "timestamp": iso_timestamp,
    }
    if canonical_status:
        meta["canonical_schema_status"] = canonical_status
    payload = {
        "meta": meta,
        "contract": contract,
    }
    serialized = yaml.safe_dump(payload, sort_keys=False).strip() + "\n"
    target_dir = Path(outdir) if outdir else OUTDIR
    target_dir.mkdir(parents=True, exist_ok=True)
    fname = f"playground_contract_{ts.strftime('%Y%m%dT%H%M%SZ')}.yml"
    outpath = target_dir / fname
    outpath.write_text(serialized, encoding="utf-8")
    print(f"Playground contract export written to {outpath}")
    return outpath


def export_canonical_schema(outdir: Path, canonical_payload: dict, canonical_status: str | None = None) -> Path:
    ts = datetime.now(timezone.utc)
    iso_timestamp = ts.isoformat().replace("+00:00", "Z")
    meta = {"commit": get_git_commit(), "timestamp": iso_timestamp}
    if canonical_status:
        meta["canonical_schema_status"] = canonical_status
    wrapper = {
        "meta": meta,
        "path": CANONICAL_SCHEMA_PATH.relative_to(ROOT).as_posix(),
        "schema": canonical_payload,
    }
    serialized = yaml.safe_dump(wrapper, sort_keys=False).strip() + "\n"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"canonical_schema_{ts.strftime('%Y%m%dT%H%M%SZ')}.yml"
    outpath.write_text(serialized, encoding="utf-8")
    print(f"Canonical schema export written to {outpath}")
    return outpath


def load_canonical_schema_or_die() -> dict:
    if not CANONICAL_SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Canonical schema missing at {CANONICAL_SCHEMA_PATH.relative_to(ROOT)}"
        )
    try:
        payload = json.loads(CANONICAL_SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Canonical schema JSON invalid: {exc}") from exc
    if payload.get("type") != "object":
        raise ValueError("Canonical schema must declare top-level type 'object'")
    required = payload.get("required", [])
    if not isinstance(required, list):
        raise ValueError("Canonical schema missing 'required' list")
    missing_required = CANONICAL_REQUIRED_TOP_LEVEL - set(required)
    if missing_required:
        raise ValueError(
            "Canonical schema required list missing keys: " + ", ".join(sorted(missing_required))
        )
    properties = payload.get("properties")
    if not isinstance(properties, dict):
        raise ValueError("Canonical schema missing 'properties' object")
    missing_properties = CANONICAL_REQUIRED_TOP_LEVEL - set(properties.keys())
    if missing_properties:
        raise ValueError(
            "Canonical schema properties missing keys: " + ", ".join(sorted(missing_properties))
        )
    return payload


def _run_canonical_validator(failure_prefix: str) -> str:
    validator = ROOT / "scripts" / "validate_products.py"
    cmd = [sys.executable, str(validator), "--check-canonical"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        detail = (result.stderr or "").strip() or (result.stdout or "").strip()
        if not detail:
            detail = "validator reported an unknown failure"
        print(f"{failure_prefix}{detail}", file=sys.stderr)
        sys.exit(result.returncode)
    status_line = (result.stdout or "").strip() or "canonical_schema: OK"
    return status_line


def _write_canonical_status(outdir: Path, status_line: str) -> None:
    if not status_line or not outdir.exists():
        return
    marker = outdir / "canonical_status.txt"
    marker.write_text(status_line + "\n", encoding="utf-8")
    print(f"Canonical schema status written to {marker}")


def _write_canonical_rollup(outdir: Path, status_line: str, artifact_types: List[str]) -> None:
    if not status_line or not artifact_types:
        return
    if not outdir.exists():
        outdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    unique_artifacts = list(dict.fromkeys(artifact_types))
    payload = {
        "canonical_schema_status": status_line,
        "timestamp": ts,
        "artifacts": unique_artifacts,
    }
    serialized = yaml.safe_dump(payload, sort_keys=False).strip() + "\n"
    rollup_path = outdir / "canonical_integrity_rollup.yml"
    rollup_path.write_text(serialized, encoding="utf-8")
    print(f"Canonical integrity rollup written to {rollup_path}")


def canonical_schema_excerpt(payload: dict | None) -> dict | None:
    if not payload:
        return None
    required = payload.get("required") or []
    prop_keys = sorted(payload.get("properties", {}).keys())
    preview_keys = prop_keys[:6]
    return {"required": required, "properties": preview_keys}


EXPORT_DISPATCH = {
    PILLAR_TEMPLATE_PRODUCT_ID: _export_pillar_template,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Export AI-friendly GuardSuite specs")
    parser.add_argument("--product", help="single product id to export")
    parser.add_argument("--all", action="store_true", help="export snapshots for every product")
    parser.add_argument("--out", default=str(OUTDIR), help="output directory for snapshots")
    args = parser.parse_args()

    needs_registry_guard = bool(args.all)
    needs_crossmap_guard = bool(args.product == "product_index") and not needs_registry_guard
    if needs_registry_guard:
        validator_prefix = REGISTRY_PREFIX
    elif needs_crossmap_guard:
        validator_prefix = CROSSMAP_PREFIX
    else:
        validator_prefix = SNAPSHOT_PREFIX

    try:
        canonical_schema = load_canonical_schema_or_die()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{validator_prefix}{exc}", file=sys.stderr)
        sys.exit(1)

    canonical_status_line = _run_canonical_validator(validator_prefix)

    canonical_excerpt = canonical_schema_excerpt(canonical_schema)

    targets = resolve_targets(args.product, args.all)
    outdir = Path(args.out)
    index_entries = load_product_index()
    rollup_reference = "canonical_integrity_rollup.yml" if args.all else None
    for pid in targets:
        exporter = EXPORT_DISPATCH.get(pid)
        if exporter:
            exporter(outdir, canonical_excerpt, canonical_status_line, rollup_reference)
        else:
            export(pid, outdir, canonical_excerpt, canonical_status_line, rollup_reference)
    if args.all:
        export_products_bundle(targets, outdir, index_entries, canonical_status_line)
        export_product_index_snapshot(outdir, canonical_status_line)
        export_contracts_bundle(index_entries, outdir, canonical_status_line)
    _write_canonical_status(outdir, canonical_status_line)
    export_canonical_schema(outdir, canonical_schema, canonical_status_line)
    artifacts = ["snapshots"]
    if args.all:
        artifacts.extend(["bundles", "registry", "crossmap", "contracts", "canonical_schema"])
    else:
        if args.product == "product_index":
            artifacts.append("crossmap")
        artifacts.append("canonical_schema")
    rollup_status_line = _run_canonical_validator(ROLLUP_PREFIX)
    _write_canonical_rollup(outdir, rollup_status_line, artifacts)


if __name__ == "__main__":
    main()
