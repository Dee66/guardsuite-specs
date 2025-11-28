#!/usr/bin/env python3
# COPILOT: Never push automatically. This script MUST remain local-only unless a secure PR workflow is implemented.
# scripts/sync_to_repo.py
"""Simulate syncing generated docs into a target product repository."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
README_NOTICE = "This repository receives generated documentation from the central guardsuite-specs repo."
DEFAULT_README_BODY = f"""# GuardSuite Documentation Mirror

{README_NOTICE}

## Updating docs

1. Regenerate specs in guardsuite-specs: `poetry run python scripts/gen_docs.py --product <id>`.
2. Export snapshots if needed: `poetry run python scripts/export_for_ai.py --product <id>`.
3. Run this sync helper from guardsuite-specs: `poetry run python scripts/sync_to_repo.py --product <id> --target <path> --force`.

> Do not edit generated docs directly. Update YAML specs and rerun the pipeline instead.
"""


def _ensure_readme(
    readme_path: Path,
    dry_run: bool,
    template_body: str,
) -> None:
    """Ensure the target README exists and carries the guard notice."""

    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        if README_NOTICE in content:
            print("[info] README already contains GuardSuite notice.")
            return
        message = (
            f"[dry-run] Would append GuardSuite notice to {readme_path}"
            if dry_run
            else f"Appending GuardSuite notice to {readme_path}"
        )
        print(message)
        if not dry_run:
            updated = content.rstrip() + "\n\n" + README_NOTICE + "\n"
            readme_path.write_text(updated, encoding="utf-8")
        return

    message = (
        f"[dry-run] Would create README at {readme_path}"
        if dry_run
        else f"Creating README at {readme_path}"
    )
    print(message)
    if not dry_run:
        readme_path.write_text(template_body.strip() + "\n", encoding="utf-8")


def prepare(
    product_id: str,
    target_repo_path: Path,
    dry_run: bool = True,
    ensure_readme: bool = False,
    readme_template: str | None = None,
) -> Path:
    src = DOCS / "products" / f"{product_id}.md"
    if not src.exists():
        raise FileNotFoundError(f"Generated doc missing: {src}")
    target_docs_dir = target_repo_path / "docs"
    repo_exists = target_repo_path.exists()

    if dry_run:
        if not repo_exists:
            print(
                f"[dry-run] Target repo missing: {target_repo_path}. Clone or create it before syncing."
            )
        else:
            if not target_docs_dir.exists():
                print(
                    f"[dry-run] Docs directory absent; would create {target_docs_dir}."
                )
            else:
                print(f"[dry-run] Docs directory present: {target_docs_dir}.")
    else:
        target_docs_dir.mkdir(parents=True, exist_ok=True)

    dest = target_docs_dir / f"{product_id}.md"
    if dry_run:
        print(f"[dry-run] Would copy {src} → {dest}")
    else:
        shutil.copy2(src, dest)
        print(f"Copied {src} → {dest}")

    readme_path = target_repo_path / "README.md"
    if repo_exists:
        if ensure_readme:
            template_body = readme_template or DEFAULT_README_BODY
            _ensure_readme(readme_path, dry_run, template_body)
        elif dry_run:
            if readme_path.exists():
                readme = readme_path.read_text(encoding="utf-8")
                if "guardsuite-specs" not in readme:
                    print(
                        f"[dry-run] README missing guardsuite-specs notice: {readme_path}"
                    )
            else:
                print(f"[dry-run] README missing at {readme_path}.")

    print("NOTE: Review changes manually before creating any remote PR.")
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync GuardSuite docs into a target repository"
    )
    parser.add_argument("--product", required=True, help="product id to sync")
    parser.add_argument(
        "--target",
        required=True,
        help="local path to target repo (for dry run or copy)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="simulate the copy (default)",
    )
    parser.add_argument(
        "--force", action="store_true", help="bypass dry run and copy files"
    )
    parser.add_argument(
        "--ensure-readme",
        action="store_true",
        help="ensure README exists (creates or appends GuardSuite notice)",
    )
    parser.add_argument(
        "--readme-template",
        help="optional template file for initializing README when missing",
    )
    args = parser.parse_args()

    effective_dry_run = args.dry_run and not args.force
    template_text = None
    if args.readme_template:
        template_path = Path(args.readme_template)
        if not template_path.exists():
            raise FileNotFoundError(f"README template not found: {template_path}")
        template_text = template_path.read_text(encoding="utf-8")

    prepare(
        args.product,
        Path(args.target),
        dry_run=effective_dry_run,
        ensure_readme=args.ensure_readme,
        readme_template=template_text,
    )


if __name__ == "__main__":
    main()
