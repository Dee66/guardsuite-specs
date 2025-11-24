from __future__ import annotations

import re

import pytest

from tests.utils import (
    CANONICAL_PRODUCT_IDS,
    KNOWN_PRODUCT_ALIASES,
    PRODUCT_SPEC_RECORDS,
    PRODUCT_SPEC_IDS,
)


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_marketing_sections_have_content(record):
    spec = record.data
    marketing = spec.get("marketing", {})
    hero = marketing.get("hero", "").strip()
    blurbs = marketing.get("blurbs", [])
    assert hero, f"marketing.hero missing or empty in {record.path}"
    assert blurbs and all(isinstance(blurb, str) and blurb.strip() for blurb in blurbs), (
        f"marketing.blurbs must contain non-empty strings in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_marketing_ctas_have_valid_hyperlinks(record):
    spec = record.data
    marketing = spec.get("marketing", {})
    ctas = marketing.get("ctas", [])
    assert ctas, f"marketing.ctas missing for {record.path}"
    for cta in ctas:
        text = cta.get("text", "").strip()
        href = cta.get("href", "")
        assert text, f"CTA text missing for {record.path}"
        assert href.startswith("/") or href.startswith("https://"), (
            f"CTA href must be absolute or root-relative in {record.path}"
        )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_release_notes_url_matches_product_identity(record):
    spec = record.data
    release = spec.get("release_metadata", {})
    url = release.get("release_notes_url", "")
    product_id = spec.get("id", record.file_id)
    version = str(spec.get("version", "")).strip()
    normalized_id = product_id.replace("_", "-")
    assert url.startswith("https://shieldcraft-ai.com/"), (
        f"release_notes_url must use shieldcraft-ai.com domain in {record.path}"
    )
    assert normalized_id in url, (
        f"release_notes_url must include product id {normalized_id} in {record.path}"
    )
    assert version and version in url, (
        f"release_notes_url must include product version {version} in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_maintainers_contacts_are_emails(record):
    spec = record.data
    maintainers = spec.get("maintainers", [])
    assert maintainers, f"Maintainers missing in {record.path}"
    for maintainer in maintainers:
        contact = maintainer.get("contact", "")
        assert "@" in contact and contact.count("@") == 1, (
            f"Maintainer contact must be an email address in {record.path}"
        )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_governance_domains_have_minimum_entries(record):
    spec = record.data
    domains = spec.get("governance_domains", [])
    assert len(domains) >= 3, f"governance_domains must contain at least 3 entries in {record.path}"
    assert all(isinstance(domain, str) and domain.strip() for domain in domains), (
        f"governance_domains entries must be non-empty strings in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_features_have_unique_and_well_formed_ids(record):
    spec = record.data
    features = spec.get("features", [])
    assert features, f"Features missing in {record.path}"
    ids = [feature.get("id", "") for feature in features]
    assert len(ids) == len(set(ids)), f"Feature IDs must be unique in {record.path}"
    for feature_id in ids:
        assert re.match(r"^[A-Z0-9-]+$", feature_id), (
            f"Feature ID {feature_id} must be uppercase alphanumeric with dashes in {record.path}"
        )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_security_contract_has_required_booleans(record):
    spec = record.data
    security = spec.get("security", {})
    required_keys = ("sanitize_all_inputs", "svg_sanitization", "wasm_compatible")
    for key in required_keys:
        assert isinstance(security.get(key), bool), f"security.{key} must be bool in {record.path}"
    sandbox_requirement = security.get("sandbox_requirement", "")
    assert isinstance(sandbox_requirement, str) and sandbox_requirement.strip(), (
        f"security.sandbox_requirement must be descriptive in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_fixpack_hint_format_contains_issue_placeholder(record):
    spec = record.data
    fixpack = spec.get("fixpack", {})
    hint_format = fixpack.get("reference_hint_format") or fixpack.get("remediation_hint_format", "")
    assert hint_format, f"FixPack hint format missing in {record.path}"
    assert "<ISSUE_ID>" in hint_format, (
        f"FixPack hint format must include <ISSUE_ID> placeholder in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_related_products_reference_known_ids(record):
    spec = record.data
    related = spec.get("related_products", [])
    assert isinstance(related, list), f"related_products must be a list in {record.path}"
    for product in related:
        if product in CANONICAL_PRODUCT_IDS:
            continue
        alias_target = KNOWN_PRODUCT_ALIASES.get(product)
        assert alias_target in CANONICAL_PRODUCT_IDS, (
            f"related product {product} not found in canonical set for {record.path}"
        )
