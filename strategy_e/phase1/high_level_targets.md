# High Level Targets

## Phase 3 – Detailed Design Expansion

Scaffolding goals for Strategy-E
- Define reusable rule-spec formats that cover YAML, JSON, and Markdown normalization.
- Provide rule validation tooling that verifies determinism and idempotence.
- Implement a lightweight rule registry that enforces ordering and prevents duplicates.

Cross-product invariants inherited from Strategy-D
- Stable canonical schema versions must be recorded in outputs.
- Issues and remediation hints must follow the canonical schema required fields.
- Fixpack hints must follow `fixpack:<ISSUE_ID>` naming and loader conventions.

Required rule-engine interfaces for `repair_runner`
- Discovery API: deterministic listing and metadata extraction without code execution.
- Execution API: safe, sandboxed (no IO) calls to normalization functions.
- Reporting API: produce diffs and attach rule provenance metadata.

Deterministic testing requirements
- Tests must assert sorted outputs (sort by severity then id when applicable).
- Use fixture-based integration tests under `tests/integration/strategy_e/`.
- Automated checks to ensure no product metadata files are modified during Phase 3 runs.

Expected CLI workflows for Phase 3
- Dry-run first: show diffs and write a canonical JSON report including `latency_ms`.
- Review and approve: `repair_runner review <report.json>` to inspect and stage apply operations.
- Apply with backup: `repair_runner apply --report <report.json> --backup-dir <dir>`.

