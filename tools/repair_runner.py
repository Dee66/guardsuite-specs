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
from typing import List, Callable
import importlib.util
import glob


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


def load_rules(rule_dir: str = "tools/repair_rules") -> List[Callable[[str], str]]:
    """Load incremental normalization rules from `tools/repair_rules/`.

    Each rule is a module exposing a `normalize(text)` function that returns
    the normalized text. Rules are applied in file-name sorted order to
    guarantee deterministic behavior.
    """
    rules: List[Callable[[str], str]] = []
    base = Path(rule_dir)
    if not base.exists():
        return rules
    # load .py files in sorted order
    files = sorted(glob.glob(str(base / "*.py")))
    # Return list of rule dicts with deterministic ordering and type classification
    loaded = []
    for f in files:
        name = Path(f).stem
        spec = importlib.util.spec_from_file_location(name, f)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "normalize") and callable(getattr(mod, "normalize")):
                # classify rule type: markdown if filename contains 'markdown', else yaml
                rtype = "markdown" if "markdown" in name.lower() else "yaml"
                loaded.append(
                    {
                        "name": name,
                        "normalize": getattr(mod, "normalize"),
                        "type": rtype,
                    }
                )
    return loaded


def apply_rules(text: str, rules: List[dict], file_type: str) -> str:
    out = text
    for r in rules:
        if r.get("type") == file_type:
            out = r["normalize"](out)
    return out


def unified_diff(a: str, b: str, fromfile: str = "a", tofile: str = "b") -> str:
    a_lines = a.splitlines(keepends=True)
    b_lines = b.splitlines(keepends=True)
    diff = difflib.unified_diff(a_lines, b_lines, fromfile=fromfile, tofile=tofile)
    return "".join(diff)


def safe_filename(path: str) -> str:
    return path.replace(os.sep, "__").lstrip(".")


def run_once(
    path: str, apply: bool = False, rules: List[Callable[[str], str]] | None = None
) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    original = p.read_text(encoding="utf-8")
    # apply incremental rules when available, otherwise fallback to base normalizer
    rules = rules if rules is not None else load_rules()
    # determine file type by suffix
    suffix = p.suffix.lower()
    if suffix in (".yml", ".yaml"):
        file_type = "yaml"
    elif suffix == ".md":
        file_type = "markdown"
    else:
        file_type = "other"

    if rules and file_type in ("yaml", "markdown"):
        normalized = apply_rules(original, rules, file_type=file_type)
    else:
        normalized = normalize_text(original)
    diff = unified_diff(
        original, normalized, fromfile=str(p), tofile=str(p) + ".normalized"
    )

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


def run_directory(
    path: str, apply: bool = False, extensions: List[str] | None = None
) -> dict:
    """Process files under `path` (recursively) and return mapping of file -> diff.

    `extensions` is a list like ['.yml', '.yaml', '.md', '.txt'] to limit processed files.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    if extensions is None:
        extensions = [".yml", ".yaml", ".md", ".txt"]
    rules = load_rules()
    results = {}
    for f in sorted(p.rglob("*")):
        if f.is_file() and f.suffix.lower() in extensions:
            try:
                diff = run_once(str(f), apply=apply, rules=rules)
                results[str(f)] = diff
            except Exception as e:
                results[str(f)] = f"ERROR: {e}"
    return results


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repair runner (minimal scaffold)")
    parser.add_argument("path", help="Path to file or directory to normalize")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write backups and diffs (default: dry-run)",
    )
    parser.add_argument(
        "--extensions",
        help="Comma-separated file extensions to process (e.g. .yml,.yaml,.md)",
    )
    args = parser.parse_args(argv)

    exts = None
    if args.extensions:
        exts = [x.strip() for x in args.extensions.split(",") if x.strip()]

    target = Path(args.path)
    try:
        if target.is_dir():
            results = run_directory(args.path, apply=args.apply, extensions=exts)
            # Print deterministic summary: files with diffs first
            for k in sorted(results.keys()):
                print(f"--- {k} ---")
                print(results[k])
        else:
            diff = run_once(args.path, apply=args.apply)
            if diff:
                print(diff)
            else:
                print("No changes needed; input already normalized.")
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.path}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
