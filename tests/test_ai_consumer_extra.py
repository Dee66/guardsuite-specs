import importlib.util
from pathlib import Path


def _load_ai_consumer_module(repo_root: str = "."):
    path = Path(repo_root) / "scripts" / "ai_consumer.py"
    spec = importlib.util.spec_from_file_location("ai_consumer", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_analyze_repos_index_basic():
    mod = _load_ai_consumer_module()
    # create a minimal repos_index structure
    repos_index = {
        "myrepo": {
            "repo_path": ".",
            "scoring": {
                "TASK1": {"final_score": 90, "metrics": {"TESTS_PASS": True, "SPEC_COVERAGE": 90}, "details": {"impl_files": [], "validation_artifacts": []}}
            },
        }
    }

    out = mod.analyze_repos_index(repos_index, enable_llm=False)
    assert "analysis" in out
    assert "myrepo" in out["analysis"]
    assert "TASK1" in out["analysis"]["myrepo"]
    # confidence mapping should exist
    assert "confidence" in out


def test_llm_opt_in_noop():
    mod = _load_ai_consumer_module()
    repos_index = {
        "r": {"repo_path": ".", "scoring": {"T": {"final_score": 50, "metrics": {}, "details": {}}}}
    }
    out_no_llm = mod.analyze_repos_index(repos_index, enable_llm=False)
    out_with_llm = mod.analyze_repos_index(repos_index, enable_llm=True)
    # With default no-op llm_enrich_analysis the outputs should be structurally similar
    assert set(out_no_llm.keys()) == set(out_with_llm.keys())
    assert out_no_llm["analysis"].keys() == out_with_llm["analysis"].keys()
