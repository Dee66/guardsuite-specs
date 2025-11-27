# Phase‑4 Activation Outline

Generated: 2025-11-27T14:05:00Z

This outline summarizes Phase‑4 preparatory work (schema, rules, evaluators) derived from Phase‑3 outputs. Files: `ai_reports/phase4_seed_schema_tasks.json`, `ai_reports/phase4_seed_rule_tasks.json`, `ai_reports/phase4_seed_evaluator_tasks.json`.

## Roadmap summary

- Phase‑4 goal: Clear Phase‑3 blockers by promoting product schemas, converting template rules to concrete rules, and implementing evaluator adapters so product-level `evaluate(resource)` contracts are satisfied.
- High-level flow: Schema promotions (early) → Rule metadata + concrete rules (mid) → Adapter implementation & tests (mid→late) → CI and governance polish (late).

## Ordered task groups

1. Schema group (early)
   - Promote each `ai_reports/schema_templates/<product>.schema.yml` → `products/<product>/schema.yml` as a small PR.
   - Populate canonical fields: `plan_id`, `schema_version`, `resources`, `metadata.source`, `metadata.ingested_at`.
   - Add sample resource examples for smoke testing.

2. Rule group (early → mid)
   - Update `rule_specs/*/00_base_rule.yml` to include `severity` and `remediation_hint`.
   - Add at least one concrete rule per product demonstrating remediation flow.
   - Run rule registry audit and iterate until no template-only rule sets remain.

3. Adapter (evaluator) group (early → mid)
   - Implement canonical adapter scaffolding mapping `evaluate(resource)` → `run_pipeline_on_text(...)`.
   - Create per-product adapter modules exposing `evaluate(resource)` that validate input against promoted schema and call the adapter scaffolding.
   - Add unit and integration tests validating adapter behavior against sample resources.

4. Orchestration & Governance (mid → late)
   - Add CI jobs to validate schemas and run adapter tests on PRs.
   - Assign product owners to orphan `rule_specs/` directories and enforce PR review flows.

## Highlights of pre‑activation requirements

- Promote templates in single-product PRs to minimize review scope and drift risk.
- Ensure CI validates promoted schemas against `guardsuite-core/canonical_schema.json`.
- Keep adapter modules small and well-tested; prefer thin wrappers that call the canonical executor.

## Suggested pilot plan

- Choose one product as pilot (recommended: `computeguard` or `vectorguard`).
- Steps for pilot:
  1. Promote product schema from `ai_reports/schema_templates` to `products/<product>/schema.yml`.
  2. Update the product base rule (`00_base_rule.yml`) to include `severity` and `remediation_hint` and add one concrete rule.
  3. Implement adapter module `strategy_e/adapters/<product>_adapter.py` exposing `evaluate(resource)` and a unit test against sample resource.
  4. Open PRs in small increments: schema PR, rule PR, adapter PR.
  5. Re-run Phase‑3 readiness scan and confirm gate transitions.

## Notes

- All tasks in this outline are preparatory; actual code changes to `products/`, `rule_specs/`, and `strategy_e/` require edits outside `ai_reports/` and should be performed via reviewed PRs.
- Use the Phase‑3 roadmap and unblock plan as the authoritative ordering for sequencing UNBLOCK-* actions.
