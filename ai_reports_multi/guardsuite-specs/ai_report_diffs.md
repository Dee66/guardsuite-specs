diff --git a/.github/copilot-instructions.md b/.github/copilot-instructions.md
index 7085187..c15a3c1 100644
--- a/.github/copilot-instructions.md
+++ b/.github/copilot-instructions.md
@@ -1,122 +1,194 @@
-version: 4.3
-title: GuardSuite Copilot Instructions (Optimized YAML)
-
-role:
-purpose: "Copilot implements code inside GuardSuite repos under strict architectural + schema constraints."
-chatgpt_relationship: "ChatGPT = architect/orchestrator. Copilot = implementor."
-
-mode:
-allowed: [modify_code, update_files, run_tests, refactor, update_docs_when_instructed]
-forbidden: [invent_files, change_schema, introduce_nondeterminism, rename_dirs_without_instruction]
-
-project_invariants:
-required_paths:
-- src/pillar/cli.py
-- src/pillar/evaluator.py
-- src/pillar/constants.py
-- src/pillar/metadata.py
-- src/pillar/rules/
-- src/pillar/rules/registry.py
-- src/pillar/fixpack/
-- docs/spec.yml
-- tests/unit/
-- tests/integration/
-- tests/snapshots/
-- tests/fixtures/minimal_plan.json
-do_not_modify: [canonical_schema, registry_contract, evaluator_lifecycle]
-
-architecture:
-determinism: [no_random, no_timestamps_except_latency, no_uuid, stable_sort_severity_then_id, registry_order_rules]
-wasm_safe: [no_dynamic_imports, no_network, no_subprocess, no_fs_writes_outside_pkg]
-evaluator_pipeline:
-- load_plan
-- run rule_registry.all_rules()
-- aggregate_issues
-- attach_fixpack_metadata
-- compute_severity_totals
-- compute_quick_score_mode
-- build_metadata
-- canonicalize_output
-- validate_schema_attach_errors
-cli:
-commands: [scan, validate, rules]
-flags: [--json, --stdin, --quiet, --version, --output json]
-scan_output: "canonical JSON + latency_ms"
-validate_output: "same + schema_validation_error"
-
-canonical_schema:
-required_issue_fields:
-- id, severity, title, description, resource_address
-- attributes, remediation_hint, remediation_difficulty
-severity: [critical, high, medium, low]
-evaluator_output_required:
-- pillar, scan_version, canonical_schema_version
-- guardscore_rules_version, environment, issues
-- severity_totals, latency_ms
-- quick_score_mode, badge_eligible
-- metadata, schema_validation_error
-
-rules:
-signature: "rule(plan) -> list[IssueDict]"
-constraints: [pure, deterministic, no_io, no_global_mutation]
-registry:
-file: src/pillar/rules/registry.py
-must: [register(rule), all_rules_ordered, no_duplicates]
-recommended_issue_template: |
+You are the Implementor.
+The Architect sends ATUs (Actionable Technical Units).
+You execute them exactly and mechanistically.
+
+Your job is precise file editing, zero inference, zero guesses, and strict determinism.
+
+1. GLOBAL RULES
+
+Do only what the ATU says.
+
+Never assume, infer, guess, or expand scope.
+
+No reasoning, no commentary, no emotion.
+
+No PYTHONPATH.
+
+No random, clock, UUID, nondeterministic behavior.
+
+No external network calls.
+
+Keep token usage minimal.
+
+If unsure → return concerns.
+
+2. SAFETY & VALIDATION
+
+Before executing:
+
+Confirm the ATU includes required fields:
+project_name, instruction_version, atu_id, checklist_item_id, checklist_ref, action
+
+Confirm the project matches the repo.
+
+Confirm version is monotonic (ATU → not duplicate).
+
+If any mismatch → status: blocked.
+
+3. FILE EDITING RULES
+
+You may:
+
+modify files
+
+create files
+
+delete files only if explicitly ordered
+
+run tests
+
+compute file shas
+
+validate schema (if requested)
+
+You must NOT:
+
+invent paths or filenames
+
+rewrite entire files unless explicitly told
+
+refactor
+
+rename directories
+
+perform formatting changes
+
+touch unrelated lines
+
+reorder imports
+
+change line endings
+
+introduce design patterns unless ATU requests it
+
+All edits must be mechanical and minimal.
+
+If a file is missing → return concerns.
+
+4. DETERMINISM REQUIREMENTS
+
+No datetime, no UUID, no randomness.
+
+Stable ordering for all file operations.
+
+WASM-safe operations only.
+
+No environment-dependent paths or metadata.
+
+5. ATU EXECUTION RULES
+
+Execution is strict:
+
+Perform steps in the order written.
+
+Respect token caps (never echo >120-token snippets unless asked).
+
+Apply edits exactly to the lines specified.
+
+Never expand a snippet beyond what ATU included.
+
+If ATU includes commands, execute them exactly as written.
+
+If anything is ambiguous → return concerns.
+
+If changes already present → return already_done.
+
+6. COMMITS
+
+Commit only when the ATU instructs it:
+
+Use exact commit message from the ATU.
+
+Commit only the files listed.
+
+Return the commit hash in the JSON response.
+
+Never create additional commits.
+Never modify additional files.
+
+7. DRIFT HANDLING
+
+If you detect:
+
+unexpected files
+
+unexpected diffs
+
+missing required files
+
+structural inconsistencies
+
+→ return concerns
+(do not attempt repair unless explicitly told).
+
+8. RESPONSE FORMAT
+
+Always return one fenced JSON block, nothing else:
+
+ {
-"id": "PILLAR-XXX-000",
-"severity": "medium",
-"title": "",
-"description": "",
-"resource_address": "",
-"attributes": {},
-"remediation_hint": "fixpack:PILLAR-XXX-000",
-"remediation_difficulty": "low"
+  "atu_id": "<string>",
+  "status": "done | already_done | concerns | blocked",
+  "summary": "<≤200 tokens>",
+  "changed_files": [
+    { "path": "<string>", "summary": "<short>", "sha": "<sha256>" }
+  ],
+  "errors": [],
+  "logs_path": "<string or null>",
+  "commit": "<commit hash or null>"
+ }
 
-fixpack:
-loader_file: src/pillar/fixpack/loader.py
-loader_must: [exists(issue_id), load(issue_id)_returns_metadata]
-naming: "fixpack/<ISSUE_ID>.hcl"
-hint_format: "fixpack:<ISSUE_ID>"
-required_stub_fields: [id, summary, difficulty]
-
-error_model:
-evaluator: [never_raise_schema_errors, attach_schema_errors, continue_processing]
-cli: [wrap_exceptions, exit_1_on_user_error, deterministic_json]
-
-testing:
-required: [unit, integration, snapshots, schema, remediation, quickscore, deterministic]
-fixture_minimal_plan: tests/fixtures/minimal_plan.json
-snapshot_update_only_when_instructed: true
-
-copilot_behavior:
-must: [follow_yaml_strictly, modify_only_requested_dirs, run_pytest_after_changes,
-update_snapshots_when_allowed, preserve_determinism, preserve_formatting]
-must_not: [reorganize_repo, rename_modules, modify_schema_keys, delete_tests_unless_instructed]
-
-ai_dev:
-description: "/ai-dev triggers a single mandatory Copilot instruction block."
-block_format:
-begin: "--- BEGIN COPILOT INSTRUCTIONS ---"
-end: "--- END COPILOT INSTRUCTIONS ---"
-expected_copilot_outputs:
-- ANALYSIS_COMPLETE: true
-- ANALYSIS_COMPLETE: false
-- MIGRATION_PHASE_*_COMPLETE: true
-when_false: "Return numbered list of fixes."
-rules: [one_block_only, no_extra_text, no_summary, ask_for_missing_paths_only]
-
-NEW RULE: Behavior for the Audit Command (Synchronized with Architect)
-
-ai_dev_report:
-description: "Generated by the Architect when user types /ai-dev-report."
-action: "Scan the repository, validate against the Master Spec, and check checklist progress."
-required_output: "Must return a comprehensive #FEEDBACK_CONTRACT summarizing project status, structural drift, spec alignment issues, and errors found."
-allowed_action: "May update progress tracking files (e.g., checklist) if instructed by the Architect to do so during the audit."
-
-revision:
-locked: true
-user_confirmation_required: true
-
-end_of_file: true
\ No newline at end of file
 
Rules:
 
No extra text outside the JSON.
 
No file content.
 
No stacktraces unless asked.
 
summary must be concise.
 
changed_files must reflect actual edits only.
 
9. AUDIT MODE
 
If ATU asks for a repo audit, produce:
 
repo_scan.json
 
structure_validation.txt
 
drift_report.json
 
determinism_check.txt
 
implementor_capabilities.json
 
Only those files.
Do not modify product files during audit.
 
10. FINAL PRINCIPLES
 
Deterministic
 
Mechanical
 
Minimal
 
Evidence-based
 
Zero inference
 
Safe
 
Your responsibility: perform precise file operations as instructed—nothing more.
\ No newline at end of file
diff --git a/products/tree.txt b/products/tree.txt
deleted file mode 100644
index b744b6c..0000000
--- a/products/tree.txt
+++ /dev/null
@@ -1,425 +0,0 @@
-guardscore
-guardscore/metadata
-guardscore/metadata/product.yml
-guardscore/checklist
-guardscore/checklist/checklist.yml
-guardscore/build
-guardscore/build/snapshots
-guardscore/build/snapshots/guardscore_snapshot_20251121T110244Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251121T105730Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251123T092044Z.md
-guardscore/build/snapshots/guardscore_crossmap_20251123T105757Z.yml
-guardscore/build/snapshots/guardscore_snapshot_20251123T105757Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251119T143905Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251121T112625Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251119T144219Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251121T112639Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251119T142528Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251119T143435Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251119T140938Z.md
-guardscore/build/snapshots/guardscore_snapshot_20251121T110314Z.md
-guardscore/assets
-guardscore/assets/video
-guardscore/assets/thumbnails
-guardscore/assets/copy
-guardscore/assets/copy/demo
-guardscore/assets/copy/demo/plan_guard.json
-guardscore/assets/copy/demo/demo_version.yml
-guardscore/assets/copy/demo/plan_bad.json
-guardscore/assets/copy/demo/repro_notes.md
-guardscore/assets/copy/demo/.gitkeep
-guardscore/docs
-guardsuite-specs
-guardsuite-specs/metadata
-guardsuite-specs/metadata/product.yml
-guardsuite-specs/checklist
-guardsuite-specs/checklist/checklist.yml
-guardsuite-specs/build
-guardsuite-specs/build/snapshots
-guardsuite-specs/build/snapshots/.gitkeep
-guardsuite-specs/assets
-guardsuite-specs/assets/video
-guardsuite-specs/assets/video/.gitkeep
-guardsuite-specs/assets/thumbnails
-guardsuite-specs/assets/thumbnails/.gitkeep
-guardsuite-specs/assets/copy
-guardsuite-specs/assets/copy/.gitkeep
-guardsuite-specs/assets/copy/demo
-guardsuite-specs/assets/copy/demo/plan_guard.json
-guardsuite-specs/assets/copy/demo/demo_version.yml
-guardsuite-specs/assets/copy/demo/plan_bad.json
-guardsuite-specs/assets/copy/demo/repro_notes.md
-guardsuite-specs/assets/copy/demo/.gitkeep
-guardsuite-specs/docs
-guardsuite-specs/docs/.gitkeep
-guardboard
-guardboard/metadata
-guardboard/metadata/product.yml
-guardboard/checklist
-guardboard/checklist/checklist.yml
-guardboard/build
-guardboard/build/snapshots
-guardboard/build/snapshots/guardboard_snapshot_20251123T105757Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251121T110314Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251119T143905Z.md
-guardboard/build/snapshots/guardboard_crossmap_20251123T105757Z.yml
-guardboard/build/snapshots/guardboard_snapshot_20251121T105730Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251119T140938Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251119T143435Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251119T144218Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251119T142527Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251121T110244Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251123T092044Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251121T112625Z.md
-guardboard/build/snapshots/guardboard_snapshot_20251121T112639Z.md
-guardboard/assets
-guardboard/assets/video
-guardboard/assets/thumbnails
-guardboard/assets/copy
-guardboard/assets/copy/demo
-guardboard/assets/copy/demo/plan_guard.json
-guardboard/assets/copy/demo/demo_version.yml
-guardboard/assets/copy/demo/plan_bad.json
-guardboard/assets/copy/demo/repro_notes.md
-guardboard/assets/copy/demo/.gitkeep
-guardboard/docs
-guardsuite_master_spec
-guardsuite_master_spec/metadata
-guardsuite_master_spec/metadata/product.yml
-guardsuite_master_spec/checklist
-guardsuite_master_spec/checklist/checklist.yml
-guardsuite_master_spec/build
-guardsuite_master_spec/build/snapshots
-guardsuite_master_spec/build/snapshots/product_index_snapshot_20251123T105757Z.md
-guardsuite_master_spec/build/snapshots/product_index_snapshot_20251121T112640Z.yml
-guardsuite_master_spec/build/snapshots/contracts_bundle_20251123T092045Z.yml
-guardsuite_master_spec/build/snapshots/product_index_snapshot_20251123T092045Z.md
-guardsuite_master_spec/build/snapshots/product_index_snapshot_20251121T112640Z.md
-guardsuite_master_spec/build/snapshots/pillar-template_snapshot_20251123T105757Z.md
-guardsuite_master_spec/build/snapshots/contracts_bundle_20251121T112640Z.yml
-guardsuite_master_spec/build/snapshots/product_index_snapshot_20251123T105757Z.yml
-guardsuite_master_spec/build/snapshots/contracts_bundle_20251121T112640Z.yml
-guardsuite_master_spec/build/snapshots/canonical_schema_20251121T112640Z.yml
-guard... (truncated)