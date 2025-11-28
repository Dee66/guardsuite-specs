import importlib.util
from pathlib import Path


def load_scanner_module():
    repo_file = Path(__file__).resolve().parents[1] / "repo-scanner.py"
    spec = importlib.util.spec_from_file_location("repo_scanner", str(repo_file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_complexity_config_via_scoring_kpis(tmp_path):
    repo = tmp_path / "repo_cfg"
    src = repo / "src"
    src.mkdir(parents=True)
    f = src / "m.py"
    # small module
    f.write_text("def a():\n    return 1\n\ndef b():\n    return 2\n", encoding="utf-8")

    # project_map with task1
    pm = {"task1": {"implementation_files": ["src/m.py"]}}

    # custom complexity config: high weight to functions, low thresholds
    scoring = {
        "complexity": {
            "weights": {"functions": 100, "pipeline": 1, "validators": 1, "classes": 1, "adapters": 1, "depth": 1},
            "thresholds": {"high": 1, "mid": 1}
        }
    }

    import yaml
    (repo / "project_map.yml").write_text(yaml.safe_dump(pm), encoding="utf-8")
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump(scoring), encoding="utf-8")

    mod = load_scanner_module()
    scanner = mod.PILScanner(str(repo))
    res = scanner.scoring_loop()
    assert "task1" in res
    comp_k = res["task1"]["metrics"]["COMPLEXITY_PROFILE"]
    # Given low thresholds and high function weight, expect complexity KPI to be 1.0
    assert comp_k == 1.0


def test_group_weights_affect_combined_score(tmp_path):
    repo = tmp_path / "repo_group"
    src = repo / "src"
    src.mkdir(parents=True)
    f = src / "m.py"
    f.write_text("def a():\n    return 1\n", encoding="utf-8")

    pm = {"task1": {"implementation_files": ["src/m.py"]}}
    scoring = {"group_weights": {"progress": 2, "compliance": 1}}

    import yaml
    (repo / "project_map.yml").write_text(yaml.safe_dump(pm), encoding="utf-8")
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump(scoring), encoding="utf-8")

    mod = load_scanner_module()
    scanner = mod.PILScanner(str(repo))
    res = scanner.scoring_loop()
    assert "task1" in res
    r = res["task1"]
    # combined_score should equal weighted average of progress and compliance posts
    pw = scoring["group_weights"]["progress"]
    cw = scoring["group_weights"]["compliance"] if "compliance" in scoring["group_weights"] else 1
    expected = int(round((r["progress_score"] * pw + r["compliance_score"] * cw) / (pw + cw)))
    assert r["combined_score"] == expected
