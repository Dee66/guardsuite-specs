# Playground Checklist Canonicalization Diff

```diff
--- workspace/strategy_d/backups/playground_checklist_pre_normalization.yml	2025-11-25 15:52:40.227310358 +0200
+++ products/playground/checklist/checklist.yml	2025-11-25 16:09:30.793608365 +0200
@@ -1,308 +1,879 @@
-checklist:
-  id: playground-checklist
-  version: "2026.04"
-  product: playground
-  pillar: crosscut
+# products/playground/checklist/checklist.yml
+# Strategy-D canonical checklist for GuardSuite Playground (browser-based deterministic evaluator)
 
-  phases:
+metadata:
+  product_id: playground
+  checklist_version: "2026.04"
+  last_updated: "2025-11-25T00:00:00Z"
+  owner: "GuardSuite Platform Team"
+  stability: ga
+
+structure_requirements:
+  - id: STRUCT-PG-001
+    description: "Preserve all legacy phase content while layering Strategy-D canonical sections."
+    required: true
+  - id: STRUCT-PG-002
+    description: "Order sections as metadata → canonical requirements → phases → legacy dump."
+    required: true
+  - id: STRUCT-PG-003
+    description: "Document WASM sandbox and determinism guarantees ahead of operational tasks."
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
+  provenance_schema_required: false
+  fragment_schemas_required: true
+  additional_schemas:
+    - schemas/playground/playground.schema.yml
+    - schemas/playground/sample_plan.schema.yml
+    - schemas/checklist_schema.yml
+    - schemas/product_schema.yml
+    - schemas/gpt_instructions_schema.yml
+    - schemas/bootstrap_schema.yml
+    - schemas/cli_output.json
+    - schemas/cli_error.json
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
+    - wasm_runtime_safety
+    - quickscore_mode_mutation
+
+fixpack_requirements:
+  fixpack_catalog_required: false
+  fixpack_metadata_required: false
+  difficulty_taxonomy_required: false
+  patch_hashing_required: false
+  remediation_examples_required: false
+
+testing_requirements:
+  unit_tests_required: true
+  integration_tests_required: true
+  snapshot_tests_required: true
+  parity_tests_required: true
+  wasm_tests_required: true
+  schema_validation_tests_required: true
+  performance_tests_required: true
+  minimum_coverage_percent: 80
+
+artifacts:
+  required_files:
+    - products/playground/checklist/checklist.yml
+    - products/playground/metadata/product.yml
+    - schemas/playground/playground.schema.yml
+    - schemas/playground/sample_plan.schema.yml
+    - schemas/cli_error.json
+    - docs/playground/README.md
+    - docs/playground/export_bundle.md
+  required_directories:
+    - products/playground
+    - schemas/playground
+    - docs/playground
+    - tests/playground
+    - bootstraps/playground
+  build_outputs:
+    - bootstraps/playground/*.json
+    - artifacts/playground_validation_reports
+
+acceptance_criteria:
+  - id: ACPT-PG-001
+    description: "Three-run determinism hash parity across Python, WASM, and browser runtimes."
+    required: true
+  - id: ACPT-PG-002
+    description: "Export bundle validates against GuardBoard and GuardScore consumers."
+    required: true
+  - id: ACPT-PG-003
+    description: "Evaluator pipeline order mirrors guardsuite-core with documented deviations."
+    required: true
+  - id: ACPT-PG-004
+    description: "Performance budgets (memory, latency, stage budgets) are met in CI."
+    required: true
+  - id: ACPT-PG-005
+    description: "UI flags, API read-only contract, and telemetry redaction behave deterministically."
+    required: true
+
+cross_product_dependencies:
+  depends_on_products:
+    - guardboard
+    - guardscore
+    - vectorscan
+    - computeguard
+  depends_on_schemas:
+    - schemas/playground/playground.schema.yml
+    - schemas/playground/sample_plan.schema.yml
+    - schemas/cli_error.json
+  depends_on_pipeline: true
+
+provenance:
+  - "Drawn from GuardSuite Playground metadata (products/playground/metadata/product.yml)."
+  - "Aligned with guardsuite-core evaluator pipeline contract and DET-001 hashing spec."
+  - "WASM sandbox invariants trace back to GuardSuite security policy dated 2025-11-18."
+
+id: playground_checklist
+version: "2026.04"
+product: playground
+pillar: crosscut
+spec_source: "products/playground/metadata/product.yml"
+
+phases:
 
   # ============================================================
   # 1. INITIALIZATION & SPEC VALIDATION
   # ============================================================
   - phase: initialization
+    summary: "Load the spec, verify pins, and ensure release metadata + evaluator wiring are valid."
     items:
-
-      - INIT-001: load_spec_and_validate_yaml_structure
-      - INIT-002: validate_required_spec_sections_present
-      - INIT-003: verify_spec_version_and_metadata
-      - INIT-004: validate_core_dependency_pin(guardsuite-core>=2.3.0)
-      - INIT-005: validate_template_dependency_pin(guardsuite-template>=2.3.0)
-      - INIT-006: validate_schema_version_pin(playground.schema>=1.1.0)
-      - INIT-007: enforce_compatibility_window(12_months)
-      - INIT-008: validate_provenance_required_false
-      - INIT-009: ensure_examples_and_docs_present
-      - INIT-010: detect_template_core_drift
-      - INIT-011: ensure_release_metadata_valid
-      - INIT-012: verify_evaluator_pipeline_defined_and_complete
+      - id: INIT-001
+        title: load_spec_and_validate_yaml_structure
+      - id: INIT-002
+        title: validate_required_spec_sections_present
+      - id: INIT-003
+        title: verify_spec_version_and_metadata
+      - id: INIT-004
+        title: validate_core_dependency_pin_guardsuite_core_>=_2_3_0
+      - id: INIT-005
+        title: validate_template_dependency_pin_guardsuite_template_>=_2_3_0
+      - id: INIT-006
+        title: validate_schema_version_pin_playground_schema_>=_1_1_0
+      - id: INIT-007
+        title: enforce_compatibility_window_12_months
+      - id: INIT-008
+        title: validate_provenance_required_false
+      - id: INIT-009
+        title: ensure_examples_and_docs_present
+      - id: INIT-010
+        title: detect_template_core_drift
+      - id: INIT-011
+        title: ensure_release_metadata_valid
+      - id: INIT-012
+        title: verify_evaluator_pipeline_defined_and_complete
 
   # ============================================================
   # 2. SCHEMA & SAMPLE PLAN VALIDATION
   # ============================================================
   - phase: schema_validation
+    summary: "Validate canonical schemas, sample plans, and UTF-8 normalization."
     items:
-
-      - SCHEMA-001: validate_canonical_schema_json
-      - SCHEMA-002: validate_playground_schema_extends_core
-      - SCHEMA-003: ensure_no_duplicate_field_definitions
-      - SCHEMA-004: validate_stable_schema_bundle_ordering
-      - SCHEMA-005: compute_and_record_schema_bundle_hash
-      - SCHEMA-006: validate_schema_version_pin_resolution
-      - SCHEMA-007: validate_canonical_json_utf8_rules
-      - SCHEMA-008: ensure_fixed64_numeric_contract_supported
-      - SCHEMA-009: validate_timestamp_normalization_contract
-      - SCHEMA-010: validate_sample_plan_schema_exists
-      - SCHEMA-011: enforce_sample_plan_required_fields
-      - SCHEMA-012: snapshot_schema_test_for_sample_plans
+      - id: SCHEMA-001
+        title: validate_canonical_schema_json
+      - id: SCHEMA-002
+        title: validate_playground_schema_extends_core
+      - id: SCHEMA-003
+        title: ensure_no_duplicate_field_definitions
+      - id: SCHEMA-004
+        title: validate_stable_schema_bundle_ordering
+      - id: SCHEMA-005
+        title: compute_and_record_schema_bundle_hash
+      - id: SCHEMA-006
+        title: validate_schema_version_pin_resolution
+      - id: SCHEMA-007
+        title: validate_canonical_json_utf8_rules
+      - id: SCHEMA-008
+        title: ensure_fixed64_numeric_contract_supported
+      - id: SCHEMA-009
+        title: validate_timestamp_normalization_contract
+      - id: SCHEMA-010
+        title: validate_sample_plan_schema_exists
+      - id: SCHEMA-011
+        title: enforce_sample_plan_required_fields
+      - id: SCHEMA-012
+        title: snapshot_schema_test_for_sample_plans
 
   # ============================================================
   # 3. EVALUATOR PIPELINE CONTRACT & PARITY
   # ============================================================
   - phase: evaluator_pipeline
+    summary: "Guarantee evaluator ordering, determinism, and documented deviations from core."
     items:
-
-      - PIPE-001: load_authoritative_pipeline_from_core
-      - PIPE-002: enforce_stage_order_matches_core
-      - PIPE-003: validate_pipeline_stage_presence:
-          stages:
-            - load_profile
-            - initialize_context
-            - discover_resources
-            - gather_metadata
-            - evaluate_rules
-            - canonicalize
-            - snapshot_normalize
-            - emit_output
-
-      - PIPE-004: verify_no_randomness_or_local_time
-      - PIPE-005: validate_no_env_based_branching
-      - PIPE-006: validate_fixed64_applied_in_all_numeric_paths
-      - PIPE-007: enforce_canonical_json_utf8_output
-      - PIPE-008: enforce_snapshot_normalization_rules
-      - PIPE-009: evaluator_determinism_across_3_runs
-      - PIPE-010: python_vs_wasm_parity_test
-      - PIPE-011: evaluator_pipeline_drift_detection_against_template
-
-      # NEW BLOCK — evaluator parity with allowed deviations
-      - PIPE-012: evaluator_parity_contract:
-          matches_core_evaluator_pipeline: true
-          exceptions:
-            - provenance_optional
-            - ui_driven_sample_plan_loading
-            - fixpack_disabled_but_hints_allowed
+      - id: PIPE-001
+        title: load_authoritative_pipeline_from_core
+      - id: PIPE-002
+        title: enforce_stage_order_matches_core
+      - id: PIPE-003
+        title: validate_pipeline_stage_presence
+        tasks:
+          - |
+            stages:
+              - load_profile
+              - initialize_context
+              - discover_resources
+              - gather_metadata
+              - evaluate_rules
+              - canonicalize
+              - snapshot_normalize
+              - emit_output
+      - id: PIPE-004
+        title: verify_no_randomness_or_local_time
+      - id: PIPE-005
+        title: validate_no_env_based_branching
+      - id: PIPE-006
+        title: validate_fixed64_applied_in_all_numeric_paths
+      - id: PIPE-007
+        title: enforce_canonical_json_utf8_output
+      - id: PIPE-008
+        title: enforce_snapshot_normalization_rules
+      - id: PIPE-009
+        title: evaluator_determinism_across_three_runs
+      - id: PIPE-010
+        title: python_vs_wasm_parity_test
+      - id: PIPE-011
+        title: evaluator_pipeline_drift_detection_against_template
+      - id: PIPE-012
+        title: evaluator_parity_contract
+        tasks:
+          - |
+            matches_core_evaluator_pipeline: true
+            exceptions:
+              - provenance_optional
+              - ui_driven_sample_plan_loading
+              - fixpack_disabled_but_hints_allowed
 
   # ============================================================
   # 4. WASM SAFETY & FORBIDDEN OPERATIONS
   # ============================================================
   - phase: wasm_safety
+    summary: "Run WASM conformance and ensure no forbidden operations execute."
     items:
-
-      - WASM-001: run_wasm_conformance_tests
-      - WASM-002: validate_forbidden_operations_prohibited:
-          forbidden:
-            - randomness
-            - system_time
-            - locale
-            - filesystem_write
-            - environment_variable_access
-            - network_access
-            - dynamic_imports
-
-      - WASM-003: ensure_wasm_runtime_is_wasi_snapshot_preview1
-      - WASM-004: validate_no_direct_fs_access
-      - WASM-005: enforce_browser_sandbox_requirement
-      - WASM-006: validate_deterministic_wasm_runtime_behavior
-      - WASM-007: wasm_safe_json_and_svg_sanitization
+      - id: WASM-001
+        title: run_wasm_conformance_tests
+      - id: WASM-002
+        title: validate_forbidden_operations_prohibited
+        tasks:
+          - |
+            forbidden:
+              - randomness
+              - system_time
+              - locale
+              - filesystem_write
+              - environment_variable_access
+              - network_access
+              - dynamic_imports
+      - id: WASM-003
+        title: ensure_wasm_runtime_is_wasi_snapshot_preview1
+      - id: WASM-004
+        title: validate_no_direct_fs_access
+      - id: WASM-005
+        title: enforce_browser_sandbox_requirement
+      - id: WASM-006
+        title: validate_deterministic_wasm_runtime_behavior
+      - id: WASM-007
+        title: wasm_safe_json_and_svg_sanitization
 
   # ============================================================
   # 5. HASHING & NORMALIZATION (DET-001 ALIGNMENT)
   # ============================================================
   - phase: hashing_and_normalization
+    summary: "Align hashing + normalization with DET-001 fixed64 contract."
     items:
-
-      - HASH-001: validate_hashing_contract_alignment_with_DET001
-      - HASH-002: enforce_SHA256_hex_lowercase
-      - HASH-003: ensure_normalized_payload_used_for_hashing
-      - HASH-004: strip_diagnostics_only_for_hashing
-      - HASH-005: enforce_fixed64_numeric_contract
-      - HASH-006: enforce_recursive_key_ordering
-      - HASH-007: enforce_UTC_Z_timestamp_normalization
-      - HASH-008: prohibit_noncanonical_fields_in_hashing:
-          fields:
-            - diagnostics
-            - pipeline_trace
-            - lifecycle_state
-            - debug*
-            - ephemeral_*
-
-      - HASH-009: canonical_json_utf8_hash_view_tests
-      - HASH-010: python_wasm_binary_hash_parity_test
+      - id: HASH-001
+        title: validate_hashing_contract_alignment_with_DET001
+      - id: HASH-002
+        title: enforce_SHA256_hex_lowercase
+      - id: HASH-003
+        title: ensure_normalized_payload_used_for_hashing
+      - id: HASH-004
+        title: strip_diagnostics_only_for_hashing
+      - id: HASH-005
+        title: enforce_fixed64_numeric_contract
+      - id: HASH-006
+        title: enforce_recursive_key_ordering
+      - id: HASH-007
+        title: enforce_UTC_Z_timestamp_normalization
+      - id: HASH-008
+        title: prohibit_noncanonical_fields_in_hashing
+        tasks:
+          - |
+            fields:
+              - diagnostics
+              - pipeline_trace
+              - lifecycle_state
+              - "debug*"
+              - "ephemeral_*"
+      - id: HASH-009
+        title: canonical_json_utf8_hash_view_tests
+      - id: HASH-010
+        title: python_wasm_binary_hash_parity_test
 
   # ============================================================
   # 6. PROVENANCE RULES
   # ============================================================
   - phase: provenance
+    summary: "Treat provenance as optional but normalized when present."
     items:
-
-      - PROV-001: validate_provenance_optional
-      - PROV-002: normalize_provenance_if_present
-      - PROV-003: enforce_deterministic_timestamps_if_present
-      - PROV-004: provenance_included_in_export_bundle
-      - PROV-005: malformed_provenance_warn_and_normalize
-      - PROV-006: verify_no_strict_provenance_requirements_apply
+      - id: PROV-001
+        title: validate_provenance_optional
+      - id: PROV-002
+        title: normalize_provenance_if_present
+      - id: PROV-003
+        title: enforce_deterministic_timestamps_if_present
+      - id: PROV-004
+        title: provenance_included_in_export_bundle
+      - id: PROV-005
+        title: malformed_provenance_warn_and_normalize
+      - id: PROV-006
+        title: verify_no_strict_provenance_requirements_apply
 
   # ============================================================
   # 7. EXPORT BUNDLE CONTRACT
   # ============================================================
   - phase: export_bundle
+    summary: "Keep export bundle canonical, WASM safe, and consumer-ready."
     items:
-
-      - EXPORT-001: enforce_export_bundle_required_fields:
-          required:
-            - metadata
-            - issues
-            - guardscore_inputs
-            - badge_preview
-
-      - EXPORT-002: allow_optional_provenance
-      - EXPORT-003: enforce_canonical_serialization
-      - EXPORT-004: prohibit_noncanonical_fields
-      - EXPORT-005: ensure_wasm_safe_export_bundle
-      - EXPORT-006: export_bundle_snapshot_determinism_test
-      - EXPORT-007: guardboard_and_guardscore_compatibility_validation
+      - id: EXPORT-001
+        title: enforce_export_bundle_required_fields
+        tasks:
+          - |
+            required:
+              - metadata
+              - issues
+              - guardscore_inputs
+              - badge_preview
+      - id: EXPORT-002
+        title: allow_optional_provenance
+      - id: EXPORT-003
+        title: enforce_canonical_serialization
+      - id: EXPORT-004
+        title: prohibit_noncanonical_fields
+      - id: EXPORT-005
+        title: ensure_wasm_safe_export_bundle
+      - id: EXPORT-006
+        title: export_bundle_snapshot_determinism_test
+      - id: EXPORT-007
+        title: guardboard_and_guardscore_compatibility_validation
 
   # ============================================================
   # 8. UI FLAG CONSTRAINTS
   # ============================================================
   - phase: ui_flags
+    summary: "Restrict UI flags to the documented allow list and enforce CLI parity."
     items:
-
-      - UI-001: validate_ui_flags_allow_list:
-          allow:
-            - canonical_json
-            - badge_preview
-            - guardscore_preview
-
-      - UI-002: validate_ui_flags_forbidden_list:
-          forbid:
-            - custom_plugins
-            - network_calls
-            - user_uploaded_binaries
-            - arbitrary_javascript
-
-      - UI-003: enforce_ui_cli_flag_parity
-      - UI-004: validate_quickscore_flag_behavior
+      - id: UI-001
+        title: validate_ui_flags_allow_list
+        tasks:
+          - |
+            allow:
+              - canonical_json
+              - badge_preview
+              - guardscore_preview
+      - id: UI-002
+        title: validate_ui_flags_forbidden_list
+        tasks:
+          - |
+            forbid:
+              - custom_plugins
+              - network_calls
+              - user_uploaded_binaries
+              - arbitrary_javascript
+      - id: UI-003
+        title: enforce_ui_cli_flag_parity
+      - id: UI-004
+        title: validate_quickscore_flag_behavior
 
   # ============================================================
   # 9. READ-ONLY API GUARANTEE
   # ============================================================
   - phase: api_readonly
+    summary: "Playground API must stay read-only with deterministic responses."
     items:
-
-      - API-001: validate_rest_endpoint_defined
-      - API-002: validate_auth_token_requirement
-      - API-003: enforce_read_only_api_guarantee
-      - API-004: prohibit_write_operations
-      - API-005: validate_rate_limits
-      - API-006: ensure_deterministic_responses
-      - API-007: validate_export_bundle_api_endpoint
+      - id: API-001
+        title: validate_rest_endpoint_defined
+      - id: API-002
+        title: validate_auth_token_requirement
+      - id: API-003
+        title: enforce_read_only_api_guarantee
+      - id: API-004
+        title: prohibit_write_operations
+      - id: API-005
+        title: validate_rate_limits
+      - id: API-006
+        title: ensure_deterministic_responses
+      - id: API-007
+        title: validate_export_bundle_api_endpoint
 
   # ============================================================
   # 10. CANONICAL ERROR CONTRACT (SANDBOX)
   # ============================================================
   - phase: error_contract
+    summary: "Sandbox errors must match guardsuite-core CLI contract and stay deterministic."
     items:
-
-      - ERR-001: validate_canonical_error_schema_matches_core(
-          schema="guardsuite-core/schemas/cli_error.json"
-        )
-      - ERR-002: enforce_sandbox_safe_error_output
-      - ERR-003: enforce_deterministic_error_output
-      - ERR-004: enforce_error_field_redaction:
-          redacted_fields:
-            - local_paths
-            - host_env
-
-      - ERR-005: ensure_canonical_error_contract_in_wasm
+      - id: ERR-001
+        title: validate_canonical_error_schema_matches_core
+        tasks:
+          - |
+            schema: guardsuite-core/schemas/cli_error.json
+      - id: ERR-002
+        title: enforce_sandbox_safe_error_output
+      - id: ERR-003
+        title: enforce_deterministic_error_output
+      - id: ERR-004
+        title: enforce_error_field_redaction
+        tasks:
+          - |
+            redacted_fields:
+              - local_paths
+              - host_env
+      - id: ERR-005
+        title: ensure_canonical_error_contract_in_wasm
 
   # ============================================================
   # 11. TELEMETRY & REDACTION
   # ============================================================
   - phase: telemetry
+    summary: "Apply telemetry minimization, redaction, and WASM-safe logging."
     items:
-
-      - TEL-001: validate_telemetry_redaction_enabled
-      - TEL-002: enforce_redaction_rules:
-          redact:
-            - resource_id
-            - tenant_id
-            - secrets
-            - tokens
-            - code_snippets_raw
-
-      - TEL-003: validate_minimized_payloads
-      - TEL-004: prohibit_paste_content_upload
-      - TEL-005: prohibit_environment_leakage
-      - TEL-006: wasm_safe_telemetry_test
-      - TEL-007: telemetry_snapshot_obfuscation_test
+      - id: TEL-001
+        title: validate_telemetry_redaction_enabled
+      - id: TEL-002
+        title: enforce_redaction_rules
+        tasks:
+          - |
+            redact:
+              - resource_id
+              - tenant_id
+              - secrets
+              - tokens
+              - code_snippets_raw
+      - id: TEL-003
+        title: validate_minimized_payloads
+      - id: TEL-004
+        title: prohibit_paste_content_upload
+      - id: TEL-005
+        title: prohibit_environment_leakage
+      - id: TEL-006
+        title: wasm_safe_telemetry_test
+      - id: TEL-007
+        title: telemetry_snapshot_obfuscation_test
 
   # ============================================================
   # 12. PERFORMANCE & LATENCY
   # ============================================================
   - phase: performance
+    summary: "Meet memory + latency budgets and enforce stage-level targets."
     items:
-
-      - PERF-001: enforce_max_memory_mb(192)
-      - PERF-002: validate_expected_runtime(<=600ms)
-      - PERF-003: validate_wasm_runtime(<=750ms)
-      - PERF-004: validate_quickscore_threshold(200_resources)
-      - PERF-005: enforce_stage_budgets:
-          sample_plan_load_ms: 80
-          evaluator_init_ms: 100
-          rule_eval_ms: 250
-          badge_calc_ms: 120
-          canonicalize_output_ms: 80
-          export_payload_ms: 50
-
-      - PERF-006: validate_realtime_refresh_interval(60000ms)
+      - id: PERF-001
+        title: enforce_max_memory_mb_192
+      - id: PERF-002
+        title: validate_expected_runtime_<=_600ms
+      - id: PERF-003
+        title: validate_wasm_runtime_<=_750ms
+      - id: PERF-004
+        title: validate_quickscore_threshold_200_resources
+      - id: PERF-005
+        title: enforce_stage_budgets
+        tasks:
+          - |
+            sample_plan_load_ms: 80
+            evaluator_init_ms: 100
+            rule_eval_ms: 250
+            badge_calc_ms: 120
+            canonicalize_output_ms: 80
+            export_payload_ms: 50
+      - id: PERF-006
+        title: validate_realtime_refresh_interval_60000ms
 
   # ============================================================
   # 13. SECURITY & SANDBOXING
   # ============================================================
   - phase: security
+    summary: "Guarantee sandbox execution and forbid unsafe browser behaviors."
     items:
-
-      - SEC-001: enforce_no_external_calls_at_runtime
-      - SEC-002: enforce_input_sanitization
-      - SEC-003: enforce_svg_sanitization
-      - SEC-004: validate_wasm_compatibility
-      - SEC-005: enforce_mandatory_sandbox_execution
-      - SEC-006: validate_safe_error_reporting
-      - SEC-007: ensure_no_identity_spoofing_paths
-      - SEC-008: validate_browser_local_storage_contract:
-          deterministic_cache_allowed: false
-          session_storage_allowed: true
-          sensitive_data_prohibited: true
+      - id: SEC-001
+        title: enforce_no_external_calls_at_runtime
+      - id: SEC-002
+        title: enforce_input_sanitization
+      - id: SEC-003
+        title: enforce_svg_sanitization
+      - id: SEC-004
+        title: validate_wasm_compatibility
+      - id: SEC-005
+        title: enforce_mandatory_sandbox_execution
+      - id: SEC-006
+        title: validate_safe_error_reporting
+      - id: SEC-007
+        title: ensure_no_identity_spoofing_paths
+      - id: SEC-008
+        title: validate_browser_local_storage_contract
+        tasks:
+          - |
+            deterministic_cache_allowed: false
+            session_storage_allowed: true
+            sensitive_data_prohibited: true
 
   # ============================================================
   # 14. TESTING & CI
   # ============================================================
   - phase: testing
+    summary: "Execute the full CI matrix across runtimes and validate schema drift."
     items:
-
-      - TEST-001: run_unit_tests
-      - TEST-002: run_integration_tests
-      - TEST-003: run_snapshot_schema_tests
-      - TEST-004: run_wasm_conformance_tests
-      - TEST-005: run_snapshot_determinism_tests
-      - TEST-006: python_vs_wasm_comparison_tests
-      - TEST-007: enforce_test_coverage(>=80)
-      - TEST-008: validate_ci_jobs_match_spec
-      - TEST-009: enforce_ci_matrix(x86_64,arm64)
-      - TEST-010: validate_checklist_schema_valid
-      - TEST-011: detect_checklist_drift_against_spec
+      - id: TEST-001
+        title: run_unit_tests
+      - id: TEST-002
+        title: run_integration_tests
+      - id: TEST-003
+        title: run_snapshot_schema_tests
+      - id: TEST-004
+        title: run_wasm_conformance_tests
+      - id: TEST-005
+        title: run_snapshot_determinism_tests
+      - id: TEST-006
+        title: python_vs_wasm_comparison_tests
+      - id: TEST-007
+        title: enforce_test_coverage_>=_80
+      - id: TEST-008
+        title: validate_ci_jobs_match_spec
+      - id: TEST-009
+        title: enforce_ci_matrix_x86_64_and_arm64
+      - id: TEST-010
+        title: validate_checklist_schema_valid
+      - id: TEST-011
+        title: detect_checklist_drift_against_spec
 
   # ============================================================
   # 15. ACCEPTANCE CRITERIA
   # ============================================================
   - phase: acceptance
+    summary: "Final gauntlet verifying determinism, exports, WASM safety, and deliverables."
     items:
-
-      - ACPT-001: verify_all_schemas_pass_validation
-      - ACPT-002: verify_pipeline_parity_with_core
-      - ACPT-003: verify_hashing_contract_parity(python, wasm)
-      - ACPT-004: verify_export_bundle_contract_passes
-      - ACPT-005: verify_deterministic_output(3_run_hash_match)
-      - ACPT-006: verify_ui_and_api_output_contracts
-      - ACPT-007: verify_wasm_forbidden_operations_enforced
-      - ACPT-008: ensure_all_deliverables_exist
-      - ACPT-009: verify_no_security_or_sandbox_violations
+      - id: ACPT-001
+        title: verify_all_schemas_pass_validation
+      - id: ACPT-002
+        title: verify_pipeline_parity_with_core
+      - id: ACPT-003
+        title: verify_hashing_contract_parity_python_and_wasm
+      - id: ACPT-004
+        title: verify_export_bundle_contract_passes
+      - id: ACPT-005
+        title: verify_deterministic_output_three_run_hash_match
+      - id: ACPT-006
+        title: verify_ui_and_api_output_contracts
+      - id: ACPT-007
+        title: verify_wasm_forbidden_operations_enforced
+      - id: ACPT-008
+        title: ensure_all_deliverables_exist
+      - id: ACPT-009
+        title: verify_no_security_or_sandbox_violations
+
+legacy_checklist_dump: |-
+  checklist:
+    id: playground-checklist
+    version: "2026.04"
+    product: playground
+    pillar: crosscut
+
+    phases:
+
+    # ============================================================
+    # 1. INITIALIZATION & SPEC VALIDATION
+    # ============================================================
+    - phase: initialization
+      items:
+
+        - INIT-001: load_spec_and_validate_yaml_structure
+        - INIT-002: validate_required_spec_sections_present
+        - INIT-003: verify_spec_version_and_metadata
+        - INIT-004: validate_core_dependency_pin(guardsuite-core>=2.3.0)
+        - INIT-005: validate_template_dependency_pin(guardsuite-template>=2.3.0)
+        - INIT-006: validate_schema_version_pin(playground.schema>=1.1.0)
+        - INIT-007: enforce_compatibility_window(12_months)
+        - INIT-008: validate_provenance_required_false
+        - INIT-009: ensure_examples_and_docs_present
+        - INIT-010: detect_template_core_drift
+        - INIT-011: ensure_release_metadata_valid
+        - INIT-012: verify_evaluator_pipeline_defined_and_complete
+
+    # ============================================================
+    # 2. SCHEMA & SAMPLE PLAN VALIDATION
+    # ============================================================
+    - phase: schema_validation
+      items:
+
+        - SCHEMA-001: validate_canonical_schema_json
+        - SCHEMA-002: validate_playground_schema_extends_core
+        - SCHEMA-003: ensure_no_duplicate_field_definitions
+        - SCHEMA-004: validate_stable_schema_bundle_ordering
+        - SCHEMA-005: compute_and_record_schema_bundle_hash
+        - SCHEMA-006: validate_schema_version_pin_resolution
+        - SCHEMA-007: validate_canonical_json_utf8_rules
+        - SCHEMA-008: ensure_fixed64_numeric_contract_supported
+        - SCHEMA-009: validate_timestamp_normalization_contract
+        - SCHEMA-010: validate_sample_plan_schema_exists
+        - SCHEMA-011: enforce_sample_plan_required_fields
+        - SCHEMA-012: snapshot_schema_test_for_sample_plans
+
+    # ============================================================
+    # 3. EVALUATOR PIPELINE CONTRACT & PARITY
+    # ============================================================
+    - phase: evaluator_pipeline
+      items:
+
+        - PIPE-001: load_authoritative_pipeline_from_core
+        - PIPE-002: enforce_stage_order_matches_core
+        - PIPE-003: validate_pipeline_stage_presence:
+            stages:
+              - load_profile
+              - initialize_context
+              - discover_resources
+              - gather_metadata
+              - evaluate_rules
+              - canonicalize
+              - snapshot_normalize
+              - emit_output
+
+        - PIPE-004: verify_no_randomness_or_local_time
+        - PIPE-005: validate_no_env_based_branching
+        - PIPE-006: validate_fixed64_applied_in_all_numeric_paths
+        - PIPE-007: enforce_canonical_json_utf8_output
+        - PIPE-008: enforce_snapshot_normalization_rules
+        - PIPE-009: evaluator_determinism_across_3_runs
+        - PIPE-010: python_vs_wasm_parity_test
+        - PIPE-011: evaluator_pipeline_drift_detection_against_template
+
+        # NEW BLOCK — evaluator parity with allowed deviations
+        - PIPE-012: evaluator_parity_contract:
+            matches_core_evaluator_pipeline: true
+            exceptions:
+              - provenance_optional
+              - ui_driven_sample_plan_loading
+              - fixpack_disabled_but_hints_allowed
+
+    # ============================================================
+    # 4. WASM SAFETY & FORBIDDEN OPERATIONS
+    # ============================================================
+    - phase: wasm_safety
+      items:
+
+        - WASM-001: run_wasm_conformance_tests
+        - WASM-002: validate_forbidden_operations_prohibited:
+            forbidden:
+              - randomness
+              - system_time
+              - locale
+              - filesystem_write
+              - environment_variable_access
+              - network_access
+              - dynamic_imports
+
+        - WASM-003: ensure_wasm_runtime_is_wasi_snapshot_preview1
+        - WASM-004: validate_no_direct_fs_access
+        - WASM-005: enforce_browser_sandbox_requirement
+        - WASM-006: validate_deterministic_wasm_runtime_behavior
+        - WASM-007: wasm_safe_json_and_svg_sanitization
+
+    # ============================================================
+    # 5. HASHING & NORMALIZATION (DET-001 ALIGNMENT)
+    # ============================================================
+    - phase: hashing_and_normalization
+      items:
+
+        - HASH-001: validate_hashing_contract_alignment_with_DET001
+        - HASH-002: enforce_SHA256_hex_lowercase
+        - HASH-003: ensure_normalized_payload_used_for_hashing
+        - HASH-004: strip_diagnostics_only_for_hashing
+        - HASH-005: enforce_fixed64_numeric_contract
+        - HASH-006: enforce_recursive_key_ordering
+        - HASH-007: enforce_UTC_Z_timestamp_normalization
+        - HASH-008: prohibit_noncanonical_fields_in_hashing:
+            fields:
+              - diagnostics
+              - pipeline_trace
+              - lifecycle_state
+              - debug*
+              - ephemeral_*
+
+        - HASH-009: canonical_json_utf8_hash_view_tests
+        - HASH-010: python_wasm_binary_hash_parity_test
+
+    # ============================================================
+    # 6. PROVENANCE RULES
+    # ============================================================
+    - phase: provenance
+      items:
+
+        - PROV-001: validate_provenance_optional
+        - PROV-002: normalize_provenance_if_present
+        - PROV-003: enforce_deterministic_timestamps_if_present
+        - PROV-004: provenance_included_in_export_bundle
+        - PROV-005: malformed_provenance_warn_and_normalize
+        - PROV-006: verify_no_strict_provenance_requirements_apply
+
+    # ============================================================
+    # 7. EXPORT BUNDLE CONTRACT
+    # ============================================================
+    - phase: export_bundle
+      items:
+
+        - EXPORT-001: enforce_export_bundle_required_fields:
+            required:
+              - metadata
+              - issues
+              - guardscore_inputs
+              - badge_preview
+
+        - EXPORT-002: allow_optional_provenance
+        - EXPORT-003: enforce_canonical_serialization
+        - EXPORT-004: prohibit_noncanonical_fields
+        - EXPORT-005: ensure_wasm_safe_export_bundle
+        - EXPORT-006: export_bundle_snapshot_determinism_test
+        - EXPORT-007: guardboard_and_guardscore_compatibility_validation
+
+    # ============================================================
+    # 8. UI FLAG CONSTRAINTS
+    # ============================================================
+    - phase: ui_flags
+      items:
+
+        - UI-001: validate_ui_flags_allow_list:
+            allow:
+              - canonical_json
+              - badge_preview
+              - guardscore_preview
+
+        - UI-002: validate_ui_flags_forbidden_list:
+            forbid:
+              - custom_plugins
+              - network_calls
+              - user_uploaded_binaries
+              - arbitrary_javascript
+
+        - UI-003: enforce_ui_cli_flag_parity
+        - UI-004: validate_quickscore_flag_behavior
+
+    # ============================================================
+    # 9. READ-ONLY API GUARANTEE
+    # ============================================================
+    - phase: api_readonly
+      items:
+
+        - API-001: validate_rest_endpoint_defined
+        - API-002: validate_auth_token_requirement
+        - API-003: enforce_read_only_api_guarantee
+        - API-004: prohibit_write_operations
+        - API-005: validate_rate_limits
+        - API-006: ensure_deterministic_responses
+        - API-007: validate_export_bundle_api_endpoint
+
+    # ============================================================
+    # 10. CANONICAL ERROR CONTRACT (SANDBOX)
+    # ============================================================
+    - phase: error_contract
+      items:
+
+        - ERR-001: validate_canonical_error_schema_matches_core(
+            schema="guardsuite-core/schemas/cli_error.json"
+          )
+        - ERR-002: enforce_sandbox_safe_error_output
+        - ERR-003: enforce_deterministic_error_output
+        - ERR-004: enforce_error_field_redaction:
+            redacted_fields:
+              - local_paths
+              - host_env
+
+        - ERR-005: ensure_canonical_error_contract_in_wasm
+
+    # ============================================================
+    # 11. TELEMETRY & REDACTION
+    # ============================================================
+    - phase: telemetry
+      items:
+
+        - TEL-001: validate_telemetry_redaction_enabled
+        - TEL-002: enforce_redaction_rules:
+            redact:
+              - resource_id
+              - tenant_id
+              - secrets
+              - tokens
+              - code_snippets_raw
+
+        - TEL-003: validate_minimized_payloads
+        - TEL-004: prohibit_paste_content_upload
+        - TEL-005: prohibit_environment_leakage
+        - TEL-006: wasm_safe_telemetry_test
+        - TEL-007: telemetry_snapshot_obfuscation_test
+
+    # ============================================================
+    # 12. PERFORMANCE & LATENCY
+    # ============================================================
+    - phase: performance
+      items:
+
+        - PERF-001: enforce_max_memory_mb(192)
+        - PERF-002: validate_expected_runtime(<=600ms)
+        - PERF-003: validate_wasm_runtime(<=750ms)
+        - PERF-004: validate_quickscore_threshold(200_resources)
+        - PERF-005: enforce_stage_budgets:
+            sample_plan_load_ms: 80
+            evaluator_init_ms: 100
+            rule_eval_ms: 250
+            badge_calc_ms: 120
+            canonicalize_output_ms: 80
+            export_payload_ms: 50
+
+        - PERF-006: validate_realtime_refresh_interval(60000ms)
+
+    # ============================================================
+    # 13. SECURITY & SANDBOXING
+    # ============================================================
+    - phase: security
+      items:
+
+        - SEC-001: enforce_no_external_calls_at_runtime
+        - SEC-002: enforce_input_sanitization
+        - SEC-003: enforce_svg_sanitization
+        - SEC-004: validate_wasm_compatibility
+        - SEC-005: enforce_mandatory_sandbox_execution
+        - SEC-006: validate_safe_error_reporting
+        - SEC-007: ensure_no_identity_spoofing_paths
+        - SEC-008: validate_browser_local_storage_contract:
+            deterministic_cache_allowed: false
+            session_storage_allowed: true
+            sensitive_data_prohibited: true
+
+    # ============================================================
+    # 14. TESTING & CI
+    # ============================================================
+    - phase: testing
+      items:
+
+        - TEST-001: run_unit_tests
+        - TEST-002: run_integration_tests
+        - TEST-003: run_snapshot_schema_tests
+        - TEST-004: run_wasm_conformance_tests
+        - TEST-005: run_snapshot_determinism_tests
+        - TEST-006: python_vs_wasm_comparison_tests
+        - TEST-007: enforce_test_coverage(>=80)
+        - TEST-008: validate_ci_jobs_match_spec
+        - TEST-009: enforce_ci_matrix(x86_64,arm64)
+        - TEST-010: validate_checklist_schema_valid
+        - TEST-011: detect_checklist_drift_against_spec
+
+    # ============================================================
+    # 15. ACCEPTANCE CRITERIA
+    # ============================================================
+    - phase: acceptance
+      items:
+
+        - ACPT-001: verify_all_schemas_pass_validation
+        - ACPT-002: verify_pipeline_parity_with_core
+        - ACPT-003: verify_hashing_contract_parity(python, wasm)
+        - ACPT-004: verify_export_bundle_contract_passes
+        - ACPT-005: verify_deterministic_output(3_run_hash_match)
+        - ACPT-006: verify_ui_and_api_output_contracts
+        - ACPT-007: verify_wasm_forbidden_operations_enforced
+        - ACPT-008: ensure_all_deliverables_exist
+        - ACPT-009: verify_no_security_or_sandbox_violations

```
