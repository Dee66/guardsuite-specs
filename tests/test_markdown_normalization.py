from pathlib import Path
import importlib.util


def load_runner():
    repo_root = Path(__file__).resolve().parents[1]
    target = repo_root / "tools" / "repair_runner.py"
    spec = importlib.util.spec_from_file_location("repair_runner", str(target))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_markdown_normalization(tmp_path):
    runner = load_runner()
    p = tmp_path / "doc.md"
    p.write_text("# Title  \n\nLine with trailing spaces    \n")
    diff = runner.run_once(str(p), apply=False)
    # Apply rules to get normalized content
    rules = runner.load_rules()
    normalized = runner.apply_rules(p.read_text(), rules, file_type="markdown")
    assert "Line with trailing spaces" in normalized
    # ensure no trailing spaces
    assert not any(line.rstrip() != line for line in normalized.splitlines())
