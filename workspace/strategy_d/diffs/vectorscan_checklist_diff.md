--- workspace/strategy_d/backups/vectorscan_checklist_pre_normalization.yml	2025-11-25 13:14:28.347460139 +0200
+++ products/vectorscan/checklist/checklist.yml	2025-11-25 13:52:57.864502023 +0200
@@ -3,6 +3,96 @@
 # Version: 2026.04
 # Action: create
 
+metadata:
+  product_id: vectorscan
+  checklist_version: "2026.04"
+  last_updated: "2025-11-25T00:00:00Z"
+  owner: "GuardSuite Platform Team"
+  stability: ga
+
+structure_requirements:
+  - id: STRUCT-VEC-001
+    description: "Phases 1-16 must remain in canonical order and aligned with the Strategy-D master checklist."
+    required: true
+
+documentation_requirements:
+  readme_required: true
+  product_docs_required: true
+  api_reference_required: false
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
+    - schemas/vectorscan/canonical_output.json
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
+    - schemas/vectorscan/canonical_output.json
+    - artifacts/schema_bundle_hash.txt
+    - artifacts/release_bundle_hash.txt
+  required_directories:
+    - rules/vectorscan
+    - adapters
+    - tests
+    - docs
+    - ci
+  build_outputs:
+    - release_bundle.zip
+
+acceptance_criteria:
+  - id: ACPT-VEC-001
+    description: "Deterministic hashing validated across python, wasm, and native runtimes."
+    required: true
+  - id: ACPT-VEC-002
+    description: "No remediation or fixpack content present in free scanner deliverables."
+    required: true
+
+cross_product_dependencies:
+  depends_on_products:
+    - guardsuite-core
+    - guardscore
+    - guardboard
+  depends_on_schemas:
+    - guardsuite-core/canonical_schema.json
+  depends_on_pipeline: true
+
+provenance:
+  - "Checklist format derived from Strategy-D canonical model."
+  - "Aligned with GuardSuite Master Spec."
+
 id: vectorscan-checklist
 version: "2026.04"
 product: vectorscan
@@ -19,13 +109,14 @@
       - INIT-001: verify_repo_contains(spec="products/vectorscan.yml", path_exists=true)
       - INIT-002: validate_spec_yaml_syntax_and_schema(spec="products/vectorscan.yml")
       - INIT-003: validate_spec_version_matches("2026.04") || warn_if_older
-      - INIT-004: verify_required_dirs_exist:
-          - schemas/vectorscan
-          - rules/vectorscan
-          - adapters
-          - tests
-          - ci
-          - docs
+      - INIT-004:
+          verify_required_dirs_exist:
+            - schemas/vectorscan
+            - rules/vectorscan
+            - adapters
+            - tests
+            - ci
+            - docs
       - INIT-005: validate_core_dependency_pin("guardsuite-core@>=2.3.0,<3.0.0")
       - INIT-006: enforce_product_type_is_free_scanner(no_paid_artifacts=true)
       - INIT-007: ensure_no_guardsuite_core_binaries_in_repo
@@ -39,10 +130,11 @@
     items:
       - SCHEMA-001: ensure canonical_output_schema exists at "schemas/vectorscan/canonical_output.json"
       - SCHEMA-002: validate_schema_against_core_fragments("guardsuite-core/canonical_schema.json")
-      - SCHEMA-003: assert_required_fields_present:
-          - metadata
-          - issues[]
-          - provenance (optional)
+      - SCHEMA-003:
+          assert_required_fields_present:
+            - metadata
+            - issues[]
+            - provenance (optional)
       - SCHEMA-004: detect_duplicate_field_definitions_in_schema
       - SCHEMA-005: validate_schema_documents_sorting_semantics(lists_documented=true)
       - SCHEMA-006: compute_and_record_schema_bundle_hash(output="artifacts/schema_bundle_hash.txt")
@@ -87,12 +179,13 @@
   - phase: rule_system
     items:
       - RULE-001: validate_rule_files_exist(rules_dir="rules/vectorscan")
-      - RULE-002: ensure_each_rule_has_required_metadata:
-          - rule_id (snake_case, namespace="vectorscan")
-          - title
-          - description
-          - severity ∈ [critical, high, medium, low, info]
-          - rationale
+      - RULE-002:
+          ensure_each_rule_has_required_metadata:
+            - rule_id (snake_case, namespace="vectorscan")
+            - title
+            - description
+            - severity ∈ [critical, high, medium, low, info]
+            - rationale
       - RULE-003: ensure_rule_ids_are_unique_across_repo
       - RULE-004: enforce_rules_do_not_invoke_remediation_or_execute_patches
       - RULE-005: validate_rule_explain_strings_match_schema
@@ -137,14 +230,15 @@
   # ============================================================
   - phase: wasm_safety
     items:
-      - WASM-001: enforce_wasm_forbidden_operations_list:
-          - randomness
-          - system_time
-          - locale
-          - filesystem_write
-          - environment_variable_access
-          - network_access
-          - dynamic_imports
+      - WASM-001:
+          enforce_wasm_forbidden_operations_list:
+            - randomness
+            - system_time
+            - locale
+            - filesystem_write
+            - environment_variable_access
+            - network_access
+            - dynamic_imports
       - WASM-002: wasm_conformance_test(prescribed_runtime="wasi_snapshot_preview1")
       - WASM-003: ensure_normalization_utils_are_wasm_safe
       - WASM-004: ensure_playground_safety_when_running_sample_plans
@@ -172,14 +266,16 @@
   # ============================================================
   - phase: observability
     items:
-      - OBS-001: validate_metrics_exist:
-          - vectorscan_runs_total
-          - vectorscan_issues_total
-          - vectorscan_partial_inputs_total
+      - OBS-001:
+          validate_metrics_exist:
+            - vectorscan_runs_total
+            - vectorscan_issues_total
+            - vectorscan_partial_inputs_total
       - OBS-002: structured_json_logs_required_and_schema_valid
-      - OBS-003: enforce_telemetry_redaction_patterns:
-          - ".*secret.*"
-          - ".*token.*"
+      - OBS-003:
+          enforce_telemetry_redaction_patterns:
+            - ".*secret.*"
+            - ".*token.*"
       - OBS-004: enforce_max_event_payload_bytes(<=16000)
       - OBS-005: ensure_no_user_paste_content_leaks_in_telemetry
 
@@ -217,11 +313,12 @@
     items:
       - PERF-001: enforce_expected_runtime_ms(<=500)
       - PERF-002: enforce_memory_cap_mb(<=150)
-      - PERF-003: validate_stage_budgets:
-          discover_ci_resources_ms: 150
-          gather_metadata_ms: 200
-          evaluate_rules_ms: 250
-          canonicalize_ms: 100
+      - PERF-003:
+          validate_stage_budgets:
+            discover_ci_resources_ms: 150
+            gather_metadata_ms: 200
+            evaluate_rules_ms: 250
+            canonicalize_ms: 100
       - PERF-004: performance_regression_test(synthetic_fixture)
 
   # ============================================================
@@ -229,12 +326,13 @@
   # ============================================================
   - phase: deliverables
     items:
-      - DELIV-001: ensure_artifacts_present:
-          - schemas/vectorscan/canonical_output.json
-          - rules/vectorscan/*.yml
-          - adapters/*/manifest.yml
-          - tests/snapshots/*
-          - ci/vectorscan-ci.yml
+      - DELIV-001:
+          ensure_artifacts_present:
+            - schemas/vectorscan/canonical_output.json
+            - rules/vectorscan/*.yml
+            - adapters/*/manifest.yml
+            - tests/snapshots/*
+            - ci/vectorscan-ci.yml
       - DELIV-002: ensure_docs_and_runbooks_present(docs/runbooks/vectorscan/*.md)
       - DELIV-003: compute_release_bundle_and_record_hash(artifacts/release_bundle_hash.txt)
       - DELIV-004: ensure_no_sensitive_data_in_release_bundle
