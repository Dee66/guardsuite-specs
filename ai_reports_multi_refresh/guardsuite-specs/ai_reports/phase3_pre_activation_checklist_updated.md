# Phase‑3 Pre‑Activation Checklist (Updated)

Generated: 2025-11-27T14:58:00Z

This is an updated copy of the Phase‑3 pre‑activation checklist reflecting work performed on branch `phase5/pilot-computeguard-clean`. It preserves the original checklist structure and records completed items, evidence, and remaining blockers.

## Schema actions
- [x] Promote `ai_reports/schema_templates/computeguard.schema.yml` -> `products/computeguard/schema.yml`
  - Evidence: `products/computeguard/schema.yml` (promoted); cited in `ai_reports/phase5_pilot_report.json`.
- [ ] Promote remaining product schema templates -> `products/<product>/schema.yml` for: `computescan`, `pipelineguard`, `pipelinescan`, `vectorguard`, `vectorscan`.
- [x] Ensure promoted schema(s) include canonical fields (`plan_id`, `schema_version`, `resources`, `metadata.source`, `metadata.ingested_at`) for `computeguard`.

## Evaluator actions
- [x] Implement canonical adapter mapping `run_pipeline_on_text` -> `evaluate(resource)` under `strategy_e/adapters/`.
  - Evidence: `strategy_e/adapters/pipeline_adapter.py` exists and normalizes rule inputs for the executor.
- [x] Create per-product adapter modules exposing `evaluate(resource)` for `computeguard`.
  - Evidence: `strategy_e/adapters/computeguard_adapter.py` scaffolded and referenced in `ai_reports/phase5_pilot_report.json`.
- [ ] Create per-product adapters for remaining products (`computescan`, `pipelineguard`, `pipelinescan`, `vectorguard`, `vectorscan`).
- [x] Validate adapters with unit tests for scaffolded adapters.
  - Evidence: `strategy_e/adapters/tests/*` and top-level `tests/*` were added; pytest run shows `48 passed` and `ai_reports/phase5_full_verification.json` records the test pass.

## Rule registry actions
- [x] Update base template rule for `computeguard` to include `severity` and `remediation_hint`.
  - Evidence: `products/computeguard/rules/00_base_rule.yml` and `ai_reports/phase5_pilot_report.json`.
- [ ] Add concrete non-template rules for remaining products.
- [ ] Re-run rule registry audit and verify no template-only products remain (`ai_reports/rule_registry_audit.json` should be updated after remaining changes).

## Orchestration actions
- [x] Confirm `ai_reports/phase3_execution_schedule.json` and `ai_reports/phase3_execution_plan.json` list planned ATUs and dependencies (files present and in-use).
- [x] Produce verification artifacts after performed changes.
  - Evidence: `ai_reports/phase5_full_verification.json`, `ai_reports/phase5_lint_fix_summary.json`, `ai_reports/phase5_flake8_raw_after.txt`.
- [ ] Add CI jobs that enforce schema validation and adapter tests on PRs (a dry‑run `.github/workflows/phase5_lint_ci.yml` was added; currently dry-run).

## Cross‑pillar / Global actions
- [ ] Promote remaining templates (UNBLOCK-G-01) product-by-product.
- [ ] Complete base template rules across all pillars and add concrete rules.
- [x] Implement canonical adapter layer and the `computeguard` evaluator adapter (partial cross-pillar progress).
- [ ] Assign owners for orphan `rule_specs/` directories and finalize promotion workflows.

## Linting, formatting, and tests
- [x] Run Black across repo (configured to 88-character line length) — many files reformatted.
- [x] Run `ruff format` (no further changes reported on the most recent run).
- [x] Capture flake8 output pre/post-format: `ai_reports/phase5_flake8_raw.txt` and `ai_reports/phase5_flake8_raw_after.txt` saved.
  - Note: `flake8` still reports many E501 and other issues across the repo; see `ai_reports/phase5_flake8_raw_after.txt`.
- [x] Run full test suite: `pytest` passed (`48 passed`) — adapter and top-level tests executed. Evidence saved in `ai_reports/phase5_full_verification.json`.

## Blocking items / Remaining work
- [ ] Promote per-product schemas for: `computescan`, `pipelineguard`, `pipelinescan`, `vectorguard`, `vectorscan`.
- [ ] Seed concrete rules for all products and re-run rule registry audit.
- [ ] Address repository-wide flake8 issues or standardize CI line-length to 88 (Black) to reduce noise and enable enforcement.
- [ ] Update CI workflow to enforce lint + pytest as blocking on PRs (currently dry-run).
- [ ] Assign product owners and governance for schema and rule promotions.

## Artifacts & evidence (selected)
- `products/computeguard/schema.yml`
- `products/computeguard/rules/00_base_rule.yml`
- `strategy_e/adapters/pipeline_adapter.py`
- `strategy_e/adapters/computeguard_adapter.py`
- `strategy_e/adapters/tests/test_pipeline_adapter.py`
- `strategy_e/adapters/tests/test_computeguard_adapter.py`
- `ai_reports/phase5_full_verification.json`
- `ai_reports/phase5_flake8_raw.txt` and `ai_reports/phase5_flake8_raw_after.txt`
- `ai_reports/phase5_lint_fix_summary.json`
- `ai_reports/phase5_pilot_report.json`
- `ai_reports/project_completion_percentage.json`

---

This file is an updated, standalone checklist. To keep the canonical checklist synchronized, consider copying these entries back into `ai_reports/phase3_pre_activation_checklist.md` or replacing that file when the apply patch tool is available.
