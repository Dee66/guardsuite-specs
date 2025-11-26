# Strategy-D Phase 11: Cross-Product Semantic Validation Report

- Generated: 2025-11-26T06:49:52.502935+00:00

## Summary

- Products scanned: 13
- Roots (no incoming edges): ['computeguard', 'computescan', 'guardboard', 'guardscore', 'guardsuite-core', 'guardsuite-specs', 'guardsuite-template', 'guardsuite_master_spec', 'pipelineguard', 'pipelinescan', 'playground', 'vectorguard', 'vectorscan']
- Cycles detected: 0
- Unreachable nodes from roots: 0

## Severity tallies

- Errors: 0
- Warnings: 15
- Info: 1

## Missing / Invalid References (Errors)

- None

## Non-bidirectional Related-Product Links (Warnings)

- None

## Products without a guardsuite-core reference (Warnings)

- computeguard
- computescan
- guardboard
- guardscore
- guardsuite-core
- guardsuite-specs
- guardsuite-template
- guardsuite_master_spec
- pipelineguard
- pipelinescan
- playground
- vectorguard
- vectorscan

## GuardBoard / GuardScore integration expectations (Warnings/Info)

- guardboard: guardscore_integration_missing
- guardscore: guardboard_integration_missing

## Master spec completeness

- None or no explicit product list present

## Dependency Graph Cycles (Errors)

- None

## Unreachable Nodes from Roots (Warning)

- None

## Dependencies on non-existent products (Errors)

- None

## Full Dependency Graph (by product)

- computeguard: []
- computescan: []
- guardboard: []
- guardscore: []
- guardsuite-core: []
- guardsuite-specs: []
- guardsuite-template: []
- guardsuite_master_spec: []
- pipelineguard: []
- pipelinescan: []
- playground: []
- vectorguard: []
- vectorscan: []

## Notes and Suggested Repairs

- Fix missing referenced products listed under Missing/Invalid References.
- Consider adding bidirectional related_products entries where appropriate.
- Ensure every product references `guardsuite-core` where expected (see warnings).
- Address cycles in the dependency graph (errors) to break circular dependencies.

