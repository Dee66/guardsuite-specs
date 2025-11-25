# playground Product Spec Gap

- metadata_path: products/playground/metadata/product.yml
- metadata_exists: True
- top_level_keys (36): api, api_readonly_guarantee, architecture, ecosystem_integrations, evaluator_pipeline_stages, export_bundle_contract, governance, hashing_contract, id, integration_points, long_description, metadata, name, performance_constraints, pillar, playground_stage_budgets, principles, product_type, product_version, provenance, provenance_required, purpose_summary, quickscore_behavior, references, release_metadata, sample_plan_schema, security, short_description, spec_version, stability_level, status, telemetry_redaction, testing, ui_flags, versioning, wasm_forbidden_operations

## Missing Canonical Fields
- version
- marketing
- features
- related_products
- products
- spec_yaml
- checklist_yaml
- gpt_instructions_yaml

## Extra Fields
- api
- api_readonly_guarantee
- ecosystem_integrations
- evaluator_pipeline_stages
- export_bundle_contract
- hashing_contract
- integration_points
- performance_constraints
- playground_stage_budgets
- principles
- product_version
- provenance_required
- purpose_summary
- quickscore_behavior
- references
- release_metadata
- sample_plan_schema
- security
- spec_version
- stability_level
- telemetry_redaction
- testing
- ui_flags
- versioning
- wasm_forbidden_operations

## Suggested Canonical Structure
```yaml
id: [present]
name: [present]
product_type: [present]
pillar: [present]
version: [missing]
status: [present]
short_description: [present]
long_description: [present]
marketing: [missing]
metadata: [present]
governance: [present]
features: [missing]
architecture: [present]
related_products: [missing]
provenance: [present]
products: [missing]
spec_yaml: [missing]
checklist_yaml: [missing]
gpt_instructions_yaml: [missing]
```
