import importlib.util
import tempfile
from pathlib import Path


def load_repair_runner_module():
    repo_root = Path(__file__).resolve().parents[1]
    target = repo_root / "tools" / "repair_runner.py"
    spec = importlib.util.spec_from_file_location("repair_runner", str(target))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_normalize_and_diff():
    repair_runner = load_repair_runner_module()
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sample.txt"
        p.write_text("line: 1\n")
        diff = repair_runner.run_once(str(p), apply=False)
        # Expect the diff to show the added normalized marker (any rule marker)
        assert "+# normalized-by" in diff
