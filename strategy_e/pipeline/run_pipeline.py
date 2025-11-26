import argparse
from pathlib import Path
from strategy_e.pipeline.loader.rule_loader import load_rule_specs
from strategy_e.pipeline.executor.pipeline_executor import run_pipeline_on_text

def main():
    parser = argparse.ArgumentParser(description="Run Strategy-E rule-spec pipeline.")
    parser.add_argument("target", help="File to run pipeline on")
    parser.add_argument("--rules", default="rule_specs", help="Path to rule_specs")
    parser.add_argument("--dry-run", action="store_true", help="Run without writing backups or modifying files")
    args = parser.parse_args()

    target_path = Path(args.target)
    rules_path = Path(args.rules)

    rules = load_rule_specs(rules_path)

    with target_path.open("r", encoding="utf-8") as f:
        original = f.read()

    result = run_pipeline_on_text(
        original,
        rules,
        path=str(target_path),
        dry_run=args.dry_run,
    )

    print("=== NORMALIZED ===")
    print(result["normalized_text"])
    print("=== VALIDATION ERRORS ===")
    for e in result["validation_errors"]:
        print(f"- {e}")
    print("=== DIFF ===")
    print(result["diff"])
    if args.dry_run:
        print("=== DRY RUN: No backups written, no file modifications applied ===")
    else:
        print("=== BACKUP CREATED ===")
        print(result.get("backup_path", "(none)"))
    print("=== END ===")


if __name__ == "__main__":
    main()
