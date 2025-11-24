# GuardBoard — Spec Snapshot
_Commit: ada9477f7404f20ae367f703bc304917be627e58 — Generated: 2025-11-24T05:30:00.085762Z_

GuardBoard is the executive-facing governance and reporting console for the
entire GuardSuite ecosystem. It consumes deterministic outputs from VectorScan,
ComputeScan, PipelineScan, and all paid “Guard” products to produce unified
scorecards, trend analysis, remediation paths, and compliance-grade reports.
GuardBoard includes GuardScore visualization, FixPack-Lite upgrade reminders,
ledger summaries (from paid products), SVG badge distribution, and cross-pillar
correlation for attack-path-aware insights. Designed for CISO dashboards,
platform leadership, and compliance teams.



## Marketing

**Hero:** One dashboard. All your GuardSuite intelligence.

- Unified GuardScore across vector, compute, and pipeline pillars
- Enterprise-ready compliance reporting and ledger summaries
- SVG score badges for teams, repos, or CI pipelines



| CTA | Link |
|-----|------|

| Request Enterprise Access | /contact |




## Spec (machine-readable excerpt)
```yaml
id: guardboard
name: GuardBoard
product_type: paid_blueprint
pillar: crosscut
version: 2.0.0
status: production
short_description: 'Executive-grade governance dashboard aggregating GuardScore, FixPack
  insights, remediation paths, compliance ledgers, and multi-pillar risk visibility.

  '
long_description: "GuardBoard is the executive-facing governance and reporting console\
  \ for the\nentire GuardSuite ecosystem. It consumes deterministic outputs from VectorScan,\n\
  ComputeScan, PipelineScan, and all paid \u201CGuard\u201D products to produce unified\n\
  scorecards, trend analysis, remediation paths, and compliance-grade reports.\nGuardBoard\
  \ includes GuardScore visualization, FixPack-Lite upgrade reminders,\nledger summaries\
  \ (from paid products), SVG badge distribution, and cross-pillar\ncorrelation for\
  \ attack-path-aware insights. Designed for CISO dashboards,\nplatform leadership,\
  \ and compliance teams.\n"
purpose_summary: 'Provide a consolidated, audit-ready governance dashboard across
  all GuardSuite products, integrating GuardScore, badge issuance, FixPack summaries,
  and multi-pillar compliance signals.

  '
marketing:
  hero: One dashboard. All your GuardSuite intelligence.
  blurbs:
  - Unified GuardScore across vector, compute, and pipeline pillars
  - Enterprise-ready compliance reporting and ledger summaries
  - SVG score badges for teams, repos, or CI pipelines
  ctas:
  - text: Request Enterprise Access
    href: /contact
architecture:
  core_dependency_id: guardsuite-core@>=1.4.0,<2.0.0
  schema_source: guardsuite-core/canonical_schema.json
  required_interfaces:
  - I_BadgeRenderer
  - I_GuardScoreConsumer
  - I_LedgerAggregator
  override_exclusion:
  - canonical.output_contract
  output_contract: strict
governance_domains:
- compliance_reporting
- risk_trend_analysis
- remediation_path_insights
- severity_weight_consistency
- score_normalization
- multi_pillar_correlation
rule_categories:
- Score Normalization & Visualization
- Compliance Ledger Aggregation
- FixPack Insight Surfacing
- Trend & Drift Analysis
- Pillar Cross-Correlation
- Badge Generation & Distribution
features:
- id: GB-FEAT-001
  title: Unified GuardScore View
  summary: Aggregates GuardScore inputs from all scanners and guards.
  included: true
- id: GB-FEAT-010
  title: Compliance Ledger Summaries
  summary: Reads ledger data from VectorGuard / ComputeGuard / PipelineGuard.
  included: true
- id: GB-FEAT-020
  title: SVG Badge Generator
  summary: Generates sanitized, signed badges for CI and repo README usage.
  included: true
- id: GB-FEAT-030
  title: FixPack Insights
  summary: Displays FixPack-Lite hints and paid FixPack upgrade paths.
  included: true
- id: GB-FEAT-040
  title: Multi-Pillar Correlation
  summary: Correlates risks across vector, compute, and pipeline pillars.
  included: true
fixpack:
  included: false
  reference_hint_format: fixpack:<ISSUE_ID>
  surfaces_hints: true
compliance:
  compliance_ledger_enabled: true
  ledger_visibility: summary_only
cli:
  base_command: guardboard
  supported_flags:
  - --json
  - --from-file
  - --stdin
  - --quiet
  reserved_flags:
  - --export-ledger
  - --export-scorecard
api:
  rest_endpoint: https://api.shieldcraft-ai.com/guardboard
  auth: GuardSuite API token
performance_constraints:
  max_memory_mb: 400
  expected_runtime_ms: 900
  large_plan_runtime_ms: 1500
  playground_runtime_ms: 1800
  quickscore_threshold_resources: 5000
  realtime_refresh_interval_ms: 120000
ecosystem_integrations:
  guardscore:
    pillar_weight: 1.0
    severity_penalties:
      critical: 40
      high: 25
      medium: 10
      low: 2
    provided_score_inputs:
    - aggregate_scores
    - score_trends
    - pillar_severity_distribution
    badge_eligibility_signal: true
  playground:
    wasm_safe: true
    max_runtime_ms: 2000
    json_sanitize: true
    svg_sanitize: true
    playground_latency_target_ms: 1500
    quick_score_mode: false
  guardboard:
    exposes_fixpack_hints: true
    shows_compliance_ledger: true
    badge_preview_supported: true
testing:
  unit_tests_required: true
  integration_tests_required: true
  snapshot_schema_test: true
  test_coverage_min_percent: 85
  ci_jobs:
  - validate_schema
  - unit
  - integration
  - snapshot_conformance
versioning:
  semver: true
  core_dependency_pin: guardsuite-core@>=1.4.0,<2.0.0
  schema_version_pin: canonical_schema@1.0.0
  breaking_change_policy: 'Requires RFC + core update + regeneration of badge contract
    documents. Must maintain backward compatibility for SVG badge schema for 12 months.

    '
interoperability_conflicts:
- GuardScore v2 migration may require badge renderer updates.
- Paid FixPack-Pro integration requires API stabilization.
future_extensions:
- Historical GuardScore trend charts
- Team-based badge leaderboard
- Enterprise policy pack ingestion
- AI-driven remediation recommendation model (2026)
security:
  no_external_calls_at_runtime: true
  sanitize_all_inputs: true
  svg_sanitization: true
  wasm_compatible: true
  sandbox_requirement: Must render badges in WASM-safe sandbox
  safe_error_reporting: true
maintainers:
- name: Deon Prinsloo
  role: AI Solutions Architect
  contact: deon@shieldcraft-ai.com
release_metadata:
  release_channel: stable
  release_notes_url: https://shieldcraft-ai.com/guardsuite/guardboard/releases/2.0.0
  published_date: '2025-11-19'
references:
  master_spec: docs/guardsuite_master_spec.md
  template_spec: templates/spec_page.md.j2
  canonical_schema: guardsuite-core/canonical_schema.json
metadata:
  version: '2025.11'
  funnel_stage: toplevel_funnel
  pricing_reference: pricing/guardsuite_pricing.yml
  ux_goals:
  - Unify GuardSuite telemetry
  - Visualize remediation health for execs
governance:
  spec_version: '2025.11'
  last_reviewed: '2025-11-23'
  owner: GuardSuite PMO
  stability_level: ga
contract_ref: null
related_products:
- guardscore
- vectorguard
- computeguard
- pipelineguard
- playground
- vectorscan
- computescan
- pipelinescan
```

## Architecture

- Core dependency: `guardsuite-core@>=1.4.0,<2.0.0`  
- Schema source: `guardsuite-core/canonical_schema.json`  
- Interfaces: I_BadgeRenderer, I_GuardScoreConsumer, I_LedgerAggregator  

- Overrides excluded: canonical.output_contract  

- Output contract: `strict`


## API Surface

- REST endpoint: `https://api.shieldcraft-ai.com/guardboard`  
- Auth: GuardSuite API token


## Feature Summary



- `GB-FEAT-001` — **Unified GuardScore View**: Aggregates GuardScore inputs from all scanners and guards. _(Included: Yes)_

- `GB-FEAT-010` — **Compliance Ledger Summaries**: Reads ledger data from VectorGuard / ComputeGuard / PipelineGuard. _(Included: Yes)_

- `GB-FEAT-020` — **SVG Badge Generator**: Generates sanitized, signed badges for CI and repo README usage. _(Included: Yes)_

- `GB-FEAT-030` — **FixPack Insights**: Displays FixPack-Lite hints and paid FixPack upgrade paths. _(Included: Yes)_

- `GB-FEAT-040` — **Multi-Pillar Correlation**: Correlates risks across vector, compute, and pipeline pillars. _(Included: Yes)_



## FixPack Snapshot



_No bundled FixPack metadata._


## Compliance & Security

- Ledger visibility: **summary_only**  
- Ledger enabled: **True**  
- Sandbox requirement: `Must render badges in WASM-safe sandbox`  
- WASM compatible: **True**  
- SVG sanitization: **True**

## Ecosystem Integrations

- GuardScore weight: 1.0 (inputs: aggregate_scores, score_trends, pillar_severity_distribution)  
- Playground latency target: 1500 ms (quick mode: False)  
- GuardBoard badge preview: True

## Performance Snapshot


- Max memory: 400 MB  
- Expected runtime: 900 ms  
- Large plan runtime: 1500 ms  

- Playground runtime: 1800 ms  
- QuickScore threshold: 5000 resources  
- Realtime refresh interval: 120000 ms  








## Versioning & Roadmap

- Core pin: `guardsuite-core@>=1.4.0,<2.0.0`  
- Schema pin: `canonical_schema@1.0.0`  
- Breaking policy: Requires RFC + core update + regeneration of badge contract documents. Must maintain backward compatibility for SVG badge schema for 12 months.



**Interoperability Risks**

- GuardScore v2 migration may require badge renderer updates.
- Paid FixPack-Pro integration requires API stabilization.



**Future Extensions**

- Historical GuardScore trend charts
- Team-based badge leaderboard
- Enterprise policy pack ingestion
- AI-driven remediation recommendation model (2026)


## References



- Master Spec: `docs/guardsuite_master_spec.md`  
- Template: `templates/spec_page.md.j2`  
- Canonical schema: `guardsuite-core/canonical_schema.json`


Generated by guardsuite-specs export tool.
