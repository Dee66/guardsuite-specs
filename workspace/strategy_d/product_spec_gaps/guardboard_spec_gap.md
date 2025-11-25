# guardboard Product Spec Gap

- metadata_path: products/guardboard/metadata/product.yml
- metadata_exists: True
- top_level_keys (32): api, architecture, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, id, integration_points, long_description, maintainers, marketing, metadata, name, performance_constraints, pillar, product_type, provenance, purpose_summary, references, related_products, release_metadata, rule_categories, security, short_description, status, testing, version, versioning

## Missing Canonical Fields
- products
- spec_yaml
- checklist_yaml
- gpt_instructions_yaml

## Extra Fields
- api
- cli
- compliance
- ecosystem_integrations
- fixpack
- future_extensions
- governance_domains
- integration_points
- maintainers
- performance_constraints
- purpose_summary
- references
- release_metadata
- rule_categories
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
products: [missing]
spec_yaml: [missing]
checklist_yaml: [missing]
gpt_instructions_yaml: [missing]
```
