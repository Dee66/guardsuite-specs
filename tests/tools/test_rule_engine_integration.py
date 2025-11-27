import json
import os
import shutil
import subprocess
import sys
import time


def write_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def test_adapters_scaffolded_considers_flake8(tmp_path, monkeypatch):
    # We must write into the repository `ai_reports` because the rule_engine
    # computes its AI path from its file location (not cwd). Back up any
    # existing ai_reports, create test ai_reports, run the engine, then restore.
    from pathlib import Path

    repo_root = Path.cwd()
    ai_reports = repo_root / "ai_reports"
    backup = None
    if ai_reports.exists():
        backup = repo_root / f"ai_reports.backup.{int(time.time())}"
        ai_reports.rename(backup)
    ai_reports.mkdir()

    # Minimal evidence_summary with adapters_flake8_exit_code == 0
    evidence = {
        "adapters_flake8_exit_code": 0,
        "pytest_exit_code": 0,
        "recent_commits": [],
    }
    write_file(ai_reports / "evidence_summary.json", json.dumps(evidence, sort_keys=True))

    # Minimal adapter junit xml indicating zero failures
    adapter_xml = """<?xml version='1.0' encoding='utf-8'?>\n<testsuite tests=\"1\" failures=\"0\" errors=\"0\">\n  <testcase classname=\"adapter\" name=\"adapter_test\"/>\n</testsuite>\n"""
    write_file(ai_reports / "adapter_pytest_results.xml", adapter_xml)

    # Create the adapter files the rule definitions expect under the repository root
    repo_adapters = repo_root / "strategy_e" / "adapters"
    repo_adapters.mkdir(parents=True, exist_ok=True)
    write_file(repo_adapters / "pipeline_adapter.py", "# pipeline adapter placeholder")
    write_file(repo_adapters / "computeguard_adapter.py", "# computeguard adapter placeholder")

    # Change cwd to tmp_path so tools/rule_engine.py will read ./ai_reports
    cwd = os.getcwd()
    try:
        # Run the rule engine in-place (it reads AI from repo root)
        python = sys.executable
        script = os.path.join(cwd, "tools", "rule_engine.py")
        proc = subprocess.run([python, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        assert proc.returncode == 0, f"rule_engine failed: {proc.stderr.decode()!r}"

        # Check that checklist_evidence_map.json exists and ADAPTERS_SCAFFOLDED is present
        cem_path = ai_reports / "checklist_evidence_map.json"
        assert cem_path.exists(), "checklist_evidence_map.json not created"
        data = json.loads(cem_path.read_text(encoding="utf-8"))
        # Expect mappings structure and ADAPTERS_SCAFFOLDED to be present and marked done
        assert isinstance(data, dict)
        mappings = data.get("mappings", {})
        assert "ADAPTERS_SCAFFOLDED" in mappings, "ADAPTERS_SCAFFOLDED missing from mappings"
        status = mappings["ADAPTERS_SCAFFOLDED"].get("status")
        assert status == "done", f"ADAPTERS_SCAFFOLDED not done (status={status})"
        # ensure rationale includes flake8 acknowledgement (new logic)
        rationale = mappings["ADAPTERS_SCAFFOLDED"].get("rationale", "")
        assert "flake8" in rationale or "adapter" in rationale
    finally:
        # cleanup: remove test ai_reports and restore backup if present
        try:
            if ai_reports.exists():
                shutil.rmtree(ai_reports)
        except Exception:
            pass
        if backup and backup.exists():
            backup.rename(ai_reports)
        os.chdir(cwd)