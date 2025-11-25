# Repository Diagnostic Report

- Generated: 2025-11-25T17:17:18.732125+00:00
- Repo clean: yes
- Untracked files: 0
- Ignored entries (visible): 23

## Category Breakdown

| Category | Count |
| --- | ---: |
| docs | 28 |
| orphaned | 2 |
| product_tree | 218 |
| schema | 13 |
| scripts | 13 |
| unexpected | 27 |
| utilities | 127 |
| workspace | 80 |

## Git Status Summary

| Status | Count |
| --- | ---: |
| derived | 135 |
| ignored | 23 |
| tracked | 350 |

## Structural Findings

- All expected product directories are present.

**Demo Scaffolding Audit**
- vectorscan: missing=None; extra=.gitkeep
- vectorguard: missing=None; extra=.gitkeep
- computescan: missing=None; extra=.gitkeep
- computeguard: missing=None; extra=.gitkeep
- pipelinescan: missing=None; extra=.gitkeep
- pipelineguard: missing=None; extra=.gitkeep
- guardboard: missing=None; extra=.gitkeep
- guardscore: missing=None; extra=.gitkeep
- guardsuite-core: missing=None; extra=.gitkeep
- guardsuite_master_spec: missing=None; extra=.gitkeep
- guardsuite-specs: missing=None; extra=.gitkeep
- guardsuite-template: missing=None; extra=.gitkeep
- playground: missing=None; extra=.gitkeep

- All monitored workspace artifacts are present.

**Unexpected Paths Detected**
- .github
- .github/copilot-instructions.md
- .github/workflows
- .github/workflows/generate_docs.yml
- .github/workflows/open_sync_pr.yml
- .gitignore
- .logs/ai-dev-latest.md
- .logs/ai-dev-report-latest.md
- .pre-commit-config.yaml
- .pytest_cache/
- .venv/
- .vscode/
- tmp
- tmp/ai-export
- tmp/ai-export/computeguard_snapshot_20251124T053000Z.md
- tmp/ai-export/computeguard_snapshot_20251124T072731Z.md
- tmp/ai-export/computescan_snapshot_20251124T053000Z.md
- tmp/ai-export/computescan_snapshot_20251124T072731Z.md
- tmp/ai-export/guardboard_snapshot_20251124T053000Z.md
- tmp/ai-export/guardboard_snapshot_20251124T072731Z.md
- tmp/ai-export/guardscore_snapshot_20251124T053000Z.md
- tmp/ai-export/guardscore_snapshot_20251124T072732Z.md
- tmp/ai-export/guardsuite-core_snapshot_20251124T053000Z.md
- tmp/ai-export/guardsuite-core_snapshot_20251124T072732Z.md
- tmp/final_products_tree.txt
- ... 2 additional paths omitted for brevity

**Orphaned GuardSuite Roots**
- guardsuite-core
- guardsuite-core/canonical_schema.json

**Ignored-but-Relevant Entries**
- .pytest_cache/
- .venv/
- .vscode/
- api/__pycache__/
- guardsuite_plugins/__pycache__/
- products/computeguard/build/
- products/computescan/build/
- products/guardboard/build/
- products/guardscore/build/
- products/guardsuite-core/build/
- products/guardsuite-specs/build/
- products/guardsuite-template/build/
- products/guardsuite_master_spec/build/
- products/pipelineguard/build/
- products/pipelinescan/build/
- products/playground/build/
- products/vectorguard/build/
- products/vectorscan/build/
- scheduler/__pycache__/
- scripts/__pycache__/
- site/
- tests/__pycache__/
- validation/__pycache__/

## Readiness Summary

Repo is clean with deterministic demo scaffolding in place. Extra `.gitkeep` files remain in each demo directory but do not block the next Strategy-D phase. Workspace scaffolding for Phases 2-4 plus Phase 6 bootstrap outputs are present. No product mutations detected after sealing cycles.
