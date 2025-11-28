from pathlib import Path
import yaml


def test_done_contract_enforcement(tmp_path):
    repo = tmp_path
    # implementation without transition
    (repo / "impl.py").write_text("def foo(): pass\n", encoding="utf-8")

    project_map = {
        "D1": {"implementation_files": ["impl.py"], "validation_artifacts": [], "task_type": "pipeline_stage"}
    }
    # task_contract requires state_transition_implemented for pipeline_stage
    task_contract = {"pipeline_stage": {"done_contract": ["state_transition_implemented"]}}
    scoring = {"score_weights": {"STATE_TRANSITION": 100}, "task_type_weights": {"pipeline_stage": 1.0}, "gates": []}

    (repo / "project_map.yml").write_text(yaml.safe_dump(project_map), encoding="utf-8")
    (repo / "task_contract.yml").write_text(yaml.safe_dump(task_contract), encoding="utf-8")
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump(scoring), encoding="utf-8")

    import importlib.util
    spec = importlib.util.spec_from_file_location("repo_scanner", Path("repo-scanner.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    scanner = mod.PILScanner(str(repo))
    # ensure scanner loads task_contract
    results = scanner.scoring_loop()
    assert "D1" in results
    # done_contract requires state_transition -> metric False -> post_gate_score should be 0 due to enforcement
    # done_contract requires state_transition -> metric 0.0 -> post_gate_score should be 0 due to enforcement
    assert results["D1"]["metrics"].get("STATE_TRANSITION") == 0.0
    assert results["D1"]["post_gate_score"] == 0
