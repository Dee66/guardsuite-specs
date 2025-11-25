# CLI Demo Flow — Strategy-D Phase 3

Defines how the CLI should behave when running in "demo mode"
once real demo content is introduced.

## High-Level Workflow
1. Load demo_version.yml
2. Load selected plan (plan_bad or plan_guard)
3. Run CLI in deterministic mode
4. Capture output
5. Compute and compare output hash
6. Emit reproducible JSON

## Deterministic Requirements
- No timestamps without normalization
- No unordered map serialization
- Same hash across all platforms
- Identical stdout/stderr formatting

**Note:**  
No CLI implementation occurs in Phase 3 — this is a planning document.
