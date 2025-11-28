#!/usr/bin/env python3
"""Update `products/computeguard/checklist/checklist.md` from `ai_reports/progress.json`.

- Updates the progress bar width and displayed percentage.
- Checks checklist items whose IDs appear in `completed_task_ids`.
- Accepts an optional mapping file (JSON) that maps suggestion IDs -> checklist search tokens.
- Produces a dry-run patch and `ai_reports/checklist_update_log.json` when requested.
"""
import argparse
import difflib
import json
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
DEFAULT_PROGRESS_PATH = os.path.join(ROOT, "ai_reports", "progress.json")
DEFAULT_CHECKLIST_PATH = os.path.join(
    ROOT, "products", "computeguard", "checklist", "checklist.md"
)
BACKUP_DIR = os.path.join(ROOT, "ai_reports", "checklist_backups")
REPORT_DIR = os.path.join(ROOT, "ai_reports")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, sort_keys=True)


def apply_mapping_to_checklist(text, completed_ids, mapping):
    """Return (new_text, applied_ids, skipped) where skipped is dict of id->reason."""
    applied = []
    skipped = {}

    # Update progress bar and percentage are handled separately by caller.
    for cid in sorted(completed_ids):
        tokens = mapping.get(cid)
        if tokens is None:
            # default to using the ID itself as token
            tokens = [cid]
        elif isinstance(tokens, str):
            tokens = [tokens]

        found_any = False
        for token in tokens:
            # Match an unchecked box containing the token anywhere on the line
            # Capture the rest of the line after the ID/token to preserve description
            pattern = rf"^- \[ \] (?P<body>.*{re.escape(token)}.*)$"
            repl = r"- [x] \g<body>"
            new_text, n = re.subn(pattern, repl, text, flags=re.MULTILINE)
            if n > 0:
                text = new_text
                found_any = True
        if found_any:
            applied.append(cid)
        else:
            skipped[cid] = "no exact unchecked checklist line matched mapping tokens"

    return text, applied, skipped


def update_progress_display(text, progress_pct):
    # Update progress bar width style (first occurrence)
    text, n1 = re.subn(r"width:\s*[0-9]+(?:\.[0-9]+)?%", f"width:{progress_pct}%", text, count=1)
    # Update displayed percentage text (first occurrence inside the inner div)
    text, n2 = re.subn(r">\s*[0-9]+(?:\.[0-9]+)?% Complete\s*<\/div>", f">{progress_pct}% Complete</div>", text, count=1)
    return text, (n1 > 0 or n2 > 0)


def make_backup(orig_text):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_name = f"checklist.md.backup.{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    with open(backup_path, "w", encoding="utf-8", newline="\n") as bf:
        bf.write(orig_text)
    return backup_path


def write_patch(orig_text, new_text, patch_path):
    diff = list(difflib.unified_diff(
        orig_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile="checklist.md",
        tofile="checklist.md.updated",
    ))
    with open(patch_path, "w", encoding="utf-8", newline="\n") as pf:
        pf.writelines(diff)
    return patch_path


def main():
    p = argparse.ArgumentParser(description="Update checklist from progress with mapping and dry-run support")
    p.add_argument("--progress", default=DEFAULT_PROGRESS_PATH, help="Path to progress.json")
    p.add_argument("--checklist", default=DEFAULT_CHECKLIST_PATH, help="Path to checklist.md")
    p.add_argument("--mapping", help="Optional JSON mapping file: {suggestion_id: token_or_list}")
    p.add_argument("--dry-run", action="store_true", help="Do not write checklist.md, instead write patch and log")
    args = p.parse_args()

    progress = load_json(args.progress)
    progress_pct = progress.get("progress_percentage")
    if progress_pct is None:
        raise SystemExit("progress.json missing 'progress_percentage'")
    completed_ids = set(progress.get("completed_task_ids", []))

    mapping = {}
    if args.mapping:
        mapping = load_json(args.mapping)

    with open(args.checklist, "r", encoding="utf-8") as f:
        orig_text = f.read()

    backup_path = make_backup(orig_text)

    # Update progress display first
    text, progress_updated = update_progress_display(orig_text, progress_pct)

    # Apply mapping-based checklist updates
    text, applied, skipped = apply_mapping_to_checklist(text, completed_ids, mapping)

    # Ensure report dir
    os.makedirs(REPORT_DIR, exist_ok=True)

    log = {
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "progress_path": args.progress,
        "checklist_path": args.checklist,
        "mapping_path": args.mapping,
        "progress_updated": progress_updated,
        "applied_ids": applied,
        "skipped_ids": skipped,
        "backup": backup_path,
    }

    log_path = os.path.join(REPORT_DIR, "checklist_update_log.json")
    write_json(log_path, log)

    patch_path = os.path.join(REPORT_DIR, "checklist_patch_dryrun.patch")
    write_patch(orig_text, text, patch_path)

    human_note_path = os.path.join(REPORT_DIR, "checklist_patch.apply.txt")
    with open(human_note_path, "w", encoding="utf-8", newline="\n") as hn:
        hn.write(f"Backup: {backup_path}\n")
        hn.write(f"Patch: {patch_path}\n")
        hn.write(f"Applied IDs: {applied}\n")
        hn.write(f"Skipped IDs: {skipped}\n")

    if args.dry_run:
        print(f"Dry-run complete. Patch written to {patch_path}")
        print(f"Update log written to {log_path}")
        return

    # Write actual checklist
    with open(args.checklist, "w", encoding="utf-8", newline="\n") as cf:
        cf.write(text)

    print(f"Updated checklist written to {args.checklist}")
    print(f"Backup saved to {backup_path}")
    print(f"Patch saved to {patch_path}")
    print(f"Update log written to {log_path}")


if __name__ == "__main__":
    main()
