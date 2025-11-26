import tempfile
from pathlib import Path

from tools import repair_runner


def test_normalize_and_diff():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sample.txt"
        p.write_text("line: 1\n")
        diff = repair_runner.run_once(str(p), apply=False)
        # Expect the diff to show the added normalized marker
        assert "+# normalized-by-repair-runner" in diff
