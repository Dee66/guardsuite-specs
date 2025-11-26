import json
import sys
from pathlib import Path
from strategy_e.validators.rule_spec_validator import validate_all_under

def main():
    base = Path("rule_specs")
    results = validate_all_under(base)
    print(json.dumps(results, indent=2))
    bad = any(results[p] for p in results)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
