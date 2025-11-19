# GuardSuite Template — Copilot Instructions

## Orientation
- Template for new GuardSuite pillars; most work happens under `src/pillar/**` with CLI + engine + renderer layers
- CLI entry (`src/pillar/cli.py`) wires loader → evaluator → renderer; always preserve deterministic stdout/json and latency accounting
- SCAN metadata constants live in `src/pillar/engine/evaluator.py`; update `PILLAR_PLACEHOLDER`, `SCAN_VERSION`, `GUARDSCORE_RULES_VERSION` when cloning for a real pillar

## Architecture & Data Flow
- Loader (`src/pillar/engine/loader.py`) accepts either a file path or stdin; enforce `MAX_PLAN_BYTES`/`MAX_PLAN_RESOURCES`, set `_oversize` flags, and never perform network I/O
- Evaluator composes pure rule helpers returning dicts shaped like `tests/snapshots/test_schema_snapshot.py` expects; use `remediation_for_issue` to generate deterministic `fixpack:<ISSUE>` hints and keep rule functions side-effect free
- Renderer (`src/pillar/renderer.py`) formats deterministic text output by sorting issues via severity/id; sanitize/strip user-controlled strings before concatenation
- Schema contracts live in `src/pillar/schema.py`; keep outputs aligned so snapshots and downstream consumers stay green
- Fixpack snippets (`fixpack/*.hcl`) must be named after issue IDs with HCL comment headers describing metadata

## Implementation Patterns
- Prefer small, isolated rule evaluators returning `Issue` dataclasses so `_severity_totals` continues to derive counts automatically
- Set `quick_score_mode` when `_oversize` is present or resource count exceeds `MAX_PLAN_RESOURCES`; `guardscore_badge` should disable eligibility in quick mode
- Always fill `environment` via `_infer_environment` to keep provider-stage inference consistent; add new keys there instead of per-rule logic
- When adding CLI options, update both `tests/unit/test_cli.py` and README usage so scaffolding instructions remain accurate

## Developer Workflow
- Use Poetry via Makefile targets: `make install` (installs poetry + deps), `make test` (`pytest -v`), `make lint` (`ruff` + `black --check`), `make format` to autofix
- Quick CLI check: `make run-example` runs `pillar.cli scan tests/fixtures/minimal_plan.json`
- Long-running or manual CLI runs should prefer `poetry run python -m pillar.cli scan --stdin < plan.json` to reuse the virtualenv
- To scaffold a new pillar, run `python scripts/scaffold_new_pillar.py <pillar_name>` from repo root; it copies the template and rewrites placeholder tokens

## Testing Guidance
- Unit coverage focuses on CLI flags (`tests/unit/test_cli.py`); extend when adding new user-facing toggles
- Integration tests (`tests/integration/test_playground_flow.py`) expect loader/evaluator parity with fixtures—keep fixture helpers in `tests/shared/loader.py` in sync
- Schema regression lives in `tests/snapshots/test_schema_snapshot.py`; update snapshots only after verifying canonical schema deltas with platform owners
- Add fixture JSON under `tests/fixtures/` and reference via shared loader to avoid duplicated path math

## Conventions & Gotchas
- Never make network calls or mutate global state inside rules; determinism and reproducibility are top-level architecture principles
- Latency is measured in `cli.scan`—rule code must remain pure so total wall time stays dominated by parsing
- Renderer output is the only text mode; JSON mode should always be raw `evaluate_plan` output (plus latency) without additional formatting
- Keep remediation hints synchronized with `fixpack/` filenames; callers look for `fixpack:<ISSUE>` markers when stitching HCL snippets
- If you change schema keys or constants, ripple updates into `README.md`, fixtures, and any scaffolding defaults so downstream teams inherit the new contract
