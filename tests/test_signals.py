import importlib.util
from pathlib import Path


def load_scanner():
    repo_file = Path(__file__).resolve().parents[1] / "repo-scanner.py"
    spec = importlib.util.spec_from_file_location("repo_scanner", str(repo_file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pipeline_detection(tmp_path):
    repo = tmp_path / "repo"
    src = repo / "src"
    src.mkdir(parents=True)
    f = src / "pipe.py"
    f.write_text("def stage_one():\n    pass\n\n@decorator\ndef pipeline_stage():\n    pass\n", encoding="utf-8")

    module = load_scanner()
    PILScanner = module.PILScanner
    scanner = PILScanner(str(repo))

    signals = scanner.scan_implementation_signals([str(f)], task_id="")
    assert signals["pipeline_stages_detected"] >= 1


def test_validator_detection(tmp_path):
    repo = tmp_path / "repo2"
    src = repo / "src"
    src.mkdir(parents=True)
    f = src / "validators.py"
    f.write_text("def validate_input(x):\n    return True\n\nclass MyValidator:\n    pass\n", encoding="utf-8")

    module = load_scanner()
    PILScanner = module.PILScanner
    scanner = PILScanner(str(repo))

    signals = scanner.scan_implementation_signals([str(f)], task_id="")
    assert signals["validators_detected"] >= 1


def test_structure_fallback_minimum(tmp_path):
    repo = tmp_path / "repo3"
    # no project_map.yml
    src = repo / "src"
    src.mkdir(parents=True)
    (src / "a.py").write_text("def f():\n    pass\n", encoding="utf-8")

    module = load_scanner()
    PILScanner = module.PILScanner
    scanner = PILScanner(str(repo))

    # empty project map
    pm = {}
    s = scanner.scan_structure(pm, impl_files=None)
    # percent_structure_complete should be at least 50 when code exists
    assert s.get("percent_structure_complete", 0) >= 50


def test_done_contract_enforcement(tmp_path):
    repo = tmp_path / "repo4"
    src = repo / "src"
    src.mkdir(parents=True)
    f = src / "m.py"
    f.write_text("def f():\n    return True\n", encoding="utf-8")

    # project_map with done_contract requiring state_transition_implemented
    pm = {
        "taskx": {
            "implementation_files": ["src/m.py"],
            "done_contract": ["state_transition_implemented"],
        }
    }
    (repo / "project_map.yml").write_text("dummy", encoding="utf-8")

    module = load_scanner()
    PILScanner = module.PILScanner
    scanner = PILScanner(str(repo))

    # monkeypatch project_map read by directly calling scoring_loop after writing a real project_map
    import yaml
    (repo / "project_map.yml").write_text(yaml.safe_dump(pm), encoding="utf-8")
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump({}), encoding="utf-8")

    results = scanner.scoring_loop()
    assert "taskx" in results
    final = results["taskx"]["final_score"]
    # without a state transition implemented, final_score should be 0 due to done_contract enforcement
    assert final == 0
