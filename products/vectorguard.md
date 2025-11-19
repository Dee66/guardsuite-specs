VectorGuard — Product Specification (V2.0.0)

This specification was generated using the GuardSuite Templated Specification System (V1.0).

1. Product Identity
Key	Value
Product Name	VectorGuard
Product ID	vectorguard
Pillar	Vector
Product Type	Paid Governance Blueprint
Core Dependency	guardsuite-core ≥1.4.0, <2.0.0
Maintainers	Dee Prinsloo — AI Solutions Architect
2. Purpose & Scope
2.1 Mission

VectorGuard provides deterministic, enterprise-grade governance for vector database infrastructure, embedding workflows, and LLM-adjacent storage architectures. It enforces 500+ hardening checks, delivers a fully canonicalized output schema, integrates with GuardScore, and ships with FixPack-Lite remediation snippets.

2.2 Problem Space

Vector workloads introduce unique risks:

Embedding leakage

Over-permissive access to vector stores

Missing encryption or KMS misconfiguration

Misconfigured network boundaries

RAG pipelines exposing sensitive embeddings

Undocumented data replication across regions

Drift between TF resources and underlying vector DB configuration

VectorGuard explicitly targets these risks for regulated or sensitive environments.

2.3 Intended Users

Cloud Security Engineers

DevOps & Platform Engineers

AI Infrastructure Teams

Compliance & Risk Engineers

Enterprise Architecture teams managing vector DB pipelines

2.4 Out of Scope

VectorGuard does not:

perform live runtime checks on deployed vector DBs

modify Terraform plans directly (FixPack snippets are deterministic samples)

monitor real-time embedding traffic

replace full SIEM systems

3. Architectural Positioning
3.1 Relationship to Pillar

VectorGuard is the paid governance blueprint for the Vector Pillar.
It extends VectorScan by adding:

full governance rule library (500+ deterministic checks)

FixPack-Lite

compliance ledger

weighted GuardScore integration

3.2 Relationship to guardsuite-core (Semantic Key-Value Form)
core_dependency_id: guardsuite-core@1.4.x
required_interfaces:
  - I_Evaluator
  - I_ScannerCLI
override_exclusion:
  - evaluator.runtime_check
  - canonical.output_contract
schema_source: guardsuite-core/canonical_schema.json
output_contract: strict

3.3 Independence & Interoperability

VectorGuard:

runs independently of other products

uses guardsuite-core for evaluation lifecycle

emits schema-compliant JSON

integrates cleanly with Playground, GuardScore, and GuardBoard

may be sold standalone with no dependency on other GuardSuite products

4. Canonical Output & Schema Conformance
4.1 Required Fields

VectorGuard MUST emit all canonical fields:

pillar
scan_version
guardscore_rules_version
canonical_schema_version
latency_ms
quick_score_mode
environment
issues[]
pillar_score_inputs
percentile_placeholder
guardscore_badge
playground_summary

4.2 Product-Specific Extensions
vectorguard:
  compliance_ledger_enabled: true
  remediation_density: true

4.3 Output Determinism

no random values

no time-varying ordering

canonicalize_output MUST be applied

schema validation MUST pass in CI

5. Rule Architecture
5.1 Rule Philosophy

Rules MUST:

be pure

be deterministic

never modify input

return IssueDict objects

conform to guardsuite-core severity semantics

avoid external API calls

5.2 Rule Categories

Network Boundary Controls

Encryption & Key Governance

IAM & Principal Hardening

Embedding Storage Security

Data Exposure & Exfiltration

Configuration Drift Detection

Resource Lifecycle Policies

5.3 Representative Rules
ID	Title	Severity	Summary
VG-NET-001	Public Vector DB Endpoint	critical	Detects vector DBs accessible from 0.0.0.0/0.
VG-ENC-004	Storage Encryption Disabled	high	Ensures vector DB and embedding buckets have encryption.
VG-IAM-021	Overly Broad Access Role	high	Detects IAM roles with wildcards in vector data paths.
VG-DRIFT-009	RAG Drift Between TF & Runtime	medium	Detects mismatch between configuration objects.
5.4 Rule Implementation Constraints

no external calls

must use guardsuite-core helpers

scoring severity mapping must match GuardScore

6. FixPack-Lite
6.1 Purpose

VectorGuard includes deterministic remediation snippets for its highest-impact issues.

6.2 Snippet Structure

Each snippet must follow:

fixpack/vector/<ISSUE_ID>.hcl


Includes metadata block:

# fixpack: ISSUE_ID
# difficulty: low|medium|high
# summary: one-line description

6.3 Mappings

Issues reference remediation snippets via:

remediation_hint: "fixpack:VG-NET-001"

6.4 Inclusion Policy

VectorGuard includes top 5–10 pillar-critical FixPacks.

7. Compliance Ledger

VectorGuard outputs a structured compliance ledger:

each rule maps to compliance status

ledger is deterministic

fully canonical JSON

exposed for GuardBoard

8. Ecosystem Integrations
8.1 GuardScore Integration
pillar_weight: 0.33
severity_penalties:
  critical: 40
  high: 25
  medium: 10
  low: 2
score_inputs:
  - issue_count_by_severity
  - fixpack_density
  - compliance_ledger_density

8.2 Playground Compatibility

WASM-safe evaluator

< 2s runtime

JSON and SVG sanitization

QuickScore fallback

8.3 GuardBoard Integration

publishes badge metadata

exposes compliance ledger panels

supports FixPack-Lite recommendation cards

9. CLI Behavior

inherits BaseScanner from guardsuite-core

vectorguard scan --stdin

supports --json, --quiet, --explain

paid-only flags:

--compliance-ledger

--fixpack-summary

10. Operational Constraints

max memory 250MB

avg runtime ~800ms

large plans up to ~1800ms

Playground runtime capped at 2000ms

11. Versioning & Release Governance

follows semantic versioning

core dependency pinned by minor version

breaking rule changes require release notes

schema changes must follow guardsuite-core RFC process

12. Testing Requirements

unit tests for all rule files

integration tests for evaluator

canonical schema snapshot tests

regression suite for FixPack-Lite mappings

13. Security Considerations

input fully sanitized

no external I/O

no environment-variable dependency

deterministic error handling

14. Appendices
Representative FixPack Example
# fixpack: VG-NET-001
# difficulty: low
resource "aws_security_group_rule" "block_public" {
  cidr_blocks = ["10.0.0.0/8"]
}