# AI-Dev Repository Scan Report

- Generated: 2025-11-25T19:35:11.910250+00:00
- Repo clean: yes
- Untracked files: 0
- Ignored entries (visible): 23

## Findings

- Scan traversed entire repo root with ignored directories recorded but not expanded.
- No tracked or untracked modifications were detected inside `products/`, satisfying sealed Strategy-D requirements.
- Workspace scaffolding artifacts enumerated below are present and unchanged.
- Demo scaffolding directories exist for every product; see verification table for per-product status.
- Unexpected/orphaned paths are unchanged from previous diagnostics and remain documented for traceability.

## Git Status Summary

| Status | Count |
| --- | ---: |
| derived | 169 |
| ignored | 23 |
| tracked | 352 |

## Category Breakdown

| Category | Count |
| --- | ---: |
| docs | 57 |
| orphaned | 2 |
| product_tree | 244 |
| schema | 13 |
| scripts | 13 |
| unexpected | 19 |
| utilities | 111 |
| workspace | 85 |

## Anomalies

**Unexpected Paths**
- `.github/`
- `.github/workflows/`
- `.github/workflows/generate_docs.yml`
- `.github/workflows/open_sync_pr.yml`
- `.gitignore`
- `.logs/`
- `.pre-commit-config.yaml`
- `.pytest_cache/`
- `.venv/`
- `.vscode/`
- `poetry.lock`
- `products/`
- `pyproject.toml`
- `tmp/`
- `tmp/ai-export/`
- `tmp/final_products_tree.txt`
- `tmp/post_cleanup_products_tree.txt`
- `tmp/strategy_c_complete.txt`
- `workspace/`

**Ignored-but-Relevant Entries**
- `.pytest_cache`
- `.venv`
- `.vscode`
- `api/__pycache__`
- `guardsuite_plugins/__pycache__`
- `products/computeguard/build`
- `products/computescan/build`
- `products/guardboard/build`
- `products/guardscore/build`
- `products/guardsuite-core/build`
- `products/guardsuite-specs/build`
- `products/guardsuite-template/build`
- `products/guardsuite_master_spec/build`
- `products/pipelineguard/build`
- `products/pipelinescan/build`
- `products/playground/build`
- `products/vectorguard/build`
- `products/vectorscan/build`
- `scheduler/__pycache__`
- `scripts/__pycache__`
- `site`
- `tests/__pycache__`
- `validation/__pycache__`

## Missing Items

- None

## Orphaned Paths

- `guardsuite-core/`
- `guardsuite-core/canonical_schema.json`

## Workspace Summary

| Artifact | Present | Notes |
| --- | :---: | --- |
| `workspace/diagnostics` | yes | ok |
| `workspace/diagnostics/repo_scan_raw.json` | yes | ok |
| `workspace/diagnostics/repo_scan_report.md` | yes | ok |
| `workspace/strategy_d/backups` | yes | ok |
| `workspace/strategy_d/checklist_gaps` | yes | ok |
| `workspace/strategy_d/checklist_gap_report.md` | yes | ok |
| `workspace/strategy_d/checklist_gap_summary.yaml` | yes | ok |
| `workspace/strategy_d/diffs` | yes | ok |
| `workspace/strategy_d/bootstrap_notes.md` | yes | ok |

## Products Summary

| Product | Checklist | Metadata | Demo Issues |
| --- | :---: | :---: | --- |
| computeguard | yes | yes | none |
| computescan | yes | yes | none |
| guardboard | yes | yes | none |
| guardscore | yes | yes | none |
| guardsuite-core | yes | yes | none |
| guardsuite-specs | yes | yes | none |
| guardsuite-template | yes | yes | none |
| guardsuite_master_spec | yes | yes | none |
| pipelineguard | yes | yes | none |
| pipelinescan | yes | yes | none |
| playground | yes | yes | none |
| vectorguard | yes | yes | none |
| vectorscan | yes | yes | none |

## Demo Scaffolding Verification

- computeguard: missing=none; extra=none
- computescan: missing=none; extra=none
- guardboard: missing=none; extra=none
- guardscore: missing=none; extra=none
- guardsuite-core: missing=none; extra=none
- guardsuite-specs: missing=none; extra=none
- guardsuite-template: missing=none; extra=none
- guardsuite_master_spec: missing=none; extra=none
- pipelineguard: missing=none; extra=none
- pipelinescan: missing=none; extra=none
- playground: missing=none; extra=none
- vectorguard: missing=none; extra=none
- vectorscan: missing=none; extra=none

## Workspace Layout Check

- All Strategy-D backup, gap, and diagnostic directories exist.
- No duplicate ATU artifacts detected in `workspace/strategy_d`.
- `workspace/diagnostics` retains prior repo scan artifacts for traceability.

## Products Tree Check

- All product directories listed under `products/` are present.
- No forbidden changes detected (git status clean for `products/`).

## Category Listings

### docs (57)
- `.github/copilot-instructions.md`
- `.logs/ai-dev-latest.md`
- `.logs/ai-dev-report-latest.md`
- `CHANGELOG.md`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `README.md`
- `SECURITY.md`
- `ai_snapshots/`
- `ai_snapshots/crossmap/`
- `docs/`
- `docs/README.md`
- `docs/assets/`
- `docs/assets/stylesheets/`
- `docs/assets/stylesheets/spec.css`
- `docs/guardsuite_master_spec.md`
- `docs/index.md`
- `docs/playground_matrix.yml`
- `docs/products/`
- `docs/products/README.md`
- `docs/products/computeguard.md`
- `docs/products/computescan.md`
- `docs/products/guardboard.md`
- `docs/products/guardscore.md`
- `docs/products/guardsuite-core.md`
- `docs/products/pillar-template.md`
- `docs/products/pipelineguard.md`
- `docs/products/pipelinescan.md`
- `docs/products/vectorguard.md`
- `docs/products/vectorscan.md`
- `mkdocs.yml`
- `site/`
- `snippets/`
- `snippets/marketing.yml`
- `snippets/playground_compliance_matrix.yml`
- `snippets/playground_example_response.yml`
- `templates/`
- `templates/checklist_schema/`
- `templates/checklist_schema/checklist_schema.yml`
- `templates/partials/`
- `templates/partials/spec_header.html`
- `templates/product_page.md.j2`
- `templates/product_schema/`
- `templates/product_schema/product_schema.yml`
- `templates/spec_page.md.j2`
- `templates/spec_snapshot.md.j2`
- `tmp/ai-export/computeguard_snapshot_20251124T053000Z.md`
- `tmp/ai-export/computeguard_snapshot_20251124T072731Z.md`
- `tmp/ai-export/computescan_snapshot_20251124T053000Z.md`
- `tmp/ai-export/computescan_snapshot_20251124T072731Z.md`
- `tmp/ai-export/guardboard_snapshot_20251124T053000Z.md`
- `tmp/ai-export/guardboard_snapshot_20251124T072731Z.md`
- `tmp/ai-export/guardscore_snapshot_20251124T053000Z.md`
- `tmp/ai-export/guardscore_snapshot_20251124T072732Z.md`
- `tmp/ai-export/guardsuite-core_snapshot_20251124T053000Z.md`
- `tmp/ai-export/guardsuite-core_snapshot_20251124T072732Z.md`

### orphaned (2)
- `guardsuite-core/`
- `guardsuite-core/canonical_schema.json`

### product_tree (244)
- `products/computeguard/`
- `products/computeguard/assets/`
- `products/computeguard/assets/copy/`
- `products/computeguard/assets/copy/demo/`
- `products/computeguard/assets/copy/demo/.gitkeep`
- `products/computeguard/assets/copy/demo/demo_version.yml`
- `products/computeguard/assets/copy/demo/plan_bad.json`
- `products/computeguard/assets/copy/demo/plan_guard.json`
- `products/computeguard/assets/copy/demo/repro_notes.md`
- `products/computeguard/assets/thumbnails/`
- `products/computeguard/assets/video/`
- `products/computeguard/assets/video/Readme.md`
- `products/computeguard/assets/video/video.yml`
- `products/computeguard/build/`
- `products/computeguard/checklist/`
- `products/computeguard/checklist/checklist.yml`
- `products/computeguard/docs/`
- `products/computeguard/metadata/`
- `products/computeguard/metadata/product.yml`
- `products/computescan/`
- `products/computescan/assets/`
- `products/computescan/assets/copy/`
- `products/computescan/assets/copy/demo/`
- `products/computescan/assets/copy/demo/.gitkeep`
- `products/computescan/assets/copy/demo/demo_version.yml`
- `products/computescan/assets/copy/demo/plan_bad.json`
- `products/computescan/assets/copy/demo/plan_guard.json`
- `products/computescan/assets/copy/demo/repro_notes.md`
- `products/computescan/assets/thumbnails/`
- `products/computescan/assets/video/`
- `products/computescan/assets/video/Readme.md`
- `products/computescan/assets/video/video.yml`
- `products/computescan/build/`
- `products/computescan/checklist/`
- `products/computescan/checklist/checklist.yml`
- `products/computescan/docs/`
- `products/computescan/metadata/`
- `products/computescan/metadata/product.yml`
- `products/guardboard/`
- `products/guardboard/assets/`
- `products/guardboard/assets/copy/`
- `products/guardboard/assets/copy/demo/`
- `products/guardboard/assets/copy/demo/.gitkeep`
- `products/guardboard/assets/copy/demo/demo_version.yml`
- `products/guardboard/assets/copy/demo/plan_bad.json`
- `products/guardboard/assets/copy/demo/plan_guard.json`
- `products/guardboard/assets/copy/demo/repro_notes.md`
- `products/guardboard/assets/thumbnails/`
- `products/guardboard/assets/video/`
- `products/guardboard/build/`
- `products/guardboard/checklist/`
- `products/guardboard/checklist/checklist.yml`
- `products/guardboard/docs/`
- `products/guardboard/metadata/`
- `products/guardboard/metadata/product.yml`
- `products/guardscore/`
- `products/guardscore/assets/`
- `products/guardscore/assets/copy/`
- `products/guardscore/assets/copy/demo/`
- `products/guardscore/assets/copy/demo/.gitkeep`
- `products/guardscore/assets/copy/demo/demo_version.yml`
- `products/guardscore/assets/copy/demo/plan_bad.json`
- `products/guardscore/assets/copy/demo/plan_guard.json`
- `products/guardscore/assets/copy/demo/repro_notes.md`
- `products/guardscore/assets/thumbnails/`
- `products/guardscore/assets/video/`
- `products/guardscore/build/`
- `products/guardscore/checklist/`
- `products/guardscore/checklist/checklist.yml`
- `products/guardscore/docs/`
- `products/guardscore/metadata/`
- `products/guardscore/metadata/product.yml`
- `products/guardsuite-core/`
- `products/guardsuite-core/assets/`
- `products/guardsuite-core/assets/copy/`
- `products/guardsuite-core/assets/copy/demo/`
- `products/guardsuite-core/assets/copy/demo/.gitkeep`
- `products/guardsuite-core/assets/copy/demo/demo_version.yml`
- `products/guardsuite-core/assets/copy/demo/plan_bad.json`
- `products/guardsuite-core/assets/copy/demo/plan_guard.json`
- `products/guardsuite-core/assets/copy/demo/repro_notes.md`
- `products/guardsuite-core/assets/thumbnails/`
- `products/guardsuite-core/assets/video/`
- `products/guardsuite-core/build/`
- `products/guardsuite-core/checklist/`
- `products/guardsuite-core/checklist/checklist.yml`
- `products/guardsuite-core/docs/`
- `products/guardsuite-core/metadata/`
- `products/guardsuite-core/metadata/product.yml`
- `products/guardsuite-specs/`
- `products/guardsuite-specs/assets/`
- `products/guardsuite-specs/assets/copy/`
- `products/guardsuite-specs/assets/copy/.gitkeep`
- `products/guardsuite-specs/assets/copy/demo/`
- `products/guardsuite-specs/assets/copy/demo/.gitkeep`
- `products/guardsuite-specs/assets/copy/demo/demo_version.yml`
- `products/guardsuite-specs/assets/copy/demo/plan_bad.json`
- `products/guardsuite-specs/assets/copy/demo/plan_guard.json`
- `products/guardsuite-specs/assets/copy/demo/repro_notes.md`
- `products/guardsuite-specs/assets/thumbnails/`
- `products/guardsuite-specs/assets/thumbnails/.gitkeep`
- `products/guardsuite-specs/assets/video/`
- `products/guardsuite-specs/assets/video/.gitkeep`
- `products/guardsuite-specs/build/`
- `products/guardsuite-specs/checklist/`
- `products/guardsuite-specs/checklist/checklist.yml`
- `products/guardsuite-specs/docs/`
- `products/guardsuite-specs/docs/.gitkeep`
- `products/guardsuite-specs/metadata/`
- `products/guardsuite-specs/metadata/product.yml`
- `products/guardsuite-template/`
- `products/guardsuite-template/assets/`
- `products/guardsuite-template/assets/copy/`
- `products/guardsuite-template/assets/copy/.gitkeep`
- `products/guardsuite-template/assets/copy/demo/`
- `products/guardsuite-template/assets/copy/demo/.gitkeep`
- `products/guardsuite-template/assets/copy/demo/demo_version.yml`
- `products/guardsuite-template/assets/copy/demo/plan_bad.json`
- `products/guardsuite-template/assets/copy/demo/plan_guard.json`
- `products/guardsuite-template/assets/copy/demo/repro_notes.md`
- `products/guardsuite-template/assets/thumbnails/`
- `products/guardsuite-template/assets/thumbnails/.gitkeep`
- `products/guardsuite-template/assets/video/`
- `products/guardsuite-template/assets/video/.gitkeep`
- `products/guardsuite-template/build/`
- `products/guardsuite-template/checklist/`
- `products/guardsuite-template/checklist/checklist.yml`
- `products/guardsuite-template/docs/`
- `products/guardsuite-template/docs/.gitkeep`
- `products/guardsuite-template/metadata/`
- `products/guardsuite-template/metadata/product.yml`
- `products/guardsuite_master_spec/`
- `products/guardsuite_master_spec/assets/`
- `products/guardsuite_master_spec/assets/copy/`
- `products/guardsuite_master_spec/assets/copy/demo/`
- `products/guardsuite_master_spec/assets/copy/demo/.gitkeep`
- `products/guardsuite_master_spec/assets/copy/demo/demo_version.yml`
- `products/guardsuite_master_spec/assets/copy/demo/plan_bad.json`
- `products/guardsuite_master_spec/assets/copy/demo/plan_guard.json`
- `products/guardsuite_master_spec/assets/copy/demo/repro_notes.md`
- `products/guardsuite_master_spec/assets/thumbnails/`
- `products/guardsuite_master_spec/assets/video/`
- `products/guardsuite_master_spec/build/`
- `products/guardsuite_master_spec/checklist/`
- `products/guardsuite_master_spec/checklist/checklist.yml`
- `products/guardsuite_master_spec/docs/`
- `products/guardsuite_master_spec/metadata/`
- `products/guardsuite_master_spec/metadata/product.yml`
- `products/list_tree.sh`
- `products/pipelineguard/`
- `products/pipelineguard/assets/`
- `products/pipelineguard/assets/copy/`
- `products/pipelineguard/assets/copy/demo/`
- `products/pipelineguard/assets/copy/demo/.gitkeep`
- `products/pipelineguard/assets/copy/demo/demo_version.yml`
- `products/pipelineguard/assets/copy/demo/plan_bad.json`
- `products/pipelineguard/assets/copy/demo/plan_guard.json`
- `products/pipelineguard/assets/copy/demo/repro_notes.md`
- `products/pipelineguard/assets/thumbnails/`
- `products/pipelineguard/assets/video/`
- `products/pipelineguard/assets/video/Readme.md`
- `products/pipelineguard/assets/video/video.yml`
- `products/pipelineguard/build/`
- `products/pipelineguard/checklist/`
- `products/pipelineguard/checklist/checklist.yml`
- `products/pipelineguard/docs/`
- `products/pipelineguard/metadata/`
- `products/pipelineguard/metadata/product.yml`
- `products/pipelinescan/`
- `products/pipelinescan/assets/`
- `products/pipelinescan/assets/copy/`
- `products/pipelinescan/assets/copy/demo/`
- `products/pipelinescan/assets/copy/demo/.gitkeep`
- `products/pipelinescan/assets/copy/demo/demo_version.yml`
- `products/pipelinescan/assets/copy/demo/plan_bad.json`
- `products/pipelinescan/assets/copy/demo/plan_guard.json`
- `products/pipelinescan/assets/copy/demo/repro_notes.md`
- `products/pipelinescan/assets/thumbnails/`
- `products/pipelinescan/assets/video/`
- `products/pipelinescan/assets/video/Readme.md`
- `products/pipelinescan/assets/video/video.yml`
- `products/pipelinescan/build/`
- `products/pipelinescan/checklist/`
- `products/pipelinescan/checklist/checklist.yml`
- `products/pipelinescan/docs/`
- `products/pipelinescan/metadata/`
- `products/pipelinescan/metadata/product.yml`
- `products/playground/`
- `products/playground/assets/`
- `products/playground/assets/copy/`
- `products/playground/assets/copy/demo/`
- `products/playground/assets/copy/demo/.gitkeep`
- `products/playground/assets/copy/demo/demo_version.yml`
- `products/playground/assets/copy/demo/plan_bad.json`
- `products/playground/assets/copy/demo/plan_guard.json`
- `products/playground/assets/copy/demo/repro_notes.md`
- `products/playground/assets/thumbnails/`
- `products/playground/assets/video/`
- `products/playground/build/`
- `products/playground/checklist/`
- `products/playground/checklist/checklist.yml`
- `products/playground/docs/`
- `products/playground/metadata/`
- `products/playground/metadata/product.yml`
- `products/product_index.yml`
- `products/tree.txt`
- `products/vectorguard/`
- `products/vectorguard/assets/`
- `products/vectorguard/assets/copy/`
- `products/vectorguard/assets/copy/demo/`
- `products/vectorguard/assets/copy/demo/.gitkeep`
- `products/vectorguard/assets/copy/demo/demo_version.yml`
- `products/vectorguard/assets/copy/demo/plan_bad.json`
- `products/vectorguard/assets/copy/demo/plan_guard.json`
- `products/vectorguard/assets/copy/demo/repro_notes.md`
- `products/vectorguard/assets/thumbnails/`
- `products/vectorguard/assets/video/`
- `products/vectorguard/assets/video/Readme.md`
- `products/vectorguard/assets/video/video.yml`
- `products/vectorguard/build/`
- `products/vectorguard/checklist/`
- `products/vectorguard/checklist/checklist.yml`
- `products/vectorguard/docs/`
- `products/vectorguard/metadata/`
- `products/vectorguard/metadata/product.yml`
- `products/vectorscan/`
- `products/vectorscan/assets/`
- `products/vectorscan/assets/copy/`
- `products/vectorscan/assets/copy/demo/`
- `products/vectorscan/assets/copy/demo/.gitkeep`
- `products/vectorscan/assets/copy/demo/demo_version.yml`
- `products/vectorscan/assets/copy/demo/plan_bad.json`
- `products/vectorscan/assets/copy/demo/plan_guard.json`
- `products/vectorscan/assets/copy/demo/repro_notes.md`
- `products/vectorscan/assets/thumbnails/`
- `products/vectorscan/assets/video/`
- `products/vectorscan/assets/video/Readme.md`
- `products/vectorscan/assets/video/video.yml`
- `products/vectorscan/build/`
- `products/vectorscan/checklist/`
- `products/vectorscan/checklist/checklist.yml`
- `products/vectorscan/docs/`
- `products/vectorscan/metadata/`
- `products/vectorscan/metadata/product.yml`

### schema (13)
- `canonical_schemas/`
- `canonical_schemas/.gitkeep`
- `product_specs/`
- `product_specs/pillar-template.schema.yml`
- `product_specs/pillar-template.yml`
- `schemas/`
- `schemas/README.md`
- `schemas/bootstrap_schema.yml`
- `schemas/checklist_schema.yml`
- `schemas/pillar-template.schema.yml`
- `schemas/playground.schema.yml`
- `schemas/product.schema.json`
- `schemas/product_schema.yml`

### scripts (13)
- `bootstrap/`
- `bootstrap/.gitkeep`
- `bootstrap/guardsuite-specs.bootstrap.json`
- `cli/`
- `cli/__init__.py`
- `cli/guardspecs_cli.py`
- `scripts/`
- `scripts/__pycache__/`
- `scripts/export_for_ai.py`
- `scripts/gen_docs.py`
- `scripts/sync_to_repo.py`
- `scripts/validate_products.py`
- `scripts/validate_yaml_schema.py`

### unexpected (19)
- `.github/`
- `.github/workflows/`
- `.github/workflows/generate_docs.yml`
- `.github/workflows/open_sync_pr.yml`
- `.gitignore`
- `.logs/`
- `.pre-commit-config.yaml`
- `.pytest_cache/`
- `.venv/`
- `.vscode/`
- `poetry.lock`
- `products/`
- `pyproject.toml`
- `tmp/`
- `tmp/ai-export/`
- `tmp/final_products_tree.txt`
- `tmp/post_cleanup_products_tree.txt`
- `tmp/strategy_c_complete.txt`
- `workspace/`

### utilities (111)
- `api/`
- `api/__init__.py`
- `api/__main__.py`
- `api/__pycache__/`
- `api/app.py`
- `api/bootstrap_api.py`
- `api/bootstrap_generator.py`
- `api/ci_integration.py`
- `api/config.py`
- `api/db.py`
- `api/products.py`
- `api/routes.py`
- `api/validate.py`
- `api/webhook_ingest.py`
- `contracts/`
- `contracts/playground_contract.yml`
- `conventions/`
- `conventions/.gitkeep`
- `db/`
- `db/README.md`
- `db/products.json`
- `governance/`
- `governance/.gitkeep`
- `guardsuite_plugins/`
- `guardsuite_plugins/__init__.py`
- `guardsuite_plugins/__pycache__/`
- `guardsuite_plugins/admonition.py`
- `pricing/`
- `pricing/guardsuite_pricing.yml`
- `release/`
- `release/.gitkeep`
- `scheduler/`
- `scheduler/__init__.py`
- `scheduler/__main__.py`
- `scheduler/__pycache__/`
- `scheduler/job.py`
- `semantic/`
- `semantic/semantic_categories.schema.yml`
- `semantic/semantic_categories.yml`
- `semantic/semantic_configuration.schema.yml`
- `semantic/semantic_configuration.yml`
- `semantic/semantic_coverage.schema.yml`
- `semantic/semantic_coverage.yml`
- `semantic/semantic_crossref.schema.yml`
- `semantic/semantic_crossref.yml`
- `semantic/semantic_entities.schema.yml`
- `semantic/semantic_entities.yml`
- `semantic/semantic_governance_index.schema.yml`
- `semantic/semantic_governance_index.yml`
- `semantic/semantic_integrity.schema.yml`
- `semantic/semantic_integrity.yml`
- `semantic/semantic_policy.schema.yml`
- `semantic/semantic_policy.yml`
- `semantic/semantic_provenance.schema.yml`
- `semantic/semantic_provenance.yml`
- `semantic/semantic_registry.schema.yml`
- `semantic/semantic_registry.yml`
- `semantic/semantic_rule_template.schema.yml`
- `semantic/semantic_rule_template.yml`
- `semantic/semantic_rules.schema.yml`
- `semantic/semantic_rules.yml`
- `semantic/semantic_rules_manifest.schema.yml`
- `semantic/semantic_rules_manifest.yml`
- `semantic/semantic_runtime.schema.yml`
- `semantic/semantic_runtime.yml`
- `semantic/semantic_runtime_capabilities.schema.yml`
- `semantic/semantic_runtime_capabilities.yml`
- `semantic/semantic_runtime_capabilities_registry.schema.yml`
- `semantic/semantic_runtime_capabilities_registry.yml`
- `semantic/semantic_runtime_capability_groups.schema.yml`
- `semantic/semantic_runtime_capability_groups.yml`
- `semantic/semantic_runtime_capability_index.schema.yml`
- `semantic/semantic_runtime_capability_index.yml`
- `semantic/semantic_runtime_capability_manifest.schema.yml`
- `semantic/semantic_runtime_capability_manifest.yml`
- `semantic/semantic_runtime_capability_map.schema.yml`
- `semantic/semantic_runtime_capability_map.yml`
- `semantic/semantic_runtime_capability_matrix.schema.yml`
- `semantic/semantic_runtime_capability_matrix.yml`
- `semantic/semantic_runtime_capability_topology.schema.yml`
- `semantic/semantic_runtime_capability_topology.yml`
- `semantic/semantic_runtime_environment.schema.yml`
- `semantic/semantic_runtime_environment.yml`
- `semantic/semantic_surface_groups.schema.yml`
- `semantic/semantic_surface_groups.yml`
- `semantic/semantic_surface_index.schema.yml`
- `semantic/semantic_surface_index.yml`
- `semantic/semantic_surface_manifest.schema.yml`
- `semantic/semantic_surface_manifest.yml`
- `semantic/semantic_surface_map.schema.yml`
- `semantic/semantic_surface_map.yml`
- `semantic/semantic_surface_matrix.schema.yml`
- `semantic/semantic_surface_matrix.yml`
- `tests/`
- `tests/__init__.py`
- `tests/__pycache__/`
- `tests/test_bootstrap_generator.py`
- `tests/test_product_metadata_contract_v2.py`
- `tests/test_product_runtime_contracts.py`
- `tests/test_product_schema_contract.py`
- `tests/test_product_semantics.py`
- `tests/test_release_metadata.py`
- `tests/test_template_field_coverage.py`
- `tests/test_yaml_validity.py`
- `tests/utils.py`
- `validation/`
- `validation/__init__.py`
- `validation/__pycache__/`
- `validation/validator.py`
- `webhooks/`
- `webhooks/__init__.py`

### workspace (85)
- `workspace/diagnostics/`
- `workspace/diagnostics/repo_scan_raw.json`
- `workspace/diagnostics/repo_scan_report.md`
- `workspace/orphans/`
- `workspace/orphans/checklists/`
- `workspace/strategy_c_closure.md`
- `workspace/strategy_d/`
- `workspace/strategy_d/backups/`
- `workspace/strategy_d/backups/computeguard_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/computescan_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/guardboard_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/guardscore_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/guardsuite-core_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/guardsuite_master_spec_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/pipelineguard_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/pipelinescan_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/playground_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/vectorguard_checklist_pre_normalization.yml`
- `workspace/strategy_d/backups/vectorscan_checklist_pre_normalization.yml`
- `workspace/strategy_d/bootstrap_notes.md`
- `workspace/strategy_d/checklist_gap_report.md`
- `workspace/strategy_d/checklist_gap_summary.yaml`
- `workspace/strategy_d/checklist_gaps/`
- `workspace/strategy_d/checklist_gaps/computeguard_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/computescan_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/guardboard_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/guardscore_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/guardsuite-core_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/guardsuite-specs_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/guardsuite-template_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/guardsuite_master_spec_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/pipelineguard_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/pipelinescan_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/playground_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/vectorguard_checklist_gap.md`
- `workspace/strategy_d/checklist_gaps/vectorscan_checklist_gap.md`
- `workspace/strategy_d/checklist_schema_notes.md`
- `workspace/strategy_d/checklists_scan_results.json`
- `workspace/strategy_d/diffs/`
- `workspace/strategy_d/diffs/computeguard_checklist_diff.md`
- `workspace/strategy_d/diffs/computescan_checklist_diff.md`
- `workspace/strategy_d/diffs/guardboard_checklist_diff.md`
- `workspace/strategy_d/diffs/guardscore_checklist_diff.md`
- `workspace/strategy_d/diffs/guardsuite-core_checklist_diff.md`
- `workspace/strategy_d/diffs/guardsuite_master_spec_checklist_diff.md`
- `workspace/strategy_d/diffs/pipelineguard_checklist_diff.md`
- `workspace/strategy_d/diffs/pipelinescan_checklist_diff.md`
- `workspace/strategy_d/diffs/playground_checklist_diff.md`
- `workspace/strategy_d/diffs/vectorguard_checklist_diff.md`
- `workspace/strategy_d/diffs/vectorscan_checklist_diff.md`
- `workspace/strategy_d/phase4_summary.md`
- `workspace/strategy_d/phase5_preamble.md`
- `workspace/strategy_d/phase6_bootstrap_summary.md`
- `workspace/strategy_d/product_schema_notes.md`
- `workspace/strategy_d/product_spec_gap_report.md`
- `workspace/strategy_d/product_spec_gaps/`
- `workspace/strategy_d/product_spec_gaps/computeguard_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/computescan_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/guardboard_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/guardscore_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/guardsuite-core_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/guardsuite-specs_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/guardsuite-template_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/guardsuite_master_spec_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/pipelineguard_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/pipelinescan_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/playground_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/vectorguard_spec_gap.md`
- `workspace/strategy_d/product_spec_gaps/vectorscan_spec_gap.md`
- `workspace/strategy_d/product_specs_scan_results.json`
- `workspace/strategy_d/scaffolding_phase2_complete.md`
- `workspace/strategy_d/scaffolding_phase3/`
- `workspace/strategy_d/scaffolding_phase3/cli_workflows/`
- `workspace/strategy_d/scaffolding_phase3/cli_workflows/cli_demo_flow.md`
- `workspace/strategy_d/scaffolding_phase3/demo_ingestion/`
- `workspace/strategy_d/scaffolding_phase3/design/`
- `workspace/strategy_d/scaffolding_phase3/design/demo_ingestion_design.md`
- `workspace/strategy_d/scaffolding_phase3/phase3_overview.md`
- `workspace/strategy_d/scaffolding_phase3/scaffolding_phase3_complete.md`
- `workspace/strategy_d/scaffolding_phase4/`
- `workspace/strategy_d/scaffolding_phase4/scaffolding_phase4_complete.md`
- `workspace/utilities/`
- `workspace/utilities/README.md`
- `workspace/utilities/list_tree.sh`
- `workspace/vectorguard_worksheet.yml`

## Readiness for Next Strategy-D Phase

- Repo is clean with demo scaffolding verified.
- Workspace artifacts required for the next Strategy-D checkpoint are present.
- No missing or duplicate ATU outputs detected; diagnostics remain deterministic.
