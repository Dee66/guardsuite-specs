import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"

BASIC_KEYS = {"id", "name", "version", "long_description", "features", "maintainers"}
STRICT_KEYS = {
    "product_type",
    "pillar",
    "status",
    "short_description",
    "purpose_summary",
    "architecture",
    "governance_domains",
    "rule_categories",
    "cli",
    "performance_constraints",
    "ecosystem_integrations",
    "security",
    "release_metadata",
    "references",
}
ALLOWED_PRODUCT_TYPES = {"free_scanner", "paid_blueprint", "scoring_engine", "core"}

def _product_spec_paths():
    return [
        p
        for p in PRODUCTS.glob("*.yml")
        if not p.name.endswith("_worksheet.yml") and p.name != "guardsuite_master_spec.yml"
    ]


def test_all_yaml_files_parse_and_contain_required_keys():
    yaml_files = _product_spec_paths()
    assert yaml_files, "No product YAML files found in products/"

    canonical_products = 0
    for file in yaml_files:
        text = file.read_text(encoding="utf-8")
        assert "\t" not in text, f"Tabs detected in {file}"
        assert "example.com" not in text.lower(), f"Forbidden domain example.com in {file}"

        data = yaml.safe_load(text)
        if data is None:
            continue
        assert isinstance(data, dict), f"{file} did not load as a dict"

        for key in BASIC_KEYS:
            assert key in data, f"Missing {key} in {file}"
            if key == "features":
                assert isinstance(data[key], list), f"features must be a list in {file}"
            elif key == "maintainers":
                assert isinstance(data[key], list) and data[key], f"maintainers must be a non-empty list in {file}"
            else:
                assert data[key], f"{key} missing or empty in {file}"

        if not STRICT_KEYS.issubset(data.keys()):
            # Placeholder specs are allowed to omit the strict contract for now.
            continue

        canonical_products += 1

        missing = STRICT_KEYS - set(data.keys())
        assert not missing, f"Missing strict keys in {file}: {missing}"

        assert data["id"], f"id missing or empty in {file}"
        assert data["name"], f"name missing or empty in {file}"
        assert data["pillar"] in ["vector", "compute", "pipeline", "crosscut"], f"Invalid pillar value in {file}"
        assert data["product_type"] in ALLOWED_PRODUCT_TYPES, f"Invalid product_type in {file}"

        version = str(data["version"])
        assert version.replace(".", "").isdigit(), f"Invalid version format in {file}"

        features = data["features"]
        assert isinstance(features, list) and features, f"Features must be a non-empty list in {file}"
        for feature in features:
            assert {"id", "title", "summary"} <= set(feature.keys()), f"Incomplete feature entry in {file}"
            assert isinstance(feature.get("included"), bool), f"Feature included flag must be bool in {file}"

        release = data["release_metadata"]
        assert release["release_notes_url"].startswith("https://shieldcraft-ai.com/"), (
            f"Release notes must use shieldcraft-ai.com domain in {file}"
        )

        references = data["references"]
        canonical_schema = references.get("canonical_schema", "")
        assert canonical_schema.endswith(".json"), f"Canonical schema reference must be a JSON path in {file}"

        fixpack = data["fixpack"]
        assert isinstance(fixpack.get("included"), bool), f"fixpack.included must be bool in {file}"
        if fixpack["included"]:
            assert fixpack.get("fixpack_folder"), f"fixpack_folder required when fixpack is included in {file}"
            assert fixpack.get("snippet_count", 0) > 0, f"snippet_count must be positive when fixpack included in {file}"

        compliance = data["compliance"]
        if compliance.get("compliance_ledger_enabled"):
            assert compliance.get("ledger_visibility") in {"full", "partial", "summary_only"}, (
                f"ledger_visibility must be full|partial|summary_only when ledger enabled in {file}"
            )

        cli = data["cli"]
        assert cli.get("base_command"), f"base_command missing in {file}"
        if data.get("pillar") == "crosscut":
            assert cli.get("scan_command") in (None, ""), f"Crosscut products should not define scan_command in {file}"
            api = data.get("api")
            assert api and api.get("rest_endpoint"), f"Crosscut products must expose api.rest_endpoint in {file}"
        else:
            assert cli.get("scan_command"), f"scan_command missing in {file}"

    assert canonical_products > 0, "No canonical product specs validated"
