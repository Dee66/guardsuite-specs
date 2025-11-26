"""Minimal deterministic repair runner scaffold.

This tool is intentionally conservative:
- `--dry-run` prints a unified diff between original and normalized content.
- `--apply` will write a diff under `workspace/strategy_d/diffs/` and a backup under `workspace/strategy_d/backups/`.

The normalizer used here is a small deterministic placeholder (appends a stable marker)
so behavior is predictable for tests and early development. Replace normalization
rules with true repair logic during implementation milestone C.1.
"""
from __future__ import annotations

import argparse
import difflib
import os
from pathlib import Path
from typing import List


def normalize_text(text: str) -> str:
    """Deterministic, idempotent placeholder normalizer.

    Appends a stable marker line if missing. Real rules should be deterministic
    and idempotent as well.
    """
    marker = "# normalized-by-repair-runner\n"
    if text.endswith(marker):
        return text
    if text.endswith("\n"):
        return text + marker
    return text + "\n" + marker


def unified_diff(a: str, b: str, fromfile: str = "a", tofile: str = "b") -> str:
    a_lines = a.splitlines(keepends=True)
    b_lines = b.splitlines(keepends=True)
    diff = difflib.unified_diff(a_lines, b_lines, fromfile=fromfile, tofile=tofile)
    return "".join(diff)


def safe_filename(path: str) -> str:
    return path.replace(os.sep, "__").lstrip(".")


def run_once(path: str, apply: bool = False) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    original = p.read_text(encoding="utf-8")
    normalized = normalize_text(original)
    diff = unified_diff(original, normalized, fromfile=str(p), tofile=str(p) + ".normalized")

    if apply:
        # create backups and diffs
        backups_dir = Path("workspace/strategy_d/backups")
        diffs_dir = Path("workspace/strategy_d/diffs")
        backups_dir.mkdir(parents=True, exist_ok=True)
        diffs_dir.mkdir(parents=True, exist_ok=True)

        backup_path = backups_dir / safe_filename(p.name + ".backup")
        diff_path = diffs_dir / (safe_filename(str(p)) + ".diff")

        # write backup (original content)
        backup_path.write_text(original, encoding="utf-8")
        # write diff
        diff_path.write_text(diff, encoding="utf-8")

    return diff


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repair runner (minimal scaffold)")
    parser.add_argument("path", help="Path to file to normalize")
    parser.add_argument("--apply", action="store_true", help="Write backups and diffs (default: dry-run)")
    args = parser.parse_args(argv)

    try:
        diff = run_once(args.path, apply=args.apply)
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.path}")
        return 2

    if diff:
        print(diff)
    else:
        print("No changes needed; input already normalized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
