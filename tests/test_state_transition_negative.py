from pathlib import Path
import yaml


def test_state_transition_negative(tmp_path):
    repo = tmp_path
    src = repo / "no_trans.py"
    src.write_text("""
def helper():
    return 1

def other():
    pass

""", encoding="utf-8")

    project_map = {
        "NT1": {"implementation_files": ["no_trans.py"], "validation_artifacts": []}
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
    assert "NT1" in results
    # Not detected -> numeric 0.0
    assert results["NT1"]["metrics"].get("STATE_TRANSITION") == 0.0
