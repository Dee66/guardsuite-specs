![Rule-Spec Validation](https://github.com/Dee66/guardsuite-specs/actions/workflows/validate_rule_specs.yml/badge.svg)
<!-- COPILOT: Maintain README clarity; never overload with technical debt. -->

# guardsuite-specs — GuardSuite Source of Truth (SoT)

## Overview
This repository is the canonical Source of Truth for GuardSuite product specifications, marketing snippets, and templated documentation. YAML definitions under `products/` flow into docs, AI snapshots, and downstream product repos via deterministic automation.

## Contributor Workflow
1. Update `products/<product>.yml` and any shared fragments in `snippets/`.
2. Run validations:
	- `python scripts/validate_products.py`
	- `python scripts/validate_yaml_schema.py`
3. Regenerate docs and AI exports.
4. Review the output under `docs/products/` and `ai_snapshots/`.
5. Use `scripts/sync_to_repo.py` (dry-run by default) before letting CI raise PRs in downstream repos. Pass `--ensure-readme` when the target repo still needs the GuardSuite notice scaffold.

### Source-of-Truth Flow
```text
products/*.yml
	↓  (validate)
scripts/validate_products.py + scripts/validate_yaml_schema.py
	↓  (render)
scripts/gen_docs.py --all  → docs/products/*.md
	↓  (export)
scripts/export_for_ai.py --all  → ai_snapshots/*.md
	↓  (sync)
scripts/sync_to_repo.py --dry-run --product <id> --target ../product-repo --ensure-readme
```

### Key References

## Canonical Rollout
Canonical enforcement is complete across validators, docs, exports, snapshots, registry, and cross-map surfaces. Each export directory now includes `canonical_integrity_rollup.yml`, a single-file health indicator referencing the validator’s one-line status for downstream automation (see Architect guidance: `file:///mnt/data/gpt-instructions.txt`).

### Sample Commands
```bash
python scripts/gen_docs.py --all
python scripts/export_for_ai.py --all
python scripts/validate_products.py && python scripts/validate_yaml_schema.py
```

## Notes

See `CONTRIBUTING.md` for contribution and release policies.

# DONE: Repository scaffold is complete and production-grade.
# Next steps: add more products, refine templates, and integrate PR automation.
