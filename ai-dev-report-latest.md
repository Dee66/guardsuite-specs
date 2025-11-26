```markdown
# AI-Dev Repository Scan Report (v33)

- Generated: 2025-11-26T07:22:58+00:00
- Repo clean: no
- Untracked files: 23
- Ignored entries (visible): 2805
- Repo health score: 96
- Repo health delta: -4

## Findings

- Repo traversal honored ignore patterns (__pycache__/, *.pyc, .venv/, dist/, build/, site/, *.egg-info/, *.log, *.tmp, *.cache, .pytest_cache/, .mypy_cache/, .ruff_cache/, .coverage, *.coverage).
- Strategy-D controlled surfaces remain present and unchanged since last deterministic repairs; tracked/untracked counts updated based on live git status.
- Workspace diagnostics artifacts remain present; raw + rendered outputs verified.
- Product demo scaffolding remains intact for every product; expected demo files present.
- YAML validation summary plus error context/recommendations/diff provided for remediation tracking.

## Repository Health Score

- Score: 96 / 100 (deductions: 2 for modified tracked files, 2 for untracked-file delta)
- Delta vs previous: -4

## Indicators of Drift

- Repo health delta: -4
- Invalid YAML count change: 0 (now 0)
- Modified tracked files: 2
- Untracked files: 23
- Ignored-visible entries: 2805

## Git Status Summary

| Status | Count |
| --- | ---: |
| tracked | 418 |
| modified | 2 |
| untracked | 23 |

## Category Breakdown

| Category | Count |
| --- | ---: |
| docs | 56 |
| orphaned | 2 |
| product_tree | 231 |
| schema | 13 |
| scripts | 12 |
| unexpected | 17 |
| utilities | 106 |
| workspace | 86 |

## Anomalies

**Modified Tracked Files**
- `workspace/strategy_d/phase11/cross_product_semantic_validation_report.md`
- `workspace/strategy_d/phase6/metadata_validation_report.md`

**Untracked Paths (sample / full list follows)**
- `products/computeguard/assets/copy/hook.txt`
- `products/computeguard/assets/copy/micro_cta.txt`
- `products/computeguard/metadata/iconic_findings.txt`
- `products/computescan/assets/copy/hook.txt`
- `products/computescan/assets/copy/micro_cta.txt`
- `products/computescan/metadata/iconic_findings.txt`
- `products/pipelineguard/assets/copy/hook.txt`
- `products/pipelineguard/assets/copy/micro_cta.txt`
- `products/pipelineguard/metadata/iconic_findings.txt`
- `products/pipelinescan/metadata/iconic_findings.txt`
- `products/vectorguard/assets/copy/hook.txt`
- `products/vectorguard/assets/copy/micro_cta.txt`
- `products/vectorguard/metadata/iconic_findings.txt`
- `products/vectorscan/assets/copy/hook.txt`
- `products/vectorscan/assets/copy/micro_cta.txt`
- `products/vectorscan/metadata/iconic_findings.txt`
- `workspace/strategy_d/phase10/metadata_validation_post.md`
- `workspace/strategy_d/phase10/repair_phase10.py`
- `workspace/strategy_d/phase11/validate_phase11.py`
- `workspace/strategy_d/phase13/run_phase13.py`
- `workspace/strategy_d/phase6/validate_phase6.py`
- `workspace/strategy_d/phase7/repair_phase7.py`
- `workspace/strategy_d/phase8/repair_phase8.py`

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

## Strategy-D Workspace Status

| Artifact | Present | Notes |
| --- | :---: | --- |
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

## Demo Scaffolding Status

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

## Valid YAML Summaries

| File | Valid | Notes |
| --- | :---: | --- |
| `product_specs/pillar-template.schema.yml` | yes | valid |
| `product_specs/pillar-template.yml` | yes | valid |
| `products/computeguard/checklist/checklist.yml` | yes | valid |
| `products/computeguard/metadata/product.yml` | yes | valid |
| `products/computescan/checklist/checklist.yml` | yes | valid |
| `products/computescan/metadata/product.yml` | yes | valid |
| `products/guardboard/checklist/checklist.yml` | yes | valid |
| `products/guardboard/metadata/product.yml` | yes | valid |
| `products/guardscore/checklist/checklist.yml` | yes | valid |
| `products/guardscore/metadata/product.yml` | yes | valid |
| `products/guardsuite-core/checklist/checklist.yml` | yes | valid |
| `products/guardsuite-core/metadata/product.yml` | yes | valid |
| `products/guardsuite-specs/checklist/checklist.yml` | yes | valid |
| `products/guardsuite-specs/metadata/product.yml` | yes | valid |
| `products/guardsuite-template/checklist/checklist.yml` | yes | valid |
| `products/guardsuite-template/metadata/product.yml` | yes | valid |
| `products/guardsuite_master_spec/checklist/checklist.yml` | yes | valid |
| `products/guardsuite_master_spec/metadata/product.yml` | yes | valid |
| `products/pipelineguard/checklist/checklist.yml` | yes | valid |
| `products/pipelineguard/metadata/product.yml` | yes | valid |
| `products/pipelinescan/checklist/checklist.yml` | yes | valid |
| `products/pipelinescan/metadata/product.yml` | yes | valid |
| `products/playground/checklist/checklist.yml` | yes | valid |
| `products/playground/metadata/product.yml` | yes | valid |
| `products/vectorguard/checklist/checklist.yml` | yes | valid |
| `products/vectorguard/metadata/product.yml` | yes | valid |
| `products/vectorscan/checklist/checklist.yml` | yes | valid |
| `products/vectorscan/metadata/product.yml` | yes | valid |
| `schemas/bootstrap_schema.yml` | yes | valid |
| `schemas/checklist_schema.yml` | yes | valid |
| `schemas/pillar-template.schema.yml` | yes | valid |
| `schemas/playground.schema.yml` | yes | valid |
| `schemas/product_schema.yml` | yes | valid |
| `templates/checklist_schema/checklist_schema.yml` | yes | valid |
| `templates/product_schema/product_schema.yml` | yes | valid |
| `workspace/strategy_d/checklist_gap_summary.yaml` | yes | valid |

## YAML Validation Diff vs Previous

- Resolved failures since v32: none

## Schema Coverage Stats

| Metric | Value |
| --- | ---: |
| Total YAML files scanned | 36 |
| Valid YAML files | 36 |
| Invalid YAML files | 0 |
| Valid coverage (%) | 100.0 |
| Product metadata present | 13 / 13 |
| Product checklists present | 13 / 13 |

## Category Listings

### docs (56)
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

### product_tree (231)
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
- `products/computescan/checklist/`
- `products/computescan/checklist/checklist.yml`
- `products/computescan/docs/`
- `products/computescan/metadata/`
- `products/computescan/metadata/product.yml`
- `products/guardboard/`
- `products/guardboard/assets/`
- `products/guardboard/assets/copy/`
- (truncated for brevity in file; full listing preserved in diagnostics JSON)

## Readiness for Next Strategy-D Phase

- Repo has small active modifications in `workspace/strategy_d` and untracked artifacts under `products/*/assets` which appear to be local demo additions; these do not impact schema coverage or YAML validity.
- Health metrics, drift indicators, and schema coverage stats refreshed for architect review.

```
