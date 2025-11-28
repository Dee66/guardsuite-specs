import importlib.util
import os
from pathlib import Path

import yaml


def load_scanner_module(root_path: Path):
    # Load the repo-scanner.py module as a module named 'repo_scanner'
    repo_file = Path(__file__).resolve().parents[1] / "repo-scanner.py"
    spec = importlib.util.spec_from_file_location("repo_scanner", str(repo_file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compute_complexity_empty_repo(tmp_path):
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()

    module = load_scanner_module(repo_dir)
    PILScanner = module.PILScanner

    scanner = PILScanner(str(repo_dir))
    score, details = scanner.compute_complexity_profile([])

    # Empty repo -> zeroed metrics and score 0
    assert isinstance(score, int)
    assert score == 0
    assert details["scaled"]["functions"] == 0
    assert details["scaled"]["validators"] == 0


def make_module_with_counts(path: Path, func_count=50, validator_count=5, stage_count=3, adapter_count=2):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    # validators
    for i in range(validator_count):
        lines.append(f"def validate_{i}(x):\n    return True\n")
    # stages
    for i in range(stage_count):
        lines.append(f"def stage_{i}():\n    pass\n")
    # adapters
    for i in range(adapter_count):
        lines.append(f"class Adapter{i}:\n    pass\n")
    # functions
    for i in range(func_count):
        lines.append(f"def f_{i}():\n    return {i}\n")

    path.write_text("\n".join(lines), encoding="utf-8")


def test_compute_complexity_high_density(tmp_path):
    repo_dir = tmp_path / "big_repo"
    src = repo_dir / "src"
    module_file = src / "m.py"
    make_module_with_counts(module_file, func_count=200, validator_count=20, stage_count=10, adapter_count=5)

    module = load_scanner_module(repo_dir)
    PILScanner = module.PILScanner
    scanner = PILScanner(str(repo_dir))

    score, details = scanner.compute_complexity_profile([str(module_file)])

    # high-density source should produce a high complexity score
    assert score >= 70
    # scaled functions should be > 0
    assert details["scaled"]["functions"] > 0


def test_scoring_loop_complexity_bucket_mapping(tmp_path):
    repo_dir = tmp_path / "integration_repo"
    src = repo_dir / "src"
    module_file = src / "m.py"
    # create a modest module to land in mid bucket
    make_module_with_counts(module_file, func_count=10, validator_count=1, stage_count=1, adapter_count=0)

    # create minimal project_map.yml and scoring_kpis.yml so scoring_loop runs
    pm = {
        "task1": {
            "implementation_files": ["src/m.py"],
        }
    }
    (repo_dir / "project_map.yml").parent.mkdir(parents=True, exist_ok=True)
    (repo_dir / "project_map.yml").write_text(yaml.safe_dump(pm), encoding="utf-8")
    (repo_dir / "scoring_kpis.yml").write_text(yaml.safe_dump({}), encoding="utf-8")

    module = load_scanner_module(repo_dir)
    PILScanner = module.PILScanner
    scanner = PILScanner(str(repo_dir))

    results = scanner.scoring_loop()
    assert isinstance(results, dict)
    assert "task1" in results
    metrics = results["task1"]["metrics"]
    # Complexity KPI must be one of the bucketed values
    assert metrics["COMPLEXITY_PROFILE"] in (0.0, 0.5, 1.0)

    # Verify that complexity mapping matches recomputed complexity score thresholds
    complexity_score, _ = scanner.compute_complexity_profile([str(module_file)])
    if complexity_score >= 70:
        expected = 1.0
    elif complexity_score >= 30:
        expected = 0.5
    else:
        expected = 0.0

    assert metrics["COMPLEXITY_PROFILE"] == expected
