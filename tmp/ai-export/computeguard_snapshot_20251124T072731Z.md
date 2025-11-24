# ComputeGuard — Spec Snapshot
_Commit: ada9477f7404f20ae367f703bc304917be627e58 — Generated: 2025-11-24T07:27:31.955429Z_

ComputeGuard is the premium compute governance and remediation blueprint for
organizations operating GPU-heavy or cost-sensitive ML/AI workloads. It
extends ComputeScan with deterministic FixPack-Lite remediation, advanced
FinOps rule coverage, full compliance ledger generation, and GuardBoard-ready
overlays. ComputeGuard is designed for teams requiring deep visibility into
GPU usage, instance sizing, cost anomalies, and compute governance.



## Marketing

**Hero:** Eliminate GPU waste with enterprise FinOps guardrails and deterministic fixes.

- Advanced GPU and compute governance with 600+ rules
- Deterministic FixPack-Lite for cost and config remediation
- Compliance ledger for FinOps auditability
- GuardScore upgrades for executive cost reporting



| CTA | Link |
|-----|------|

| Get ComputeGuard | /buy/computeguard |




## Spec (machine-readable excerpt)
```yaml
id: computeguard
name: ComputeGuard
product_type: paid_blueprint
pillar: compute
version: 2.0.0
status: production
short_description: 'Enterprise FinOps governance, deterministic remediation, compliance
  ledger, and premium GuardScore inputs for GPU and compute-heavy infrastructure.

  '
long_description: 'ComputeGuard is the premium compute governance and remediation
  blueprint for

  organizations operating GPU-heavy or cost-sensitive ML/AI workloads. It

  extends ComputeScan with deterministic FixPack-Lite remediation, advanced

  FinOps rule coverage, full compliance ledger generation, and GuardBoard-ready

  overlays. ComputeGuard is designed for teams requiring deep visibility into

  GPU usage, instance sizing, cost anomalies, and compute governance.

  '
purpose_summary: 'Provide deterministic cost governance, remediation, and compliance-level
  visibility across GPU and compute infrastructure.

  '
marketing:
  hero: Eliminate GPU waste with enterprise FinOps guardrails and deterministic fixes.
  blurbs:
  - Advanced GPU and compute governance with 600+ rules
  - Deterministic FixPack-Lite for cost and config remediation
  - Compliance ledger for FinOps auditability
  - GuardScore upgrades for executive cost reporting
  ctas:
  - text: Get ComputeGuard
    href: /buy/computeguard
architecture:
  core_dependency_id: guardsuite-core@>=1.4.0,<2.0.0
  schema_source: guardsuite-core/canonical_schema.json
  required_interfaces:
  - I_Evaluator
  - I_ScannerCLI
  - I_ComplianceLedger
  override_exclusion:
  - canonical.output_contract
  - evaluator.runtime_override
  - compliance.disable_ledger
  output_contract: strict
governance_domains:
- cost_finops
- gpu_provisioning
- instance_sizing
- autoscaling_risk
- spot_instance_policy
- drift_detection
- observability_gaps
- compliance_mapping
- deterministic_remediation
rule_categories:
- GPU Provisioning & Utilization
- Rightsizing & Instance Sizing
- Autoscaling Safety
- Spot & Preemptible Policy
- Idle/Orphaned Resource Detection
- Cost Escalation Pattern Detection
- Observability & Telemetry
- Compliance Mapping
- Deterministic Remediation
features:
- id: CMPG-FEAT-010
  title: Full Compute Governance Coverage
  summary: 600+ advanced compute and GPU governance checks.
  included: true
- id: CMPG-FEAT-020
  title: Compliance Ledger
  summary: Detailed FinOps and cost-governance ledger output.
  included: true
- id: CMPG-FEAT-030
  title: FixPack-Lite Remediation
  summary: Deterministic cost and GPU remediation snippets.
  included: true
- id: CMPG-FEAT-040
  title: Advanced GuardScore Inputs
  summary: Premium scoring metrics for compute waste and cost anomalies.
  included: true
- id: CMPG-FEAT-050
  title: Pipeline-aware Compute Governance
  summary: Flags risky upstream/downstream compute dependencies.
  included: true
fixpack:
  included: true
  fixpack_folder: fixpack/compute
  reference_hint_format: fixpack:<ISSUE_ID>
  surfaces_hints: true
  snippet_count: 10
compliance:
  compliance_ledger_enabled: true
  ledger_visibility: full
  ledger_schema_version: 1.0.0
cli:
  base_command: computeguard
  scan_command: computeguard scan
  supported_flags:
  - --json
  - --stdin
  - --quiet
  - --explain
  - --output json
  - --fixpack-summary
  - --compliance-ledger
  reserved_flags:
  - --ledger-only
  - --fixpack-diff
performance_constraints:
  max_memory_mb: 260
  expected_runtime_ms: 850
  large_plan_runtime_ms: 2000
  playground_runtime_ms: 2100
  quickscore_threshold_resources: 800
ecosystem_integrations:
  guardscore:
    pillar_weight: 0.33
    severity_penalties:
      critical: 40
      high: 25
      medium: 10
      low: 2
    provided_score_inputs:
    - gpu_waste_estimate
    - compute_cost_risk
    - remediation_hint_count
    - fixpack_applied_count
    - compliance_ledger_item_count
    - resource_count
    badge_eligibility_signal: true
  playground:
    wasm_safe: true
    max_runtime_ms: 2000
    playground_latency_target_ms: 1600
    json_sanitize: true
    svg_sanitize: true
    quick_score_mode: true
  guardboard:
    exposes_fixpack_hints: true
    shows_compliance_ledger: true
    badge_preview_supported: true
    advanced_score_overlays: true
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
  breaking_change_policy: 'Any breaking change requires a guardsuite-core RFC, FinOps
    ledger schema migration note, and coordinated release with ComputeScan.

    '
interoperability_conflicts:
- Cost-governance FixPack interactions may require GuardScore v2 recalibration.
- Future GPU telemetry hooks require coordinated schema updates.
future_extensions:
- Inference cost modeling
- GPU topology governance
- Cluster autoscaler deep heuristics
security:
  no_external_calls_at_runtime: true
  sanitize_all_inputs: true
  svg_sanitization: true
  wasm_compatible: true
  sandbox_requirement: Playground runtime must be WASM sandboxed
  safe_error_reporting: true
maintainers:
- name: Deon Prinsloo
  role: AI Solutions Architect
  contact: deon@shieldcraft-ai.com
release_metadata:
  release_channel: stable
  release_notes_url: https://shieldcraft-ai.com/guardsuite/computeguard/releases/2.0.0
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
  - Deliver turnkey compute governance
  - Expose executive-ready GuardBoard signals
governance:
  spec_version: '2025.11'
  last_reviewed: '2025-11-23'
  owner: GuardSuite PMO
  stability_level: ga
contract_ref: null
related_products:
- computescan
- guardscore
- guardboard
- playground
```

## Architecture

- Core dependency: `guardsuite-core@>=1.4.0,<2.0.0`  
- Schema source: `guardsuite-core/canonical_schema.json`  
- Interfaces: I_Evaluator, I_ScannerCLI, I_ComplianceLedger  

- Overrides excluded: canonical.output_contract, evaluator.runtime_override, compliance.disable_ledger  

- Output contract: `strict`



## Feature Summary



- `CMPG-FEAT-010` — **Full Compute Governance Coverage**: 600+ advanced compute and GPU governance checks. _(Included: Yes)_

- `CMPG-FEAT-020` — **Compliance Ledger**: Detailed FinOps and cost-governance ledger output. _(Included: Yes)_

- `CMPG-FEAT-030` — **FixPack-Lite Remediation**: Deterministic cost and GPU remediation snippets. _(Included: Yes)_

- `CMPG-FEAT-040` — **Advanced GuardScore Inputs**: Premium scoring metrics for compute waste and cost anomalies. _(Included: Yes)_

- `CMPG-FEAT-050` — **Pipeline-aware Compute Governance**: Flags risky upstream/downstream compute dependencies. _(Included: Yes)_



## FixPack Snapshot



- Reference hints: `fixpack:<ISSUE_ID>`  
- Surfaces hints: **True**




## Compliance & Security

- Ledger visibility: **full**  
- Ledger enabled: **True**  
- Sandbox requirement: `Playground runtime must be WASM sandboxed`  
- WASM compatible: **True**  
- SVG sanitization: **True**

## Ecosystem Integrations

- GuardScore weight: 0.33 (inputs: gpu_waste_estimate, compute_cost_risk, remediation_hint_count, fixpack_applied_count, compliance_ledger_item_count, resource_count)  
- Playground latency target: 1600 ms (quick mode: True)  
- GuardBoard badge preview: True

## Performance Snapshot


- Max memory: 260 MB  
- Expected runtime: 850 ms  
- Large plan runtime: 2000 ms  

- Playground runtime: 2100 ms  
- QuickScore threshold: 800 resources  








## Versioning & Roadmap

- Core pin: `guardsuite-core@>=1.4.0,<2.0.0`  
- Schema pin: `canonical_schema@1.0.0`  
- Breaking policy: Any breaking change requires a guardsuite-core RFC, FinOps ledger schema migration note, and coordinated release with ComputeScan.



**Interoperability Risks**

- Cost-governance FixPack interactions may require GuardScore v2 recalibration.
- Future GPU telemetry hooks require coordinated schema updates.



**Future Extensions**

- Inference cost modeling
- GPU topology governance
- Cluster autoscaler deep heuristics


## References



- Master Spec: `docs/guardsuite_master_spec.md`  
- Template: `templates/spec_page.md.j2`  
- Canonical schema: `guardsuite-core/canonical_schema.json`


Generated by guardsuite-specs export tool.
