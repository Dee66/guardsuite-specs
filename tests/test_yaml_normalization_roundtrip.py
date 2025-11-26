import tempfile
from pathlib import Path
import importlib.util
import yaml


def load_runner():
    repo_root = Path(__file__).resolve().parents[1]
    target = repo_root / "tools" / "repair_runner.py"
    spec = importlib.util.spec_from_file_location("repair_runner", str(target))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_yaml_normalization_roundtrip(tmp_path):
    runner = load_runner()
    # create yaml file
    p = tmp_path / "sample.yml"
    p.write_text("b: 2\na: 1\n")
    # run once (dry-run) which will apply YAML rules
    diff = runner.run_once(str(p), apply=False)
    # ensure result is valid YAML when applying rules manually
    rules = runner.load_rules()
    normalized = runner.apply_rules(p.read_text(), rules, file_type="yaml")
    data = yaml.safe_load(normalized)
    assert isinstance(data, dict)
    # keys should be present
    assert "a" in data and "b" in data
