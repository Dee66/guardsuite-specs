diff --git a/products/computeguard/checklist/checklist.yml b/products/computeguard/checklist/checklist.yml
index 63fb0ff..cec6fb0 100644
--- a/products/computeguard/checklist/checklist.yml
+++ b/products/computeguard/checklist/checklist.yml
@@ -1,10 +1,124 @@
+# products/computeguard/checklist/checklist.yml
+# Strategy-D canonical checklist for ComputeGuard (paid blueprint)
+
+metadata:
+  product_id: computeguard
+  checklist_version: "2025.11"
+  last_updated: "2025-11-25T00:00:00Z"
+  owner: "GuardSuite Platform Team"
+  stability: ga
+
+structure_requirements:
+  - id: STRUCT-CG-001
+    description: "Retain all ComputeGuard phases in canonical Strategy-D order with summaries and items intact."
+    required: true
+  - id: STRUCT-CG-002
+    description: "Each item must keep its original id, description text, and deterministic intent."
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
+    - schemas/evaluator_output_schema.yml
+    - schemas/cli_output.json
+    - schemas/cli_error.json
+    - schemas/compliance_ledger_schema.yml
+    - schemas/fixpack_metadata_schema.yml
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
+    - canonicalization_rules
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
+  minimum_coverage_percent: 85
+
+artifacts:
+  required_files:
+    - schemas/evaluator_output_schema.yml
+    - schemas/cli_output.json
+    - schemas/cli_error.json
+    - schemas/compliance_ledger_schema.yml
+    - catalog/index.yml
+  required_directories:
+    - fixpack
+    - catalog
+    - examples/rules
+    - tests
+    - docs
+  build_outputs:
+    - artifacts/ledgers
+    - artifacts/fixpack_previews
+
+acceptance_criteria:
+  - id: ACPT-CG-001
+    description: "Evaluator, CLI, ledger, and fixpack schemas all validate with canonical validator."
+    required: true
+  - id: ACPT-CG-002
+    description: "Determinism suites (snapshot + fixpack) achieve 3-run parity."
+    required: true
+  - id: ACPT-CG-003
+    description: "Performance budgets satisfied for CI, Playground, and ledger generation."
+    required: true
+  - id: ACPT-CG-004
+    description: "Documentation set (architecture, fixpack, ledger) reviewed and complete."
+    required: true
+
+cross_product_dependencies:
+  depends_on_products:
+    - computescan
+    - guardscore
+    - guardboard
+  depends_on_schemas:
+    - guardsuite-core/canonical_schema.json
+  depends_on_pipeline: true
+
+provenance:
+  - "Checklist derived from Strategy-D canonical paid-blueprint pattern."
+  - "Aligned with ComputeGuard master spec and GuardSuite governance rules."
+
 id: computeguard_checklist
 version: "2025.11"
+product: computeguard
 pillar: compute
-product: ComputeGuard
+spec_source: "products/computeguard/metadata/product.yml"
 
 phases:
 
+  # ============================================================
+  # INITIALIZATION
+  # ============================================================
   - phase: initialization
     summary: "Prepare repo, validate initial structure, and ensure toolchain readiness."
     items:
@@ -29,6 +143,9 @@ phases:
       - id: INIT-010
         description: "Validate spec.yml and checklist.yml conform to guard-specs schema."
 
+  # ============================================================
+  # DIRECTORY CONVENTIONS
+  # ============================================================
   - phase: directory_conventions
     summary: "Confirm structure, naming, and required resource layout."
     items:
@@ -43,6 +160,9 @@ phases:
       - id: DIR-005
         description: "Validate examples/rules bundle directory and file naming."
 
+  # ============================================================
+  # EVALUATOR IMPLEMENTATION
+  # ============================================================
   - phase: evaluator_implementation
     summary: "Implement evaluator pipeline using template-provided orchestration and pillar-specific rule bundles."
     items:
@@ -63,6 +183,9 @@ phases:
       - id: EVAL-008
         description: "Implement environment normalization hook before output serialization."
 
+  # ============================================================
+  # RULE BUNDLE
+  # ============================================================
   - phase: rule_bundle
     summary: "Create and verify ComputeGuard rule bundles."
     items:
@@ -77,6 +200,9 @@ phases:
       - id: RULE-005
         description: "Ensure rule metadata (severity, category, title, description) matches schema."
 
+  # ============================================================
+  # FIXPACK SYSTEM
+  # ============================================================
   - phase: fixpack_system
     summary: "Implement FixPack-Lite system with normalized previews and deterministic outputs."
     items:
@@ -95,6 +221,9 @@ phases:
       - id: FP-007
         description: "Implement fixpack hint exposure for GuardBoard."
 
+  # ============================================================
+  # COMPLIANCE LEDGER
+  # ============================================================
   - phase: compliance_ledger
     summary: "Implement audit-grade FinOps ledger system based on schema."
     items:
@@ -109,6 +238,9 @@ phases:
       - id: LEDGER-005
         description: "Expose ledger for GuardBoard consumption via CLI."
 
+  # ============================================================
+  # CLI
+  # ============================================================
   - phase: cli
     summary: "Implement ComputeGuard CLI with full contract compliance."
     items:
@@ -133,6 +265,9 @@ phases:
       - id: CLI-010
         description: "Implement fixpack-summary and compliance-ledger flags."
 
+  # ============================================================
+  # INTEGRATIONS
+  # ============================================================
   - phase: integrations
     summary: "Integrate ComputeGuard with GuardScore, GuardBoard, Playground."
     items:
@@ -147,6 +282,9 @@ phases:
       - id: INT-005
         description: "Validate quick-score mode behavior."
 
+  # ============================================================
+  # DETERMINISM AND NORMALIZATION
+  # ============================================================
   - phase: determinism_and_normalization
     summary: "Enforce cross-machine deterministic behavior."
     items:
@@ -165,6 +303,9 @@ phases:
       - id: DET-007
         description: "Ensure ledger artifacts are deterministic."
 
+  # ============================================================
+  # PERFORMANCE
+  # ============================================================
   - phase: performance
     summary: "Validate product performance under expected constraints."
     items:
@@ -179,6 +320,9 @@ phases:
       - id: PERF-005
         description: "Implement CI perf regression tests."
 
+  # ============================================================
+  # SECURITY
+  # ============================================================
   - phase: security
     summary: "Implement sandboxing, safe errors, sanitization."
     items:
@@ -193,6 +337,9 @@ phases:
       - id: SEC-005
         description: "Ensure safe error reporting (no stack-leaks, no paths)."
 
+  # ============================================================
+  # TESTING
+  # ============================================================
   - phase: testing
     summary: "Complete unit, integration, snapshot, and schema testing."
     items:
@@ -213,6 +360,9 @@ phases:
       - id: TEST-008
         description: "Add test preventing forbidden overrides."
 
+  # ============================================================
+  # CI/CD
+  # ============================================================
   - phase: ci_cd
     summary: "Configure CI contract and quality gates."
     items:
@@ -227,6 +377,9 @@ phases:
       - id: CI-005
         description: "Ensure CI uses dev-shim until guardsuite-core is released."
 
+  # ============================================================
+  # DOCUMENTATION
+  # ============================================================
   - phase: documentation
     summary: "Produce developer docs, architecture notes, API docs, ledger guides."
     items:
@@ -245,6 +398,9 @@ phases:
       - id: DOC-007
         description: "Document migration paths and versioning."
 
+  # ============================================================
+  # ACCEPTANCE
+  # ============================================================
   - phase: acceptance
     summary: "Acceptance checks before release."
     items:
@@ -266,4 +422,3 @@ phases:
         description: "Developer docs MUST be complete and accurate."
       - id: ACC-009
         description: "Checklist MUST be fully complete."
-
