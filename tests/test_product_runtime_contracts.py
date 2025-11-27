from __future__ import annotations

import pytest

from tests.utils import PRODUCT_SPEC_RECORDS, PRODUCT_SPEC_IDS


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_cli_base_command_matches_product_id(record):
    spec = record.data
    base_command = spec.get("cli", {}).get("base_command", "")
    product_id = spec.get("id", record.file_id)
    assert base_command, f"cli.base_command missing in {record.path}"
    normalized_base = base_command.replace("_", "-")
    normalized_id = product_id.replace("_", "-")
    assert normalized_base.startswith(normalized_id.split("-")[0]), (
        f"cli.base_command must align with product id in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_cli_scan_command_aligns_with_base_command(record):
    spec = record.data
    cli = spec.get("cli", {})
    scan_command = (cli.get("scan_command") or "").strip()
    base_command = cli.get("base_command", "").strip()
    pillar = spec.get("pillar")
    if pillar == "crosscut":
        assert scan_command in {
            "",
            None,
        }, f"Crosscut products should not define scan_command ({record.path})"
        return
    assert scan_command and scan_command.startswith(base_command), (
        f"scan_command must start with base_command for {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_cli_supported_flags_include_json(record):
    spec = record.data
    cli = spec.get("cli", {})
    flags = cli.get("supported_flags", [])
    reserved = cli.get("reserved_flags", [])
    assert flags, f"cli.supported_flags missing for {record.path}"
    assert all(flag.startswith("--") for flag in flags), (
        f"cli.supported_flags entries must start with -- ({record.path})"
    )
    if "--json" in flags:
        return
    assert any(entry.startswith("--output") for entry in reserved), (
        f"CLI must expose JSON-capable flag via supported or reserved set in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_api_rest_endpoint_uses_https(record):
    spec = record.data
    api = spec.get("api", {})
    if not api:
        assert spec.get("product_type") in {
            "paid_blueprint",
            "free_scanner",
        }, f"API block missing for unexpected product type in {record.path}"
        return

    endpoint = api.get("rest_endpoint")
    base_url = api.get("base_url", "")
    if endpoint and endpoint.startswith("https://"):
        return
    if endpoint and endpoint.startswith("/"):
        assert base_url.startswith("https://"), (
            f"Relative rest_endpoint requires https base_url in {record.path}"
        )
        return
    assert base_url.startswith("https://"), (
        f"API base_url must use https in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_performance_constraints_have_positive_targets(record):
    spec = record.data
    perf = spec.get("performance_constraints", {})
    required = (
        "max_memory_mb",
        "expected_runtime_ms",
        "playground_runtime_ms",
        "quickscore_threshold_resources",
    )
    for key in required:
        value = perf.get(key)
        assert isinstance(value, int) and value > 0, (
            f"performance_constraints.{key} must be positive int in {record.path}"
        )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_guardscore_severity_penalties_descend(record):
    spec = record.data
    penalties = (
        spec.get("ecosystem_integrations", {})
        .get("guardscore", {})
        .get("severity_penalties", {})
    )
    required_order = ["critical", "high", "medium", "low"]
    values = [penalties.get(name) for name in required_order]
    assert all(isinstance(value, int) and value > 0 for value in values), (
        f"guardscore.severity_penalties must define positive ints in {record.path}"
    )
    assert values == sorted(values, reverse=True), (
        f"guardscore.severity_penalties must descend by severity in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_playground_integration_declares_wasm_safety(record):
    spec = record.data
    playground = spec.get("ecosystem_integrations", {}).get("playground", {})
    bool_keys = ("wasm_safe", "json_sanitize", "svg_sanitize", "quick_score_mode")
    for key in bool_keys:
        assert isinstance(playground.get(key), bool), (
            f"playground.{key} must be bool in {record.path}"
        )
    assert playground.get("wasm_safe") is True, (
        f"playground.wasm_safe must be true in {record.path}"
    )


@pytest.mark.parametrize("record", PRODUCT_SPEC_RECORDS, ids=PRODUCT_SPEC_IDS)
def test_guardboard_integration_declares_badge_controls(record):
    spec = record.data
    guardboard = spec.get("ecosystem_integrations", {}).get("guardboard", {})
    required_keys = (
        "exposes_fixpack_hints",
        "shows_compliance_ledger",
        "badge_preview_supported",
    )
    for key in required_keys:
        assert isinstance(guardboard.get(key), bool), (
            f"guardboard.{key} must be bool in {record.path}"
        )
