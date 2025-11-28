import yaml
from pathlib import Path


def test_state_transition_detection(tmp_path):
    repo = tmp_path
    # create an implementation file with a decorator-based state transition
    src = repo / "state_mod.py"
    src.write_text("""
def helper():
    pass

@state_transition
def apply_changes(state):
    return state

""", encoding="utf-8")

    project_map = {
        "ST1": {
            "implementation_files": ["state_mod.py"],
            "validation_artifacts": [],
        }
    }
    scoring = {"score_weights": {"STATE_TRANSITION": 100}, "task_type_weights": {}}

    (repo / "project_map.yml").write_text(yaml.safe_dump(project_map), encoding="utf-8")
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump(scoring), encoding="utf-8")

    import importlib.util

    spec = importlib.util.spec_from_file_location("repo_scanner", Path("repo-scanner.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    scanner = mod.PILScanner(str(repo))
    results = scanner.scoring_loop()

    assert "ST1" in results
    # STATE_TRANSITION KPI represented as numeric (1.0 when detected)
    assert results["ST1"]["metrics"].get("STATE_TRANSITION") == 1.0
    assert results["ST1"]["pre_gate_score"] == 100
