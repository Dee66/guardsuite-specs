import os
import yaml
from pathlib import Path
import runpy


def _load_scanner_module(repo_root: str):
    # load the scanner implementation from the repository root (not the tmp repo)
    base = os.path.dirname(__file__)
    modpath = os.path.join(base, "..", "repo-scanner.py")
    ns = runpy.run_path(modpath)
    return ns["PILScanner"]


def test_none_kpi_mapped_neutral(tmp_path):
    # minimal repo with one implementation file and scoring_kpis present
    repo = tmp_path
    (repo / "a.py").write_text("print('hello')\n", encoding="utf-8")

    project_map = {
        "T1": {"implementation_files": ["a.py"], "validation_artifacts": [], "task_type": "pipeline_stage"}
    }
    scoring = {"version": 1, "score_weights": {"CODE_ARTIFACT_PRESENT": 100}, "gates": []}

    (repo / "project_map.yml").write_text(yaml.safe_dump(project_map), encoding="utf-8")
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump(scoring), encoding="utf-8")

    PILScanner = _load_scanner_module(str(repo))
    s = PILScanner(str(repo))
    results = s.scoring_loop()
    assert "T1" in results
    metrics = results["T1"]["metrics"]
    # STATE_TRANSITION not requested or required -> should be neutral mapped to 0.5
    assert "STATE_TRANSITION" in metrics
    assert metrics["STATE_TRANSITION"] == 0.5


def test_new_kpis_present_and_range(tmp_path):
    repo = tmp_path
    (repo / "a.py").write_text("def foo():\n    return 1\n", encoding="utf-8")

    project_map = {
        "T1": {"implementation_files": ["a.py"], "validation_artifacts": [], "task_type": "pipeline_stage"}
    }
    scoring = {"version": 1, "score_weights": {"STRUCTURAL_COMPLETENESS": 50, "IMPLEMENTATION_COMPLETENESS": 50}, "gates": []}

    (repo / "project_map.yml").write_text(yaml.safe_dump(project_map), encoding="utf-8")
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump(scoring), encoding="utf-8")

    PILScanner = _load_scanner_module(str(repo))
    s = PILScanner(str(repo))
    results = s.scoring_loop()
    assert "T1" in results
    metrics = results["T1"]["metrics"]
    # new KPIs should be present and numeric in 0.0,0.5,1.0 range
    for k in ("STRUCTURAL_COMPLETENESS", "IMPLEMENTATION_COMPLETENESS", "PIPELINE_STAGE_COMPLETENESS", "VALIDATOR_COMPLETENESS"):
        assert k in metrics
        assert metrics[k] in (0.0, 0.5, 1.0)
