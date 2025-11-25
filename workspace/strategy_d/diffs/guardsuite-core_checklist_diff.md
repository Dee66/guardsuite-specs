--- workspace/strategy_d/backups/guardsuite-core_checklist_pre_normalization.yml	2025-11-25 15:06:43.819451835 +0200
+++ products/guardsuite-core/checklist/checklist.yml	2025-11-25 15:09:18.108170686 +0200
@@ -1,258 +1,388 @@
-checklist:
-  id: guardsuite-core-checklist
-  version: 2026.04
-  product: guardsuite-core
-
-  phases:
-
-    # ============================================================
-    # PHASE 1 — INITIALIZATION & ENVIRONMENT VALIDATION
-    # ============================================================
-    - phase: initialization
-      items:
-        - INIT-001: verify_repository_structure_matches_spec
-        - INIT-002: ensure_required_directories_exist
-        - INIT-003: validate_core_dependency_pin_format
-        - INIT-004: enforce_semver_versioning_policy
-        - INIT-005: check_forbidden_overrides_enforced_flag
-        - INIT-006: ensure_runbooks_present
-        - INIT-007: validate_examples_directory_exists
-        - INIT-008: examples_snapshot_determinism_smoke_test
-        - INIT-009: ensure_operator_docs_present_and_valid
-        - INIT-010: detect_spec_updated_timestamp_correct
-
-        # Compatibility & Template Synchronization
-        - COMP-001: validate_core_schema_version_pin
-        - COMP-002: validate_core_dependency_pin
-        - COMP-003: enforce_compatibility_window
-        - COMP-004: run_downstream_smoke_tests_against_template_and_guardscore
-        - TMP-001: validate_template_invariants_match_core
-        - TMP-002: detect_drift_between_template_and_core_schemas
-        - TMP-003: enforce_template_pipeline_contract_consistency
-
-
-    # ============================================================
-    # PHASE 2 — SCHEMA & FRAGMENT GOVERNANCE
-    # ============================================================
-    - phase: schema_governance
-      items:
-        - SCHEMA-001: validate_canonical_schema_exists
-        - SCHEMA-002: validate_provenance_schema_exists
-        - SCHEMA-003: validate_mandatory_fragment_fields_present
-        - SCHEMA-004: run_fragment_validation_command
-        - SCHEMA-005: validate_fragment_migration_policy
-        - SCHEMA-006: ensure_fragment_compatibility_matrix_enforced
-
-        # Integrity & Hashing
-        - SCHEMA-007: ensure_no_duplicate_field_definitions
-        - SCHEMA-008: validate_canonical_schema_bundle_hash
-        - SCHEMA-009: enforce_stable_schema_bundle_ordering
-        - SCHEMA-010: detect_schema_fragment_drift
-        - SCHEMA-011: validate_fragment_versioning_matches_pins
-
-        # Forbidden Override Detection (NEW)
-        - GOV-008: static_analysis_forbidden_override_detection
-
-
-    # ============================================================
-    # PHASE 3 — PROVENANCE ENFORCEMENT
-    # ============================================================
-    - phase: provenance
-      items:
-        - PROV-001: validate_required_provenance_fields_present
-        - PROV-002: ensure_input_hash_sha256_exists
-        - PROV-003: validate_provenance_signature
-        - PROV-004: reject_missing_provenance
-        - PROV-005: enforce_canonical_timestamp_format
-        - PROV-006: provenance_hash_crosscheck_against_canonical_input
-
-
-    # ============================================================
-    # PHASE 4 — CANONICALIZATION ENFORCEMENT
-    # ============================================================
-    - phase: canonicalization
-      items:
-        - CAN-001: enforce_key_ordering
-        - CAN-002: enforce_unicode_normalization_nfc
-        - CAN-003: enforce_canonical_json_utf8
-        - CAN-004: enforce_fixed64_float_rules
-        - CAN-005: enforce_missing_fields_set_to_null
-        - CAN-006: ensure_output_fields_removed
-        - CAN-007: canonical_key_ordering_cross_runtime_test
-
-
-    # ============================================================
-    # PHASE 5 — BINARY CORE, ABI & FALLBACK POLICY
-    # ============================================================
-    - phase: binary_core
-      items:
-        - BIN-001: verify_all_required_modules_present
-        - BIN-002: validate_abi_manifest_exists
-        - BIN-003: verify_binary_signatures
-        - BIN-004: verify_binary_checksums
-        - BIN-005: run_parity_tests_native_vs_python
-        - BIN-006: test_fallback_policy
-        - BIN-007: enforce_supported_architectures
-        - BIN-008: parity_test_across_wasm_python_native
-        - BIN-009: verify_binary_loading_cross_architecture
-        - BIN-010: fallback_policy_inversion_tests
-
-        # Integrity / Drift
-        - BIN-011: validate_binary_abi_matrix_integrity
-        - BIN-012: validate_signing_chain_and_integrity
-        - BIN-013: detect_binary_drift_against_manifest
-
-
-    # ============================================================
-    # PHASE 6 — WASM SAFETY & SANDBOXING
-    # ============================================================
-    - phase: wasm
-      items:
-        - WASM-001: run_wasm_conformance_tests
-        - WASM-002: detect_forbidden_operations
-        - WASM-003: enforce_wasm_compatible_flag
-        - WASM-004: validate_disallowed_syscalls_under_wasi   # NEW
-        - WASM-005: ensure_cli_executes_in_sandboxed_fs       # NEW
-
-
-    # ============================================================
-    # PHASE 7 — TELEMETRY, LOGGING & METRICS
-    # ============================================================
-    - phase: observability
-      items:
-        - OBS-001: validate_telemetry_schema
-        - OBS-002: enforce_required_telemetry_fields_present
-        - OBS-003: enforce_redaction_patterns
-        - OBS-004: validate_structured_json_logging
-        - OBS-005: validate_log_redaction_fields
-        - OBS-006: validate_trace_id_required
-        - OBS-007: enforce_event_rate_limits
-
-        # Metrics (NEW)
-        - OBS-008: expose_required_metrics
-        - OBS-009: validate_metric_names_and_labels
-        - OBS-010: validate_metric_counter_behavior
-        - OBS-011: validate_observability_pipeline_determinism
-
-
-    # ============================================================
-    # PHASE 8 — ERROR SYSTEM VALIDATION
-    # ============================================================
-    - phase: error_system
-      items:
-        - ERR-001: validate_error_code_mapping_complete
-        - ERR-002: validate_error_schema_exists
-        - ERR-003: enforce_no_stacktrace_in_production
-        - ERR-004: validate_deterministic_error_output
-        - ERR-005: enforce_error_forbidden_fields
-
-        # New required error fields
-        - ERR-006: enforce_required_error_fields_present
-        - ERR-007: validate_error_timestamp_utc_format
-        - ERR-008: validate_error_hash_is_sha256
-
-        # NEW (cross-arch determinism)
-        - ERR-009: cross_arch_error_determinism_test
-
-
-    # ============================================================
-    # PHASE 9 — API CONTRACT & OPENAPI VALIDATION
-    # ============================================================
-    - phase: api
-      items:
-        - API-001: validate_openapi_schema_against_local
-        - API-002: enforce_payload_limits
-        - API-003: enforce_default_timeout
-        - API-004: validate_auth_enabled
-
-        # NEW
-        - API-006: test_invalid_auth_token_rejected
-        - API-007: enforce_api_rate_limits
-        - API-008: openapi_conformance_end_to_end
-
-
-    # ============================================================
-    # PHASE 10 — FIXPACK REGISTRY GOVERNANCE
-    # ============================================================
-    - phase: fixpack_registry
-      items:
-        - FX-001: validate_fixpack_schema
-        - FX-002: enforce_signature_required
-        - FX-003: enforce_deterministic_ordering
-        - FX-004: validate_search_contract_behavior
-
-        # NEW
-        - FX-006: compute_registry_index_hash
-        - FX-007: enforce_signature_chain_integrity
-        - FX-008: validate_fixpack_registry_against_schema_fragments
-
-
-    # ============================================================
-    # PHASE 11 — SNAPSHOT NORMALIZATION
-    # ============================================================
-    - phase: snapshots
-      items:
-        - SNAP-001: validate_snapshot_strip_fields
-        - SNAP-002: validate_snapshot_timestamp_normalization
-        - SNAP-003: enforce_three_run_hash_identity
-        - SNAP-004: canonical_serialization_snapshot_test
-        - SNAP-005: reject_unknown_fields_in_snapshot_outputs
-
-        # NEW
-        - SNAP-006: examples_snapshot_determinism
-
-
-    # ============================================================
-    # PHASE 12 — CROSS-PILLAR / CROSS-SPEC INTEGRATION
-    # ============================================================
-    - phase: cross_pillar
-      items:
-        - XREPO-001: verify_guardscore_integration
-        - XREPO-002: verify_playground_integration
-        - XREPO-003: validate_guardboard_contract
-        - XREPO-004: detect_cross_pillar_schema_drift
-        - XREPO-005: detect_cross_pillar_pipeline_drift
-
-
-    # ============================================================
-    # PHASE 13 — OPERATOR MODE CONFORMANCE (NEW)
-    # ============================================================
-    - phase: operator_mode
-      items:
-        - OPS-001: validate_operator_mode_commands
-        - OPS-002: validate_safe_error_reporting_in_operator_mode
-
-
-    # ============================================================
-    # PHASE 14 — CI ENFORCEMENT (NEW)
-    # ============================================================
-    - phase: ci_validation
-      items:
-        - CI-001: validate_ci_matrix_targets
-        - CI-002: ensure_all_ci_jobs_present
-        - CI-003: verify_binary_signature_check_in_ci
-        - CI-004: validate_wasm_conformance_in_ci
-        - CI-005: enforce_parity_tests_in_ci
-        - CI-006: validate_snapshot_tests_in_ci
-
-        # NEW items
-        - CI-009: validate_core_checklist_schema           # new
-        - CI-010: detect_checklist_drift_against_spec      # new
-
-
-    # ============================================================
-    # PHASE 15 — RELEASE VALIDATION & ACCEPTANCE CRITERIA
-    # ============================================================
-    - phase: acceptance
-      items:
-        - ACPT-001: canonical_schemas_validate
-        - ACPT-002: provenance_valid_and_hash_verified
-        - ACPT-003: binary_signatures_verified
-        - ACPT-004: snapshot_determinism_valid
-        - ACPT-005: evaluator_pipeline_matches_authoritative_table
-        - ACPT-006: cli_and_api_match_openapi_contracts
-
-        # NEW
-        - ACPT-007: verify_pipeline_invariants_against_authoritative_table
-        - ACPT-008: verify_binary_parity_including_wasm
-        - ACPT-009: enforce_openapi_conformance_end_to_end
+# products/guardsuite-core/checklist/checklist.yml
+# Strategy-D canonical checklist for GuardSuite Core (deterministic runtime backbone)
+
+metadata:
+  product_id: guardsuite-core
+  checklist_version: "2026.04"
+  last_updated: "2025-11-25T00:00:00Z"
+  owner: "GuardSuite Platform Team"
+  stability: ga
+
+structure_requirements:
+  - id: STRUCT-GCORE-001
+    description: "Preserve every historical phase, identifier, and description exactly as authored."
+    required: true
+  - id: STRUCT-GCORE-002
+    description: "Follow Strategy-D ordering: metadata ⇒ canonical sections ⇒ phases ⇒ acceptance gates."
+    required: true
+  - id: STRUCT-GCORE-003
+    description: "Embed evaluator, schema, and binary governance notes ahead of all phase listings."
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
+    - schemas/core/canonical_schema.json
+    - schemas/provenance_schema.yml
+    - schemas/fixpack_schema.yml
+    - schemas/telemetry_event_schema.yml
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
+    - engine.payload_serializer
+    - evaluator.stage_order
+    - binary.abi_matrix
+
+fixpack_requirements:
+  fixpack_catalog_required: true
+  fixpack_metadata_required: true
+  difficulty_taxonomy_required: true
+  patch_hashing_required: true
+  remediation_examples_required: true
+
+testing_requirements:
+  unit_tests_required: true
+  integration_tests_required: true
+  snapshot_tests_required: true
+  parity_tests_required: true
+  wasm_tests_required: true
+  schema_validation_tests_required: true
+  performance_tests_required: true
+  minimum_coverage_percent: 90
+
+artifacts:
+  required_files:
+    - schemas/core/canonical_schema.json
+    - schemas/provenance_schema.yml
+    - schemas/fixpack_schema.yml
+    - fixpacks/registry_index.yml
+    - artifacts/abi/binary_abi_matrix.yml
+    - api/openapi.yml
+    - docs/runbooks/parity_failure.md
+    - docs/runbooks/schema_drift.md
+    - docs/runbooks/binary_compromise.md
+  required_directories:
+    - schemas/core
+    - schemas/pillar
+    - fixpacks
+    - artifacts/binaries
+    - artifacts/abi
+    - docs
+    - tests
+    - ci
+    - examples
+  build_outputs:
+    - artifacts/binaries/linux-x86_64
+    - artifacts/binaries/linux-arm64
+    - artifacts/binaries/macos-x86_64
+    - artifacts/snapshots
+
+acceptance_criteria:
+  - id: ACPT-GCORE-001
+    description: "Canonical schemas, provenance schema, and fragment bundles validate without drift."
+    required: true
+  - id: ACPT-GCORE-002
+    description: "Binary core signatures, checksums, and ABI manifests verify across all supported arches."
+    required: true
+  - id: ACPT-GCORE-003
+    description: "Evaluator pipeline stages execute in published order with deterministic output hashes."
+    required: true
+  - id: ACPT-GCORE-004
+    description: "Snapshot normalization suite produces identical hashes across three runs and platforms."
+    required: true
+  - id: ACPT-GCORE-005
+    description: "FixPack registry manifests, signatures, and difficulty taxonomy validate end-to-end."
+    required: true
+
+cross_product_dependencies:
+  depends_on_products: []
+  depends_on_schemas:
+    - schemas/core/canonical_schema.json
+    - schemas/provenance_schema.yml
+    - schemas/fixpack_schema.yml
+    - schemas/telemetry_event_schema.yml
+  depends_on_pipeline: true
+
+provenance:
+  - "Derived from GuardSuite Core charter v2026.04."
+  - "Aligned with guardsuite-template evaluator pipeline invariants."
+  - "Backed by ABI manifest artifacts/abi/binary_abi_matrix.yml."
+
+id: guardsuite-core-checklist
+version: "2026.04"
+product: guardsuite-core
+pillar: crosscut
+spec_source: "products/guardsuite-core/metadata/product.yml"
+
+phases:
+
+  # ============================================================
+  # PHASE 1 — INITIALIZATION & ENVIRONMENT VALIDATION
+  # ============================================================
+  - phase: initialization
+    items:
+      - INIT-001: verify_repository_structure_matches_spec
+      - INIT-002: ensure_required_directories_exist
+      - INIT-003: validate_core_dependency_pin_format
+      - INIT-004: enforce_semver_versioning_policy
+      - INIT-005: check_forbidden_overrides_enforced_flag
+      - INIT-006: ensure_runbooks_present
+      - INIT-007: validate_examples_directory_exists
+      - INIT-008: examples_snapshot_determinism_smoke_test
+      - INIT-009: ensure_operator_docs_present_and_valid
+      - INIT-010: detect_spec_updated_timestamp_correct
+
+      # Compatibility & Template Synchronization
+      - COMP-001: validate_core_schema_version_pin
+      - COMP-002: validate_core_dependency_pin
+      - COMP-003: enforce_compatibility_window
+      - COMP-004: run_downstream_smoke_tests_against_template_and_guardscore
+      - TMP-001: validate_template_invariants_match_core
+      - TMP-002: detect_drift_between_template_and_core_schemas
+      - TMP-003: enforce_template_pipeline_contract_consistency
+
+
+  # ============================================================
+  # PHASE 2 — SCHEMA & FRAGMENT GOVERNANCE
+  # ============================================================
+  - phase: schema_governance
+    items:
+      - SCHEMA-001: validate_canonical_schema_exists
+      - SCHEMA-002: validate_provenance_schema_exists
+      - SCHEMA-003: validate_mandatory_fragment_fields_present
+      - SCHEMA-004: run_fragment_validation_command
+      - SCHEMA-005: validate_fragment_migration_policy
+      - SCHEMA-006: ensure_fragment_compatibility_matrix_enforced
+
+      # Integrity & Hashing
+      - SCHEMA-007: ensure_no_duplicate_field_definitions
+      - SCHEMA-008: validate_canonical_schema_bundle_hash
+      - SCHEMA-009: enforce_stable_schema_bundle_ordering
+      - SCHEMA-010: detect_schema_fragment_drift
+      - SCHEMA-011: validate_fragment_versioning_matches_pins
+
+      # Forbidden Override Detection (NEW)
+      - GOV-008: static_analysis_forbidden_override_detection
+
+
+  # ============================================================
+  # PHASE 3 — PROVENANCE ENFORCEMENT
+  # ============================================================
+  - phase: provenance
+    items:
+      - PROV-001: validate_required_provenance_fields_present
+      - PROV-002: ensure_input_hash_sha256_exists
+      - PROV-003: validate_provenance_signature
+      - PROV-004: reject_missing_provenance
+      - PROV-005: enforce_canonical_timestamp_format
+      - PROV-006: provenance_hash_crosscheck_against_canonical_input
+
+
+  # ============================================================
+  # PHASE 4 — CANONICALIZATION ENFORCEMENT
+  # ============================================================
+  - phase: canonicalization
+    items:
+      - CAN-001: enforce_key_ordering
+      - CAN-002: enforce_unicode_normalization_nfc
+      - CAN-003: enforce_canonical_json_utf8
+      - CAN-004: enforce_fixed64_float_rules
+      - CAN-005: enforce_missing_fields_set_to_null
+      - CAN-006: ensure_output_fields_removed
+      - CAN-007: canonical_key_ordering_cross_runtime_test
+
+
+  # ============================================================
+  # PHASE 5 — BINARY CORE, ABI & FALLBACK POLICY
+  # ============================================================
+  - phase: binary_core
+    items:
+      - BIN-001: verify_all_required_modules_present
+      - BIN-002: validate_abi_manifest_exists
+      - BIN-003: verify_binary_signatures
+      - BIN-004: verify_binary_checksums
+      - BIN-005: run_parity_tests_native_vs_python
+      - BIN-006: test_fallback_policy
+      - BIN-007: enforce_supported_architectures
+      - BIN-008: parity_test_across_wasm_python_native
+      - BIN-009: verify_binary_loading_cross_architecture
+      - BIN-010: fallback_policy_inversion_tests
+
+      # Integrity / Drift
+      - BIN-011: validate_binary_abi_matrix_integrity
+      - BIN-012: validate_signing_chain_and_integrity
+      - BIN-013: detect_binary_drift_against_manifest
+
+
+  # ============================================================
+  # PHASE 6 — WASM SAFETY & SANDBOXING
+  # ============================================================
+  - phase: wasm
+    items:
+      - WASM-001: run_wasm_conformance_tests
+      - WASM-002: detect_forbidden_operations
+      - WASM-003: enforce_wasm_compatible_flag
+      - WASM-004: validate_disallowed_syscalls_under_wasi
+      - WASM-005: ensure_cli_executes_in_sandboxed_fs
+
+
+  # ============================================================
+  # PHASE 7 — TELEMETRY, LOGGING & METRICS
+  # ============================================================
+  - phase: observability
+    items:
+      - OBS-001: validate_telemetry_schema
+      - OBS-002: enforce_required_telemetry_fields_present
+      - OBS-003: enforce_redaction_patterns
+      - OBS-004: validate_structured_json_logging
+      - OBS-005: validate_log_redaction_fields
+      - OBS-006: validate_trace_id_required
+      - OBS-007: enforce_event_rate_limits
+
+      # Metrics (NEW)
+      - OBS-008: expose_required_metrics
+      - OBS-009: validate_metric_names_and_labels
+      - OBS-010: validate_metric_counter_behavior
+      - OBS-011: validate_observability_pipeline_determinism
+
+
+  # ============================================================
+  # PHASE 8 — ERROR SYSTEM VALIDATION
+  # ============================================================
+  - phase: error_system
+    items:
+      - ERR-001: validate_error_code_mapping_complete
+      - ERR-002: validate_error_schema_exists
+      - ERR-003: enforce_no_stacktrace_in_production
+      - ERR-004: validate_deterministic_error_output
+      - ERR-005: enforce_error_forbidden_fields
+
+      # New required error fields
+      - ERR-006: enforce_required_error_fields_present
+      - ERR-007: validate_error_timestamp_utc_format
+      - ERR-008: validate_error_hash_is_sha256
+
+      # NEW (cross-arch determinism)
+      - ERR-009: cross_arch_error_determinism_test
+
+
+  # ============================================================
+  # PHASE 9 — API CONTRACT & OPENAPI VALIDATION
+  # ============================================================
+  - phase: api
+    items:
+      - API-001: validate_openapi_schema_against_local
+      - API-002: enforce_payload_limits
+      - API-003: enforce_default_timeout
+      - API-004: validate_auth_enabled
+
+      # NEW
+      - API-006: test_invalid_auth_token_rejected
+      - API-007: enforce_api_rate_limits
+      - API-008: openapi_conformance_end_to_end
+
+
+  # ============================================================
+  # PHASE 10 — FIXPACK REGISTRY GOVERNANCE
+  # ============================================================
+  - phase: fixpack_registry
+    items:
+      - FX-001: validate_fixpack_schema
+      - FX-002: enforce_signature_required
+      - FX-003: enforce_deterministic_ordering
+      - FX-004: validate_search_contract_behavior
+
+      # NEW
+      - FX-006: compute_registry_index_hash
+      - FX-007: enforce_signature_chain_integrity
+      - FX-008: validate_fixpack_registry_against_schema_fragments
+
+
+  # ============================================================
+  # PHASE 11 — SNAPSHOT NORMALIZATION
+  # ============================================================
+  - phase: snapshots
+    items:
+      - SNAP-001: validate_snapshot_strip_fields
+      - SNAP-002: validate_snapshot_timestamp_normalization
+      - SNAP-003: enforce_three_run_hash_identity
+      - SNAP-004: canonical_serialization_snapshot_test
+      - SNAP-005: reject_unknown_fields_in_snapshot_outputs
+
+      # NEW
+      - SNAP-006: examples_snapshot_determinism
+
+
+  # ============================================================
+  # PHASE 12 — CROSS-PILLAR / CROSS-SPEC INTEGRATION
+  # ============================================================
+  - phase: cross_pillar
+    items:
+      - XREPO-001: verify_guardscore_integration
+      - XREPO-002: verify_playground_integration
+      - XREPO-003: validate_guardboard_contract
+      - XREPO-004: detect_cross_pillar_schema_drift
+      - XREPO-005: detect_cross_pillar_pipeline_drift
+
+
+  # ============================================================
+  # PHASE 13 — OPERATOR MODE CONFORMANCE (NEW)
+  # ============================================================
+  - phase: operator_mode
+    items:
+      - OPS-001: validate_operator_mode_commands
+      - OPS-002: validate_safe_error_reporting_in_operator_mode
+
+
+  # ============================================================
+  # PHASE 14 — CI ENFORCEMENT (NEW)
+  # ============================================================
+  - phase: ci_validation
+    items:
+      - CI-001: validate_ci_matrix_targets
+      - CI-002: ensure_all_ci_jobs_present
+      - CI-003: verify_binary_signature_check_in_ci
+      - CI-004: validate_wasm_conformance_in_ci
+      - CI-005: enforce_parity_tests_in_ci
+      - CI-006: validate_snapshot_tests_in_ci
+
+      # NEW items
+      - CI-009: validate_core_checklist_schema
+      - CI-010: detect_checklist_drift_against_spec
+
+
+  # ============================================================
+  # PHASE 15 — RELEASE VALIDATION & ACCEPTANCE CRITERIA
+  # ============================================================
+  - phase: acceptance
+    items:
+      - ACPT-001: canonical_schemas_validate
+      - ACPT-002: provenance_valid_and_hash_verified
+      - ACPT-003: binary_signatures_verified
+      - ACPT-004: snapshot_determinism_valid
+      - ACPT-005: evaluator_pipeline_matches_authoritative_table
+      - ACPT-006: cli_and_api_match_openapi_contracts
+
+      # NEW
+      - ACPT-007: verify_pipeline_invariants_against_authoritative_table
+      - ACPT-008: verify_binary_parity_including_wasm
+      - ACPT-009: enforce_openapi_conformance_end_to_end
+
