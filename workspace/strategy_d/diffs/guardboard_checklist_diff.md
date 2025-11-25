--- workspace/strategy_d/backups/guardboard_checklist_pre_normalization.yml	2025-11-25 14:56:56.156441326 +0200
+++ products/guardboard/checklist/checklist.yml	2025-11-25 14:59:13.364253784 +0200
@@ -1,387 +1,526 @@
+# products/guardboard/checklist/checklist.yml
+# Strategy-D canonical checklist for GuardBoard (experience blueprint)
+
+metadata:
+  product_id: guardboard
+  checklist_version: "2025.11"
+  last_updated: "2025-11-25T00:00:00Z"
+  owner: "GuardSuite Platform Team"
+  stability: ga
+
+structure_requirements:
+  - id: STRUCT-GB-001
+    description: "Preserve every historical GuardBoard phase, item id, title, and task text verbatim."
+    required: true
+  - id: STRUCT-GB-002
+    description: "Follow Strategy-D ordering: metadata ⇒ canonical requirement blocks ⇒ phases ⇒ acceptance."
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
+    - schemas/guardboard/dashboard_payload.json
+    - schemas/guardboard/export_bundle.json
+    - schemas/guardboard/resource_inspector_schema.yml
+    - schemas/guardboard/preview_viewer_schema.yml
+    - schemas/guardboard/compliance_ledger_schema.yml
+
+evaluator_requirements:
+  pipeline_must_match_template: true
+  canonicalization_required: true
+  wasm_safety_required: true
+  deterministic_output_required: true
+  timestamp_normalization_required: true
+  prohibited_overrides:
+    - canonical.output_contract
+    - renderer.layout_contract
+    - export.signing_contract
+
+fixpack_requirements:
+  fixpack_catalog_required: false
+  fixpack_metadata_required: false
+  difficulty_taxonomy_required: false
+  patch_hashing_required: false
+  remediation_examples_required: false
+  wasm_safe_snippets_required: false
+
+testing_requirements:
+  unit_tests_required: true
+  integration_tests_required: true
+  snapshot_tests_required: true
+  parity_tests_required: true
+  wasm_tests_required: false
+  schema_validation_tests_required: true
+  performance_tests_required: true
+  minimum_coverage_percent: 85
+
+artifacts:
+  required_files:
+    - repos/guardboard/spec.yml
+    - schemas/guardboard/dashboard_payload.json
+    - schemas/guardboard/export_bundle.json
+    - schemas/guardboard/resource_inspector_schema.yml
+    - schemas/guardboard/preview_viewer_schema.yml
+    - api/openapi.yml
+  required_directories:
+    - src
+    - api
+    - web
+    - services
+    - schemas
+    - tests
+    - docs
+    - ci
+  build_outputs:
+    - artifacts/dashboard_payloads
+    - artifacts/export_bundles
+    - artifacts/preview_snapshots
+
+acceptance_criteria:
+  - id: ACPT-GB-001
+    description: "All ingested artifacts validate against schemas before rendering or export."
+    required: true
+  - id: ACPT-GB-002
+    description: "Determinism suites prove dashboard, preview, and export reproducibility across three runs."
+    required: true
+  - id: ACPT-GB-003
+    description: "RBAC, security controls, and sandboxed preview execution validated via automated tests."
+    required: true
+  - id: ACPT-GB-004
+    description: "Performance targets (page load, API latency) satisfied in CI load tests."
+    required: true
+
+cross_product_dependencies:
+  depends_on_products:
+    - computeguard
+    - computescan
+    - pipelinescan
+    - vectorscan
+    - guardscore
+  depends_on_schemas:
+    - guardsuite-core/canonical_schema.json
+    - schemas/guardboard/dashboard_payload.json
+    - schemas/guardboard/export_bundle.json
+  depends_on_pipeline: true
+
+provenance:
+  - "Derived from GuardSuite Platform dashboard charter v2025.11."
+  - "Aligned with Strategy-D experience blueprint requirements."
+
 id: guardboard_checklist
-product: GuardBoard
 version: "2025.11"
-status: active
+product: guardboard
+pillar: ui
+spec_source: "products/guardboard/metadata/product.yml"
 
 phases:
 
-# ======================================================================
-# 1. INITIALIZATION & REPO BOOTSTRAP
-# ======================================================================
-- id: INIT-001
-  title: "Verify repository structure"
-  tasks:
-    - Ensure directories exist: src/, api/, web/, services/, schemas/, tests/, docs/, ci/
-    - Verify pyproject or package.json (UI) in place
-    - Ensure dev-shims for schema validation (if applicable)
-
-- id: INIT-002
-  title: "Add spec + manifest"
-  tasks:
-    - Add repos/guardboard/spec.yml
-    - Add product manifest (API version, artifact versions supported)
-
-- id: INIT-003
-  title: "Validate directory conventions"
-  tasks:
-    - schemas/: only schema files (dashboard, export_bundle, inspector, etc.)
-    - api/: OpenAPI specs + handlers
-    - web/: UI code
-    - services/: ingest worker, renderer, export service
-    - tests/: unit, integration, snapshot, e2e
-
-# ======================================================================
-# 2. SCHEMAS (PAYLOAD + ARTIFACTS)
-# ======================================================================
-- id: SCHEMA-001
-  title: "Implement dashboard payload schema"
-  tasks:
-    - Define canonical dashboard payload format
-    - Validate example payloads against schema
-
-- id: SCHEMA-002
-  title: "Implement export bundle schema"
-  tasks:
-    - Include artifacts, provenance, schema versions, audit slice
-
-- id: SCHEMA-003
-  title: "Implement inspector + preview schemas"
-  tasks:
-    - resource_inspector_schema.yml
-    - preview_viewer_schema.yml
-
-- id: SCHEMA-004
-  title: "Validate producer artifacts"
-  tasks:
-    - Compliance ledger schema
-    - Preview schema
-    - GuardScore input schema
-    - CLI JSON schema
-    - Enforce schema validation for sample artifacts
-
-# ======================================================================
-# 3. INGESTION PIPELINE
-# ======================================================================
-- id: INGEST-001
-  title: "Implement webhook ingestion"
-  tasks:
-    - HMAC/JWS signature verification
-    - Replay protection window enforcement
-    - Error handling & structured logs
-
-- id: INGEST-002
-  title: "Implement artifact validation pipeline"
-  tasks:
-    - schema_validation
-    - provenance_check
-    - deduplication rules
-    - timestamp normalization
-    - cache invalidation triggers
-
-- id: INGEST-003
-  title: "Implement pull mode"
-  tasks:
-    - periodic polling (configurable)
-    - handle backfill logic
-    - poison queue routing
-
-# ======================================================================
-# 4. ARTIFACT CACHE
-# ======================================================================
-- id: CACHE-001
-  title: "Implement cache storage"
-  tasks:
-    - in-memory + distributed cache support
-    - TTL + stale_while_revalidate
-
-- id: CACHE-002
-  title: "Implement cache invalidation contract"
-  tasks:
-    - invalidate on artifact_ingested
-    - invalidate on schema_version change
-    - invalidate on RBAC policy change
-    - test distributed invalidation propagation
-
-# ======================================================================
-# 5. ARTIFACT MERGE & AGGREGATION
-# ======================================================================
-- id: MERGE-001
-  title: "Implement artifact merge strategy"
-  tasks:
-    - merge_by resource_id
-    - conflict resolution: latest_timestamp_utc
-    - retain superseded artifacts for audit
-
-- id: MERGE-002
-  title: "Implement timeline merge"
-  tasks:
-    - combine ledger events, previews, scores
-    - deterministic ordering (timestamp_utc asc, then artifact_id)
-
-# ======================================================================
-# 6. RBAC IMPLEMENTATION
-# ======================================================================
-- id: RBAC-001
-  title: "Implement role → capability matrix"
-  tasks:
-    - viewer, analyst, operator, approver, admin
-    - permission checks per endpoint/action
-
-- id: RBAC-002
-  title: "Add attribute-based filtering"
-  tasks:
-    - redact sensitive fields per role
-    - enforce tenant_id boundaries
-
-- id: RBAC-003
-  title: "RBAC test suite"
-  tasks:
-    - positive + negative authorization tests
-    - full coverage for each endpoint
-
-# ======================================================================
-# 7. API SURFACE (REST + OPTIONAL GRAPHQL)
-# ======================================================================
-- id: API-001
-  title: "Implement REST endpoints"
-  tasks:
-    - GET /artifacts/ledger
-    - GET /artifacts/preview
-    - GET /scores/{resource_id}
-    - GET /dashboards/{dashboard_id}
-    - POST /exports
-    - POST /webhooks/ingest (signed)
-
-- id: API-002
-  title: "Implement pagination, caching, filtering"
-  tasks:
-    - page/per_page rules
-    - severity/rule_id filters
-    - caching headers + ETags
-
-- id: API-003
-  title: "Generate OpenAPI spec"
-  tasks:
-    - api/openapi.yml
-    - match implementation via contract tests
+  # ======================================================================
+  # 1. INITIALIZATION & REPO BOOTSTRAP
+  # ======================================================================
+  - phase: initialization_repo_bootstrap
+    summary: "Prepare repository layout, manifests, and deterministic scaffolding."
+    items:
+      - id: INIT-001
+        title: "Verify repository structure"
+        tasks:
+          - "Ensure directories exist: src/, api/, web/, services/, schemas/, tests/, docs/, ci/."
+          - "Verify pyproject or package.json (UI) in place."
+          - "Ensure dev-shims for schema validation (if applicable)."
+      - id: INIT-002
+        title: "Add spec + manifest"
+        tasks:
+          - "Add repos/guardboard/spec.yml."
+          - "Add product manifest (API version, artifact versions supported)."
+      - id: INIT-003
+        title: "Validate directory conventions"
+        tasks:
+          - "schemas/: only schema files (dashboard, export_bundle, inspector, etc.)."
+          - "api/: OpenAPI specs + handlers."
+          - "web/: UI code."
+          - "services/: ingest worker, renderer, export service."
+          - "tests/: unit, integration, snapshot, e2e."
+
+  # ======================================================================
+  # 2. SCHEMAS (PAYLOAD + ARTIFACTS)
+  # ======================================================================
+  - phase: schemas_payload_artifacts
+    summary: "Implement and validate dashboard, export, inspector, and producer schemas."
+    items:
+      - id: SCHEMA-001
+        title: "Implement dashboard payload schema"
+        tasks:
+          - "Define canonical dashboard payload format."
+          - "Validate example payloads against schema."
+      - id: SCHEMA-002
+        title: "Implement export bundle schema"
+        tasks:
+          - "Include artifacts, provenance, schema versions, audit slice."
+      - id: SCHEMA-003
+        title: "Implement inspector + preview schemas"
+        tasks:
+          - "resource_inspector_schema.yml."
+          - "preview_viewer_schema.yml."
+      - id: SCHEMA-004
+        title: "Validate producer artifacts"
+        tasks:
+          - "Compliance ledger schema."
+          - "Preview schema."
+          - "GuardScore input schema."
+          - "CLI JSON schema."
+          - "Enforce schema validation for sample artifacts."
+
+  # ======================================================================
+  # 3. INGESTION PIPELINE
+  # ======================================================================
+  - phase: ingestion_pipeline
+    summary: "Build webhook, validation, and polling pathways for artifact ingestion."
+    items:
+      - id: INGEST-001
+        title: "Implement webhook ingestion"
+        tasks:
+          - "HMAC/JWS signature verification."
+          - "Replay protection window enforcement."
+          - "Error handling & structured logs."
+      - id: INGEST-002
+        title: "Implement artifact validation pipeline"
+        tasks:
+          - "schema_validation."
+          - "provenance_check."
+          - "deduplication rules."
+          - "timestamp normalization."
+          - "cache invalidation triggers."
+      - id: INGEST-003
+        title: "Implement pull mode"
+        tasks:
+          - "periodic polling (configurable)."
+          - "handle backfill logic."
+          - "poison queue routing."
+
+  # ======================================================================
+  # 4. ARTIFACT CACHE
+  # ======================================================================
+  - phase: artifact_cache
+    summary: "Implement cache storage and invalidation contracts."
+    items:
+      - id: CACHE-001
+        title: "Implement cache storage"
+        tasks:
+          - "in-memory + distributed cache support."
+          - "TTL + stale_while_revalidate."
+      - id: CACHE-002
+        title: "Implement cache invalidation contract"
+        tasks:
+          - "invalidate on artifact_ingested."
+          - "invalidate on schema_version change."
+          - "invalidate on RBAC policy change."
+          - "test distributed invalidation propagation."
+
+  # ======================================================================
+  # 5. ARTIFACT MERGE & AGGREGATION
+  # ======================================================================
+  - phase: artifact_merge_and_aggregation
+    summary: "Merge artifacts into deterministic timelines and audit views."
+    items:
+      - id: MERGE-001
+        title: "Implement artifact merge strategy"
+        tasks:
+          - "merge_by resource_id."
+          - "conflict resolution: latest_timestamp_utc."
+          - "retain superseded artifacts for audit."
+      - id: MERGE-002
+        title: "Implement timeline merge"
+        tasks:
+          - "combine ledger events, previews, scores."
+          - "deterministic ordering (timestamp_utc asc, then artifact_id)."
+
+  # ======================================================================
+  # 6. RBAC IMPLEMENTATION
+  # ======================================================================
+  - phase: rbac_implementation
+    summary: "Enforce role-based access controls, redaction, and coverage tests."
+    items:
+      - id: RBAC-001
+        title: "Implement role → capability matrix"
+        tasks:
+          - "viewer, analyst, operator, approver, admin."
+          - "permission checks per endpoint/action."
+      - id: RBAC-002
+        title: "Add attribute-based filtering"
+        tasks:
+          - "redact sensitive fields per role."
+          - "enforce tenant_id boundaries."
+      - id: RBAC-003
+        title: "RBAC test suite"
+        tasks:
+          - "positive + negative authorization tests."
+          - "full coverage for each endpoint."
+
+  # ======================================================================
+  # 7. API SURFACE (REST + OPTIONAL GRAPHQL)
+  # ======================================================================
+  - phase: api_surface
+    summary: "Implement REST/GraphQL endpoints, pagination, and OpenAPI contracts."
+    items:
+      - id: API-001
+        title: "Implement REST endpoints"
+        tasks:
+          - "GET /artifacts/ledger."
+          - "GET /artifacts/preview."
+          - "GET /scores/{resource_id}."
+          - "GET /dashboards/{dashboard_id}."
+          - "POST /exports."
+          - "POST /webhooks/ingest (signed)."
+      - id: API-002
+        title: "Implement pagination, caching, filtering"
+        tasks:
+          - "page/per_page rules."
+          - "severity/rule_id filters."
+          - "caching headers + ETags."
+      - id: API-003
+        title: "Generate OpenAPI spec"
+        tasks:
+          - "api/openapi.yml."
+          - "match implementation via contract tests."
+      - id: API-004
+        title: "GraphQL gateway (optional)"
+        tasks:
+          - "auto-generate schema from artifact schemas."
+          - "authorization wiring."
+
+  # ======================================================================
+  # 8. DASHBOARD RENDERER
+  # ======================================================================
+  - phase: dashboard_renderer
+    summary: "Build dashboard registry, deterministic payload builder, and inspector."
+    items:
+      - id: RENDER-001
+        title: "Implement dashboard registry"
+        tasks:
+          - "versioned dashboard definitions."
+          - "stored under config/dashboards/."
+          - "schema validation."
+      - id: RENDER-002
+        title: "Implement deterministic dashboard payload builder"
+        tasks:
+          - "input = canonical artifact set."
+          - "output = snapshot tested payload."
+          - "ensure timezone = UTC."
+      - id: RENDER-003
+        title: "Implement resource inspector"
+        tasks:
+          - "artifact timeline."
+          - "preview viewer."
+          - "GuardScore overlay."
+
+  # ======================================================================
+  # 9. FRONT-END (WEB)
+  # ======================================================================
+  - phase: front_end_web
+    summary: "Implement deterministic UI skeletons, preview viewers, and SSR snapshots."
+    items:
+      - id: WEB-001
+        title: "UI skeleton"
+        tasks:
+          - "executive dashboard."
+          - "engineering dashboard."
+          - "compliance dashboard."
+      - id: WEB-002
+        title: "Preview viewer"
+        tasks:
+          - "normalized diff."
+          - "confidence score."
+          - "apply hints."
+      - id: WEB-003
+        title: "Frontend determinism"
+        tasks:
+          - "pinned node version."
+          - "pinned dependencies."
+          - "normalized SSR snapshots."
+
+  # ======================================================================
+  # 10. EXPORTS & AUDIT BUNDLES
+  # ======================================================================
+  - phase: exports_and_audit_bundles
+    summary: "Implement export services, signing, and deterministic snapshot tests."
+    items:
+      - id: EXPORT-001
+        title: "Implement export job service"
+        tasks:
+          - "json, csv, pdf."
+          - "PDF must be deterministic & signed."
+      - id: EXPORT-002
+        title: "Bundle signing"
+        tasks:
+          - "use platform KMS."
+          - "rotate signing keys."
+          - "include key_id for verification."
+      - id: EXPORT-003
+        title: "Snapshot tests for export payloads"
+        tasks:
+          - "3-run determinism."
+          - "CI cross-image test."
+
+  # ======================================================================
+  # 11. DETERMINISM & SNAPSHOTS
+  # ======================================================================
+  - phase: determinism_and_snapshots
+    summary: "Prove dashboard and export determinism across runs and platforms."
+    items:
+      - id: DET-001
+        title: "Dashboard payload determinism"
+        tasks:
+          - "3-run identical hash."
+          - "cross-platform normalization."
+      - id: DET-002
+        title: "Export determinism"
+        tasks:
+          - "deterministic layout, fonts, metadata."
+          - "no local timezone use."
+
+  # ======================================================================
+  # 12. PERFORMANCE & SCALABILITY
+  # ======================================================================
+  - phase: performance_and_scalability
+    summary: "Run load tests, scaling checks, and telemetry backpressure controls."
+    items:
+      - id: PERF-001
+        title: "Load tests"
+        tasks:
+          - "page_load_time_ms ≤ 600 (95th)."
+          - "api_99th ≤ 1200ms."
+      - id: PERF-002
+        title: "Concurrent load scaling"
+        tasks:
+          - "simulate 5000 users."
+          - "measure cache hit ratio."
+      - id: PERF-003
+        title: "Telemetry backpressure"
+        tasks:
+          - "return 429 when ingest rate too high."
+          - "validate retry/backoff behavior."
+
+  # ======================================================================
+  # 13. OBSERVABILITY
+  # ======================================================================
+  - phase: observability
+    summary: "Collect metrics, tracing, and structured logs for GuardBoard flows."
+    items:
+      - id: OBS-001
+        title: "Metrics"
+        tasks:
+          - "dashboards_rendered_total."
+          - "api_requests_total."
+          - "ingest_total{status}."
+          - "cache_hit_ratio."
+      - id: OBS-002
+        title: "Tracing"
+        tasks:
+          - "ingest → validation → cache → render → export."
+      - id: OBS-003
+        title: "Structured logs"
+        tasks:
+          - "request_id, user_id, artifact_id, action."
+
+  # ======================================================================
+  # 14. SECURITY CONTROLS
+  # ======================================================================
+  - phase: security_controls
+    summary: "Enforce transport, sandbox, and redaction security controls."
+    items:
+      - id: SEC-001
+        title: "Transport security"
+        tasks:
+          - "enforce TLS 1.2+."
+          - "enable HSTS."
+      - id: SEC-002
+        title: "Sandbox preview execution"
+        tasks:
+          - "WASM or equivalent sandbox."
+          - "block network egress."
+      - id: SEC-003
+        title: "Redaction mechanisms"
+        tasks:
+          - "redact sensitive fields per role & export type."
+
+  # ======================================================================
+  # 15. CI/CD & QUALITY GATES
+  # ======================================================================
+  - phase: ci_cd_quality_gates
+    summary: "Configure CI jobs, forbidden override checks, and regression gates."
+    items:
+      - id: CI-001
+        title: "CI pipeline"
+        tasks:
+          - "validate_schema."
+          - "unit."
+          - "integration."
+          - "e2e."
+          - "snapshot_conformance."
+          - "perf_regression."
+      - id: CI-002
+        title: "Forbidden overrides"
+        tasks:
+          - "static check for schema/output contract drift."
+
+  # ======================================================================
+  # 16. DOCUMENTATION
+  # ======================================================================
+  - phase: documentation
+    summary: "Produce API docs, dashboard authoring guide, and ingest runbooks."
+    items:
+      - id: DOC-001
+        title: "API docs"
+        tasks:
+          - "OpenAPI validated & published."
+          - "examples for each endpoint."
+      - id: DOC-002
+        title: "Dashboard authoring guide"
+        tasks:
+          - "schema."
+          - "versioning rules."
+      - id: DOC-003
+        title: "Ingest pipeline runbook"
+        tasks:
+          - "schema drift."
+          - "replay attacks."
+          - "poison queue handling."
+
+  # ======================================================================
+  # 17. ACCEPTANCE GATES
+  # ======================================================================
+  - phase: acceptance_gates
+    summary: "Final readiness validation for schema, RBAC, determinism, performance, and security."
+    items:
+      - id: ACPT-001
+        title: "Schema validation"
+        tasks:
+          - "all consumed artifacts validate at ingest."
+      - id: ACPT-002
+        title: "RBAC enforcement"
+        tasks:
+          - "automated tests verifying all roles."
+      - id: ACPT-003
+        title: "Determinism"
+        tasks:
+          - "dashboard + export determinism proven in CI."
+      - id: ACPT-004
+        title: "Performance"
+        tasks:
+          - "meets page_load + api latency targets."
+      - id: ACPT-005
+        title: "Security"
+        tasks:
+          - "sandbox, TLS, redaction validated."
 
-- id: API-004
-  title: "GraphQL gateway (optional)"
-  tasks:
-    - auto-generate schema from artifact schemas
-    - authorization wiring
-
-# ======================================================================
-# 8. DASHBOARD RENDERER
-# ======================================================================
-- id: RENDER-001
-  title: "Implement dashboard registry"
-  tasks:
-    - versioned dashboard definitions
-    - stored under config/dashboards/
-    - schema validation
-
-- id: RENDER-002
-  title: "Implement deterministic dashboard payload builder"
-  tasks:
-    - input = canonical artifact set
-    - output = snapshot tested payload
-    - ensure timezone = UTC
-
-- id: RENDER-003
-  title: "Implement resource inspector"
-  tasks:
-    - artifact timeline
-    - preview viewer
-    - GuardScore overlay
-
-# ======================================================================
-# 9. FRONT-END (WEB)
-# ======================================================================
-- id: WEB-001
-  title: "UI skeleton"
-  tasks:
-    - executive dashboard
-    - engineering dashboard
-    - compliance dashboard
-
-- id: WEB-002
-  title: "Preview viewer"
-  tasks:
-    - normalized diff
-    - confidence score
-    - apply hints
-
-- id: WEB-003
-  title: "Frontend determinism"
-  tasks:
-    - pinned node version
-    - pinned dependencies
-    - normalized SSR snapshots
-
-# ======================================================================
-# 10. EXPORTS & AUDIT BUNDLES
-# ======================================================================
-- id: EXPORT-001
-  title: "Implement export job service"
-  tasks:
-    - json, csv, pdf
-    - PDF must be deterministic & signed
-
-- id: EXPORT-002
-  title: "Bundle signing"
-  tasks:
-    - use platform KMS
-    - rotate signing keys
-    - include key_id for verification
-
-- id: EXPORT-003
-  title: "Snapshot tests for export payloads"
-  tasks:
-    - 3-run determinism
-    - CI cross-image test
-
-# ======================================================================
-# 11. DETRMINISM & SNAPSHOTS
-# ======================================================================
-- id: DET-001
-  title: "Dashboard payload determinism"
-  tasks:
-    - 3-run identical hash
-    - cross-platform normalization
-
-- id: DET-002
-  title: "Export determinism"
-  tasks:
-    - deterministic layout, fonts, metadata
-    - no local timezone use
-
-# ======================================================================
-# 12. PERFORMANCE & SCALABILITY
-# ======================================================================
-- id: PERF-001
-  title: "Load tests"
-  tasks:
-    - page_load_time_ms ≤ 600 (95th)
-    - api_99th ≤ 1200ms
-
-- id: PERF-002
-  title: "Concurrent load scaling"
-  tasks:
-    - simulate 5000 users
-    - measure cache hit ratio
-
-- id: PERF-003
-  title: "Telemetry backpressure"
-  tasks:
-    - return 429 when ingest rate too high
-    - validate retry/backoff behavior
-
-# ======================================================================
-# 13. OBSERVABILITY
-# ======================================================================
-- id: OBS-001
-  title: "Metrics"
-  tasks:
-    - dashboards_rendered_total
-    - api_requests_total
-    - ingest_total{status}
-    - cache_hit_ratio
-
-- id: OBS-002
-  title: "Tracing"
-  tasks:
-    - ingest → validation → cache → render → export
-
-- id: OBS-003
-  title: "Structured logs"
-  tasks:
-    - request_id, user_id, artifact_id, action
-
-# ======================================================================
-# 14. SECURITY CONTROLS
-# ======================================================================
-- id: SEC-001
-  title: "Transport security"
-  tasks:
-    - enforce TLS 1.2+
-    - enable HSTS
-
-- id: SEC-002
-  title: "Sandbox preview execution"
-  tasks:
-    - WASM or equivalent sandbox
-    - block network egress
-
-- id: SEC-003
-  title: "Redaction mechanisms"
-  tasks:
-    - redact sensitive fields per role & export type
-
-# ======================================================================
-# 15. CI/CD & QUALITY GATES
-# ======================================================================
-- id: CI-001
-  title: "CI pipeline"
-  tasks:
-    - validate_schema
-    - unit
-    - integration
-    - e2e
-    - snapshot_conformance
-    - perf_regression
-
-- id: CI-002
-  title: "Forbidden overrides"
-  tasks:
-    - static check for schema/output contract drift
-
-# ======================================================================
-# 16. DOCUMENTATION
-# ======================================================================
-- id: DOC-001
-  title: "API docs"
-  tasks:
-    - OpenAPI validated & published
-    - examples for each endpoint
-
-- id: DOC-002
-  title: "Dashboard authoring guide"
-  tasks:
-    - schema
-    - versioning rules
-
-- id: DOC-003
-  title: "Ingest pipeline runbook"
-  tasks:
-    - schema drift
-    - replay attacks
-    - poison queue handling
-
-# ======================================================================
-# 17. ACCEPTANCE GATES
-# ======================================================================
-- id: ACPT-001
-  title: "Schema validation"
-  tasks:
-    - all consumed artifacts validate at ingest
-
-- id: ACPT-002
-  title: "RBAC enforcement"
-  tasks:
-    - automated tests verifying all roles
-
-- id: ACPT-003
-  title: "Determinism"
-  tasks:
-    - dashboard + export determinism proven in CI
-
-- id: ACPT-004
-  title: "Performance"
-  tasks:
-    - meets page_load + api latency targets
-
-- id: ACPT-005
-  title: "Security"
-  tasks:
-    - sandbox, TLS, redaction validated
