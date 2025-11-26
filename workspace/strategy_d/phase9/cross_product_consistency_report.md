# Strategy-D Phase 9: Cross-Product Consistency Audit

- Generated: 2025-11-26T06:44:22.584618+00:00

## Rules

- Analysis-only: no product files modified
- Deterministic alphabetical product order
- Severity: `error`, `warning`, `info`

## Summary Pass/Fail Table

| Product | Metadata | Checklist | Demo | In product_index | Cross-ref OK | Overall |
| --- | :---: | :---: | :---: | :---: | :---: | --- |
| computeguard | yes | yes | yes | yes | yes | PASS |
| computescan | yes | yes | yes | yes | yes | PASS |
| guardboard | yes | yes | yes | yes | yes | PASS |
| guardscore | yes | yes | yes | yes | yes | PASS |
| guardsuite-core | yes | yes | yes | yes | yes | PASS |
| guardsuite-specs | yes | yes | yes | yes | yes | WARN |
| guardsuite-template | yes | yes | yes | yes | yes | WARN |
| guardsuite_master_spec | yes | yes | yes | yes | yes | PASS |
| pipelineguard | yes | yes | yes | yes | yes | PASS |
| pipelinescan | yes | yes | yes | yes | yes | WARN |
| playground | yes | yes | yes | yes | yes | PASS |
| vectorguard | yes | yes | yes | yes | yes | WARN |
| vectorscan | yes | yes | yes | yes | yes | PASS |

## Aggregate Summary

- Products scanned: 13
- Errors (products with errors): 0
- Warnings (products with warnings): 4
- Info-only (no errors/warnings): 9

## Findings (per product)

### computeguard

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

### computescan

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

### guardboard

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

### guardscore

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

### guardsuite-core

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

### guardsuite-specs

- Overall: WARN
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1
  - id_mismatch: `guard-specs` != folder `guardsuite-specs`

### guardsuite-template

- Overall: WARN
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1
  - name_empty

### guardsuite_master_spec

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

### pipelineguard

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

### pipelinescan

- Overall: WARN
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1
  - name_empty

### playground

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

### vectorguard

- Overall: WARN
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1
  - name_empty

### vectorscan

- Overall: PASS
- Metadata present and valid: yes
- Checklist present and structurally valid: yes
- Demo scaffolding present: yes
- Present in product_index: yes
- Details:
  - extraneous_fields_count: 1

## Notes and Next Steps

- This audit is analysis-only; no files were modified.
- Items flagged `FAIL` need direct fixes in product metadata/checklist/demo files.
- Run Phase 10 to apply repairs after review.
