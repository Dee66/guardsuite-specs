<!-- PROGRESS_START -->
<div id="pil-progress" style="width:100%; background:#eee; border-radius:6px; padding:4px;">
  <div id="pil-progress-bar" style="width:2%; height:18px; border-radius:4px; background:#e74c3c;"></div>
</div>
<p id="pil-progress-text">2% complete</p>
<!-- PROGRESS_END -->

# PIL Implementation Checklist

This file converts the `PIL checklist.txt` into an actionable checklist derived from the PIL specification. Each item is a single actionable task that can be checked off as completed. Use the included script `scripts/update_pil_progress.py` to update the colored progress bar above to reflect the number of checked items.

- **PHASE 0 — AI IMPLEMENTOR RULES (MANDATORY)**

- [x] Never guess during implementation.
- [ ] Never generate placeholder logic or TODOs inside delivered files.
- [ ] Only produce the specific files requested by the instruction.
- [ ] Never modify or create additional files unless explicitly told.
- [ ] Use exact filenames and folder paths provided in instructions.
- [ ] Preserve comments and version fields in YAML files when updating them.
- [ ] Validate YAML syntax before finalizing YAML outputs.
- [ ] Validate Python syntax for any new Python files.
- [ ] Include all required imports in new Python files.
- [ ] Strictly follow the specification — do not deviate from requirements.
- [ ] If any step is ambiguous, ask for clarification instead of guessing.

**PHASE 1 — Establish Foundational PIL Contracts**

Note: Each file below must be created at the repo root when implemented.

*`scoring_kpis.yml`*
- [ ] Add a top-level `version` field and preserve it in future edits.
- [ ] Implement `score_weights` as integers summing to 100.
- [ ] Implement `task_type_weights` as floating point multipliers.
- [ ] Add `gates` as a list of KPI names that cap scores if they fail.
- [ ] Add a minimal example block demonstrating the fields.

*`repo_contract.yml`*
- [ ] Define `sanity_checks` list of mandatory repository checks (e.g., `product.yml` exists, `src/` exists).
- [ ] Define `required_structure` with file patterns and directory names.
- [ ] Define `complexity_profile_metrics` (e.g., `module_count`, `pipeline_stage_count`).
- [ ] Add descriptive comments for each field in the YAML.

*`project_map.yml`*
- [ ] Use `task_id` as the root key for each task entry.
- [ ] For each task entry include `task_source` (referential pointer).
- [ ] Include `dependencies` as a list of prerequisite task IDs.
- [ ] Add `implementation_files` listing source paths (with placeholders like `src/<pillar_name>/...`).
- [ ] Add `validation_artifacts` listing tests, snapshots, expected outputs.
- [ ] Add `confidence_requirements` with allowed values: `STATIC`, `DYNAMIC`, `AI_REVIEW`.
- [ ] Document pathing conventions (examples with placeholders).

*`task_contract.yml`*
- [ ] Define `task_type` classification for scoring weights (e.g., `pipeline_stage`, `documentation`).
- [ ] Implement `done_contract` as a list of binary requirements (e.g., `implementation_files_present: true`).
- [ ] Add `ambiguity_flags` field initialized as an empty list.
- [ ] Provide example blocks for at least two task types (pipeline_stage and documentation).

**PHASE 2 — Build PIL Generator Engine (`repo-scanner.py`)**

Global: The implementation must be a class `PILScanner`. Include necessary imports at top.

- [ ] Create `PILScanner` class skeleton and state management fields.
- [ ] Implement `calculate_artifact_hash(file_path)` using SHA-256; return `MISSING_FILE_HASH` sentinel for missing files.
- [ ] Implement `ast_check(file_path, required_signature)` that parses AST and returns `(is_compliant: bool, diagnostic_message: str)`.
- [ ] Implement `run_sanity_gate()` to read `repo_contract.yml` and return structured health object; must not throw exceptions.
- [ ] Implement `version_and_drift_detection()` to compare hashes to a previous scan and produce The Delta.
- [ ] Implement `check_dependencies()` to verify prerequisites in `repos_index`/master index before scoring a task.
- [ ] Implement the primary scoring loop that iterates tasks, validates `done_contract`, applies `gates`, and multiplies by `task_type_weights`.
- [ ] Output a per-task dictionary of detailed results from the scoring loop.
- [ ] Implement `compute_spec_coverage()` that compares `product.yml` and `checklist.yml` against `project_map.yml` mappings and returns a coverage ratio.
- [ ] Implement `compute_complexity_profile()` to run static counts (module count, pipeline stage count) using `ast` and `os.listdir`.

**PHASE 3 — Master Index and AI Integration**

- [ ] Implement `aggregate_all_repos(repo_list)` that executes the `PILScanner` for each repo path and aggregates results.
- [ ] Ensure the top-level key in the generated `repos_index.yml` is the actual `repo_name`.
- [ ] Add `progress_history` as an ASCII block-character sparkline string (e.g., ` ▂▅█`) representing historical scores.
- [ ] Produce an AI Input Contract doc block describing the required payload (contracts, master index, Delta, code subset).
- [ ] Produce an AI Output Contract doc block specifying fields: `analysis`, `missing_transition`, `semantic_violations`, `spec_coverage_delta`, `recommendation`, `confidence`.
- [ ] Include the explicit "Do Not Guess" rule in the AI prompt documentation.

**DELIVERY / VALIDATION ITEMS**

- [ ] Add comments and examples where helpful in all YAML files created above.
- [ ] Validate YAML and Python syntax for created files before marking them done.
- [ ] Ensure all created code is deterministic (no random UUIDs, timestamps in outputs, etc.) unless explicitly required.
- [ ] Add or update repository-level documentation referencing these files (optional, request separately).

---

Usage

- To update the progress bar after marking checklist items, run:

```bash
python3 scripts/update_pil_progress.py pil_checklist.md
```

The script will update the HTML/CSS progress block between `<!-- PROGRESS_START -->
<div id="pil-progress" style="width:100%; background:#eee; border-radius:6px; padding:4px;">
  <div id="pil-progress-bar" style="width:2%; height:18px; border-radius:4px; background:#e74c3c;"></div>
</div>
<p id="pil-progress-text">2% complete</p>
<!-- PROGRESS_END -->` in-place.
