# guardscore Product Spec Gap

- metadata_path: products/guardscore/metadata/product.yml
- metadata_exists: True
- top_level_keys (40): api, architecture, badge_contract, checklist_yaml, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, gpt_instructions_yaml, id, integration_points, interoperability_conflicts, long_description, maintainers, marketing, metadata, name, owner, performance_constraints, pillar, product_type, products, provenance, purpose_summary, references, related_products, release_metadata, rule_categories, scoring_model, security, short_description, spec_yaml, status, testing, version, versioning

## Missing Canonical Fields
- None

## Extra Fields
- api
- badge_contract
- cli
- compliance
- ecosystem_integrations
- fixpack
- future_extensions
- governance_domains
- integration_points
- interoperability_conflicts
- maintainers
- owner
- performance_constraints
- purpose_summary
- references
- release_metadata
- rule_categories
- scoring_model
- security
- testing
- versioning

## Suggested Canonical Structure
```yaml
id: [present]
name: [present]
product_type: [present]
pillar: [present]
version: [present]
status: [present]
short_description: [present]
long_description: [present]
marketing: [present]
metadata: [present]
governance: [present]
features: [present]
architecture: [present]
related_products: [present]
provenance: [present]
products: [present]
spec_yaml: [present]
checklist_yaml: [present]
gpt_instructions_yaml: [present]
```
