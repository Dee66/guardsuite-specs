# AI Input Contract

This document describes the exact payload shape expected by the AI analysis step that consumes the master `repos_index` produced by `aggregate_all_repos`.

Top-level object: `repos_index` (mapping)

- repo_name: {
  - repo_path: string (absolute path)
  - tasks: mapping task_id -> { final_score: int, status: "done"|"pending" }
  - scoring: mapping task_id -> detailed scoring object (see `repo-scanner.py` output)
  - deltas: { changed: [files], missing: [files], unchanged: [files], details: { file: { previous, current } } }
  - dependencies: mapping task_id -> { ok: bool, details: { dep_id: { found, status, repo, satisfied } } }
  - progress_history_values: [float]  # historical average final scores for this repo
  - progress_history: string       # sparkline representation of `progress_history_values`
}

Notes:
- All numeric scores are in the range 0..100 and are deterministic.
- `scoring` objects include `metrics`, `pre_gate_score`, `post_gate_score`, `final_score`, and `details` entries.
- The AI consumer MUST NOT assume any missing fields and should validate the presence and types of required keys.

Do Not Guess rule:
- The AI must not invent facts; if required evidence is missing, report `missing_evidence` entries with explicit file paths and checks that failed.

Confidence guidance:
- Use `progress_history_values` and `ambiguity_flags` (from task metadata) to calibrate confidence. Historical volatility should lower confidence.
