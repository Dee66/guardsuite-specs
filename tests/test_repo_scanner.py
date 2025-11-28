import importlib.util
import os
from pathlib import Path


def _load_repo_scanner_module(repo_root: str):
    path = Path(repo_root) / "repo-scanner.py"
    spec = importlib.util.spec_from_file_location("repo_scanner", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_compute_complexity_profile(tmp_path):
    # create a sample file with 50 lines
    f = tmp_path / "a.py"
    content = "\n".join(["# line %d" % i for i in range(50)])
    f.write_text(content, encoding="utf-8")

    mod = _load_repo_scanner_module(".")
    scanner = mod.PILScanner(str(tmp_path))
    complexity_score, details = scanner.compute_complexity_profile([str(f)])

    # Implementation-richness profile returns details with counts
    assert isinstance(details, dict)
    assert details.get("function_count", 0) == 0
    assert details.get("class_count", 0) == 0
    assert 0 <= complexity_score <= 100


def test_compute_spec_coverage():
    mod = _load_repo_scanner_module(".")
    scanner = mod.PILScanner(".")
    entry = {"task_spec_coverage": [{"covered": True}, {"covered": False}, {"covered": True}]}
    cov = scanner.compute_spec_coverage(entry)
    # 2 of 3 covered -> 66 (rounded down)
    assert cov == int((2 / 3) * 100)


def test_scoring_loop_basic(tmp_path):
    # prepare minimal repo with a single implementation file and project_map + scoring_kpis
    repo = tmp_path
    (repo / "a.py").write_text("print('ok')\n", encoding="utf-8")

    project_map = {
        "T1": {
            "implementation_files": ["a.py"],
            "validation_artifacts": [],
            "task_type": "documentation",
        }
    }
    scoring = {
        "version": 1,
        "score_weights": {"CODE_ARTIFACT_PRESENT": 100},
        "task_type_weights": {"documentation": 1.5},
        "gates": [],
    }

    import yaml

    (repo / "project_map.yml").write_text(yaml.safe_dump(project_map), encoding="utf-8")
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump(scoring), encoding="utf-8")

    mod = _load_repo_scanner_module(".")
    scanner = mod.PILScanner(str(repo))
    results = scanner.scoring_loop()

    assert "T1" in results
    res = results["T1"]
    # CODE_ARTIFACT_PRESENT -> pre_gate_score should be 100, type multiplier 1.5 -> final 150
    assert res.get("pre_gate_score") == 100
    assert int(res.get("final_score")) == 150
import runpy
import json
import os
from pathlib import Path

import pytest


def load_scanner():
    ns = runpy.run_path(os.path.join(os.path.dirname(__file__), "..", "repo-scanner.py"))
    PILScanner = ns["PILScanner"]
    return PILScanner


def test_compute_spec_coverage_simple():
    PILScanner = load_scanner()
    s = PILScanner(".")
    entry = {"task_spec_coverage": [{"spec_section": "a", "covered": True}, {"spec_section": "b", "covered": False}]}
    pct = s.compute_spec_coverage(entry)
    assert pct == 50


def test_compute_complexity_profile(tmp_path):
    PILScanner = load_scanner()
    s = PILScanner(".")
    f = tmp_path / "mod.py"
    # create 25-line file
    content = "\n".join([f"# line {i}" for i in range(25)])
    f.write_text(content, encoding="utf-8")
    complexity, details = s.compute_complexity_profile([str(f)])
    assert isinstance(details, dict)
    assert details.get("function_count", 0) == 0
    assert details.get("class_count", 0) == 0
    assert 0 <= complexity <= 100
