#!/usr/bin/env python3
"""Update the progress bar in `pil_checklist.md`.

Usage:
    python3 scripts/update_pil_progress.py path/to/pil_checklist.md

The script locates the markers `<!-- PROGRESS_START -->` and `<!-- PROGRESS_END -->`
and replaces the block between them with an HTML progress bar reflecting the
percentage of checked items (`- [x]`). Deterministic and does not use timestamps.
"""

from pathlib import Path
import re
import sys

PROG_START = "<!-- PROGRESS_START -->"
PROG_END = "<!-- PROGRESS_END -->"


def count_checkboxes(text: str):
    # Matches lines starting with a list marker and a checkbox like: - [ ] or - [x]
    pattern = r"^[ \t]*[-*]\s*\[([ xX])\]"
    matches = re.findall(pattern, text, flags=re.M)
    total = len(matches)
    completed = sum(1 for m in matches if m.lower() == "x")
    return total, completed


def build_progress_block(pct: int) -> str:
    # Choose color based on percentage: green, orange, red
    if pct >= 75:
        color = "#2ecc71"
    elif pct >= 40:
        color = "#f39c12"
    else:
        color = "#e74c3c"

    bar = (
        f"{PROG_START}\n"
        "<div id=\"pil-progress\" style=\"width:100%; background:#eee; border-radius:6px; padding:4px;\">\n"
        f"  <div id=\"pil-progress-bar\" style=\"width:{pct}%; height:18px; border-radius:4px; background:{color};\"></div>\n"
        "</div>\n"
        f"<p id=\"pil-progress-text\">{pct}% complete</p>\n"
        f"{PROG_END}"
    )
    return bar


def update_file(path: Path):
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")

    total, completed = count_checkboxes(text)
    pct = 0
    if total:
        pct = int(round((completed / total) * 100))

    new_block = build_progress_block(pct)

    # Replace existing progress block between markers (if present), otherwise insert at top
    if PROG_START in text and PROG_END in text:
        new_text = re.sub(
            re.escape(PROG_START) + r".*?" + re.escape(PROG_END),
            new_block,
            text,
            flags=re.S,
        )
    else:
        # Prepend the progress block
        new_text = new_block + "\n" + text

    path.write_text(new_text, encoding="utf-8")
    return total, completed, pct


def main(argv):
    p = Path(argv[1]) if len(argv) > 1 else Path("pil_checklist.md")
    total, completed, pct = update_file(p)
    print(f"Updated {p} — {completed}/{total} checked ({pct}%)")


if __name__ == "__main__":
    main(sys.argv)
