<!-- Generated from products/computeguard/checklist/checklist.yml -->
<!-- LF line endings are used -->

<!-- Overall progress bar (colour) -->
<div role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="94" style="width:100%; background:#e6eef0; border-radius:8px; padding:6px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.04);">
  <div style="width:94.0%; background:linear-gradient(90deg,#4caf50,#2e7d32); color:#fff; padding:10px 12px; text-align:right; border-radius:6px; font-weight:700; transition:width 0.5s ease;">
    <span style="display:inline-block; background:rgba(0,0,0,0.12); padding:4px 8px; border-radius:999px; font-size:0.95em;">94.0% Complete</span>
  </div>
</div>

# ComputeGuard Checklist (converted from checklist.yml)

> Checklist version: 2025.11 - last updated: 2025-11-25T00:00:00Z
>
> Owner: GuardSuite Platform Team
>
> Stability: GA
>
---

## Phase: initialization
*Summary:* Prepare repo, validate initial structure, and ensure toolchain readiness.

- [ ] INIT-001: Ensure poetry install succeeds with no flags.
- [ ] INIT-002: Verify presence of required directory layout: `src/`, `schemas/`, `fixpack/`, `catalog/`, `examples/rules/`, `tests/`, `docs/`.
- [ ] INIT-003: Validate example rule bundle directory: `examples/rules/*` exists and contains at least one example file.
- [ ] INIT-004: Validate existence of catalog directory and index file `catalog/index.yml`.
- [ ] INIT-005: Validate presence of at least 3 example fixpacks under `catalog/`.
- [ ] INIT-006: Ensure all schema files declared in spec exist under `/schemas`.
- [ ] INIT-007: Run schema validator to ensure all YAML/JSON schemas are syntactically valid.
- [ ] INIT-008: Verify presence of dev-shim for guardsuite-core (issue model + serializer stubs).
- [ ] INIT-009: Ensure sample dataset exists for snapshot and perf tests (`tests/data`).
- [ ] INIT-010: Validate `spec.yml` and `checklist.yml` conform to guard-specs schema.

## Phase: directory_conventions
*Summary:* Confirm structure, naming, and required resource layout.

- [ ] DIR-001: Enforce required folder structure and naming conventions exactly as in spec.
- [ ] DIR-002: Validate schema directory: `/schemas/*.yml` and `*.json` follow naming rules.
- [ ] DIR-003: Validate fixpack directory: `fixpack/compute` contains only template-defined content.
- [ ] DIR-004: Validate catalog directory structure and file extensions.
- [ ] DIR-005: Validate `examples/rules` bundle directory and file naming.

## Phase: evaluator_implementation
*Summary:* Implement evaluator pipeline using template-provided orchestration and pillar-specific rule bundles.

- [ ] EVAL-001: Integrate pillar rule bundles into evaluator pipeline.
- [ ] EVAL-002: Implement compute-specific transformations and metadata enrichment.
- [ ] EVAL-003: Ensure evaluator output conforms to `/schemas/evaluator_output_schema.yml`.
- [ ] EVAL-004: Register all rule categories defined in spec.
- [ ] EVAL-005: Enforce deterministic sorting of results by severity then rule_id.
- [ ] EVAL-006: Ensure evaluator uses canonical serializer from dev-shim or core when available.
- [ ] EVAL-007: Add evaluator-level resource metrics (checks_executed_total, plan_size, etc.).
- [ ] EVAL-008: Implement environment normalization hook before output serialization.

## Phase: rule_bundle
*Summary:* Create and verify ComputeGuard rule bundles.

- [ ] RULE-001: Implement example rule bundle in `examples/rules/`.
- [ ] RULE-002: Ensure example bundle emits at least 4 severities (critical, high, medium, low).
- [ ] RULE-003: Validate rule IDs follow canonical naming pattern.
- [ ] RULE-004: Confirm example rules align with example fixpacks.
- [ ] RULE-005: Ensure rule metadata (severity, category, title, description) matches schema.

## Phase: fixpack_system
*Summary:* Implement FixPack-Lite system with normalized previews and deterministic outputs.

- [ ] FP-001: Implement fixpack catalog loader using template fixpack loader.
- [ ] FP-002: Create >=3 example fixpacks under `catalog/` with valid metadata.
- [ ] FP-003: Ensure fixpack references valid rule IDs from example rule bundle.
- [ ] FP-004: Implement `snippet_count` requirement (>=10 remediation snippets).
- [ ] FP-005: Implement preview engine (dry-run, normalized).
- [ ] FP-006: Normalize preview diffs for snapshot safety (strip paths, timestamps).
- [ ] FP-007: Implement fixpack hint exposure for GuardBoard.

## Phase: compliance_ledger
*Summary:* Implement audit-grade FinOps ledger system based on schema.

- [ ] LEDGER-001: Implement compliance ledger generator.
- [ ] LEDGER-002: Ensure ledger conforms to `/schemas/compliance_ledger_schema.yml`.
- [ ] LEDGER-003: Ensure ledger items include required fields: `timestamp_utc`, `product_id`, `rule_id`, `severity`, `fixpack_ref`, `applied_flag`, `notes`.
- [ ] LEDGER-004: Implement deterministic ledger ordering (rule_id asc).
- [ ] LEDGER-005: Expose ledger for GuardBoard consumption via CLI.

## Phase: cli
*Summary:* Implement ComputeGuard CLI with full contract compliance.

- [ ] CLI-001: Implement base command `computeguard`.
- [ ] CLI-002: Implement scan command `computeguard scan`.
- [ ] CLI-003: Add support for flags listed in spec (`json`, `stdin`, `quiet`, `explain`, etc.).
- [ ] CLI-004: Implement reserved flags (`--ledger-only`, `--fixpack-diff`) with stubs or restrictions.
- [ ] CLI-005: Ensure `--json` output conforms to `/schemas/cli_output.json`.
- [ ] CLI-006: Ensure error payloads conform to `/schemas/cli_error.json`.
- [ ] CLI-007: Implement strict-mode exit code policy.
- [ ] CLI-008: Ensure explain mode supports both human and machine-readable output.
- [ ] CLI-009: Validate CLI help output lists all verbs/flags in canonical order.
- [ ] CLI-010: Implement fixpack-summary and compliance-ledger flags.

## Phase: integrations
*Summary:* Integrate ComputeGuard with GuardScore, GuardBoard, Playground.

- [ ] INT-001: Expose GuardScore input metrics as per spec.
- [ ] INT-002: Validate GuardBoard fixpack hints integration contract.
- [ ] INT-003: Validate that Compliance Ledger artifacts are consumable by GuardBoard.
- [ ] INT-004: Ensure WASM-safe execution for Playground (json/svg sanitization).
- [ ] INT-005: Validate quick-score mode behavior.

## Phase: determinism_and_normalization
*Summary:* Enforce cross-machine deterministic behavior.

- [ ] DET-001: Implement canonical key ordering and lexicographic result sorting.
- [ ] DET-002: Strip absolute paths from all outputs.
- [ ] DET-003: Normalize path separators for cross-OS compatibility.
- [ ] DET-004: Remove platform-specific metadata (python version, OS).
- [ ] DET-005: Ensure snapshot tests produce identical output across 3 runs.
- [ ] DET-006: Validate deterministic fixpack previews across 3 runs.
- [ ] DET-007: Ensure ledger artifacts are deterministic.

## Phase: performance
*Summary:* Validate product performance under expected constraints.

- [ ] PERF-001: Ensure max memory usage <= 260 MB.
- [ ] PERF-002: Ensure typical runtime <= 850 ms on representative dataset.
- [ ] PERF-003: Ensure large plan runtime <= 2000 ms.
- [ ] PERF-004: Validate Playground runtime <= 2100 ms.
- [ ] PERF-005: Implement CI perf regression tests.

## Phase: security
*Summary:* Implement sandboxing, safe errors, sanitization.

- [ ] SEC-001: Remove secrets from product code (use placeholders only).
- [ ] SEC-002: Sanitize all user inputs (JSON, CLI).
- [ ] SEC-003: Sanitize SVG outputs for GuardBoard/Playground.
- [ ] SEC-004: Implement WASM sandbox contract for Playground.
- [ ] SEC-005: Ensure safe error reporting (no stack-leaks, no paths).

## Phase: testing
*Summary:* Complete unit, integration, snapshot, and schema testing.

- [ ] TEST-001: Achieve >=85% unit test coverage.
- [ ] TEST-002: Implement integration tests covering evaluator, fixpack, CLI.
- [ ] TEST-003: Run snapshot tests using normalization rules.
- [ ] TEST-004: Ensure snapshot tests pass on multiple CI images.
- [ ] TEST-005: Ensure schema validation tests exist for all schemas.
- [ ] TEST-006: Add example rule-bundle severity coverage test.
- [ ] TEST-007: Test CLI help output formatting and semantics.
- [ ] TEST-008: Add test preventing forbidden overrides.

## Phase: ci_cd
*Summary:* Configure CI contract and quality gates.

- [ ] CI-001: Ensure CI runs: validate_schema, unit, integration, snapshot_conformance, perf_regression.
- [ ] CI-002: Add forbidden override enforcement test to CI.
- [ ] CI-003: Add schema drift detection.
- [ ] CI-004: Add spec/checklist alignment validation.
- [ ] CI-005: Ensure CI uses dev-shim until guardsuite-core is released.

## Phase: documentation
*Summary:* Produce developer docs, architecture notes, API docs, ledger guides.

- [ ] DOC-001: Document evaluator architecture and extension points.
- [ ] DOC-002: Document fixpack system and snippet schema.
- [ ] DOC-003: Document compliance ledger schema and consumption.
- [ ] DOC-004: Document CLI contract and usage examples.
- [ ] DOC-005: Document determinism rules and snapshot process.
- [ ] DOC-006: Document integration surfaces for GuardScore and GuardBoard.
- [ ] DOC-007: Document migration paths and versioning.

## Phase: acceptance
*Summary:* Acceptance checks before release.

- [ ] ACC-001: Evaluator output MUST validate against evaluator schema.
- [ ] ACC-002: CLI output MUST validate against cli_output.json.
- [ ] ACC-003: Fixpack preview MUST be deterministic across 3 runs.
- [ ] ACC-004: Compliance ledger MUST validate schema.
 - [x] ACC-005: All unit, integration, snapshot tests MUST pass.
 - [ ] ACC-006: Performance thresholds MUST be met.
- [ ] ACC-007: Forbidden overrides MUST not exist.
- [ ] ACC-008: Developer docs MUST be complete and accurate.
- [ ] ACC-009: Checklist MUST be fully complete.

---

*Generated from `checklist.yml` — convert to Markdown with checkboxes for manual checking in PRs or local edits.*
