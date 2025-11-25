diff --git a/products/pipelineguard/checklist/checklist.yml b/products/pipelineguard/checklist/checklist.yml
index b49dad3..1f8e4d4 100644
--- a/products/pipelineguard/checklist/checklist.yml
+++ b/products/pipelineguard/checklist/checklist.yml
@@ -1,198 +1,450 @@
-checklist:
-  version: 2026.04
-  product: pipelineguard
-  pillar: pipeline
+# products/pipelineguard/checklist/checklist.yml
+# Strategy-D canonical checklist for PipelineGuard (paid blueprint)
 
-  phases:
+metadata:
+  product_id: pipelineguard
+  checklist_version: "2026.04"
+  last_updated: "2025-11-25T00:00:00Z"
+  owner: "GuardSuite Platform Team"
+  stability: ga
+
+structure_requirements:
+  - id: STRUCT-PG-001
+    description: "Embed all historical PipelineGuard phases and item IDs without alteration."
+    required: true
+  - id: STRUCT-PG-002
+    description: "Follow Strategy-D ordering: metadata ⇒ requirements ⇒ phases ⇒ acceptance."
+    required: true
+
+documentation_requirements:
+  readme_required: true
+  product_docs_required: true
+  api_reference_required: true
+  examples_required: true
+  changelog_required: true
+  release_notes_required: true
+
+schema_requirements:
+  canonical_schema_required: true
+  metadata_schema_required: true
+  provenance_schema_required: true
+  fragment_schemas_required: true
+  additional_schemas:
+    - schemas/pipelineguard/canonical_schema.json
+    - schemas/pipelineguard/export_bundle.json
+    - schemas/pipelineguard/compliance_ledger.json
+    - schemas/pipelineguard/fixpack_metadata.json
+
+evaluator_requirements:
+  pipeline_must_match_template: true
+  canonicalization_required: true
+  wasm_safety_required: true
+  deterministic_output_required: true
+  timestamp_normalization_required: true
+  prohibited_overrides:
+    - canonical.output_contract
+    - evaluator.runtime_override
+    - compliance.disable_ledger
+    - fixpack.runtime_override
+    - provenance.disable_validation
+
+fixpack_requirements:
+  fixpack_catalog_required: true
+  fixpack_metadata_required: true
+  difficulty_taxonomy_required: true
+  patch_hashing_required: true
+  remediation_examples_required: true
+  wasm_safe_snippets_required: true
+
+testing_requirements:
+  unit_tests_required: true
+  integration_tests_required: true
+  snapshot_tests_required: true
+  parity_tests_required: true
+  wasm_tests_required: true
+  schema_validation_tests_required: true
+  performance_tests_required: true
+  minimum_coverage_percent: 85
+
+artifacts:
+  required_files:
+    - products/pipelineguard/metadata/product.yml
+    - schemas/pipelineguard/canonical_schema.json
+    - schemas/pipelineguard/export_bundle.json
+    - schemas/pipelineguard/compliance_ledger.json
+    - schemas/pipelineguard/fixpack_metadata.json
+    - ci/pipelineguard-ci.yml
+  required_directories:
+    - fixpack/pipeline
+    - schemas/pipelineguard
+    - rules/pipelineguard
+    - docs/products/pipelineguard
+    - tests/pipelineguard
+    - examples
+  build_outputs:
+    - artifacts/ledgers
+    - artifacts/fixpack_previews
+    - artifacts/schema_reports
+
+acceptance_criteria:
+  - id: ACPT-PG-001
+    description: "Evaluator, CLI, ledger, and fixpack bundles validate against canonical schemas."
+    required: true
+  - id: ACPT-PG-002
+    description: "Snapshot, parity, and WASM determinism suites pass across three runs."
+    required: true
+  - id: ACPT-PG-003
+    description: "FixPack-Lite snippets remain deterministic, signed, and provenance-backed."
+    required: true
+  - id: ACPT-PG-004
+    description: "Compliance ledger hash-chain integrity verified end-to-end."
+    required: true
+
+cross_product_dependencies:
+  depends_on_products:
+    - pipelinescan
+    - guardscore
+    - guardboard
+    - computeguard
+  depends_on_schemas:
+    - guardsuite-core/canonical_schema.json
+    - schemas/pipelineguard/canonical_schema.json
+    - schemas/pipelineguard/compliance_ledger.json
+  depends_on_pipeline: true
+
+provenance:
+  - "Checklist derived from PipelineGuard charter v2026.04 and Strategy-D paid blueprint baseline."
+  - "Aligned with GuardSuite governance rules and FixPack-Lite remediation contracts."
+
+id: pipelineguard_checklist
+version: "2026.04"
+product: pipelineguard
+pillar: pipeline
+spec_source: "products/pipelineguard/metadata/product.yml"
+
+phases:
 
   # ============================================================
   # 1. INITIALIZATION & BLUEPRINT SETUP
   # ============================================================
   - phase: initialization
+    summary: "Validate spec alignment, template sync, and foundational governance settings."
     items:
-      - INIT-001: load_spec_and_validate_yaml_structure
-      - INIT-002: ensure_required_sections_present
-      - INIT-003: verify_spec_version_matches_release_metadata
-      - INIT-004: enforce_forbidden_overrides_declared
-      - INIT-005: validate_core_dependency_pin(guardsuite-core>=2.4.0)
-      - INIT-006: validate_schema_version_pin(canonical_schema>=2.0.0)
-      - INIT-007: enforce_compatibility_window(12_months)
-      - INIT-008: validate_blueprint_inheritance(pipelinescan>=2.0)
-      - INIT-009: load_template_spec_and_validate_sync
-      - INIT-010: detect_template_core_drift
-      - INIT-011: ensure_checklist_schema_valid
-      - INIT-012: detect_checklist_drift_against_spec
+      - id: INIT-001
+        description: "load_spec_and_validate_yaml_structure"
+      - id: INIT-002
+        description: "ensure_required_sections_present"
+      - id: INIT-003
+        description: "verify_spec_version_matches_release_metadata"
+      - id: INIT-004
+        description: "enforce_forbidden_overrides_declared"
+      - id: INIT-005
+        description: "validate_core_dependency_pin(guardsuite-core>=2.4.0)"
+      - id: INIT-006
+        description: "validate_schema_version_pin(canonical_schema>=2.0.0)"
+      - id: INIT-007
+        description: "enforce_compatibility_window(12_months)"
+      - id: INIT-008
+        description: "validate_blueprint_inheritance(pipelinescan>=2.0)"
+      - id: INIT-009
+        description: "load_template_spec_and_validate_sync"
+      - id: INIT-010
+        description: "detect_template_core_drift"
+      - id: INIT-011
+        description: "ensure_checklist_schema_valid"
+      - id: INIT-012
+        description: "detect_checklist_drift_against_spec"
 
   # ============================================================
   # 2. SCHEMA, FRAGMENTS & CANONICALIZATION
   # ============================================================
   - phase: schema_validation
+    summary: "Guarantee canonical schema bundles, normalization, and deterministic serialization."
     items:
-      - SCHEMA-001: validate_canonical_schema_json
-      - SCHEMA-002: validate_pipelineguard_schema_extends_core_schema
-      - SCHEMA-003: detect_duplicate_field_definitions
-      - SCHEMA-004: validate_stable_schema_bundle_ordering
-      - SCHEMA-005: compute_schema_bundle_hash_and_store
-      - SCHEMA-006: validate_schema_version_pin_resolves_correctly
-      - SCHEMA-007: validate_input_canonicalization_rules_apply
-      - SCHEMA-008: enforce_key_ordering_in_all_outputs
-      - SCHEMA-009: validate_timestamp_normalization_utc_z
-      - SCHEMA-010: validate_fixed_64_numeric_semantics
-      - SCHEMA-011: ensure_snapshot_normalization_rules_present(3_runs_identical)
+      - id: SCHEMA-001
+        description: "validate_canonical_schema_json"
+      - id: SCHEMA-002
+        description: "validate_pipelineguard_schema_extends_core_schema"
+      - id: SCHEMA-003
+        description: "detect_duplicate_field_definitions"
+      - id: SCHEMA-004
+        description: "validate_stable_schema_bundle_ordering"
+      - id: SCHEMA-005
+        description: "compute_schema_bundle_hash_and_store"
+      - id: SCHEMA-006
+        description: "validate_schema_version_pin_resolves_correctly"
+      - id: SCHEMA-007
+        description: "validate_input_canonicalization_rules_apply"
+      - id: SCHEMA-008
+        description: "enforce_key_ordering_in_all_outputs"
+      - id: SCHEMA-009
+        description: "validate_timestamp_normalization_utc_z"
+      - id: SCHEMA-010
+        description: "validate_fixed_64_numeric_semantics"
+      - id: SCHEMA-011
+        description: "ensure_snapshot_normalization_rules_present(3_runs_identical)"
 
   # ============================================================
   # 3. GOVERNANCE & OVERRIDE PROTECTION
   # ============================================================
   - phase: governance_enforcement
+    summary: "Enforce blueprint governance, RFC policy, and forbidden override detection."
     items:
-      - GOV-001: enforce_changelog_required
-      - GOV-002: enforce_codeowners_required
-      - GOV-003: enforce_rfc_required_for_major
-      - GOV-004: validate_governance_domains_declared
-      - GOV-005: validate_rule_categories_declared
-      - GOV-006: validate_forbidden_overrides_list
-      - GOV-007: static_analysis_forbidden_override_detection
-      - GOV-008: enforce_breaking_change_policy_structure
+      - id: GOV-001
+        description: "enforce_changelog_required"
+      - id: GOV-002
+        description: "enforce_codeowners_required"
+      - id: GOV-003
+        description: "enforce_rfc_required_for_major"
+      - id: GOV-004
+        description: "validate_governance_domains_declared"
+      - id: GOV-005
+        description: "validate_rule_categories_declared"
+      - id: GOV-006
+        description: "validate_forbidden_overrides_list"
+      - id: GOV-007
+        description: "static_analysis_forbidden_override_detection"
+      - id: GOV-008
+        description: "enforce_breaking_change_policy_structure"
 
   # ============================================================
   # 4. EVALUATOR PIPELINE CONTRACT
   # ============================================================
   - phase: evaluator_pipeline
+    summary: "Align evaluator stages with template definition and deterministic constraints."
     items:
-      - PIPE-001: load_template_pipeline_definition
-      - PIPE-002: validate_stage_order_matches_template
-      - PIPE-003: enforce_no_randomness_or_local_time
-      - PIPE-004: enforce_no_env_based_branching
-      - PIPE-005: enforce_canonical_json_utf8_output
-      - PIPE-006: validate_snapshot_normalization_determinism
-      - PIPE-007: evaluator_determinism_test_across_3_runs
-      - PIPE-008: evaluator_parity_test(x86_arm_wasm)
-      - PIPE-009: provenance_validation_in_pipeline_evaluator
-      - PIPE-010: rule_engine_contract_validation
-      - PIPE-011: drift_detection_behavior_test
+      - id: PIPE-001
+        description: "load_template_pipeline_definition"
+      - id: PIPE-002
+        description: "validate_stage_order_matches_template"
+      - id: PIPE-003
+        description: "enforce_no_randomness_or_local_time"
+      - id: PIPE-004
+        description: "enforce_no_env_based_branching"
+      - id: PIPE-005
+        description: "enforce_canonical_json_utf8_output"
+      - id: PIPE-006
+        description: "validate_snapshot_normalization_determinism"
+      - id: PIPE-007
+        description: "evaluator_determinism_test_across_3_runs"
+      - id: PIPE-008
+        description: "evaluator_parity_test(x86_arm_wasm)"
+      - id: PIPE-009
+        description: "provenance_validation_in_pipeline_evaluator"
+      - id: PIPE-010
+        description: "rule_engine_contract_validation"
+      - id: PIPE-011
+        description: "drift_detection_behavior_test"
 
   # ============================================================
   # 5. FIXPACK-LITE REMEDIATION
   # ============================================================
   - phase: fixpack_lite
+    summary: "Validate deterministic remediation snippets, metadata, and provenance."
     items:
-      - FX-001: validate_fixpack_folder_structure
-      - FX-002: validate_snippet_count(10)
-      - FX-003: ensure_snippet_deterministic_ordering
-      - FX-004: validate_fixpack_signature_chain
-      - FX-005: validate_fixpack_metadata_schema
-      - FX-006: provenance_required_for_all_snippets
-      - FX-007: wasm_safe_snippets_required
-      - FX-008: validate_fixpack_hint_format
-      - FX-009: validate_fixpack_registry_state_for_guardscore_inputs
+      - id: FX-001
+        description: "validate_fixpack_folder_structure"
+      - id: FX-002
+        description: "validate_snippet_count(10)"
+      - id: FX-003
+        description: "ensure_snippet_deterministic_ordering"
+      - id: FX-004
+        description: "validate_fixpack_signature_chain"
+      - id: FX-005
+        description: "validate_fixpack_metadata_schema"
+      - id: FX-006
+        description: "provenance_required_for_all_snippets"
+      - id: FX-007
+        description: "wasm_safe_snippets_required"
+      - id: FX-008
+        description: "validate_fixpack_hint_format"
+      - id: FX-009
+        description: "validate_fixpack_registry_state_for_guardscore_inputs"
 
   # ============================================================
   # 6. COMPLIANCE LEDGER
   # ============================================================
   - phase: compliance_ledger
+    summary: "Enforce audit-grade ledger schema, hash chain, and parity coverage."
     items:
-      - LEDGER-001: validate_ledger_schema_version(1.0.1)
-      - LEDGER-002: enforce_hash_chain_required
-      - LEDGER-003: enforce_provenance_links
-      - LEDGER-004: enforce_canonical_ledger_entry_order
-      - LEDGER-005: validate_deterministic_timestamps
-      - LEDGER-006: validate_ledger_index_monotonic
-      - LEDGER-007: validate_shard_partition_consistency
-      - LEDGER-008: enforce_canonical_json_utf8_serialization
-      - LEDGER-009: compliance_ledger_parity_test(x86_arm_wasm)
-      - LEDGER-010: validate_fixpack_entries_recorded_in_ledger
+      - id: LEDGER-001
+        description: "validate_ledger_schema_version(1.0.1)"
+      - id: LEDGER-002
+        description: "enforce_hash_chain_required"
+      - id: LEDGER-003
+        description: "enforce_provenance_links"
+      - id: LEDGER-004
+        description: "enforce_canonical_ledger_entry_order"
+      - id: LEDGER-005
+        description: "validate_deterministic_timestamps"
+      - id: LEDGER-006
+        description: "validate_ledger_index_monotonic"
+      - id: LEDGER-007
+        description: "validate_shard_partition_consistency"
+      - id: LEDGER-008
+        description: "enforce_canonical_json_utf8_serialization"
+      - id: LEDGER-009
+        description: "compliance_ledger_parity_test(x86_arm_wasm)"
+      - id: LEDGER-010
+        description: "validate_fixpack_entries_recorded_in_ledger"
 
   # ============================================================
   # 7. CLI HARNESS CONTRACT
   # ============================================================
   - phase: cli
+    summary: "Confirm CLI entrypoints, flags, sandboxing, and deterministic help output."
     items:
-      - CLI-001: validate_cli_entrypoints
-      - CLI-002: validate_scan_command_present
-      - CLI-003: ensure_supported_flags_match_spec
-      - CLI-004: ensure_reserved_flags_enforced
-      - CLI-005: validate_machine_parseable_help_output
-      - CLI-006: enforce_canonical_error_output
-      - CLI-007: validate_cli_under_wasm
-      - CLI-008: cli_parity_test(x86_arm_wasm)
-      - CLI-009: validate_invalid_flag_error_schema
-      - CLI-010: enforce_cli_sandbox_filesystem_rules
+      - id: CLI-001
+        description: "validate_cli_entrypoints"
+      - id: CLI-002
+        description: "validate_scan_command_present"
+      - id: CLI-003
+        description: "ensure_supported_flags_match_spec"
+      - id: CLI-004
+        description: "ensure_reserved_flags_enforced"
+      - id: CLI-005
+        description: "validate_machine_parseable_help_output"
+      - id: CLI-006
+        description: "enforce_canonical_error_output"
+      - id: CLI-007
+        description: "validate_cli_under_wasm"
+      - id: CLI-008
+        description: "cli_parity_test(x86_arm_wasm)"
+      - id: CLI-009
+        description: "validate_invalid_flag_error_schema"
+      - id: CLI-010
+        description: "enforce_cli_sandbox_filesystem_rules"
 
   # ============================================================
   # 8. PERFORMANCE BUDGETS
   # ============================================================
   - phase: performance
+    summary: "Meet memory, runtime, and stage budget expectations for enterprise workloads."
     items:
-      - PERF-001: enforce_max_memory_mb(230)
-      - PERF-002: validate_expected_runtime(650ms)
-      - PERF-003: validate_large_plan_runtime(1500ms)
-      - PERF-004: validate_playground_runtime(1800ms)
-      - PERF-005: enforce_stage_budget(discover_ci_sources_ms=200)
-      - PERF-006: enforce_stage_budget(provenance_verification_ms=250)
-      - PERF-007: enforce_stage_budget(permission_graph_build_ms=150)
-      - PERF-008: enforce_stage_budget(evaluate_rules_ms=300)
-      - PERF-009: enforce_stage_budget(remediation_synthesis_ms=150)
-      - PERF-010: enforce_stage_budget(canonicalize_output_ms=150)
-      - PERF-011: enforce_stage_budget(ledger_write_ms=120)
+      - id: PERF-001
+        description: "enforce_max_memory_mb(230)"
+      - id: PERF-002
+        description: "validate_expected_runtime(650ms)"
+      - id: PERF-003
+        description: "validate_large_plan_runtime(1500ms)"
+      - id: PERF-004
+        description: "validate_playground_runtime(1800ms)"
+      - id: PERF-005
+        description: "enforce_stage_budget(discover_ci_sources_ms=200)"
+      - id: PERF-006
+        description: "enforce_stage_budget(provenance_verification_ms=250)"
+      - id: PERF-007
+        description: "enforce_stage_budget(permission_graph_build_ms=150)"
+      - id: PERF-008
+        description: "enforce_stage_budget(evaluate_rules_ms=300)"
+      - id: PERF-009
+        description: "enforce_stage_budget(remediation_synthesis_ms=150)"
+      - id: PERF-010
+        description: "enforce_stage_budget(canonicalize_output_ms=150)"
+      - id: PERF-011
+        description: "enforce_stage_budget(ledger_write_ms=120)"
 
   # ============================================================
   # 9. ECOSYSTEM INTEGRATIONS
   # ============================================================
   - phase: integrations
+    summary: "Validate GuardScore, GuardBoard, and Playground integration contracts."
     items:
-      - INTEG-001: validate_guardscore_inputs_exist
-      - INTEG-002: validate_penalty_map_structure
-      - INTEG-003: validate_badge_eligibility_signal
-      - INTEG-004: validate_playground_wasm_safe
-      - INTEG-005: validate_guardboard_compliance_ledger_visibility
-      - INTEG-006: validate_provenance_chain_insights_enabled
-      - INTEG-007: validate_guardboard_overlays_consistency
-      - INTEG-008: validate_penalty_values_consistency_with_guardscore
+      - id: INTEG-001
+        description: "validate_guardscore_inputs_exist"
+      - id: INTEG-002
+        description: "validate_penalty_map_structure"
+      - id: INTEG-003
+        description: "validate_badge_eligibility_signal"
+      - id: INTEG-004
+        description: "validate_playground_wasm_safe"
+      - id: INTEG-005
+        description: "validate_guardboard_compliance_ledger_visibility"
+      - id: INTEG-006
+        description: "validate_provenance_chain_insights_enabled"
+      - id: INTEG-007
+        description: "validate_guardboard_overlays_consistency"
+      - id: INTEG-008
+        description: "validate_penalty_values_consistency_with_guardscore"
 
   # ============================================================
   # 10. SECURITY & SANDBOXING
   # ============================================================
   - phase: security
+    summary: "Maintain sandboxing, sanitization, and forbidden override protections."
     items:
-      - SEC-001: enforce_no_external_calls
-      - SEC-002: enforce_sanitize_all_inputs
-      - SEC-003: enforce_svg_sanitization
-      - SEC-004: enforce_wasm_compatibility
-      - SEC-005: ensure_wasi_sandbox_requirement_met
-      - SEC-006: validate_safe_error_reporting
-      - SEC-007: test_for_forbidden_override_attempts
-      - SEC-008: validate_no_nondeterministic_io
-      - SEC-009: validate_identity_spoofing_protections
+      - id: SEC-001
+        description: "enforce_no_external_calls"
+      - id: SEC-002
+        description: "enforce_sanitize_all_inputs"
+      - id: SEC-003
+        description: "enforce_svg_sanitization"
+      - id: SEC-004
+        description: "enforce_wasm_compatibility"
+      - id: SEC-005
+        description: "ensure_wasi_sandbox_requirement_met"
+      - id: SEC-006
+        description: "validate_safe_error_reporting"
+      - id: SEC-007
+        description: "test_for_forbidden_override_attempts"
+      - id: SEC-008
+        description: "validate_no_nondeterministic_io"
+      - id: SEC-009
+        description: "validate_identity_spoofing_protections"
 
   # ============================================================
   # 11. TESTING & CI
   # ============================================================
   - phase: testing_ci
+    summary: "Execute full CI matrix (x86 + arm + WASM) with determinism and schema checks."
     items:
-      - TEST-001: run_unit_tests
-      - TEST-002: run_integration_tests
-      - TEST-003: run_snapshot_schema_tests
-      - TEST-004: run_parity_tests
-      - TEST-005: run_wasm_conformance_tests
-      - TEST-006: run_evaluator_determinism_tests
-      - TEST-007: enforce_test_coverage(>=85)
-      - TEST-008: validate_ci_jobs_match_spec
-      - TEST-009: enforce_ci_matrix(x86_64,arm64)
-      - TEST-010: validate_checklist_schema_valid
-      - TEST-011: detect_checklist_drift_against_spec
+      - id: TEST-001
+        description: "run_unit_tests"
+      - id: TEST-002
+        description: "run_integration_tests"
+      - id: TEST-003
+        description: "run_snapshot_schema_tests"
+      - id: TEST-004
+        description: "run_parity_tests"
+      - id: TEST-005
+        description: "run_wasm_conformance_tests"
+      - id: TEST-006
+        description: "run_evaluator_determinism_tests"
+      - id: TEST-007
+        description: "enforce_test_coverage(>=85)"
+      - id: TEST-008
+        description: "validate_ci_jobs_match_spec"
+      - id: TEST-009
+        description: "enforce_ci_matrix(x86_64,arm64)"
+      - id: TEST-010
+        description: "validate_checklist_schema_valid"
+      - id: TEST-011
+        description: "detect_checklist_drift_against_spec"
 
   # ============================================================
   # 12. ACCEPTANCE CRITERIA
   # ============================================================
   - phase: acceptance
+    summary: "Final verification of schema, remediation, ledger, and integration readiness."
     items:
-      - ACPT-001: verify_all_canonical_schemas_pass
-      - ACPT-002: verify_provenance_enforced_and_hash_valid
-      - ACPT-003: verify_fixpack_signature_chain_passes
-      - ACPT-004: verify_snapshot_determinism_3_run_hash_match
-      - ACPT-005: verify_evaluator_pipeline_invariants
-      - ACPT-006: verify_cli_and_api_output_match_contracts
-      - ACPT-007: verify_guardscore_inputs_populated
-      - ACPT-008: verify_wasm_conformance_end_to_end
-      - ACPT-009: verify_all_deliverables_exist
-      - ACPT-010: validate_all_deliverables_against_spec
+      - id: ACPT-001
+        description: "verify_all_canonical_schemas_pass"
+      - id: ACPT-002
+        description: "verify_provenance_enforced_and_hash_valid"
+      - id: ACPT-003
+        description: "verify_fixpack_signature_chain_passes"
+      - id: ACPT-004
+        description: "verify_snapshot_determinism_3_run_hash_match"
+      - id: ACPT-005
+        description: "verify_evaluator_pipeline_invariants"
+      - id: ACPT-006
+        description: "verify_cli_and_api_output_match_contracts"
+      - id: ACPT-007
+        description: "verify_guardscore_inputs_populated"
+      - id: ACPT-008
+        description: "verify_wasm_conformance_end_to_end"
+      - id: ACPT-009
+        description: "verify_all_deliverables_exist"
+      - id: ACPT-010
+        description: "validate_all_deliverables_against_spec"
+
