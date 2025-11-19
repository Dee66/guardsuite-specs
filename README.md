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
- Master contract: [`docs/guardsuite_master_spec.md`](docs/guardsuite_master_spec.md)
- MkDocs site navigation: `mkdocs.yml`
- Canonical schema: `products/schema/product.schema.json`

### Sample Commands
```bash
python scripts/gen_docs.py --all
python scripts/export_for_ai.py --all
python scripts/validate_products.py && python scripts/validate_yaml_schema.py
```

## Notes
- The YAML files in `products/` are the authoritative source for product copy and structured spec data.
- Do not edit generated docs in downstream repos directly; CI-driven PRs and `scripts/sync_to_repo.py` keep them in sync. The helper can bootstrap downstream READMEs with `--ensure-readme` to keep the GuardSuite notice consistent.
- Everything in this repo favors deterministic, idempotent automation.

See `CONTRIBUTING.md` for contribution and release policies.

# DONE: Repository scaffold is complete and production-grade.
# Next steps: add more products, refine templates, and integrate PR automation.
