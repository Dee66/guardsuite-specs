# Initial Design Outline

## Phase 3 – Detailed Design Expansion

Scaffolding goals for Strategy-E
- Provide rule-spec templates that are machine-readable and human-reviewable.
- Produce deterministic, idempotent normalizers that do not delete user content.
- Generate safe, versioned diff bundles and backups for every apply operation.

Cross-product invariants inherited from Strategy-D
- Canonical output schema must be preserved across products.
- Deterministic ordering for rules, issues, and output (alphabetical or explicit order).
- Non-destructive transformations: unknown fields moved to `x_legacy` rather than removed.
- No use of network, subprocesses, or non-deterministic sources (no randomness, no timestamps except latency measurements).

Required rule-engine interfaces for `repair_runner`
- `load_rules(rule_dir: str) -> list[RuleMeta]`: deterministic, sorted discovery of rule specs/modules.
- `apply_rules(text: str, rules: list, file_type: str) -> str`: apply only matching rules and return normalized text.
- Rule module contract: a pure function such as `normalize(text: str) -> str` for text-based rules; for structured data, `normalize_dict(data: dict) -> dict`.
- Rule metadata (id, name, severity, inputs, outputs) must be discoverable without executing side effects.
- Rules must declare applicable file types/extensions and an explicit canonical order when needed.

Deterministic testing requirements
- All tests must use stable fixtures and avoid time-dependent assertions.
- Test fixtures must be deterministic and stored under `tests/fixtures/` with stable ordering.
- Snapshot tests must be updated only with explicit intention and recorded in `ai_snapshots/`.
- Use dry-run modes in tests to ensure no product data is modified.

Expected CLI workflows for Phase 3
- `repair_runner scan <path> --dry-run [--rules-dir]` — produce unified diffs and a canonical JSON report.
- `repair_runner apply <path> --rules-dir [--backup-dir]` — make deterministic, reversible edits and emit a diff bundle.
- `repair_runner rules list` — enumerate available rules, their types, and declared order.
- All CLI operations support `--json`, `--quiet`, and stable `--output` formats.

