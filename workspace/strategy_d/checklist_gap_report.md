# Checklist Gap Report

## computeguard
- Present keys: ['id', 'version', 'pillar', 'product', 'phases']
- Missing canonical keys: ['metadata', 'structure_requirements', 'documentation_requirements', 'schema_requirements', 'evaluator_requirements', 'fixpack_requirements', 'testing_requirements', 'artifacts', 'acceptance_criteria', 'cross_product_dependencies', 'provenance']
- Extra keys: ['id', 'version', 'pillar', 'product', 'phases']
- Malformed/empty structures: ['metadata missing or empty']

## computescan
- Error parsing checklist: while scanning a simple key
  in "<unicode string>", line 59, column 7:
          VALIDATION_ERROR=2, RUNTIME_ERRO ... 
          ^
could not find expected ':'
  in "<unicode string>", line 61, column 1:
    - id: SCHEMA-004
    ^

## guardboard
- Present keys: ['id', 'product', 'version', 'status', 'phases']
- Missing canonical keys: ['metadata', 'structure_requirements', 'documentation_requirements', 'schema_requirements', 'evaluator_requirements', 'fixpack_requirements', 'testing_requirements', 'artifacts', 'acceptance_criteria', 'cross_product_dependencies', 'provenance']
- Extra keys: ['id', 'product', 'version', 'status', 'phases']
- Malformed/empty structures: ['metadata missing or empty']

## guardscore
- Error parsing checklist: mapping values are not allowed here
  in "<unicode string>", line 180, column 88:
     ... own_pillar_behavior: ignore (NEW: test that unknown pillars do n ... 
                                         ^

## guardsuite-core
- Present keys: ['checklist']
- Missing canonical keys: ['metadata', 'structure_requirements', 'documentation_requirements', 'schema_requirements', 'evaluator_requirements', 'fixpack_requirements', 'testing_requirements', 'artifacts', 'acceptance_criteria', 'cross_product_dependencies', 'provenance']
- Extra keys: ['checklist']
- Malformed/empty structures: ['metadata missing or empty']

## guardsuite-specs
- Error parsing checklist: mapping values are not allowed here
  in "<unicode string>", line 129, column 11:
          desc: list products (paginated)
              ^

## guardsuite-template
- Present keys: ['id', 'product', 'version', 'status', 'phases', 'acceptance_criteria', 'deliverables']
- Missing canonical keys: ['metadata', 'structure_requirements', 'documentation_requirements', 'schema_requirements', 'evaluator_requirements', 'fixpack_requirements', 'testing_requirements', 'artifacts', 'cross_product_dependencies', 'provenance']
- Extra keys: ['id', 'product', 'version', 'status', 'phases', 'deliverables']
- Malformed/empty structures: ['metadata missing or empty']

## guardsuite_master_spec
- Error parsing checklist: mapping values are not allowed here
  in "<unicode string>", line 129, column 11:
          desc: list products (paginated)
              ^

## pipelineguard
- Present keys: ['checklist']
- Missing canonical keys: ['metadata', 'structure_requirements', 'documentation_requirements', 'schema_requirements', 'evaluator_requirements', 'fixpack_requirements', 'testing_requirements', 'artifacts', 'acceptance_criteria', 'cross_product_dependencies', 'provenance']
- Extra keys: ['checklist']
- Malformed/empty structures: ['metadata missing or empty']

## pipelinescan
- Error parsing checklist: mapping values are not allowed here
  in "<unicode string>", line 15, column 52:
     ... nsure_required_directories_exist:
                                         ^

## playground
- Error parsing checklist: mapping values are not allowed here
  in "<unicode string>", line 55, column 51:
     ... validate_pipeline_stage_presence:
                                         ^

## vectorguard
- Present keys: ['checklist']
- Missing canonical keys: ['metadata', 'structure_requirements', 'documentation_requirements', 'schema_requirements', 'evaluator_requirements', 'fixpack_requirements', 'testing_requirements', 'artifacts', 'acceptance_criteria', 'cross_product_dependencies', 'provenance']
- Extra keys: ['checklist']
- Malformed/empty structures: ['metadata missing or empty']

## vectorscan
- Error parsing checklist: mapping values are not allowed here
  in "<unicode string>", line 22, column 45:
     ... -004: verify_required_dirs_exist:
                                         ^
