PIL Implementation Overview

This repository contains the PIL (Product Implementation Lifecycle) scaffolding and tools used to validate, score, and analyze implementation tasks.

Quick commands

- Update the checklist progress bar:

```bash
python3 scripts/update_pil_progress.py pil_checklist.md
```

- Run strict YAML/content validation:

```bash
python3 scripts/validate_yaml_strict.py
# to fail on missing implementation files:
python3 scripts/validate_yaml_strict.py --fail-missing-files
```

- Validate validation artifacts (tests/files referenced in `project_map.yml`):

```bash
python3 scripts/validate_validation_artifacts.py
```

- Run the aggregator + deterministic AI consumer (generates `repos_index.yml` and `ai_analysis.yml`):

```bash
python3 scripts/aggregate_and_analyze.py
```

- Run the AI consumer directly:

```bash
python3 scripts/ai_consumer.py repos_index.yml ai_analysis.yml
```

- Run unit tests (recommended to run specific tests to avoid unrelated failures):

```bash
pytest -q tests/test_ai_consumer.py
```

Notes

- All validation and analysis tools are deterministic and avoid network calls by default.
- LLM enrichment is implemented as an opt-in hook in `scripts/ai_consumer.py` and is a safe no-op unless explicitly enabled and configured by the user.
- Use the `pil_checklist.md` to track progress and to run `scripts/update_pil_progress.py` after making checklist changes.
