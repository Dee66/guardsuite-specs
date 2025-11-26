# Strategy-E Phase 3 — Implementation Plan

Generated: 2025-11-26T07:35:40+00:00 (deterministic scaffold)

## Purpose

Translate Strategy-D outputs (validation reports, diffs, `x_legacy` candidates, and diagnostics) into a prioritized, timeboxed implementation plan to safely operationalize repairs and review cycles.

## Scope

- Implement deterministic, idempotent repair runners and verification tests.
- Create manual-review checkpoints for `x_legacy` payloads and high-risk edits.
- Add CI checks and a lightweight staging workflow for proposed metadata edits.

Out of scope: merging changes to product metadata without explicit human approval; large UX work; infra changes outside repository.

## Assumptions

- Work follows repository invariants: no PYTHONPATH changes, no deletions of user content (move to `x_legacy` instead), deterministic ordering.
- Phase-2 artifacts and Strategy-D diffs are the canonical source for repair targets.

## Roles (placeholders — replace with real owners)

- Product Lead: `@product-owner`
- Engineering Lead: `@eng-lead`
- Implementation Engineer: `@engineer`
- Reviewer / QA: `@reviewer`
- Security/Policy Reviewer: `@security`

## Deliverables

1. `workspace/strategy_e/phase3/tasks.md` (this file)
2. `tools/repair_runner.py` — deterministic repair runner (idempotent)
3. `tests/` unit + integration tests for repairs
4. CI job `ci/repair_verify.yml` to run validators and tests on repair branches
5. `workspace/strategy_e/phase3/review_checklist.md` — human review checklist for `x_legacy`

## Milestones & Tasks

Milestone A — Analysis & Prioritization (1 week)
- A.1: Review Strategy-D Phase 11 & 13 reports and collect actionable items. Owner: `@engineer`. Effort: 2d. Acceptance: prioritized list in `workspace/strategy_e/phase3/analysis/prioritized_items.md`.
- A.2: Compile full `x_legacy` inventory and tag each item with severity + rationale. Owner: `@engineer`. Effort: 2d. Acceptance: `workspace/strategy_d/x_legacy_inventory.yml` exists and each entry has `severity` and `notes`.

Milestone B — Design & Safety Controls (1 week)
- B.1: Design the repair runner signature (`repair(plan_path) -> list[Issue]`) consistent with repository evaluator contracts. Owner: `@eng-lead`. Effort: 2d. Acceptance: design doc `workspace/strategy_e/phase3/design/repair_runner_spec.md` reviewed by `@product-owner`.
- B.2: Define safety rules (no delete; move to `x_legacy`; always produce diffs; deterministic order). Owner: `@security`. Effort: 1d. Acceptance: `repair_runner_spec.md` contains safety rules and examples.

Milestone C — Implementation (2 weeks)
- C.1: Implement `tools/repair_runner.py` (idempotent, dry-run, apply modes). Owner: `@engineer`. Effort: 5d. Acceptance: `tools/repair_runner.py --dry-run` produces deterministic diffs matching existing `workspace/strategy_d/diffs/` for test inputs.
- C.2: Implement automated writer to create diffs under `workspace/strategy_d/diffs/` and backup originals to `workspace/strategy_d/backups/`. Owner: `@engineer`. Effort: 3d. Acceptance: backups and diffs created for sample inputs.

Milestone D — Tests & CI (1 week)
- D.1: Add unit tests for individual repair rules. Owner: `@engineer`. Effort: 3d. Acceptance: tests pass locally and in CI.
- D.2: Add integration test that runs the full pipeline on a minimal fixture (use `tests/fixtures/minimal_plan.json`). Owner: `@engineer`. Effort: 2d. Acceptance: integration test passes and produces expected diffs.
- D.3: Add CI job `ci/repair_verify.yml` to run the runner in `--dry-run` and validate outputs. Owner: `@eng-lead`. Effort: 1d. Acceptance: CI job exists and is green on the repair branch.

Milestone E — Human Review Workflow & Handoff (3 days)
- E.1: Create `workspace/strategy_e/phase3/review_checklist.md` with review steps for `x_legacy` and high-severity changes. Owner: `@product-owner`. Effort: 1d. Acceptance: checklist reviewed by `@reviewer`.
- E.2: Define PR template and branch naming convention for repair PRs. Owner: `@eng-lead`. Effort: 1d. Acceptance: `.github/PULL_REQUEST_TEMPLATE/repair_pr.md` added.

Milestone F — Pilot & Rollout (1 week)
- F.1: Run pilot on a small set of low-risk items from prioritized list. Owner: `@engineer`. Effort: 3d. Acceptance: pilot diffs created, reviewed, and merged by humans.
- F.2: Collect feedback and tune repair rules. Owner: `@product-owner`. Effort: 2d. Acceptance: updated rules and tests.

## Acceptance Criteria (phase-level)

- All repairs are idempotent and reversible (backups + diffs present).
- No user content deleted; unexpected keys are moved to `x_legacy` with explanatory notes.
- Deterministic output ordering for all generated files.
- Tests and CI ensure no regressions; security review completed for high-risk rules.

## Risks & Mitigations

- Risk: Over-aggressive repairs may change intended metadata. Mitigation: run in `--dry-run` by default, require human signoff for apply.
- Risk: Merge conflicts. Mitigation: small atomic commits and PRs; prefer human review on larger changes.

## Communication & Timeline

- Weekly syncs during implementation (Engineering + Product). Owner: `@product-owner`.
- Estimated elapsed time to MVP: 5 weeks (Analysis 1w, Design 1w, Implementation & Tests 3w, Pilot 1w) — parallelize where possible.

## Next immediate steps (today)

1. Assign owners to top 5 prioritized items from Strategy-D Phase 11. (Owner: `@product-owner`)
2. Create an issue tracker board entry for Phase 3 and add tasks above. (Owner: `@eng-lead`)
3. Begin implementing `tools/repair_runner.py` in a feature branch. (Owner: `@engineer`)

---

If you want, I can now create the feature branch and scaffold `tools/repair_runner.py` with a minimal dry-run entrypoint and tests. Proceed? (yes/no)
