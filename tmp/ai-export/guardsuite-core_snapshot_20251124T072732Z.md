# GuardSuite Core — Spec Snapshot
_Commit: ada9477f7404f20ae367f703bc304917be627e58 — Generated: 2025-11-24T07:27:32.037678Z_

GuardSuite Core is the shared runtime, schema bundle, and CLI harness that all
GuardSuite scanners, blueprints, and governance tooling depend on. It contains
canonical JSON schemas, deterministic loader utilities, registry management for
FixPack packs, and the GuardScore contract definitions. Every pillar consumes
this package to guarantee consistent plan ingestion, issue serialization, and
doc/template rendering. GuardSuite Core is versioned alongside the pillars and
enforces strict backwards compatibility windows so downstream products can
adopt new schema features confidently.



## Marketing

**Hero:** Powering every GuardSuite scanner, blueprint, and dashboard.

- Canonical schemas and runtime harness shared across pillars
- Deterministic plan loader, renderer, and FixPack registry
- Versioned GuardScore contracts with long-term compatibility



| CTA | Link |
|-----|------|

| Explore GuardSuite Core | /docs/guardsuite-core |




## Spec (machine-readable excerpt)
```yaml
id: guardsuite-core
name: GuardSuite Core
product_type: core
pillar: crosscut
version: 2.0.0
status: production
short_description: 'Canonical libraries, schemas, and CLI glue that power every GuardSuite
  pillar with deterministic parsing, validation, and renderer utilities.

  '
long_description: 'GuardSuite Core is the shared runtime, schema bundle, and CLI harness
  that all

  GuardSuite scanners, blueprints, and governance tooling depend on. It contains

  canonical JSON schemas, deterministic loader utilities, registry management for

  FixPack packs, and the GuardScore contract definitions. Every pillar consumes

  this package to guarantee consistent plan ingestion, issue serialization, and

  doc/template rendering. GuardSuite Core is versioned alongside the pillars and

  enforces strict backwards compatibility windows so downstream products can

  adopt new schema features confidently.

  '
purpose_summary: 'Provide a single, versioned source of truth for schemas, runtimes,
  and CLI harnesses that every GuardSuite pillar consumes for deterministic behavior.

  '
marketing:
  hero: Powering every GuardSuite scanner, blueprint, and dashboard.
  blurbs:
  - Canonical schemas and runtime harness shared across pillars
  - Deterministic plan loader, renderer, and FixPack registry
  - Versioned GuardScore contracts with long-term compatibility
  ctas:
  - text: Explore GuardSuite Core
    href: /docs/guardsuite-core
architecture:
  core_dependency_id: guardsuite-core@>=2.0.0
  schema_source: guardsuite-core/canonical_schema.json
  required_interfaces:
  - I_PlanLoader
  - I_IssueSerializer
  - I_TemplateRenderer
  override_exclusion:
  - canonical.output_contract
  - engine.payload_serializer
  output_contract: strict
governance_domains:
- schema_governance
- cli_tooling
- fixpack_registry
- scoring_contracts
- template_rendering
- compliance_controls
rule_categories:
- Schema Evolution & Compatibility
- CLI Harness & Transport
- FixPack Lifecycle Guardrails
- GuardScore Contract Enforcement
- Template Rendering & Docs
features:
- id: CORE-FEAT-010
  title: Canonical Schema Bundle
  summary: Ships JSON Schema + Python contracts for every pillar.
  included: true
- id: CORE-FEAT-020
  title: Deterministic Loader
  summary: Shared plan/YAML ingestion with strict limits.
  included: true
- id: CORE-FEAT-030
  title: FixPack Registry
  summary: Registers remediation snippets and metadata for paid products.
  included: true
- id: CORE-FEAT-040
  title: Template + Renderer SDK
  summary: Jinja + Markdown renderer utilities for docs and snapshots.
  included: true
fixpack:
  included: false
  reference_hint_format: fixpack:<ISSUE_ID>
  surfaces_hints: false
compliance:
  compliance_ledger_enabled: false
  ledger_visibility: none
cli:
  base_command: guardsuite-core
  supported_flags:
  - --schema
  - --plan
  - --strict
  - --output json
  reserved_flags:
  - --experimental
api:
  rest_endpoint: https://api.shieldcraft-ai.com/guardsuite-core
  auth: GuardSuite API token
performance_constraints:
  max_memory_mb: 256
  expected_runtime_ms: 400
  large_plan_runtime_ms: 900
  playground_runtime_ms: 1000
  quickscore_threshold_resources: 1500
  realtime_refresh_interval_ms: 30000
ecosystem_integrations:
  guardscore:
    pillar_weight: 0.0
    severity_penalties:
      critical: 40
      high: 25
      medium: 10
      low: 2
    provided_score_inputs:
    - guardscore_contract_version
    - schema_version
    - fixpack_registry_state
    badge_eligibility_signal: false
  playground:
    wasm_safe: true
    max_runtime_ms: 1500
    playground_latency_target_ms: 900
    json_sanitize: true
    svg_sanitize: true
    quick_score_mode: false
  guardboard:
    exposes_fixpack_hints: true
    shows_compliance_ledger: false
    badge_preview_supported: false
testing:
  unit_tests_required: true
  integration_tests_required: true
  snapshot_schema_test: true
  test_coverage_min_percent: 90
  ci_jobs:
  - validate_schema
  - unit
  - integration
  - snapshot_conformance
versioning:
  semver: true
  core_dependency_pin: guardsuite-core@>=2.0.0
  schema_version_pin: canonical_schema@2.0.0
  breaking_change_policy: 'Requires guardsuite-core RFC, coordinated pillar updates,
    and template & doc regeneration before release.

    '
interoperability_conflicts:
- Schema upgrades require simultaneous GuardScore recalibration.
- FixPack registry format changes can break paid pillar ingestion.
future_extensions:
- Rust-based WASM harness
- FixPack signature validation
- Schema diff tooling for release PRs
security:
  no_external_calls_at_runtime: true
  sanitize_all_inputs: true
  svg_sanitization: true
  wasm_compatible: true
  sandbox_requirement: Core CLI must run in WASM sandbox for Playground linting
  safe_error_reporting: true
maintainers:
- name: Deon Prinsloo
  role: AI Solutions Architect
  contact: deon@shieldcraft-ai.com
release_metadata:
  release_channel: stable
  release_notes_url: https://shieldcraft-ai.com/guardsuite/guardsuite-core/releases/2.0.0
  published_date: '2025-11-19'
references:
  master_spec: docs/guardsuite_master_spec.md
  template_spec: templates/spec_page.md.j2
  canonical_schema: guardsuite-core/canonical_schema.json
metadata:
  version: '2025.11'
  funnel_stage: mid_funnel
  pricing_reference: pricing/guardsuite_pricing.yml
  ux_goals:
  - Coordinate canonical schema evolution
  - Expose evaluator/runtime guarantees
governance:
  spec_version: '2025.11'
  last_reviewed: '2025-11-23'
  owner: GuardSuite PMO
  stability_level: ga
contract_ref: null
related_products:
- vectorscan
- vectorguard
- computescan
- computeguard
- pipelinescan
- pipelineguard
- guardscore
- guardboard
- playground
```

## Architecture

- Core dependency: `guardsuite-core@>=2.0.0`  
- Schema source: `guardsuite-core/canonical_schema.json`  
- Interfaces: I_PlanLoader, I_IssueSerializer, I_TemplateRenderer  

- Overrides excluded: canonical.output_contract, engine.payload_serializer  

- Output contract: `strict`


## API Surface

- REST endpoint: `https://api.shieldcraft-ai.com/guardsuite-core`  
- Auth: GuardSuite API token


## Feature Summary



- `CORE-FEAT-010` — **Canonical Schema Bundle**: Ships JSON Schema + Python contracts for every pillar. _(Included: Yes)_

- `CORE-FEAT-020` — **Deterministic Loader**: Shared plan/YAML ingestion with strict limits. _(Included: Yes)_

- `CORE-FEAT-030` — **FixPack Registry**: Registers remediation snippets and metadata for paid products. _(Included: Yes)_

- `CORE-FEAT-040` — **Template + Renderer SDK**: Jinja + Markdown renderer utilities for docs and snapshots. _(Included: Yes)_



## FixPack Snapshot



_No bundled FixPack metadata._


## Compliance & Security

- Ledger visibility: **none**  
- Ledger enabled: **False**  
- Sandbox requirement: `Core CLI must run in WASM sandbox for Playground linting`  
- WASM compatible: **True**  
- SVG sanitization: **True**

## Ecosystem Integrations

- GuardScore weight: 0.0 (inputs: guardscore_contract_version, schema_version, fixpack_registry_state)  
- Playground latency target: 900 ms (quick mode: False)  
- GuardBoard badge preview: False

## Performance Snapshot


- Max memory: 256 MB  
- Expected runtime: 400 ms  
- Large plan runtime: 900 ms  

- Playground runtime: 1000 ms  
- QuickScore threshold: 1500 resources  
- Realtime refresh interval: 30000 ms  








## Versioning & Roadmap

- Core pin: `guardsuite-core@>=2.0.0`  
- Schema pin: `canonical_schema@2.0.0`  
- Breaking policy: Requires guardsuite-core RFC, coordinated pillar updates, and template & doc regeneration before release.



**Interoperability Risks**

- Schema upgrades require simultaneous GuardScore recalibration.
- FixPack registry format changes can break paid pillar ingestion.



**Future Extensions**

- Rust-based WASM harness
- FixPack signature validation
- Schema diff tooling for release PRs


## References



- Master Spec: `docs/guardsuite_master_spec.md`  
- Template: `templates/spec_page.md.j2`  
- Canonical schema: `guardsuite-core/canonical_schema.json`


Generated by guardsuite-specs export tool.
