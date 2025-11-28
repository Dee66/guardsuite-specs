#!/usr/bin/env python3
"""Minimal single-file runner for the PIL scanner.

Drop this file into a repo root (alongside `repo-scanner.py` and `scripts/pil_bootstrap.py`) and run:
  python3 scripts/pil-runner.py

It will perform safe, non-destructive bootstrapping (create missing templates/placeholders),
then run the scanner and print YAML results. Designed to be minimal and portable.
"""
from __future__ import annotations

import sys
from pathlib import Path


def ensure_pyyaml():
    try:
        import yaml  # type: ignore

        return True
    except Exception:
        print("Missing dependency: pyyaml is required. Install: pip install pyyaml", file=sys.stderr)
        return False


def main() -> int:
    repo_root = Path.cwd()

    if not ensure_pyyaml():
        return 2

    # Attempt to import and call pil_bootstrap helpers if available
    boot = None
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("pil_bootstrap", str(repo_root / "scripts" / "pil_bootstrap.py"))
        if spec and spec.loader:
            boot = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(boot)
    except Exception:
        boot = None

    created_files = []
    if boot is not None:
        # safe, minimal bootstrapping: create templates, placeholders, structure, inits
        try:
            created_files.extend(boot.create_missing_templates(repo_root))
            created_files.extend(boot.create_placeholders_from_project_map(repo_root, make_tests_pass=False))
            created_files.extend(boot.create_required_structure(repo_root))
            created_files.extend(boot.ensure_package_inits(repo_root))
        except Exception as e:  # pragma: no cover - runtime
            print("Bootstrap helper ran into an issue:", e, file=sys.stderr)

    # Import and run the scanner
    try:
        import importlib.util
        import yaml

        spec = importlib.util.spec_from_file_location("repo_scanner", str(repo_root / "repo-scanner.py"))
        if not spec or not spec.loader:
            print("repo-scanner.py not found in repo root. Place the scanner file in repo root.", file=sys.stderr)
            return 3
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        scanner = mod.PILScanner(str(repo_root))
        results = scanner.scoring_loop()
        print(yaml.safe_dump(results))
        return 0
    except Exception as exc:  # pragma: no cover - runtime
        print("Failed to run repo-scanner:", exc, file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
