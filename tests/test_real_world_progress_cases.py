import importlib.util
import json
from pathlib import Path


def _load_scanner(repo_root: str):
    path = Path(repo_root) / "repo-scanner.py"
    spec = importlib.util.spec_from_file_location("repo_scanner", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PILScanner(str(repo_root))


def run_and_get_scores(base_fixture: Path):
    scanner = _load_scanner(".")
    # instantiate scanner pointing at fixture
    s = scanner.__class__(repo_path=str(base_fixture))
    res = s.scoring_loop()
    # return first task metrics tuple
    if not res:
        return None
    tid, data = next(iter(res.items()))
    m = data.get("metrics", {})
    return {
        "task_id": tid,
        "progress_score": int(data.get("progress_score", 0)),
        "compliance_score": int(data.get("compliance_score", 0)),
        "combined_score": int(data.get("combined_score", 0)),
        "final_score": int(data.get("final_score", 0)),
        "metrics": m,
    }


def test_caseA_strong_impl_no_metadata():
    f = Path(__file__).parent / "fixtures" / "caseA"
    out = run_and_get_scores(f)
    assert out is not None
    # progress should be positive and greater than compliance
    assert out["progress_score"] > 0
    assert out["progress_score"] > out["compliance_score"]
    assert out["compliance_score"] == 0


def test_caseB_strong_impl_partial_metadata():
    f = Path(__file__).parent / "fixtures" / "caseB"
    out = run_and_get_scores(f)
    assert out is not None
    assert out["progress_score"] >= 70
    # partial metadata -> compliance should be capped (not full 100)
    assert out["compliance_score"] < 100


def test_caseC_full_metadata_weak_impl():
    f = Path(__file__).parent / "fixtures" / "caseC"
    out = run_and_get_scores(f)
    assert out is not None
    # weak implementation -> progress low
    assert out["progress_score"] < 50
    # full metadata -> compliance reasonably high
    assert out["compliance_score"] >= 60


def test_caseD_state_transition_not_required_neutral():
    f = Path(__file__).parent / "fixtures" / "caseD"
    scanner = _load_scanner(".")
    s = scanner.__class__(repo_path=str(f))
    res = s.scoring_loop()
    _, data = next(iter(res.items()))
    metrics = data.get("metrics", {})
    # STATE_TRANSITION should be neutral (0.5)
    assert float(metrics.get("STATE_TRANSITION", 0.5)) == 0.5
    # progress unaffected (implementation-focused)
    assert int(data.get("progress_score", 0)) > 0


def test_caseE_missing_spec_coverage_neutral():
    f = Path(__file__).parent / "fixtures" / "caseE"
    out = run_and_get_scores(f)
    assert out is not None
    # SPEC_COVERAGE in metrics should be neutral (0.5)
    assert float(out["metrics"].get("SPEC_COVERAGE", 0.5)) == 0.5
    # progress unaffected
    assert out["progress_score"] > 0
