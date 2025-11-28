# Phase‑4 Consolidated Pre‑Activation Briefing

Generated: 2025-11-27T14:10:00Z

This briefing condenses the Phase‑4 seed tasks (schema, rules, evaluator adapters) into an actionable, human‑readable plan. Sources: `phase4_seed_schema_tasks.json`, `phase4_seed_rule_tasks.json`, `phase4_seed_evaluator_tasks.json`.

## Executive summary

- Goal: Clear Phase‑3 blockers and enable Phase‑3 activation by promoting product schemas, converting template rules to concrete rules with required metadata, and implementing per‑product evaluator adapters that expose `evaluate(resource)`.
- Primary immediate work: promote per‑product schema templates (small PRs), add required rule metadata + one concrete rule per product, and implement the canonical adapter scaffolding and per‑product adapters.
- Readiness snapshot: Phase‑3 remains BLOCKED until the above tasks are completed and verified.

## Per‑product schema tasks (summary)

- computeguard
  - Template: `ai_reports/schema_templates/computeguard.schema.yml`
  - Target: `products/computeguard/schema.yml`
  - Required fields: `plan_id`, `schema_version`, `resources`, `metadata.source`, `metadata.ingested_at`
  - Validation: schema validation vs `guardsuite-core/canonical_schema.json`; include sample resource for smoke test

- computescan
  - Template: `ai_reports/schema_templates/computescan.schema.yml`
  - Target: `products/computescan/schema.yml` (same required fields & validation)

- pipelineguard
  - Template: `ai_reports/schema_templates/pipelineguard.schema.yml`
  - Target: `products/pipelineguard/schema.yml`
  - Validation: confirm mapping to pipeline executor input shape

- pipelinescan
  - Template: `ai_reports/schema_templates/pipelinescan.schema.yml`
  - Target: `products/pipelinescan/schema.yml`

- vectorguard
  - Template: `ai_reports/schema_templates/vectorguard.schema.yml`
  - Target: `products/vectorguard/schema.yml`

- vectorscan
  - Template: `ai_reports/schema_templates/vectorscan.schema.yml`
  - Target: `products/vectorscan/schema.yml`

Notes: Promote templates via small, single‑product PRs; run CI schema validation for each PR.

## Per‑product rule tasks (summary)

- For each product (computeguard, computescan, pipelineguard, pipelinescan, vectorguard, vectorscan):
  - Early: Update `rule_specs/<product>/00_base_rule.yml` to include `severity` and `remediation_hint` (and optional `created_by`, `last_reviewed`).
  - Mid: Add at least one concrete non‑template rule demonstrating remediation flow and linking to product schema fields.
  - Mid: Run rule registry audit and ensure no product remains template‑only. Regenerate `ai_reports/rule_registry_audit.json` after changes.

Global rule tasks:
- Apply consistent metadata schema across base templates (severity, remediation_hint, created_by, last_reviewed).
- Establish rule naming/discovery conventions and integrate registry audit into CI to prevent future template‑only rule PRs.

## Evaluator adapter tasks (summary)

- Canonical adapter (global / pipeline)
  - Create a minimal canonical adapter mapping `evaluate(resource)` -> `run_pipeline_on_text(text, rules, ...)` (module: `strategy_e/adapters/pipeline_adapter.py`).
  - Document input/output contract and normalize outputs to violations + remediation_hint.

- Per‑product adapters
  - Implement `strategy_e/adapters/<product>_adapter.py` for each product exposing `evaluate(resource)`.
  - Each adapter must validate input against the promoted product schema and return a structured violations list mapping to rule IDs and remediation hints.
  - Add unit tests: adapter should accept the sample resource from the product schema and produce expected structure.

- Binding requirements
  - Adapters must accept resources conforming to product schema and return violations referencing schema fields.
  - Document adapter API and include in a shared README and CI job.

## Global sequencing overview

Recommended deterministic sequence (derived from Phase‑3 unblock plan and roadmap):

1. UNBLOCK‑G‑01 — Promote all schema templates (early). Prefer product‑by‑product PRs.
2. Per‑product schema promotions (UNBLOCK‑*-01 / UNBLOCK‑*-02) as early tasks.
3. UNBLOCK‑P‑01 — Implement canonical adapter mapping (pipeline adapter) so adapter scaffolding exists.
4. Per‑product rule metadata updates (add severity + remediation_hint) and add one concrete rule (mid).
5. Implement per‑product adapters and unit/integration tests (mid → late).
6. UNBLOCK‑G‑02 / UNBLOCK‑G‑03 — Finalize rule registry and adapter validations in CI.
7. Governance tasks (UNBLOCK‑G‑04): assign owners and add PR promotion workflows.

Notes: This sequencing is dependency‑driven, calendar‑agnostic, and intended to minimize drift and PR review scope.

## Readiness & blockers snapshot

- Current readiness: BLOCKED (Phase‑3 gates: schema_gate, evaluator_gate, rule_registry_gate are BLOCKED or PARTIAL).
- Top blockers:
  - Missing product schema files for all mapped products
  - Template‑only rule registry entries lacking `severity` and `remediation_hint`
  - Missing per‑product `evaluate(resource)` adapters (pipeline pillar partial due to executor availability)
  - Orphan `rule_specs/` directories need ownership assignments

## Recommended immediate pilot

- Pick one product for pilot (suggestion: `computeguard` or `vectorguard`).
- Pilot steps (small PR flow):
  1. Promote the product schema from `ai_reports/schema_templates` → `products/<product>/schema.yml` and run CI schema validation.
  2. Update the product base rule (`00_base_rule.yml`) to include `severity` and `remediation_hint` and add one concrete rule.
  3. Implement adapter module `strategy_e/adapters/<product>_adapter.py` exposing `evaluate(resource)` and a unit test using the sample resource.
  4. Re-run Phase‑3 readiness scans and verify gate transitions.

---
End of briefing.
