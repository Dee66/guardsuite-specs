# Strategy-D Phase 6: Metadata Conformance Validation Report

- Generated: 2025-11-26T06:31:37.566227+00:00
- Canonical schema: `schemas/product_schema.yml`

## Summary

- Products checked: 13
- Missing metadata files: 0
- Products with issues: 13

## Findings (per product)

### vectorscan

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `compliance` | field `compliance` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `features` | field `features` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `future_extensions` | field `future_extensions` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `governance_domains` | field `governance_domains` not defined in canonical schema |
| extraneous | extraneous-field | `interoperability_conflicts` | field `interoperability_conflicts` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `related_products` | field `related_products` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `rule_categories` | field `rule_categories` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |

### vectorguard

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `deterministic_normalization_layer` | field `deterministic_normalization_layer` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `status` | optional field `status` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `id` | required field `id` missing |
| required/missing | missing-field | `name` | required field `name` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |
| required/missing | missing-field | `version` | required field `version` missing |

### computescan

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `api` | field `api` not defined in canonical schema |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `compliance` | field `compliance` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `features` | field `features` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `future_extensions` | field `future_extensions` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `governance_domains` | field `governance_domains` not defined in canonical schema |
| extraneous | extraneous-field | `integration_points` | field `integration_points` not defined in canonical schema |
| extraneous | extraneous-field | `interoperability_conflicts` | field `interoperability_conflicts` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `related_products` | field `related_products` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `rule_categories` | field `rule_categories` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |

### computeguard

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `api` | field `api` not defined in canonical schema |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `compliance` | field `compliance` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `features` | field `features` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `future_extensions` | field `future_extensions` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `governance_domains` | field `governance_domains` not defined in canonical schema |
| extraneous | extraneous-field | `integration_points` | field `integration_points` not defined in canonical schema |
| extraneous | extraneous-field | `interoperability_conflicts` | field `interoperability_conflicts` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `related_products` | field `related_products` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `rule_categories` | field `rule_categories` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |

### pipelinescan

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `acceptance_criteria` | field `acceptance_criteria` not defined in canonical schema |
| extraneous | extraneous-field | `artifact_contract` | field `artifact_contract` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `deliverables` | field `deliverables` not defined in canonical schema |
| extraneous | extraneous-field | `determinism` | field `determinism` not defined in canonical schema |
| extraneous | extraneous-field | `evaluator_pipeline` | field `evaluator_pipeline` not defined in canonical schema |
| extraneous | extraneous-field | `examples_and_docs` | field `examples_and_docs` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `governance_notes` | field `governance_notes` not defined in canonical schema |
| extraneous | extraneous-field | `guardboard_integration` | field `guardboard_integration` not defined in canonical schema |
| extraneous | extraneous-field | `guardscore_integration` | field `guardscore_integration` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `observability` | field `observability` not defined in canonical schema |
| extraneous | extraneous-field | `performance` | field `performance` not defined in canonical schema |
| extraneous | extraneous-field | `principles` | field `principles` not defined in canonical schema |
| extraneous | extraneous-field | `purpose` | field `purpose` not defined in canonical schema |
| extraneous | extraneous-field | `resource_capabilities` | field `resource_capabilities` not defined in canonical schema |
| extraneous | extraneous-field | `responsibility_boundary` | field `responsibility_boundary` not defined in canonical schema |
| extraneous | extraneous-field | `rule_system` | field `rule_system` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| extraneous | extraneous-field | `wasm_safety` | field `wasm_safety` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `status` | optional field `status` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `id` | required field `id` missing |
| required/missing | missing-field | `name` | required field `name` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |
| required/missing | missing-field | `version` | required field `version` missing |

### pipelineguard

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `compliance` | field `compliance` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `features` | field `features` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `future_extensions` | field `future_extensions` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `governance_domains` | field `governance_domains` not defined in canonical schema |
| extraneous | extraneous-field | `integration_points` | field `integration_points` not defined in canonical schema |
| extraneous | extraneous-field | `interoperability_conflicts` | field `interoperability_conflicts` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `products` | field `products` not defined in canonical schema |
| extraneous | extraneous-field | `provenance` | field `provenance` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `related_products` | field `related_products` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `rule_categories` | field `rule_categories` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |

### guardboard

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `api` | field `api` not defined in canonical schema |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `compliance` | field `compliance` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `features` | field `features` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `future_extensions` | field `future_extensions` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `governance_domains` | field `governance_domains` not defined in canonical schema |
| extraneous | extraneous-field | `integration_points` | field `integration_points` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `provenance` | field `provenance` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `related_products` | field `related_products` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `rule_categories` | field `rule_categories` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |

### guardscore

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `api` | field `api` not defined in canonical schema |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `badge_contract` | field `badge_contract` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `compliance` | field `compliance` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `features` | field `features` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `future_extensions` | field `future_extensions` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `governance_domains` | field `governance_domains` not defined in canonical schema |
| extraneous | extraneous-field | `integration_points` | field `integration_points` not defined in canonical schema |
| extraneous | extraneous-field | `interoperability_conflicts` | field `interoperability_conflicts` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `products` | field `products` not defined in canonical schema |
| extraneous | extraneous-field | `provenance` | field `provenance` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `related_products` | field `related_products` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `rule_categories` | field `rule_categories` not defined in canonical schema |
| extraneous | extraneous-field | `scoring_model` | field `scoring_model` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |

### guardsuite-core

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `api` | field `api` not defined in canonical schema |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `compliance` | field `compliance` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `features` | field `features` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `future_extensions` | field `future_extensions` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `governance_domains` | field `governance_domains` not defined in canonical schema |
| extraneous | extraneous-field | `integration_points` | field `integration_points` not defined in canonical schema |
| extraneous | extraneous-field | `interoperability_conflicts` | field `interoperability_conflicts` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `products` | field `products` not defined in canonical schema |
| extraneous | extraneous-field | `provenance` | field `provenance` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `related_products` | field `related_products` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `rule_categories` | field `rule_categories` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |

### guardsuite_master_spec

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `ci` | field `ci` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `index` | field `index` not defined in canonical schema |
| extraneous | extraneous-field | `integrations` | field `integrations` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `release` | field `release` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `schemas` | field `schemas` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `templates` | field `templates` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |

### guardsuite-specs

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `api` | field `api` not defined in canonical schema |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `compliance` | field `compliance` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `features` | field `features` not defined in canonical schema |
| extraneous | extraneous-field | `fixpack` | field `fixpack` not defined in canonical schema |
| extraneous | extraneous-field | `future_extensions` | field `future_extensions` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `governance_domains` | field `governance_domains` not defined in canonical schema |
| extraneous | extraneous-field | `integration_points` | field `integration_points` not defined in canonical schema |
| extraneous | extraneous-field | `interoperability_conflicts` | field `interoperability_conflicts` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `maintainers` | field `maintainers` not defined in canonical schema |
| extraneous | extraneous-field | `marketing` | field `marketing` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `related_products` | field `related_products` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `rule_categories` | field `rule_categories` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |

### guardsuite-template

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `acceptance_criteria` | field `acceptance_criteria` not defined in canonical schema |
| extraneous | extraneous-field | `adapter_boundary` | field `adapter_boundary` not defined in canonical schema |
| extraneous | extraneous-field | `binary_abi_matrix` | field `binary_abi_matrix` not defined in canonical schema |
| extraneous | extraneous-field | `binary_core` | field `binary_core` not defined in canonical schema |
| extraneous | extraneous-field | `bootstrap_outputs` | field `bootstrap_outputs` not defined in canonical schema |
| extraneous | extraneous-field | `ci_contract` | field `ci_contract` not defined in canonical schema |
| extraneous | extraneous-field | `cli` | field `cli` not defined in canonical schema |
| extraneous | extraneous-field | `configuration` | field `configuration` not defined in canonical schema |
| extraneous | extraneous-field | `cross_repo_integration` | field `cross_repo_integration` not defined in canonical schema |
| extraneous | extraneous-field | `deliverables` | field `deliverables` not defined in canonical schema |
| extraneous | extraneous-field | `determinism` | field `determinism` not defined in canonical schema |
| extraneous | extraneous-field | `evaluator_pipeline` | field `evaluator_pipeline` not defined in canonical schema |
| extraneous | extraneous-field | `fixpacks` | field `fixpacks` not defined in canonical schema |
| extraneous | extraneous-field | `frontend_determinism` | field `frontend_determinism` not defined in canonical schema |
| extraneous | extraneous-field | `lifecycle_state_machine` | field `lifecycle_state_machine` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `mission` | field `mission` not defined in canonical schema |
| extraneous | extraneous-field | `multitenancy` | field `multitenancy` not defined in canonical schema |
| extraneous | extraneous-field | `output_contract` | field `output_contract` not defined in canonical schema |
| extraneous | extraneous-field | `performance_contract` | field `performance_contract` not defined in canonical schema |
| extraneous | extraneous-field | `pillar_interop` | field `pillar_interop` not defined in canonical schema |
| extraneous | extraneous-field | `pillar_minimum_files` | field `pillar_minimum_files` not defined in canonical schema |
| extraneous | extraneous-field | `principles` | field `principles` not defined in canonical schema |
| extraneous | extraneous-field | `resource_discovery` | field `resource_discovery` not defined in canonical schema |
| extraneous | extraneous-field | `responsibility_boundary` | field `responsibility_boundary` not defined in canonical schema |
| extraneous | extraneous-field | `rule_system` | field `rule_system` not defined in canonical schema |
| extraneous | extraneous-field | `scaffolding` | field `scaffolding` not defined in canonical schema |
| extraneous | extraneous-field | `schema_sources` | field `schema_sources` not defined in canonical schema |
| extraneous | extraneous-field | `schemas` | field `schemas` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `self_test` | field `self_test` not defined in canonical schema |
| extraneous | extraneous-field | `severity_mapping` | field `severity_mapping` not defined in canonical schema |
| extraneous | extraneous-field | `telemetry` | field `telemetry` not defined in canonical schema |
| extraneous | extraneous-field | `verify` | field `verify` not defined in canonical schema |
| extraneous | extraneous-field | `versioning_policy` | field `versioning_policy` not defined in canonical schema |
| extraneous | extraneous-field | `versions` | field `versions` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `status` | optional field `status` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `id` | required field `id` missing |
| required/missing | missing-field | `name` | required field `name` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |
| required/missing | missing-field | `version` | required field `version` missing |

### playground

- Metadata present: yes
| Severity | Type | Field | Detail |
| --- | --- | --- | --- |
| extraneous | extraneous-field | `api` | field `api` not defined in canonical schema |
| extraneous | extraneous-field | `api_readonly_guarantee` | field `api_readonly_guarantee` not defined in canonical schema |
| extraneous | extraneous-field | `architecture` | field `architecture` not defined in canonical schema |
| extraneous | extraneous-field | `ecosystem_integrations` | field `ecosystem_integrations` not defined in canonical schema |
| extraneous | extraneous-field | `evaluator_pipeline_stages` | field `evaluator_pipeline_stages` not defined in canonical schema |
| extraneous | extraneous-field | `export_bundle_contract` | field `export_bundle_contract` not defined in canonical schema |
| extraneous | extraneous-field | `governance` | field `governance` not defined in canonical schema |
| extraneous | extraneous-field | `hashing_contract` | field `hashing_contract` not defined in canonical schema |
| extraneous | extraneous-field | `integration_points` | field `integration_points` not defined in canonical schema |
| extraneous | extraneous-field | `long_description` | field `long_description` not defined in canonical schema |
| extraneous | extraneous-field | `metadata` | field `metadata` not defined in canonical schema |
| extraneous | extraneous-field | `performance_constraints` | field `performance_constraints` not defined in canonical schema |
| extraneous | extraneous-field | `pillar` | field `pillar` not defined in canonical schema |
| extraneous | extraneous-field | `playground_stage_budgets` | field `playground_stage_budgets` not defined in canonical schema |
| extraneous | extraneous-field | `principles` | field `principles` not defined in canonical schema |
| extraneous | extraneous-field | `product_type` | field `product_type` not defined in canonical schema |
| extraneous | extraneous-field | `product_version` | field `product_version` not defined in canonical schema |
| extraneous | extraneous-field | `provenance` | field `provenance` not defined in canonical schema |
| extraneous | extraneous-field | `provenance_required` | field `provenance_required` not defined in canonical schema |
| extraneous | extraneous-field | `purpose_summary` | field `purpose_summary` not defined in canonical schema |
| extraneous | extraneous-field | `quickscore_behavior` | field `quickscore_behavior` not defined in canonical schema |
| extraneous | extraneous-field | `references` | field `references` not defined in canonical schema |
| extraneous | extraneous-field | `release_metadata` | field `release_metadata` not defined in canonical schema |
| extraneous | extraneous-field | `sample_plan_schema` | field `sample_plan_schema` not defined in canonical schema |
| extraneous | extraneous-field | `security` | field `security` not defined in canonical schema |
| extraneous | extraneous-field | `short_description` | field `short_description` not defined in canonical schema |
| extraneous | extraneous-field | `spec_version` | field `spec_version` not defined in canonical schema |
| extraneous | extraneous-field | `stability_level` | field `stability_level` not defined in canonical schema |
| extraneous | extraneous-field | `telemetry_redaction` | field `telemetry_redaction` not defined in canonical schema |
| extraneous | extraneous-field | `testing` | field `testing` not defined in canonical schema |
| extraneous | extraneous-field | `ui_flags` | field `ui_flags` not defined in canonical schema |
| extraneous | extraneous-field | `versioning` | field `versioning` not defined in canonical schema |
| extraneous | extraneous-field | `wasm_forbidden_operations` | field `wasm_forbidden_operations` not defined in canonical schema |
| optional/missing | missing-field-optional | `bootstrap_version` | optional field `bootstrap_version` missing |
| optional/missing | missing-field-optional | `tags` | optional field `tags` missing |
| optional/missing | missing-field-optional | `validation_errors` | optional field `validation_errors` missing |
| required/missing | missing-field | `checklist_yaml` | required field `checklist_yaml` missing |
| required/missing | missing-field | `gpt_instructions_yaml` | required field `gpt_instructions_yaml` missing |
| required/missing | missing-field | `owner` | required field `owner` missing |
| required/missing | missing-field | `spec_yaml` | required field `spec_yaml` missing |
| required/missing | missing-field | `version` | required field `version` missing |

## Aggregate Summary

| Severity classification | Count |
| --- | ---: |
| extraneous | 341 |
| optional/missing | 42 |
| required/missing | 46 |

