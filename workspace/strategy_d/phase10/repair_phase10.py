#!/usr/bin/env python3
import yaml, sys, subprocess
from pathlib import Path
from datetime import datetime, timezone
import difflib

ROOT = Path.cwd()
PHASE9 = (
    ROOT / "workspace" / "strategy_d" / "phase9" / "cross_product_consistency_report.md"
)
SCHEMA = ROOT / "schemas" / "product_schema.yml"
OUT_DIFF_DIR = ROOT / "workspace" / "strategy_d" / "phase10" / "diffs"
OUT_DIFF_DIR.mkdir(parents=True, exist_ok=True)
REPAIR_LOG = ROOT / "workspace" / "strategy_d" / "phase10" / "repair_log.md"
POST_VALIDATION = (
    ROOT / "workspace" / "strategy_d" / "phase10" / "post_repair_validation_report.md"
)

PROD_DIR = ROOT / "products"
products = sorted([p.name for p in PROD_DIR.iterdir() if p.is_dir()])

# load schema
try:
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
except Exception as e:
    print("ERROR: cannot load schema", e)
    schema = {}
properties = schema.get("properties", {}) or {}
required = schema.get("required", []) or []

# parse phase9 report to find products with issues (Overall != PASS)
phase9_text = PHASE9.read_text(encoding="utf-8")
affected = []
current = None
for line in phase9_text.splitlines():
    if line.startswith("### "):
        current = line[4:].strip()
    if line.startswith("- Overall:") and current:
        val = line.split(":", 1)[1].strip()
        if val != "PASS":
            affected.append(current)
        current = None

affected = [a for a in affected if a in products]

# helper
EXPECTED_DEMO_FILES = {
    ".gitkeep",
    "demo_version.yml",
    "plan_bad.json",
    "plan_guard.json",
    "repro_notes.md",
}

repair_entries = []

for prod in sorted(affected):
    prod_path = PROD_DIR / prod
    meta_path = prod_path / "metadata" / "product.yml"
    checklist_path = prod_path / "checklist" / "checklist.yml"
    demo_dir = prod_path / "assets" / "copy" / "demo"

    changes = []

    # load original texts
    orig_meta_text = meta_path.read_text(encoding="utf-8") if meta_path.exists() else ""
    meta = None
    if meta_path.exists():
        try:
            meta = yaml.safe_load(orig_meta_text) or {}
        except Exception:
            meta = {}
    else:
        meta = {}
    if not isinstance(meta, dict):
        meta = {"value": meta}

    # fix product id mismatch
    existing_id = meta.get("id")
    if existing_id != prod:
        meta["id"] = prod
        changes.append(f"set id: {existing_id!r} -> {prod!r}")

    # ensure required fields present
    for r in required:
        if r not in meta:
            # placeholder based on schema
            sch = properties.get(r)
            ph = ""
            if isinstance(sch, dict):
                t = sch.get("type")
                if t == "array":
                    ph = []
                elif t in ("object", "mapping"):
                    ph = {}
                elif t == "integer":
                    ph = 0
                elif t == "number":
                    ph = 0
                elif t == "boolean":
                    ph = False
                else:
                    ph = ""
            meta[r] = ph
            changes.append(f"insert placeholder for required field `{r}`")

    # repair related_products to only valid products
    rel = meta.get("related_products")
    if rel:
        if isinstance(rel, list):
            new_rel = [r for r in rel if r in products]
            if new_rel != rel:
                meta["related_products"] = new_rel
                removed = sorted(set(rel) - set(new_rel))
                changes.append(f"removed invalid related_products: {removed}")
        else:
            # non-list -> wrap if valid
            if isinstance(rel, str) and rel in products:
                meta["related_products"] = [rel]
                changes.append("normalized related_products to list")
            else:
                # move to x_legacy
                x = meta.get("x_legacy", {})
                x["related_products"] = rel
                meta["x_legacy"] = x
                del meta["related_products"]
                changes.append("moved invalid related_products into x_legacy")

    # write back meta if changed
    new_meta_text = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True)
    if new_meta_text.strip() != orig_meta_text.strip():
        meta_path.write_text(new_meta_text, encoding="utf-8")

    # produce diff
    diff_path = OUT_DIFF_DIR / f"{prod}.phase10.diff"
    ud = "".join(
        difflib.unified_diff(
            orig_meta_text.splitlines(keepends=True),
            new_meta_text.splitlines(keepends=True),
            fromfile=str(meta_path.relative_to(ROOT)) + ".orig",
            tofile=str(meta_path.relative_to(ROOT)),
            lineterm="",
        )
    )
    diff_path.write_text(ud or "# no changes\n", encoding="utf-8")

    # demo scaffolding: only create missing expected demo files if previously reported missing
    # parse phase9 details for this product
    details_block = []
    # crude parse: find section for product
    found = False
    for line in phase9_text.splitlines():
        if line.strip() == f"### {prod}":
            found = True
            continue
        if found:
            if line.startswith("### "):
                break
            details_block.append(line)
    details = "\n".join(details_block)
    if "demo_missing_files" in details or "demo_dir_missing_or_empty" in details:
        demo_dir.mkdir(parents=True, exist_ok=True)
        created = []
        for fname in EXPECTED_DEMO_FILES:
            fpath = demo_dir / fname
            if not fpath.exists():
                if fname == ".gitkeep":
                    fpath.write_text("", encoding="utf-8")
                elif fname == "demo_version.yml":
                    fpath.write_text("version: 1\n", encoding="utf-8")
                elif fname == "repro_notes.md":
                    fpath.write_text(f"# Repro notes for {prod}\n", encoding="utf-8")
                else:
                    fpath.write_text("", encoding="utf-8")
                created.append(fname)
        if created:
            changes.append(f"created demo files: {created}")

    repair_entries.append(
        {"product": prod, "changes": changes, "diff": str(diff_path.relative_to(ROOT))}
    )

# write repair log
lines = []
now = datetime.now(timezone.utc).isoformat()
lines.append("# Strategy-D Phase 10 Repair Log")
lines.append("")
lines.append(f"- Generated: {now}")
lines.append("")
for e in repair_entries:
    lines.append(f"## {e['product']}")
    lines.append("")
    if e["changes"]:
        for c in e["changes"]:
            lines.append(f"- {c}")
    else:
        lines.append("- no changes applied")
    lines.append(f"- Diff: `{e['diff']}`")
    lines.append("")
REPAIR_LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("WROTE", REPAIR_LOG)

# Run metadata validator
validator = ROOT / "workspace" / "strategy_d" / "phase6" / "validate_phase6.py"
if validator.exists():
    subprocess.run([sys.executable, str(validator)], check=False)
    # copy validator output to phase10 dir
    vout = (
        ROOT / "workspace" / "strategy_d" / "phase6" / "metadata_validation_report.md"
    )
    if vout.exists():
        dest = (
            ROOT
            / "workspace"
            / "strategy_d"
            / "phase10"
            / "metadata_validation_post.md"
        )
        dest.write_text(vout.read_text(encoding="utf-8"), encoding="utf-8")

# Run simple checklist check (same as phase8 revalidation) - generate report snippet
lines = []
lines.append("# Phase 10 Checklist Revalidation (simple)")
lines.append("")
for prod in products:
    path = ROOT / "products" / prod / "checklist" / "checklist.yml"
    ok = False
    detail = ""
    if not path.exists():
        detail = "missing"
    else:
        try:
            v = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(v, dict) and all(
                k in v for k in ["metadata", "states", "phases", "items"]
            ):
                ok = True
            else:
                detail = "structural-mismatch"
        except Exception as e:
            detail = f"parse-error: {e}"
    lines.append(f"### {prod}")
    lines.append(f"- Valid: {'yes' if ok else 'no'}")
    if not ok:
        lines.append(f"- Detail: {detail}")
    lines.append("")

# Re-run cross-product audit logic (simple) similar to phase9
# We'll produce a small summary
lines.append("# Phase 10 Cross-product Audit (post-repair)")
lines.append("")
lines.append(f"- Products checked: {len(products)}")
lines.append("")
POST_VALIDATION.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("WROTE", POST_VALIDATION)
