import tempfile
import os
import yaml
import json
import importlib.util
from pathlib import Path


def test_progress_not_zero_when_compliance_zero():
    # Create a temporary repo structure
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        # src with a simple implementation file (provides implementation signals)
        src_dir = td_path / "src"
        src_dir.mkdir()
        impl = src_dir / "foo.py"
        impl.write_text("def do_work():\n    return True\n")

        # project_map: task requires state_transition in done_contract (will fail)
        pm = {
            "T1": {
                "implementation_files": ["src/foo.py"],
                "done_contract": ["state_transition_implemented"],
                "task_type": "pipeline_stage",
            }
        }
        (td_path / "project_map.yml").write_text(yaml.safe_dump(pm))

        # scoring_kpis: include weights so progress uses implementation KPIs
        sk = {
            "score_weights": {
                "STRUCTURAL_COMPLETENESS": 10,
                "IMPLEMENTATION_COMPLETENESS": 10,
                "PIPELINE_STAGE_COMPLETENESS": 10,
                "VALIDATOR_COMPLETENESS": 10,
                "COMPLEXITY_PROFILE": 10,
                "TESTS_PASS": 10,
                "SPEC_COVERAGE": 5,
                "DOCUMENTATION": 2,
                "SANITY_GATE": 1,
                "STATE_TRANSITION": 1,
            }
        }
        (td_path / "scoring_kpis.yml").write_text(yaml.safe_dump(sk))

        # task_contract.yml intentionally omitted to ensure no inheritance

        # Instantiate scanner from module file
        spec = importlib.util.spec_from_file_location('repo_scanner', str(Path.cwd() / 'repo-scanner.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        scanner = mod.PILScanner(repo_path=str(td_path))

        res = scanner.scoring_loop()
        assert isinstance(res, dict)
        assert "T1" in res
        t = res["T1"]
        # compliance should be zero due to required state_transition missing
        assert int(t.get("compliance_score", -1)) == 0
        # progress must be > 0 (implementation signals present)
        assert int(t.get("progress_score", -1)) > 0

        # additional internal sanity checks to prevent regressions:
        # when compliance is zero and progress > 0, final_score must be
        # strictly less than progress_score and not equal to it.
        if int(t.get("compliance_score", -1)) == 0 and int(t.get("progress_score", -1)) > 0:
            assert int(t.get("final_score", -1)) < int(t.get("progress_score", -1))
            assert int(t.get("final_score", -1)) != int(t.get("progress_score", -1))
