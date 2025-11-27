# Phase‑3 Pre‑Activation Checklist

Generated: 2025-11-27T13:50:00Z

This checklist is a compact, actionable pre‑activation list derived from `ai_reports/phase3_readiness_gate.json`.

## Schema actions
- [ ] Promote `ai_reports/schema_templates/<product>.schema.yml` -> `products/<product>/schema.yml` for each missing product (see `ai_reports/phase3_unblock_plan.json` and `ai_reports/phase3_activation_roadmap.json`).
- [ ] Ensure each promoted product schema contains canonical fields: `plan_id`, `schema_version`, `resources`, `metadata.source`, `metadata.ingested_at`.
- [ ] Open small, reviewable PRs per product with CI schema validation enabled (follow `UNBLOCK-G-01`).

## Evaluator actions
- [ ] Implement canonical adapter mapping `run_pipeline_on_text` -> `evaluate(resource)` under `strategy_e/adapters/` (see `UNBLOCK-P-01`).
- [ ] Create per-product adapter modules exposing `evaluate(resource)` that call the canonical executor or product-specific logic (see `UNBLOCK-V-04`, `UNBLOCK-C-04`).
- [ ] Validate adapters with unit tests that assert `evaluate(resource)` returns expected normalized outputs.

## Rule registry actions
- [ ] Update all base template rules (`rule_specs/*/00_base_rule.yml`) to include `severity` and `remediation_hint` (UNBLOCK-G-02).
- [ ] Add at least one concrete, non-template rule per product so product rule sets are not template‑only.
- [ ] Run rule registry audit after changes and verify no template-only products remain (regenerate `ai_reports/rule_registry_audit.json`).

## Orchestration actions
- [ ] Ensure `ai_reports/phase3_execution_schedule.json` remains aligned with promoted schema and adapter changes.
- [ ] After schema promotions and base-rule completion, re-run readiness scans to update `ai_reports/phase3_activation_gate.json` and `ai_reports/phase3_readiness_gate.json`.
- [ ] Add CI jobs that automatically validate schema promotions and adapter tests on PRs.

## Cross‑pillar / Global actions
- [ ] Promote all templates (UNBLOCK-G-01) in a controlled order: prefer product-by-product PRs to reduce review scope.
- [ ] Implement canonical adapter layer and per-product adapters (UNBLOCK-G-03) and validate end-to-end with the pipeline executor.
- [ ] Complete base template rules across pillars by adding required metadata and concrete rules (UNBLOCK-G-02).
- [ ] Assign owners for orphan rule_specs and add promotion workflows (UNBLOCK-G-04).

## Blocking items summary
- [ ] Missing product-level schema files: `computeguard`, `computescan`, `pipelineguard`, `pipelinescan`, `vectorguard`, `vectorscan`.
- [ ] Template-only rule_registry entries lacking `severity` and `remediation_hint` across `vector`, `compute`, `pipeline` pillars.
- [ ] Missing per-product `evaluate(resource)` adapters (pipeline pillar is partial due to existing executor).
- [ ] Orphan `rule_specs/` directories require ownership decisions.

---
Follow the recommended execution flow in `ai_reports/phase3_activation_roadmap.json` and mark items complete as PRs land. After completing early items (schema promotions + adapter skeleton), re-run the readiness scan to verify gates transition from BLOCKED → PARTIAL → READY.
