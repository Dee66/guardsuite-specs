diff --git a/products/pipelinescan/checklist/checklist.yml b/products/pipelinescan/checklist/checklist.yml
index 031390e..1d6c858 100644
--- a/products/pipelinescan/checklist/checklist.yml
+++ b/products/pipelinescan/checklist/checklist.yml
@@ -1,163 +1,351 @@
-checklist:
-  id: pipelinescan-checklist
-  version: "2026.04"
-  product: pipelinescan
-  pillar: pipeline
+# products/pipelinescan/checklist/checklist.yml
+# Strategy-D canonical checklist for PipelineScan (free scanner blueprint)
 
-  phases:
+metadata:
+  product_id: pipelinescan
+  checklist_version: "2026.04"
+  last_updated: "2025-11-25T00:00:00Z"
+  owner: "GuardSuite Platform Team"
+  stability: ga
+
+structure_requirements:
+  - id: STRUCT-PS-001
+    description: "Preserve all historical PipelineScan phases and item wording while embedding canonical framing."
+    required: true
+  - id: STRUCT-PS-002
+    description: "Honor Strategy-D ordering (metadata ⇒ requirements ⇒ phases ⇒ acceptance)."
+    required: true
+
+documentation_requirements:
+  readme_required: true
+  product_docs_required: true
+  api_reference_required: true
+  examples_required: true
+  changelog_required: true
+  release_notes_required: false
+
+schema_requirements:
+  canonical_schema_required: true
+  metadata_schema_required: true
+  provenance_schema_required: true
+  fragment_schemas_required: true
+  additional_schemas:
+    - schemas/pipelinescan/canonical_output.json
+    - schemas/pipelinescan/export_bundle.json
+    - schemas/pipelinescan/provenance.json
+    - schemas/pipelinescan/telemetry.json
+
+evaluator_requirements:
+  pipeline_must_match_template: true
+  canonicalization_required: true
+  wasm_safety_required: true
+  deterministic_output_required: true
+  timestamp_normalization_required: true
+  prohibited_overrides:
+    - canonicalization_rules
+    - evaluator.pipeline_stage_order
+    - wasm_runtime_contract
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
+    - products/pipelinescan/spec.yml
+    - schemas/pipelinescan/canonical_output.json
+    - schemas/pipelinescan/export_bundle.json
+    - schemas/pipelinescan/telemetry.json
+    - ci/pipelinescan-ci.yml
+  required_directories:
+    - schemas/pipelinescan
+    - adapters
+    - rules/pipelinescan
+    - tests
+    - docs
+    - examples/scenarios
+  build_outputs:
+    - artifacts/snapshots
+    - artifacts/schema_reports
+
+acceptance_criteria:
+  - id: ACPT-PS-001
+    description: "Canonical output validates with DET-001 normalization and schema bundle."
+    required: true
+  - id: ACPT-PS-002
+    description: "Snapshot determinism confirmed across 3 runs and runtimes."
+    required: true
+  - id: ACPT-PS-003
+    description: "Security/IP guardrails (no binaries, no fixpacks) enforced."
+    required: true
+  - id: ACPT-PS-004
+    description: "CLI and telemetry contracts pass automated validation."
+    required: true
+
+cross_product_dependencies:
+  depends_on_products:
+    - guardscore
+    - guardboard
+  depends_on_schemas:
+    - guardsuite-core/canonical_schema.json
+    - guardsuite-core/provenance_schema.json
+  depends_on_pipeline: true
+
+provenance:
+  - "Checklist derived from Strategy-D canonical free-scanner baseline."
+  - "Aligned with PipelineScan spec products/pipelinescan/spec.yml."
+
+id: pipelinescan_checklist
+version: "2026.04"
+product: pipelinescan
+pillar: pipeline
+spec_source: "products/pipelinescan/spec.yml"
+
+phases:
 
   # ============================================================
   # PHASE 1 — INITIALIZATION & REPO STRUCTURE
   # ============================================================
   - phase: initialization
+    summary: "Validate repo layout, spec alignment, and absence of forbidden assets."
     items:
-      - INIT-001: verify_repository_structure_matches_spec
-      - INIT-002: ensure_required_directories_exist:
-          include:
-            - schemas/pipelinescan
-            - rules/pipelinescan
-            - adapters
-            - tests
-            - ci
-            - docs
-      - INIT-003: validate_spec_version_and_metadata
-      - INIT-004: confirm_pipelinescan_is_free_scanner (non_ip_exposing)
-      - INIT-005: validate_core_dependency_pin("guardsuite-core@>=2.3.0,<3.0.0")
-      - INIT-006: validate_template_pipeline_contract_synced
-      - INIT-007: detect_template_core_drift
-      - INIT-008: enforce_semver_and_release_metadata_valid
-      - INIT-009: validate_no_core_binaries_present
-      - INIT-010: validate_no_fixpack_content_present
+      - id: INIT-001
+        description: "verify_repository_structure_matches_spec"
+      - id: INIT-002
+        description: "ensure_required_directories_exist"
+        include:
+          - schemas/pipelinescan
+          - rules/pipelinescan
+          - adapters
+          - tests
+          - ci
+          - docs
+      - id: INIT-003
+        description: "validate_spec_version_and_metadata"
+      - id: INIT-004
+        description: "confirm_pipelinescan_is_free_scanner (non_ip_exposing)"
+      - id: INIT-005
+        description: "validate_core_dependency_pin(\"guardsuite-core@>=2.3.0,<3.0.0\")"
+      - id: INIT-006
+        description: "validate_template_pipeline_contract_synced"
+      - id: INIT-007
+        description: "detect_template_core_drift"
+      - id: INIT-008
+        description: "enforce_semver_and_release_metadata_valid"
+      - id: INIT-009
+        description: "validate_no_core_binaries_present"
+      - id: INIT-010
+        description: "validate_no_fixpack_content_present"
 
   # ============================================================
   # PHASE 2 — SCHEMA VALIDATION & CANONICAL OUTPUT
   # ============================================================
   - phase: schema_validation
+    summary: "Ensure canonical schemas, bundles, and exports match template contracts."
     items:
-      - SCHEMA-001: validate_canonical_output_schema_exists
-      - SCHEMA-002: validate_schema_extends_core_fragments
-      - SCHEMA-003: validate_schema_fields_required:
-          fields:
-            - metadata
-            - issues
-            - provenance(optional)
-      - SCHEMA-004: detect_duplicate_field_definitions
-      - SCHEMA-005: validate_stable_schema_bundle_ordering
-      - SCHEMA-006: compute_schema_bundle_hash
-      - SCHEMA-007: validate_schema_version_pin
-      - SCHEMA-008: validate_export_bundle_contract:
-          required_fields:
-            - metadata
-            - issues
-            - guardscore_inputs
-      - SCHEMA-009: validate_sample_plan_compatibility_if_present
-      - SCHEMA-010: enforce_export_bundle_wasm_safety_and_forbidden_field_rules   # ← Added
+      - id: SCHEMA-001
+        description: "validate_canonical_output_schema_exists"
+      - id: SCHEMA-002
+        description: "validate_schema_extends_core_fragments"
+      - id: SCHEMA-003
+        description: "validate_schema_fields_required"
+        fields:
+          - metadata
+          - issues
+          - provenance(optional)
+      - id: SCHEMA-004
+        description: "detect_duplicate_field_definitions"
+      - id: SCHEMA-005
+        description: "validate_stable_schema_bundle_ordering"
+      - id: SCHEMA-006
+        description: "compute_schema_bundle_hash"
+      - id: SCHEMA-007
+        description: "validate_schema_version_pin"
+      - id: SCHEMA-008
+        description: "validate_export_bundle_contract"
+        required_fields:
+          - metadata
+          - issues
+          - guardscore_inputs
+      - id: SCHEMA-009
+        description: "validate_sample_plan_compatibility_if_present"
+      - id: SCHEMA-010
+        description: "enforce_export_bundle_wasm_safety_and_forbidden_field_rules"
 
   # ============================================================
   # PHASE 3 — EVALUATOR PIPELINE (TEMPLATE-ALIGNED)
   # ============================================================
   - phase: evaluator_pipeline
+    summary: "Run evaluator stages exactly as provided by template with deterministic behavior."
     items:
-      - PIPE-001: load_canonical_pipeline_from_template
-      - PIPE-002: validate_stage_order_matches_template:
-          stages:
-            - load_profile
-            - initialize_context
-            - load_schema
-            - validate_schema
-            - discover_ci_resources
-            - gather_metadata
-            - evaluate_rules
-            - canonicalize_output
-            - snapshot_normalize
-            - emit_output
-      - PIPE-003: enforce_no_remediation_execution
-      - PIPE-004: enforce_no_core_binaries_loaded
-      - PIPE-005: ensure_pipeline_is_deterministic
-      - PIPE-006: evaluator_must_preserve_pipeline_trace_outside_hash
-      - PIPE-007: evaluator_parity_python_vs_wasm
-      - PIPE-008: evaluator_mutation_safety(no_resource_mutation)
+      - id: PIPE-001
+        description: "load_canonical_pipeline_from_template"
+      - id: PIPE-002
+        description: "validate_stage_order_matches_template"
+        stages:
+          - load_profile
+          - initialize_context
+          - load_schema
+          - validate_schema
+          - discover_ci_resources
+          - gather_metadata
+          - evaluate_rules
+          - canonicalize_output
+          - snapshot_normalize
+          - emit_output
+      - id: PIPE-003
+        description: "enforce_no_remediation_execution"
+      - id: PIPE-004
+        description: "enforce_no_core_binaries_loaded"
+      - id: PIPE-005
+        description: "ensure_pipeline_is_deterministic"
+      - id: PIPE-006
+        description: "evaluator_must_preserve_pipeline_trace_outside_hash"
+      - id: PIPE-007
+        description: "evaluator_parity_python_vs_wasm"
+      - id: PIPE-008
+        description: "evaluator_mutation_safety(no_resource_mutation)"
 
   # ============================================================
   # PHASE 4 — RESOURCE CAPABILITIES & ADAPTERS
   # ============================================================
   - phase: adapters
+    summary: "Validate adapters remain read-only, WASM-safe, and follow manifest contract."
     items:
-      - ADAPT-001: validate_adapter_manifest_structure
-      - ADAPT-002: validate_adapter_capabilities:
-          required:
-            - ci_platform_metadata
-            - artifact_manifest_parsing
-      - ADAPT-003: ensure_no_secrets_collected
-      - ADAPT-004: validate_read_only_adapter_behavior
-      - ADAPT-005: canonicalize_adapter_resource_ids
-      - ADAPT-006: ensure_adapter_follows_deterministic_metadata_contract
-      - ADAPT-007: ensure_no_provider_specific_ip_leakage
-      - ADAPT-008: validate_adapter_wasm_safety                       # ← Added
-      - ADAPT-009: static_analysis_no_mutating_operations_in_adapters # ← Added
+      - id: ADAPT-001
+        description: "validate_adapter_manifest_structure"
+      - id: ADAPT-002
+        description: "validate_adapter_capabilities"
+        required:
+          - ci_platform_metadata
+          - artifact_manifest_parsing
+      - id: ADAPT-003
+        description: "ensure_no_secrets_collected"
+      - id: ADAPT-004
+        description: "validate_read_only_adapter_behavior"
+      - id: ADAPT-005
+        description: "canonicalize_adapter_resource_ids"
+      - id: ADAPT-006
+        description: "ensure_adapter_follows_deterministic_metadata_contract"
+      - id: ADAPT-007
+        description: "ensure_no_provider_specific_ip_leakage"
+      - id: ADAPT-008
+        description: "validate_adapter_wasm_safety"
+      - id: ADAPT-009
+        description: "static_analysis_no_mutating_operations_in_adapters"
 
   # ============================================================
   # PHASE 5 — RULE SYSTEM (READ-ONLY)
   # ============================================================
   - phase: rule_system
+    summary: "Guarantee rule bundle metadata completeness and deterministic behavior."
     items:
-      - RULE-001: validate_rule_id_namespace("pipelinescan")
-      - RULE-002: ensure_all_rules_have_required_fields:
+      - id: RULE-001
+        description: "validate_rule_id_namespace(\"pipelinescan\")"
+      - id: RULE-002
+        description: "ensure_all_rules_have_required_fields"
+        required_fields:
           - rule_id
           - severity
           - description
-      - RULE-003: validate_rules_deterministic
-      - RULE-004: validate_no_rule_invokes_remediation
-      - RULE-005: ensure_rule_metadata_has_no_ip_sensitive_content
-      - RULE-006: validate_rule_severity_buckets(critical/high/medium/low/info)
-      - RULE-007: validate_rule_metadata_completeness(rationale, group, explain, remediation_hint_id) # ← Added
+      - id: RULE-003
+        description: "validate_rules_deterministic"
+      - id: RULE-004
+        description: "validate_no_rule_invokes_remediation"
+      - id: RULE-005
+        description: "ensure_rule_metadata_has_no_ip_sensitive_content"
+      - id: RULE-006
+        description: "validate_rule_severity_buckets(critical/high/medium/low/info)"
+      - id: RULE-007
+        description: "validate_rule_metadata_completeness(rationale, group, explain, remediation_hint_id)"
 
   # ============================================================
   # PHASE 6 — DETERMINISM & HASHING (DET-001 ALIGNMENT)
   # ============================================================
   - phase: determinism
+    summary: "Apply DET-001 normalization and hashing rules across payloads and runtimes."
     items:
-      - DET-001: normalize_payload_according_to_DET001
-      - DET-002: enforce_canonical_key_ordering
-      - DET-003: enforce_fixed64_numeric_contract
-      - DET-004: normalize_paths (OS-independent)
-      - DET-005: normalize_timestamps(utc_iso8601_z)
-      - DET-006: strip_diagnostics_only_for_hashing
-      - DET-007: hashing_contract_sha256_canonical_json_utf8
-      - DET-008: enforce_no_nondeterministic_io
-      - DET-009: snapshot_3run_identical_hash_required
-      - DET-010: python_vs_wasm_hash_parity
+      - id: DET-001
+        description: "normalize_payload_according_to_DET001"
+      - id: DET-002
+        description: "enforce_canonical_key_ordering"
+      - id: DET-003
+        description: "enforce_fixed64_numeric_contract"
+      - id: DET-004
+        description: "normalize_paths (OS-independent)"
+      - id: DET-005
+        description: "normalize_timestamps(utc_iso8601_z)"
+      - id: DET-006
+        description: "strip_diagnostics_only_for_hashing"
+      - id: DET-007
+        description: "hashing_contract_sha256_canonical_json_utf8"
+      - id: DET-008
+        description: "enforce_no_nondeterministic_io"
+      - id: DET-009
+        description: "snapshot_3run_identical_hash_required"
+      - id: DET-010
+        description: "python_vs_wasm_hash_parity"
 
   # ============================================================
   # PHASE 7 — PROVENANCE (OPTIONAL BUT VALIDATED)
   # ============================================================
   - phase: provenance
+    summary: "Allow optional provenance while enforcing validation when present."
     items:
-      - PROV-001: validate_provenance_if_present
-      - PROV-002: allow_missing_provenance(but_mark_source_unverified)
-      - PROV-003: validate_signature_if_provided
-      - PROV-004: canonicalize_provenance_fields
-      - PROV-005: ensure_no_external_signature_resolution
-      - PROV-006: provenance_excluded_from_hash_if_noncanonical
+      - id: PROV-001
+        description: "validate_provenance_if_present"
+      - id: PROV-002
+        description: "allow_missing_provenance(but_mark_source_unverified)"
+      - id: PROV-003
+        description: "validate_signature_if_provided"
+      - id: PROV-004
+        description: "canonicalize_provenance_fields"
+      - id: PROV-005
+        description: "ensure_no_external_signature_resolution"
+      - id: PROV-006
+        description: "provenance_excluded_from_hash_if_noncanonical"
 
   # ============================================================
   # PHASE 8 — FIXPACK / REMEDIATION SAFEGUARDS
   # ============================================================
   - phase: remediation_safeguards
+    summary: "Enforce no-remediation posture and ban fixpack artifacts."
     items:
-      - FIX-001: ensure_fixpack_included_false
-      - FIX-002: validate_no_fixpack_directories_present
-      - FIX-003: validate_no_patch_snippets_or_remediation_code
-      - FIX-004: ensure_fixpack_references_are_opaque_ids_only
-      - FIX-005: enforce_no_fixpack_execution_paths_in_code
+      - id: FIX-001
+        description: "ensure_fixpack_included_false"
+      - id: FIX-002
+        description: "validate_no_fixpack_directories_present"
+      - id: FIX-003
+        description: "validate_no_patch_snippets_or_remediation_code"
+      - id: FIX-004
+        description: "ensure_fixpack_references_are_opaque_ids_only"
+      - id: FIX-005
+        description: "enforce_no_fixpack_execution_paths_in_code"
 
   # ============================================================
   # PHASE 9 — WASM SAFETY
   # ============================================================
   - phase: wasm_safety
+    summary: "Meet WASM runtime restrictions and detectors."
     items:
-      - WASM-001: enforce_wasm_compatible_flag
-      - WASM-002: detect_forbidden_operations:
+      - id: WASM-001
+        description: "enforce_wasm_compatible_flag"
+      - id: WASM-002
+        description: "detect_forbidden_operations"
+        forbidden_ops:
           - randomness
           - system_time
           - locale
@@ -165,93 +353,149 @@ checklist:
           - environment_variable_access
           - network_access
           - dynamic_imports
-      - WASM-003: wasm_parity_test
-      - WASM-004: memory_safe_path_normalization
+      - id: WASM-003
+        description: "wasm_parity_test"
+      - id: WASM-004
+        description: "memory_safe_path_normalization"
 
   # ============================================================
   # PHASE 10 — SECURITY & IP PROTECTION
   # ============================================================
   - phase: security
+    summary: "Verify sanitization, no IP leakage, and template-aligned safeguards."
     items:
-      - SEC-001: enforce_sanitize_all_inputs
-      - SEC-002: validate_no_external_calls
-      - SEC-003: enforce_forbidden_ip_exposure_rules
-      - SEC-004: ensure_no_core_binary_files_present
-      - SEC-005: ensure_no_fixpack_snippet_presence
-      - SEC-006: enforce_telemetry_redaction_rules
-      - SEC-007: forbid_leaking_internal_abi_references
-      - SEC-008: validate_readonly_scanner_behavior
+      - id: SEC-001
+        description: "enforce_sanitize_all_inputs"
+      - id: SEC-002
+        description: "validate_no_external_calls"
+      - id: SEC-003
+        description: "enforce_forbidden_ip_exposure_rules"
+      - id: SEC-004
+        description: "ensure_no_core_binary_files_present"
+      - id: SEC-005
+        description: "ensure_no_fixpack_snippet_presence"
+      - id: SEC-006
+        description: "enforce_telemetry_redaction_rules"
+      - id: SEC-007
+        description: "forbid_leaking_internal_abi_references"
+      - id: SEC-008
+        description: "validate_readonly_scanner_behavior"
 
   # ============================================================
   # PHASE 11 — TELEMETRY & OBSERVABILITY
   # ============================================================
   - phase: observability
+    summary: "Ensure telemetry payloads obey size, structure, and redaction contracts."
     items:
-      - OBS-001: validate_telemetry_payloads
-      - OBS-002: enforce_redaction(resource_id, tenant_id, tokens)
-      - OBS-003: enforce_payload_limits(<=16000_bytes)
-      - OBS-004: structured_json_logs_required
-      - OBS-005: deterministic_logging_required
-      - OBS-006: validate_metrics_exist:
+      - id: OBS-001
+        description: "validate_telemetry_payloads"
+      - id: OBS-002
+        description: "enforce_redaction(resource_id, tenant_id, tokens)"
+      - id: OBS-003
+        description: "enforce_payload_limits(<=16000_bytes)"
+      - id: OBS-004
+        description: "structured_json_logs_required"
+      - id: OBS-005
+        description: "deterministic_logging_required"
+      - id: OBS-006
+        description: "validate_metrics_exist"
+        metrics:
           - pipelinescan_runs_total
           - pipelinescan_issues_total
           - pipelinescan_partial_inputs_total
-      - OBS-007: enforce_no_sensitive_data_in_logs
-      - OBS-008: validate_telemetry_event_limits(max_events_per_scan=50, max_events_per_rule_execution=5)  # ← Added
+      - id: OBS-007
+        description: "enforce_no_sensitive_data_in_logs"
+      - id: OBS-008
+        description: "validate_telemetry_event_limits(max_events_per_scan=50, max_events_per_rule_execution=5)"
 
   # ============================================================
   # PHASE 12 — CLI CONTRACT
   # ============================================================
   - phase: cli
+    summary: "Verify CLI verbs, flags, help, and outputs align with canonical schema."
     items:
-      - CLI-001: validate_cli_entrypoint
-      - CLI-002: validate_supported_flags
-      - CLI-003: validate_reserved_flags_behave_correctly
-      - CLI-004: machine_parseable_help_required
-      - CLI-005: validate_exit_code_mapping
-      - CLI-006: canonical_error_output_required
-      - CLI-007: ensure_cli_does_not_expose_internal_ip
+      - id: CLI-001
+        description: "validate_cli_entrypoint"
+      - id: CLI-002
+        description: "validate_supported_flags"
+      - id: CLI-003
+        description: "validate_reserved_flags_behave_correctly"
+      - id: CLI-004
+        description: "machine_parseable_help_required"
+      - id: CLI-005
+        description: "validate_exit_code_mapping"
+      - id: CLI-006
+        description: "canonical_error_output_required"
+      - id: CLI-007
+        description: "ensure_cli_does_not_expose_internal_ip"
 
   # ============================================================
   # PHASE 13 — PERFORMANCE
   # ============================================================
   - phase: performance
+    summary: "Meet runtime and memory expectations with stage-level budgets."
     items:
-      - PERF-001: enforce_runtime_target_ms(400)
-      - PERF-002: enforce_memory_cap_mb(192)
-      - PERF-003: validate_stage_budgets:
+      - id: PERF-001
+        description: "enforce_runtime_target_ms(400)"
+      - id: PERF-002
+        description: "enforce_memory_cap_mb(192)"
+      - id: PERF-003
+        description: "validate_stage_budgets"
+        stage_budgets:
           discover_ci_resources_ms: 150
           gather_metadata_ms: 200
           evaluate_rules_ms: 250
           canonicalize_ms: 100
-      - PERF-004: performance_regression_tests
+      - id: PERF-004
+        description: "performance_regression_tests"
 
   # ============================================================
   # PHASE 14 — TESTING & CI
   # ============================================================
   - phase: testing_ci
+    summary: "Execute unit/integration/snapshot/parity suites with schema alignment."
     items:
-      - TEST-001: run_unit_tests
-      - TEST-002: run_integration_tests
-      - TEST-003: run_snapshots(3_runs_hash_identical)
-      - TEST-004: run_wasm_conformance_tests
-      - TEST-005: run_parity_tests_python_vs_wasm
-      - TEST-006: enforce_test_coverage(>=75)
-      - TEST-007: validate_ci_jobs_match_spec
-      - TEST-008: validate_checklist_schema_valid
-      - TEST-009: detect_checklist_drift_against_spec
-      - INTEG-001: validate_penalty_map_consistency_with_guardscore   # ← Added
+      - id: TEST-001
+        description: "run_unit_tests"
+      - id: TEST-002
+        description: "run_integration_tests"
+      - id: TEST-003
+        description: "run_snapshots(3_runs_hash_identical)"
+      - id: TEST-004
+        description: "run_wasm_conformance_tests"
+      - id: TEST-005
+        description: "run_parity_tests_python_vs_wasm"
+      - id: TEST-006
+        description: "enforce_test_coverage(>=75)"
+      - id: TEST-007
+        description: "validate_ci_jobs_match_spec"
+      - id: TEST-008
+        description: "validate_checklist_schema_valid"
+      - id: TEST-009
+        description: "detect_checklist_drift_against_spec"
+      - id: INTEG-001
+        description: "validate_penalty_map_consistency_with_guardscore"
 
   # ============================================================
   # PHASE 15 — ACCEPTANCE
   # ============================================================
   - phase: acceptance
+    summary: "Final readiness checks before release or publication."
     items:
-      - ACPT-001: verify_canonical_schema_validates_all_outputs
-      - ACPT-002: verify_snapshot_determinism
-      - ACPT-003: verify_no_fixpack_or_core_binary_content
-      - ACPT-004: verify_export_bundle_contract_valid
-      - ACPT-005: verify_evaluator_pipeline_matches_template
-      - ACPT-006: verify_hash_parity(sha256_canonical)
-      - ACPT-007: verify_security_and_ip_safeguards
-      - ACPT-008: verify_cli_contract
+      - id: ACPT-001
+        description: "verify_canonical_schema_validates_all_outputs"
+      - id: ACPT-002
+        description: "verify_snapshot_determinism"
+      - id: ACPT-003
+        description: "verify_no_fixpack_or_core_binary_content"
+      - id: ACPT-004
+        description: "verify_export_bundle_contract_valid"
+      - id: ACPT-005
+        description: "verify_evaluator_pipeline_matches_template"
+      - id: ACPT-006
+        description: "verify_hash_parity(sha256_canonical)"
+      - id: ACPT-007
+        description: "verify_security_and_ip_safeguards"
+      - id: ACPT-008
+        description: "verify_cli_contract"
+
