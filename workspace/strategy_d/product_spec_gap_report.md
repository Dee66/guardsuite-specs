# Strategy-D Product Spec Gap Report

- Canonical schema: templates/product_schema/product_schema.yml
- Products scanned: 13

## Canonical Top-Level Keys

```yaml
- id
- name
- product_type
- pillar
- version
- status
- short_description
- long_description
- marketing
- metadata
- governance
- features
- architecture
- related_products
- provenance
- products
- spec_yaml
- checklist_yaml
- gpt_instructions_yaml
```

## Product Findings

### computeguard

- metadata_path: products/computeguard/metadata/product.yml
- metadata_exists: True
- top_level_keys (32): api, architecture, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, id, integration_points, interoperability_conflicts, long_description, maintainers, marketing, metadata, name, performance_constraints, pillar, product_type, purpose_summary, references, related_products, release_metadata, rule_categories, security, short_description, status, testing, version, versioning
- missing_canonical_fields (5): provenance, products, spec_yaml, checklist_yaml, gpt_instructions_yaml
- extra_fields (18): api, cli, compliance, ecosystem_integrations, fixpack, future_extensions, governance_domains, integration_points, interoperability_conflicts, maintainers, performance_constraints, purpose_summary, references, release_metadata, rule_categories, security, testing, versioning

### computescan

- metadata_path: products/computescan/metadata/product.yml
- metadata_exists: True
- top_level_keys (32): api, architecture, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, id, integration_points, interoperability_conflicts, long_description, maintainers, marketing, metadata, name, performance_constraints, pillar, product_type, purpose_summary, references, related_products, release_metadata, rule_categories, security, short_description, status, testing, version, versioning
- missing_canonical_fields (5): provenance, products, spec_yaml, checklist_yaml, gpt_instructions_yaml
- extra_fields (18): api, cli, compliance, ecosystem_integrations, fixpack, future_extensions, governance_domains, integration_points, interoperability_conflicts, maintainers, performance_constraints, purpose_summary, references, release_metadata, rule_categories, security, testing, versioning

### guardboard

- metadata_path: products/guardboard/metadata/product.yml
- metadata_exists: True
- top_level_keys (32): api, architecture, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, id, integration_points, long_description, maintainers, marketing, metadata, name, performance_constraints, pillar, product_type, provenance, purpose_summary, references, related_products, release_metadata, rule_categories, security, short_description, status, testing, version, versioning
- missing_canonical_fields (4): products, spec_yaml, checklist_yaml, gpt_instructions_yaml
- extra_fields (17): api, cli, compliance, ecosystem_integrations, fixpack, future_extensions, governance_domains, integration_points, maintainers, performance_constraints, purpose_summary, references, release_metadata, rule_categories, security, testing, versioning

### guardscore

- metadata_path: products/guardscore/metadata/product.yml
- metadata_exists: True
- top_level_keys (40): api, architecture, badge_contract, checklist_yaml, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, gpt_instructions_yaml, id, integration_points, interoperability_conflicts, long_description, maintainers, marketing, metadata, name, owner, performance_constraints, pillar, product_type, products, provenance, purpose_summary, references, related_products, release_metadata, rule_categories, scoring_model, security, short_description, spec_yaml, status, testing, version, versioning
- missing_canonical_fields (0): None
- extra_fields (21): api, badge_contract, cli, compliance, ecosystem_integrations, fixpack, future_extensions, governance_domains, integration_points, interoperability_conflicts, maintainers, owner, performance_constraints, purpose_summary, references, release_metadata, rule_categories, scoring_model, security, testing, versioning

### guardsuite-core

- metadata_path: products/guardsuite-core/metadata/product.yml
- metadata_exists: True
- top_level_keys (38): api, architecture, checklist_yaml, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, gpt_instructions_yaml, id, integration_points, interoperability_conflicts, long_description, maintainers, marketing, metadata, name, owner, performance_constraints, pillar, product_type, products, provenance, purpose_summary, references, related_products, release_metadata, rule_categories, security, short_description, spec_yaml, status, testing, version, versioning
- missing_canonical_fields (0): None
- extra_fields (19): api, cli, compliance, ecosystem_integrations, fixpack, future_extensions, governance_domains, integration_points, interoperability_conflicts, maintainers, owner, performance_constraints, purpose_summary, references, release_metadata, rule_categories, security, testing, versioning

### guardsuite-specs

- metadata_path: products/guardsuite-specs/metadata/product.yml
- metadata_exists: True
- top_level_keys (36): api, architecture, checklist_yaml, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, gpt_instructions_yaml, id, integration_points, interoperability_conflicts, long_description, maintainers, marketing, metadata, name, owner, performance_constraints, pillar, product_type, purpose_summary, references, related_products, release_metadata, rule_categories, security, short_description, spec_yaml, status, testing, version, versioning
- missing_canonical_fields (2): provenance, products
- extra_fields (19): api, cli, compliance, ecosystem_integrations, fixpack, future_extensions, governance_domains, integration_points, interoperability_conflicts, maintainers, owner, performance_constraints, purpose_summary, references, release_metadata, rule_categories, security, testing, versioning

### guardsuite-template

- metadata_path: products/guardsuite-template/metadata/product.yml
- metadata_exists: True
- top_level_keys (36): acceptance_criteria, adapter_boundary, binary_abi_matrix, binary_core, bootstrap_outputs, ci_contract, cli, configuration, cross_repo_integration, deliverables, determinism, evaluator_pipeline, fixpacks, frontend_determinism, lifecycle_state_machine, metadata, mission, multitenancy, output_contract, performance_contract, pillar_interop, pillar_minimum_files, principles, resource_discovery, responsibility_boundary, rule_system, scaffolding, schema_sources, schemas, security, self_test, severity_mapping, telemetry, verify, versioning_policy, versions
- missing_canonical_fields (18): id, name, product_type, pillar, version, status, short_description, long_description, marketing, governance, features, architecture, related_products, provenance, products, spec_yaml, checklist_yaml, gpt_instructions_yaml
- extra_fields (35): acceptance_criteria, adapter_boundary, binary_abi_matrix, binary_core, bootstrap_outputs, ci_contract, cli, configuration, cross_repo_integration, deliverables, determinism, evaluator_pipeline, fixpacks, frontend_determinism, lifecycle_state_machine, mission, multitenancy, output_contract, performance_contract, pillar_interop, pillar_minimum_files, principles, resource_discovery, responsibility_boundary, rule_system, scaffolding, schema_sources, schemas, security, self_test, severity_mapping, telemetry, verify, versioning_policy, versions

### guardsuite_master_spec

- metadata_path: products/guardsuite_master_spec/metadata/product.yml
- metadata_exists: True
- top_level_keys (23): architecture, ci, governance, id, index, integrations, long_description, maintainers, marketing, name, pillar, product_type, purpose_summary, references, release, release_metadata, schemas, security, short_description, status, templates, testing, version
- missing_canonical_fields (8): metadata, features, related_products, provenance, products, spec_yaml, checklist_yaml, gpt_instructions_yaml
- extra_fields (12): ci, index, integrations, maintainers, purpose_summary, references, release, release_metadata, schemas, security, templates, testing

### pipelineguard

- metadata_path: products/pipelineguard/metadata/product.yml
- metadata_exists: True
- top_level_keys (37): architecture, checklist_yaml, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, gpt_instructions_yaml, id, integration_points, interoperability_conflicts, long_description, maintainers, marketing, metadata, name, owner, performance_constraints, pillar, product_type, products, provenance, purpose_summary, references, related_products, release_metadata, rule_categories, security, short_description, spec_yaml, status, testing, version, versioning
- missing_canonical_fields (0): None
- extra_fields (18): cli, compliance, ecosystem_integrations, fixpack, future_extensions, governance_domains, integration_points, interoperability_conflicts, maintainers, owner, performance_constraints, purpose_summary, references, release_metadata, rule_categories, security, testing, versioning

### pipelinescan

- metadata_path: products/pipelinescan/metadata/product.yml
- metadata_exists: True
- parse_error: mapping values are not allowed here
  in "/home/dee/workspace/AI/GuardSuite/guardsuite-specs/products/pipelinescan/metadata/product.yml", line 127, column 68
- top_level_keys (0): None
- missing_canonical_fields (0): None
- extra_fields (0): None

### playground

- metadata_path: products/playground/metadata/product.yml
- metadata_exists: True
- top_level_keys (36): api, api_readonly_guarantee, architecture, ecosystem_integrations, evaluator_pipeline_stages, export_bundle_contract, governance, hashing_contract, id, integration_points, long_description, metadata, name, performance_constraints, pillar, playground_stage_budgets, principles, product_type, product_version, provenance, provenance_required, purpose_summary, quickscore_behavior, references, release_metadata, sample_plan_schema, security, short_description, spec_version, stability_level, status, telemetry_redaction, testing, ui_flags, versioning, wasm_forbidden_operations
- missing_canonical_fields (8): version, marketing, features, related_products, products, spec_yaml, checklist_yaml, gpt_instructions_yaml
- extra_fields (25): api, api_readonly_guarantee, ecosystem_integrations, evaluator_pipeline_stages, export_bundle_contract, hashing_contract, integration_points, performance_constraints, playground_stage_budgets, principles, product_version, provenance_required, purpose_summary, quickscore_behavior, references, release_metadata, sample_plan_schema, security, spec_version, stability_level, telemetry_redaction, testing, ui_flags, versioning, wasm_forbidden_operations

### vectorguard

- metadata_path: products/vectorguard/metadata/product.yml
- metadata_exists: True
- top_level_keys (1): deterministic_normalization_layer
- missing_canonical_fields (19): id, name, product_type, pillar, version, status, short_description, long_description, marketing, metadata, governance, features, architecture, related_products, provenance, products, spec_yaml, checklist_yaml, gpt_instructions_yaml
- extra_fields (1): deterministic_normalization_layer

### vectorscan

- metadata_path: products/vectorscan/metadata/product.yml
- metadata_exists: True
- top_level_keys (30): architecture, cli, compliance, ecosystem_integrations, features, fixpack, future_extensions, governance, governance_domains, id, interoperability_conflicts, long_description, maintainers, marketing, metadata, name, performance_constraints, pillar, product_type, purpose_summary, references, related_products, release_metadata, rule_categories, security, short_description, status, testing, version, versioning
- missing_canonical_fields (5): provenance, products, spec_yaml, checklist_yaml, gpt_instructions_yaml
- extra_fields (16): cli, compliance, ecosystem_integrations, fixpack, future_extensions, governance_domains, interoperability_conflicts, maintainers, performance_constraints, purpose_summary, references, release_metadata, rule_categories, security, testing, versioning
