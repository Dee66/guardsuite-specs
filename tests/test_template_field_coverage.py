import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"
TEMPLATES = ROOT / "templates"
EXCLUDED_SPECS = {"guardsuite_master_spec.yml", "guardsuite-template.yml", "pillar-template.yml"}

TEMPLATE_FILES = [
    TEMPLATES / "spec_page.md.j2",
    TEMPLATES / "spec_snapshot.md.j2",
    TEMPLATES / "partials" / "spec_header.html",
]

# High-level fields that must be referenced in templates. We check by looking for the
# name "product.<field>" in the template sources. This is intentionally lightweight
# but catches regressions when adding new YAML keys that docs need to surface.
REQUIRED_FIELDS = [
    "marketing.hero",
    "marketing.blurbs",
    "marketing.ctas",
    "architecture.core_dependency_id",
    "architecture.required_interfaces",
    "architecture.override_exclusion",
    "architecture.output_contract",
    "ecosystem_integrations.guardscore.pillar_weight",
    "ecosystem_integrations.guardscore.provided_score_inputs",
    "ecosystem_integrations.playground.max_runtime_ms",
    "ecosystem_integrations.playground.quick_score_mode",
    "ecosystem_integrations.guardboard.badge_preview_supported",
    "performance_constraints.large_plan_runtime_ms",
    "performance_constraints.realtime_refresh_interval_ms",
    "versioning.core_dependency_pin",
    "versioning.schema_version_pin",
    "interoperability_conflicts",
    "future_extensions",
    "scoring_model.description",
    "badge_contract.badge_svg_fields",
    "integration_points.products_consuming",
    "api.rest_endpoint",
]

FIELD_ALIASES = {
    "ecosystem_integrations.playground.max_runtime_ms": [
        "playground.max_runtime_ms",
    ],
    "ecosystem_integrations.playground.quick_score_mode": [
        "playground.quick_score_mode",
        "integration_points.playground.quick_score_mode_supported",
    ],
    "ecosystem_integrations.guardboard.badge_preview_supported": [
        "guardboard.badge_preview_supported",
    ],
    "ecosystem_integrations.guardscore.provided_score_inputs": [
        "provided_inputs",
    ],
    "performance_constraints.large_plan_runtime_ms": [
        "perf.large_plan_runtime_ms",
    ],
    "performance_constraints.realtime_refresh_interval_ms": [
        "perf.realtime_refresh_interval_ms",
    ],
}

# Template references that no longer exist in YAML should be removed. If a template
# references any of these strings the test should fail.
FORBIDDEN_TEMPLATE_SNIPPETS = [
    "product.references.docs_page",
]


def _template_text() -> str:
    contents = []
    for path in TEMPLATE_FILES:
        assert path.exists(), f"Template missing: {path}"
        contents.append(path.read_text(encoding="utf-8"))
    return "\n".join(contents)


def test_required_fields_have_template_references():
    text = _template_text()
    for field in REQUIRED_FIELDS:
        needle = f"product.{field}"
        aliases = FIELD_ALIASES.get(field, [])
        if needle in text:
            continue
        if any(alias in text for alias in aliases):
            continue
        assert False, f"Template missing reference to `{needle}`"


def test_templates_do_not_reference_removed_fields():
    text = _template_text()
    for forbidden in FORBIDDEN_TEMPLATE_SNIPPETS:
        assert forbidden not in text, f"Template still references removed field `{forbidden}`"


def test_all_product_yaml_fields_are_known():
    """Quick sanity check that top-level fields are consistent across products."""
    known_fields = {
        "id",
        "name",
        "product_type",
        "pillar",
        "version",
        "status",
        "short_description",
        "long_description",
        "purpose_summary",
        "marketing",
        "architecture",
        "governance_domains",
        "rule_categories",
        "features",
        "fixpack",
        "compliance",
        "cli",
        "performance_constraints",
        "ecosystem_integrations",
        "testing",
        "versioning",
        "interoperability_conflicts",
        "future_extensions",
        "security",
        "maintainers",
        "release_metadata",
        "references",
        "api",
        "scoring_model",
        "badge_contract",
        "integration_points",
        "metadata",
        "governance",
        "related_products",
        "owner",
        "spec_yaml",
        "checklist_yaml",
        "gpt_instructions_yaml",
        "provenance",
        "products",
    }

    for spec_path in PRODUCTS.glob("*.yml"):
        if spec_path.name.endswith("_worksheet.yml") or spec_path.name in EXCLUDED_SPECS:
            continue
        data = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
        unknown = set(data.keys()) - known_fields
        assert not unknown, f"Unexpected top-level fields {unknown} in {spec_path}"
