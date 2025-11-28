import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def write_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def test_adapters_scaffolded_blocks_on_flake8_failure(tmp_path):
    repo_root = Path.cwd()
    ai_reports = repo_root / "ai_reports"
    backup = None
    if ai_reports.exists():
        backup = repo_root / f"ai_reports.backup.{int(time.time())}"
        ai_reports.rename(backup)
    ai_reports.mkdir()

    # evidence summary: adapters flake8 non-zero (simulated lint failure)
    evidence = {
        "adapters_flake8_exit_code": 1,
        "pytest_exit_code": 0,
        "recent_commits": [],
    }
    write_file(ai_reports / "evidence_summary.json", json.dumps(evidence, sort_keys=True))

    # adapter junit xml indicating zero failures (tests passing)
    adapter_xml = """<?xml version='1.0' encoding='utf-8'?>\n<testsuite tests=\"1\" failures=\"0\" errors=\"0\">\n  <testcase classname=\"adapter\" name=\"adapter_test\"/>\n</testsuite>\n"""
    write_file(ai_reports / "adapter_pytest_results.xml", adapter_xml)

    # ensure the adapter files referenced by rules exist
    repo_adapters = repo_root / "strategy_e" / "adapters"
    repo_adapters.mkdir(parents=True, exist_ok=True)
    write_file(repo_adapters / "pipeline_adapter.py", "# pipeline adapter placeholder")
    write_file(repo_adapters / "computeguard_adapter.py", "# computeguard adapter placeholder")

    try:
        python = sys.executable
        script = os.path.join(str(repo_root), "tools", "rule_engine.py")
        proc = subprocess.run([python, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        assert proc.returncode == 0, f"rule_engine failed: {proc.stderr.decode()!r}"

        cem_path = ai_reports / "checklist_evidence_map.json"
        assert cem_path.exists(), "checklist_evidence_map.json not created"
        data = json.loads(cem_path.read_text(encoding="utf-8"))
        mappings = data.get("mappings", {})
        assert "ADAPTERS_SCAFFOLDED" in mappings
        status = mappings["ADAPTERS_SCAFFOLDED"].get("status")
        assert status != "done", f"ADAPTERS_SCAFFOLDED should not be done when adapters flake8 exit != 0 (status={status})"
        rationale = mappings["ADAPTERS_SCAFFOLDED"].get("rationale", "")
        assert "flake8" in rationale or "adapter" in rationale
    finally:
        # cleanup
        try:
            if ai_reports.exists():
                shutil.rmtree(ai_reports)
        except Exception:
            pass
        if backup and backup.exists():
            backup.rename(ai_reports)