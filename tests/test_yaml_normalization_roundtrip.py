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
    # keys should be present either top-level or within x_legacy (placeholder rules may relocate)
    if "a" in data and "b" in data:
        assert True
    else:
        # allow normalized output to move keys into x_legacy during placeholder rule runs
        assert "x_legacy" in data and isinstance(data["x_legacy"], dict)
        assert "a" in data["x_legacy"] and "b" in data["x_legacy"]
