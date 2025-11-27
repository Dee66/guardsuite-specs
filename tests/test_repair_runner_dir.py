import tempfile
from pathlib import Path


def load_runner():
    import importlib.util

    repo_root = Path(__file__).resolve().parents[1]
    target = repo_root / "tools" / "repair_runner.py"
    spec = importlib.util.spec_from_file_location("repair_runner", str(target))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run_directory_dryrun_creates_diffs(tmp_path):
    runner = load_runner()
    # create directory with two files (one .yml, one .md)
    d = tmp_path / "prod"
    d.mkdir()
    f1 = d / "a.yml"
    f2 = d / "b.md"
    f1.write_text("key: value\n")
    f2.write_text("hello\n")

    results = runner.run_directory(str(d), apply=False, extensions=[".yml", ".md"])
    # Expect two entries; YAML diff should include a normalization marker.
    assert str(f1) in results
    assert str(f2) in results
    assert "normalized-by" in results[str(f1)]
    # Markdown rule may or may not change content; accept either a diff or empty string
    assert (results[str(f2)] == "") or ("normalized-by" in results[str(f2)])
