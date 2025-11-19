# GuardSuite Master Specification (V1.1)

## Purpose
This master specification defines the shared guardrails, terminology, and lifecycle expectations for every GuardSuite pillar. Individual product specs (for example, VectorScan or ComputeGuard) inherit these source-of-truth principles.

## Core Principles
1. **Deterministic Inputs** — All scanners must consume declarative artifacts (Terraform plans, CI manifests, compute state) with no network lookups.
2. **Schema-First** — Canonical YAML specs feed renderers, fixpacks, and AI exports. No documentation is ever edited downstream.
3. **Human + Machine Ready** — Every release must produce readable docs, JSON artifacts, and AI-ready snapshots from the same data.
4. **Safe Automation** — Sync scripts and workflows default to dry-run behavior until human reviewers opt-in to push changes.

## Delivery Lifecycle
| Stage | Artifact | Outcome |
| --- | --- | --- |
| Spec Authoring | `products/<id>.yml` | Maintainers update structured copy, features, and fixpacks. |
| Validation | `scripts/validate_products.py` & `scripts/validate_yaml_schema.py` | Ensures schema compliance before rendering. |
| Rendering | `scripts/gen_docs.py` | Produces Markdown for docs and downstream repos. |
| AI Snapshot | `scripts/export_for_ai.py` | Generates deterministic paste-ready summaries. |
| Sync | `scripts/sync_to_repo.py` | Copies docs into target repos under human supervision. |

## Pillar Expectations
- **GuardScore Alignment** — Every product must record severity levels compatible with GuardScore rollups.
- **FixPack Parity** — If a rule exposes remediation, a matching `fixpack/<ISSUE>.hcl` entry must exist before release.
- **Latency Budget** — Total CLI runtime per scan must remain under 5 minutes for 95th percentile plans.

## Versioning
- Major changes to schema keys require bumping this document to the next minor version and notifying downstream repos.
- Patch releases focus on copy or metadata adjustments that do not change schema compatibility.

Refer to this master spec whenever onboarding a new GuardSuite pillar or expanding existing products.
