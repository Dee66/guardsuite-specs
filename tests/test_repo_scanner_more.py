import runpy
import os
import json
from pathlib import Path

import pytest


def load_scanner_module():
    ns = runpy.run_path(os.path.join(os.path.dirname(__file__), "..", "repo-scanner.py"))
    return ns


def test_scoring_loop_structure():
    ns = load_scanner_module()
    PILScanner = ns["PILScanner"]
    s = PILScanner(".")
    res = s.scoring_loop()
    assert isinstance(res, dict)
    # project_map.yml contains CORE-001 and DOC-001
    assert "CORE-001" in res
    assert "DOC-001" in res


def test_version_and_drift_detection_details():
    ns = load_scanner_module()
    PILScanner = ns["PILScanner"]
    s = PILScanner(".")
    deltas = s.version_and_drift_detection()
    assert isinstance(deltas, dict)
    assert "details" in deltas


def test_check_dependencies_behavior():
    ns = load_scanner_module()
    PILScanner = ns["PILScanner"]
    s = PILScanner(".")
    # build a fake repos_index where INIT-001 is done in repo A
    repos_index = {"repo-A": {"task_details": {"INIT-001": {"status": "done"}}}}
    result = s.check_dependencies("CORE-001", repos_index)
    assert isinstance(result, dict)
    assert result.get("details", {}).get("INIT-001", {}).get("satisfied") is True


def test_aggregate_and_serialize(tmp_path):
    ns = load_scanner_module()
    aggregate_all_repos = ns["aggregate_all_repos"]
    save_repos_index = ns["save_repos_index"]
    repo_list = ["."]
    aggregated = aggregate_all_repos(repo_list)
    assert isinstance(aggregated, dict)
    # top-level key should be current repo directory name
    repo_name = Path(".").resolve().name
    assert repo_name in aggregated
    # write file
    out = tmp_path / "repos_index.yml"
    save_repos_index(aggregated, str(out))
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert repo_name in text
