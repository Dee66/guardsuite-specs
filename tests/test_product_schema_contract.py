import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"
EXCLUDED = {"guardsuite_master_spec.yml", "guardsuite-template.yml", "pillar-template.yml"}

def load_yaml(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))

def test_yaml_schema_contract_is_consistent():
    canonical_specs = 0
    for file in PRODUCTS.glob("*.yml"):
        if file.name.endswith("_worksheet.yml"):
            continue
        if file.name in EXCLUDED:
            continue
        data = load_yaml(file)
        if not data:
            continue

        if "ecosystem_integrations" not in data:
            continue

        canonical_specs += 1
        eco = data["ecosystem_integrations"]

        assert {"guardscore", "playground", "guardboard"} <= set(eco.keys())

        g = eco["guardscore"]
        assert "pillar_weight" in g
        assert "severity_penalties" in g
        sp = g["severity_penalties"]
        required_severities = {"critical", "high", "medium", "low"}
        assert required_severities <= set(sp.keys())
        for sev in required_severities:
            assert isinstance(sp[sev], int) and sp[sev] > 0, (
                f"Severity penalty for {sev} must be positive integer in {file}"
            )

        p = eco["playground"]
        for key in ("max_runtime_ms", "playground_latency_target_ms", "wasm_safe"):
            assert key in p, f"Missing {key} in playground block for {file}"
        for bool_key in ("wasm_safe", "json_sanitize", "svg_sanitize", "quick_score_mode"):
            assert isinstance(p[bool_key], bool), f"{bool_key} must be bool in {file}"

        b = eco["guardboard"]
        for key in ("exposes_fixpack_hints", "shows_compliance_ledger", "badge_preview_supported"):
            assert key in b, f"Missing {key} in guardboard block for {file}"

        cli = data["cli"]
        scan_cmd = cli.get("scan_command")
        if not scan_cmd:
            assert data.get("pillar") == "crosscut", f"scan_command missing in {file}"
            api = data.get("api")
            assert api and api.get("rest_endpoint"), f"Crosscut product must expose api.rest_endpoint in {file}"
        else:
            assert isinstance(scan_cmd, str) and scan_cmd.strip(), f"scan_command must be non-empty string in {file}"
        flags = cli.get("supported_flags", [])
        assert flags, f"supported_flags must be non-empty in {file}"
        assert all(flag.startswith("--") for flag in flags), f"Flags must start with -- in {file}"

        security = data["security"]
        for key in ("sanitize_all_inputs", "svg_sanitization", "wasm_compatible", "sandbox_requirement"):
            assert key in security, f"Missing {key} in security block for {file}"

        assert data.get("purpose_summary"), f"purpose_summary missing in {file}"

        compliance = data.get("compliance", {})
        assert isinstance(compliance.get("ledger_visibility"), str), f"ledger_visibility missing in {file}"

        perf = data["performance_constraints"]
        perf_keys = ["expected_runtime_ms", "playground_runtime_ms", "quickscore_threshold_resources"]
        if data.get("pillar") == "crosscut":
            perf_keys.append("realtime_refresh_interval_ms")
        else:
            perf_keys.append("large_plan_runtime_ms")
        for key in perf_keys:
            assert key in perf, f"Missing {key} in performance constraints for {file}"
            assert isinstance(perf[key], int) and perf[key] > 0, f"{key} must be positive int in {file}"

        marketing = data.get("marketing", {})
        ctas = marketing.get("ctas", [])
        assert ctas, f"marketing.ctas must be populated in {file}"
        for cta in ctas:
            assert cta.get("text") and cta.get("href"), f"CTA entries require text and href in {file}"

    assert canonical_specs > 0, "No canonical product specs validated"
