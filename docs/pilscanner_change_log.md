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
