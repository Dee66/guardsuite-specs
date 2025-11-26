# Strategy-E Phase 3 — Detailed Design Plan

## Goal
Expand Phase-3 design into full actionable tasks for Copilot automation,
focusing on deterministic repairs, cross-product normalization, and
integration with repair_runner.

## Required Components
- Normalization rule specification format
- Deterministic execution order rules
- Error-tolerant YAML loader behavior
- CLI entrypoints for dry-run and apply modes
- Diff generation contract
- Logging and audit requirements
- Test coverage expectations

## Outputs Expected
- rule_specs/<product>/<rule>.yml
- repair_runner integration notes
- auto-generated diff bundles
- deterministic test fixtures

## Constraints
- No changes to product metadata/checklists until Phase-4
- No use of PYTHONPATH
- LF line endings required

## Next Steps
Phase 4 will convert this design into scaffolding definitions
and rule-spec templates.

