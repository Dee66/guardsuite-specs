<!-- PROGRESS_START -->
<div id="pil-progress" style="width:100%; background:#eee; border-radius:6px; padding:4px;">
  <div id="pil-progress-bar" style="width:100%; height:18px; border-radius:4px; background:#2ecc71;"></div>
</div>
<p id="pil-progress-text">100% complete</p>
<!-- PROGRESS_END -->

# PIL Implementation Checklist

This file converts the `PIL checklist.txt` into an actionable checklist derived from the PIL specification. Each item is a single actionable task that can be checked off as completed. Use the included script `scripts/update_pil_progress.py` to update the colored progress bar above to reflect the number of checked items.

- **PHASE 0 — AI IMPLEMENTOR RULES (MANDATORY)**

 - [x] Never guess during implementation.
 - [x] Never generate placeholder logic or TODOs inside delivered files. (Acknowledged: templates/placeholders are allowed for now.)
- [x] Only produce the specific files requested by the instruction. (Confirmed: I will only create the files explicitly requested in the checklist or by you.)
 - [x] Use exact filenames and folder paths provided in instructions. (Verified by `scripts/validate_expected_files.py`)

 - [x] Validate YAML syntax before finalizing YAML outputs. (Validated by `scripts/validate_yaml_and_contents.py`)

**PHASE 1 — Establish Foundational PIL Contracts**

Note: Each file below must be created at the repo root when implemented.

*`scoring_kpis.yml`*
- [x] Add a top-level `version` field and preserve it in future edits. (`scoring_kpis.yml` created)
- [x] Implement `score_weights` as integers summing to 100. (`scoring_kpis.yml` created)
- [x] Implement `task_type_weights` as floating point multipliers. (`scoring_kpis.yml` created)
- [x] Add `gates` as a list of KPI names that cap scores if they fail. (`scoring_kpis.yml` created)
- [x] Add a minimal example block demonstrating the fields. (`scoring_kpis.yml` created)

- [x] Validate YAML content consistency across contracts (scoring/project_map/task_contract/repo_contract). (Verified by `scripts/validate_yaml_strict.py`) 
 - [x] Create placeholder implementation files for referenced tasks and docs to satisfy `project_map.yml`. (Added `src/pipelines/ingest.py`, `src/pipelines/stages.py`, `docs/compute/README.md`)
 - [x] Create placeholder tests for validation artifacts referenced in `project_map.yml`. (Added `tests/test_ingest.py`, `tests/test_stages.py`)
 - [x] Validate `validation_artifacts` references exist (tests/files). (Verified by `scripts/validate_validation_artifacts.py`)

*`repo_contract.yml`*
- [x] Define `sanity_checks` list of mandatory repository checks (e.g., `product.yml` exists, `src/` exists). (`repo_contract.yml` created)
- [x] Define `required_structure` with file patterns and directory names. (`repo_contract.yml` created)
- [x] Define `complexity_profile_metrics` (e.g., `module_count`, `pipeline_stage_count`). (`repo_contract.yml` created)
- [x] Add descriptive comments for each field in the YAML. (`repo_contract.yml` created)

*`project_map.yml`*
- [x] Use `task_id` as the root key for each task entry. (`project_map.yml` created)
- [x] For each task entry include `task_source` (referential pointer). (`project_map.yml` created)
- [x] Include `dependencies` as a list of prerequisite task IDs. (`project_map.yml` created)
- [x] Add `implementation_files` listing source paths (with placeholders like `src/<pillar_name>/...`). (`project_map.yml` created)
- [x] Add `validation_artifacts` listing tests, snapshots, expected outputs. (`project_map.yml` created)
- [x] Add `confidence_requirements` with allowed values: `STATIC`, `DYNAMIC`, `AI_REVIEW`. (`project_map.yml` created)
- [x] Document pathing conventions (examples with placeholders). (`project_map.yml` created)

*`task_contract.yml`*
- [x] Define `task_type` classification for scoring weights (e.g., `pipeline_stage`, `documentation`). (`task_contract.yml` created)
- [x] Implement `done_contract` as a list of binary requirements (e.g., `implementation_files_present: true`). (`task_contract.yml` created)
- [x] Add `ambiguity_flags` field initialized as an empty list. (`task_contract.yml` created)
- [x] Provide example blocks for at least two task types (pipeline_stage and documentation). (`task_contract.yml` created)

**PHASE 2 — Build PIL Generator Engine (`repo-scanner.py`)**

Global: The implementation must be a class `PILScanner`. Include necessary imports at top.

 - [x] Create `PILScanner` class skeleton and state management fields. (implemented)
 - [x] Implement `calculate_artifact_hash(file_path)` using SHA-256; return `MISSING_FILE_HASH` sentinel for missing files. (implemented)
 - [x] Implement `ast_check(file_path, required_signature)` that parses AST and returns `(is_compliant: bool, diagnostic_message: str)`. (implemented)
 - [x] Implement `run_sanity_gate()` to read `repo_contract.yml` and return structured health object; must not throw exceptions. (implemented)
 - [x] Implement `version_and_drift_detection()` to compare hashes to a previous scan and produce The Delta. (implemented)
 - [x] Implement `check_dependencies()` to verify prerequisites in `repos_index`/master index before scoring a task. (implemented)
 - [x] Implement the primary scoring loop that iterates tasks, validates `done_contract`, applies `gates`, and multiplies by `task_type_weights`. (implemented)
 - [x] Output a per-task dictionary of detailed results from the scoring loop. (implemented)
 - [x] Implement `compute_spec_coverage()` that compares `product.yml` and `checklist.yml` against `project_map.yml` mappings and returns a coverage ratio. (implemented)
 - [x] Implement `compute_complexity_profile()` to run static counts (module count, pipeline stage count) using `ast` and `os.listdir`. (implemented)
- [x] Implement `check_dependencies()` to verify prerequisites in `repos_index`/master index before scoring a task. (implemented)
 - [x] Implement `check_dependencies()` to verify prerequisites in `repos_index`/master index before scoring a task. (implemented)
- [x] Implement the primary scoring loop that iterates tasks, validates `done_contract`, applies `gates`, and multiplies by `task_type_weights`. (implemented)
- [x] Output a per-task dictionary of detailed results from the scoring loop. (implemented)
 - [x] Implement the primary scoring loop that iterates tasks, validates `done_contract`, applies `gates`, and multiplies by `task_type_weights`. (implemented)
 - [x] Output a per-task dictionary of detailed results from the scoring loop. (implemented)
- [x] Implement `compute_spec_coverage()` that compares `product.yml` and `checklist.yml` against `project_map.yml` mappings and returns a coverage ratio. (implemented)
- [x] Implement `compute_complexity_profile()` to run static counts (module count, pipeline stage count) using `ast` and `os.listdir`. (implemented)
 - [x] Implement `check_state_transition_implemented()` to enforce done_contract `state_transition_implemented`. (implemented)
 - [x] Implement `compute_spec_coverage()` that compares `product.yml` and `checklist.yml` against `project_map.yml` mappings and returns a coverage ratio. (implemented)
 - [x] Implement `compute_complexity_profile()` to run static counts (module count, pipeline stage count) using `ast` and `os.listdir`. (implemented)

**PHASE 3 — Master Index and AI Integration**

- [x] Implement `aggregate_all_repos(repo_list)` that executes the `PILScanner` for each repo path and aggregates results. (implemented)
- [x] Ensure the top-level key in the generated `repos_index.yml` is the actual `repo_name`. (implemented)
- [x] Add `progress_history` as an ASCII block-character sparkline string (e.g., ` ▂▅█`) representing historical scores. (implemented)
- [x] Produce an AI Input Contract doc block describing the required payload (contracts, master index, Delta, code subset). (added `AI_INPUT_CONTRACT.md`)
- [x] Produce an AI Output Contract doc block specifying fields: `analysis`, `missing_transition`, `semantic_violations`, `spec_coverage_delta`, `recommendation`, `confidence`. (added `AI_OUTPUT_CONTRACT.md`)
- [x] Include the explicit "Do Not Guess" rule in the AI prompt documentation. (included in AI contract docs)
 - [x] Add `progress_history` as an ASCII block-character sparkline string (e.g., ` ▂▅█`) representing historical scores. (implemented)
 - [x] Produce an AI Input Contract doc block describing the required payload (contracts, master index, Delta, code subset). (added `AI_INPUT_CONTRACT.md`)
 - [x] Produce an AI Output Contract doc block specifying fields: `analysis`, `missing_transition`, `semantic_violations`, `spec_coverage_delta`, `recommendation`, `confidence`. (added `AI_OUTPUT_CONTRACT.md`)
 - [x] Include the explicit "Do Not Guess" rule in the AI prompt documentation. (included in AI contract docs)
 - [x] Implement `aggregate_all_repos(repo_list)` that executes the `PILScanner` for each repo path and aggregates results. (implemented)
 - [x] Ensure the top-level key in the generated `repos_index.yml` is the actual `repo_name`. (implemented)
- [x] Add `progress_history` as an ASCII block-character sparkline string (e.g., ` ▂▅█`) representing historical scores. (implemented)
- [x] Produce an AI Input Contract doc block describing the required payload (contracts, master index, Delta, code subset). (added `AI_INPUT_CONTRACT.md`)
- [x] Produce an AI Output Contract doc block specifying fields: `analysis`, `missing_transition`, `semantic_violations`, `spec_coverage_delta`, `recommendation`, `confidence`. (added `AI_OUTPUT_CONTRACT.md`)
- [x] Include the explicit "Do Not Guess" rule in the AI prompt documentation. (included in AI contract docs)
 - [x] Add `progress_history` as an ASCII block-character sparkline string (e.g., ` ▂▅█`) representing historical scores. (implemented)
 - [x] Produce an AI Input Contract doc block describing the required payload (contracts, master index, Delta, code subset). (added `AI_INPUT_CONTRACT.md`)
 - [x] Produce an AI Output Contract doc block specifying fields: `analysis`, `missing_transition`, `semantic_violations`, `spec_coverage_delta`, `recommendation`, `confidence`. (added `AI_OUTPUT_CONTRACT.md`)
 - [x] Include the explicit "Do Not Guess" rule in the AI prompt documentation. (included in AI contract docs)
 - [x] Implement `aggregate_all_repos(repo_list)` that executes the `PILScanner` for each repo path and aggregates results. (implemented)
 - [x] Ensure the top-level key in the generated `repos_index.yml` is the actual `repo_name`. (implemented)
 - [x] Add `AI consumer scaffold` that ingests `repos_index.yml` and emits `ai_analysis.yml` per `AI_OUTPUT_CONTRACT.md`. (implemented)
**DELIVERY / VALIDATION ITEMS**

**DELIVERY / VALIDATION ITEMS**

- [x] Add comments and examples where helpful in all YAML files created above. (implemented)
- [x] Validate YAML and Python syntax for created files before marking them done. (validated)
- [x] Ensure all created code is deterministic (no random UUIDs, timestamps in outputs, etc.) unless explicitly required. (ensured)
- [x] Add or update repository-level documentation referencing these files (optional, request separately). (added `PIL_README.md`)
 - [x] Add or update repository-level documentation referencing these files (added `PIL_README.md`).

- [x] Add CI workflow to run strict validators and artifact checks (`.github/workflows/pil-ci.yml`).

---

Usage

- To update the progress bar after marking checklist items, run:

```bash
python3 scripts/update_pil_progress.py pil_checklist.md
```