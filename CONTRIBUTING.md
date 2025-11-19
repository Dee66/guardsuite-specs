# Contributing to guardsuite-specs

Guidelines
- The authoritative content lives in `products/*.yml` and `snippets/*.yml`.
- Make edits to YAML files; generate docs with `scripts/gen_docs.py` and verify locally.
- For automated sync PRs, use the `open_sync_pr` workflow (manual dispatch) until automation is approved.

PR checklist
- [ ] Update product YAML files only (where appropriate)
- [ ] Run `python scripts/gen_docs.py --product <product>`
- [ ] Validate generated docs in `docs/`
- [ ] Ensure `pyproject.toml` dev dependencies install and tests pass

Security
- Do not add secrets to this repo. Use GH Actions secrets for remote push operations.
