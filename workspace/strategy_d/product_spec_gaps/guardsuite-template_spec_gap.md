# guardsuite-template Product Spec Gap

- metadata_path: products/guardsuite-template/metadata/product.yml
- metadata_exists: True
- top_level_keys (36): acceptance_criteria, adapter_boundary, binary_abi_matrix, binary_core, bootstrap_outputs, ci_contract, cli, configuration, cross_repo_integration, deliverables, determinism, evaluator_pipeline, fixpacks, frontend_determinism, lifecycle_state_machine, metadata, mission, multitenancy, output_contract, performance_contract, pillar_interop, pillar_minimum_files, principles, resource_discovery, responsibility_boundary, rule_system, scaffolding, schema_sources, schemas, security, self_test, severity_mapping, telemetry, verify, versioning_policy, versions

## Missing Canonical Fields
- id
- name
- product_type
- pillar
- version
- status
- short_description
- long_description
- marketing
- governance
- features
- architecture
- related_products
- provenance
- products
- spec_yaml
- checklist_yaml
- gpt_instructions_yaml

## Extra Fields
- acceptance_criteria
- adapter_boundary
- binary_abi_matrix
- binary_core
- bootstrap_outputs
- ci_contract
- cli
- configuration
- cross_repo_integration
- deliverables
- determinism
- evaluator_pipeline
- fixpacks
- frontend_determinism
- lifecycle_state_machine
- mission
- multitenancy
- output_contract
- performance_contract
- pillar_interop
- pillar_minimum_files
- principles
- resource_discovery
- responsibility_boundary
- rule_system
- scaffolding
- schema_sources
- schemas
- security
- self_test
- severity_mapping
- telemetry
- verify
- versioning_policy
- versions

## Suggested Canonical Structure
```yaml
id: [missing]
name: [missing]
product_type: [missing]
pillar: [missing]
version: [missing]
status: [missing]
short_description: [missing]
long_description: [missing]
marketing: [missing]
metadata: [present]
governance: [missing]
features: [missing]
architecture: [missing]
related_products: [missing]
provenance: [missing]
products: [missing]
spec_yaml: [missing]
checklist_yaml: [missing]
gpt_instructions_yaml: [missing]
```
