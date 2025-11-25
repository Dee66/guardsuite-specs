# guardsuite_master_spec Product Spec Gap

- metadata_path: products/guardsuite_master_spec/metadata/product.yml
- metadata_exists: True
- top_level_keys (23): architecture, ci, governance, id, index, integrations, long_description, maintainers, marketing, name, pillar, product_type, purpose_summary, references, release, release_metadata, schemas, security, short_description, status, templates, testing, version

## Missing Canonical Fields
- metadata
- features
- related_products
- provenance
- products
- spec_yaml
- checklist_yaml
- gpt_instructions_yaml

## Extra Fields
- ci
- index
- integrations
- maintainers
- purpose_summary
- references
- release
- release_metadata
- schemas
- security
- templates
- testing

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
metadata: [missing]
governance: [present]
features: [missing]
architecture: [present]
related_products: [missing]
provenance: [missing]
products: [missing]
spec_yaml: [missing]
checklist_yaml: [missing]
gpt_instructions_yaml: [missing]
```
