# PILScanner Change Log — v3

## Summary of the v3 behavioral guarantees
- Implementation-first scoring: `progress_score` reflects code and test evidence only, and is insulated from compliance metadata.
- Compliance checks remain separate and cannot reduce `progress_score` (they affect `compliance_score` and downstream gated outputs).
- Missing or absent metadata is treated neutrally rather than punitive.

## Progress vs compliance separation
- `progress_score`: derived from implementation signals (code structure, tests, validators, pipeline stages, complexity/richness).
- `compliance_score`: derived from policy/spec coverage, declared gates, and state-transition expectations.
- Gates act as caps on compliance/combined outputs only; they do not lower `progress_score`.

## Neutral metadata model
- Unspecified metadata fields map to a neutral value (0.5) when used in scoring, preventing absent declarations from penalizing progress.
- Explicit zeros or failing validations remain punitive and affect `compliance_score` when declared.

## KPI discreteness rules
- Several KPIs are bucketized to canonical values (0.0, 0.5, 1.0) where policy consumers expect discrete bands (e.g., `IMPLEMENTATION_COMPLETENESS`).
- Continuous heuristics (complexity/richness) are computed then mapped into discrete KPI bands consistent with test expectations.

## Deterministic adapter behavior
- Adapter modules used during scanning expose deterministic `evaluate()` implementations to avoid import-time or runtime variability during test collection.
- A minimal fallback in `strategy_e.adapters.__init__` ensures adapter availability during test runs.

## Implementation-first scoring model
- Implementation signals (functions, classes, pipeline stages, adapters, validators, unit tests) are combined into an implementation-richness profile.
- `progress_score` aggregates structural completeness, implementation completeness, pipeline completeness, validator presence, and complexity/richness.
- `combined_score` and `final_score` are derived post compliance gating; `progress_score` is preserved regardless of compliance failures.

## Heuristic detection overview (pipeline, validators, complexity)
- Pipeline stages: detected by scanning for named stage functions/classes or pipeline adapter registration; strong implementation signals can satisfy expected pipeline presence.
- Validators: detected via test or validator artifacts; presence/absence influences validator KPIs but missing declared validators is neutral only if not explicitly required.
- Complexity → richness: LOC-only heuristics replaced with an implementation-richness heuristic combining function/class counts, module depth, pipeline/adapter/validator signals, and normalized weights.

## Test strategy outline (unit, heuristic, integration)
- Unit tests: focused tests for helper heuristics (bucketization, pipeline/validator subscores) live in `tests/test_heuristics.py`.
- Heuristic tests: fixture repos exercise real-world variants (see `tests/fixtures/caseA..caseE`) and assert progress/compliance outputs.
- Integration: full test suite runs exercise adapter fallbacks, scanner entrypoints, and end-to-end `repos_index.scan.json` production.

---
Notes: This changelog is intentionally concise — it documents behavioral guarantees and test strategy to help maintainers review changes without reading the full implementation.
**PILScanner v3 — Change Log and Developer Notes**

Summary of the v3 behavioral guarantees
- Progress scoring is implementation-first and deterministic: evidence derived from code, tests, and deterministic adapters drives `progress_score` independent of policy/compliance metadata.
- Compliance scoring is separate and does not reduce `progress_score`; gates apply as caps to compliance and to the final combined score only where explicitly configured.

Progress vs compliance separation
- `progress_score`: derived solely from implementation evidence (source files, functions/classes, pipeline stages, validators, tests).
- `compliance_score`: derived from declared metadata, spec coverage, gates, and policy checks.
- Final scores present both `progress_score` and `compliance_score` distinctly; gating or `done_contract` flags affect compliance and combined calculations but do not lower `progress_score`.

Neutral metadata model
- Missing or unknown metadata values are treated as neutral (midpoint) rather than negative. This prevents absent/partial metadata from penalizing implementation progress.

KPI discreteness rules
- Certain KPIs are bucketized into canonical values to improve determinism and testability (0.0, 0.5, 1.0) where tests require discrete thresholds (e.g., `IMPLEMENTATION_COMPLETENESS`).
- Continuous signals (e.g., complexity/richness) are computed then mapped to KPI bands for downstream aggregation.

Deterministic adapter behavior
- Adapters include minimal deterministic `evaluate()` implementations used during scanning and testing to avoid import-time failures and non-deterministic behavior.
- Adapters are lightweight and produce reproducible outputs (violations, counts, scores) to keep scanning deterministic during CI/test collection.

Implementation-first scoring model
- Implementation signals (functions, classes, pipeline stages, validators, adapters, tests) are aggregated into an implementation-richness heuristic and a set of canonical KPIs.
- `progress_score` weights these implementation KPIs and is designed to reward evidence of working implementation even when metadata is sparse.

Heuristic detection overview (pipeline, validators, complexity)
- Pipeline stages: inferred from explicit stage declarations and from implementation signals (modules named/annotated as stages, pipeline adapter usage, function/class patterns).
- Validators: detected by presence of validator modules/tests or adapter evaluation harnesses. When validation artifacts are declared but not found, validator KPIs are penalized; if not declared, they are neutral.
- Complexity -> Richness: replaces LOC-only heuristics. Combines multiple signals (module depth, functions/classes per module, presence of adapters/validators/pipeline stages) into a normalized richness score.

Test strategy outline (unit, heuristic, integration)
- Unit tests: focused tests for helper heuristics (bucketization, pipeline completeness, validator scoring) live in `tests/test_heuristics.py`.
- Heuristic tests: fixture repos under `tests/fixtures/` exercise real-world-like scenarios; `tests/test_real_world_progress_cases.py` asserts progress/compliance separation and expected numeric thresholds.
- Integration: full test-suite runs exercise adapter determinism, scanner end-to-end behavior, and ensure the scan JSON contains `progress_score`, `compliance_score`, `combined_score`, and diagnostics.

Notes
- This changelog is intentionally concise; reviewers should inspect `repo-scanner.py` for the implementation details of the heuristics and the deterministic adapter implementations in `strategy_e/adapters/`.

---
Generated: concise developer note for PILScanner v3
