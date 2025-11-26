import yaml
from pathlib import Path

def load_rule_specs(base_path: Path):
    """
    Deterministically loads all rule-spec YAMLs from rule_specs/<product>/ directories.
    Returns a list of parsed rule-spec dicts sorted lexicographically by file path.
    """
    rule_files = sorted(base_path.rglob("*.yml"))
    specs = []
    for file in rule_files:
        with file.open("r", encoding="utf-8") as f:
            specs.append((str(file), yaml.safe_load(f)))
    return specs
