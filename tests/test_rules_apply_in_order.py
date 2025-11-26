import tempfile
from pathlib import Path
import importlib.util


def load_runner():
    import importlib.util
    repo_root = Path(__file__).resolve().parents[1]
    target = repo_root / "tools" / "repair_runner.py"
    spec = importlib.util.spec_from_file_location("repair_runner", str(target))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_rules_apply_in_order(tmp_path):
    # Create two simple rule modules in a temp dir to verify alphabetical load order
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    # rule a -> append marker A
    (rules_dir / "a_rule.py").write_text('def normalize(text):\n    return text+"A\\n"')
    # rule b -> append marker B
    (rules_dir / "b_rule.py").write_text('def normalize(text):\n    return text+"B\\n"')

    runner = load_runner()
    # Load rules from temp dir
    rules = runner.load_rules(str(rules_dir))
    # Expect alphabetical order a_rule then b_rule
    names = [r["name"] for r in rules]
    assert names == ["a_rule", "b_rule"]
    # Apply rules of type 'yaml' by simulating file_type
    text = "orig\n"
    out = runner.apply_rules(text, rules, file_type="yaml")
    # Since we didn't set types in test modules, load_rules will classify them as yaml
    assert out.endswith("A\nB\n")
