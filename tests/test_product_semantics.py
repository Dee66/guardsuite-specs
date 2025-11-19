from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_compliance_and_purpose_alignment():
    specs = [
        p
        for p in PRODUCTS.glob("*.yml")
        if not p.name.endswith("_worksheet.yml") and p.name != "guardsuite_master_spec.yml"
    ]
    assert specs, "No product specs found"

    validated = 0
    for path in specs:
        data = load_yaml(path)
        if not data:
            continue

        purpose = data.get("purpose_summary", "").strip()
        assert purpose, f"purpose_summary must be populated in {path}"
        assert len(purpose) > 40, f"purpose_summary too short in {path}"

        compliance = data.get("compliance", {})
        ledger_enabled = compliance.get("compliance_ledger_enabled", False)
        visibility = compliance.get("ledger_visibility")

        if ledger_enabled:
            assert visibility in {"full", "partial", "summary_only"}, (
                f"ledger_visibility must be full|partial|summary_only when enabled in {path}"
            )
        else:
            assert visibility in {"none", None}, f"ledger_visibility must be none when disabled in {path}"

        fixpack = data.get("fixpack", {})
        if fixpack.get("included"):
            assert data.get("product_type") == "paid_blueprint", (
                f"FixPack should only be included for paid products ({path})"
            )
        validated += 1

    assert validated > 0, "No canonical products validated for semantics"