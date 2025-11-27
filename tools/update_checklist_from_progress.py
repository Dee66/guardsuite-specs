#!/usr/bin/env python3
"""Update `products/computeguard/checklist/checklist.md` from `ai_reports/progress.json`.

- Updates the progress bar width and displayed percentage.
- Checks checklist items whose IDs appear in `completed_task_ids`.
- Writes a backup to `ai_reports/checklist_backups/`.
"""
import json
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
PROGRESS_PATH = os.path.join(ROOT, "ai_reports", "progress.json")
CHECKLIST_PATH = os.path.join(ROOT, "products", "computeguard", "checklist", "checklist.md")
BACKUP_DIR = os.path.join(ROOT, "ai_reports", "checklist_backups")

with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
    progress = json.load(f)

progress_pct = progress.get("progress_percentage")
if progress_pct is None:
    raise SystemExit("progress.json missing 'progress_percentage'")
completed_ids = set(progress.get("completed_task_ids", []))

with open(CHECKLIST_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Update progress bar width style (first occurrence)
text, n1 = re.subn(r"width:\s*[0-9]+(?:\.[0-9]+)?%", f"width:{progress_pct}%", text, count=1)
# Update displayed percentage text (first occurrence inside the inner div)
text, n2 = re.subn(r">\s*[0-9]+(?:\.[0-9]+)?% Complete\s*<\/div>", f">{progress_pct}% Complete</div>", text, count=1)

# Update checklist items: mark as done when ID in completed_ids
# Pattern matches lines like: - [ ] INIT-001: description
for cid in sorted(completed_ids):
    # only match unchecked boxes
    pattern = rf"^- \[ \] {re.escape(cid)}\b"
    repl = f"- [x] {cid}"
    text, n = re.subn(pattern, repl, text, flags=re.MULTILINE)

# Ensure backup dir
os.makedirs(BACKUP_DIR, exist_ok=True)
backup_name = f"checklist.md.backup.{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
backup_path = os.path.join(BACKUP_DIR, backup_name)
with open(backup_path, "w", encoding="utf-8", newline="\n") as bf:
    bf.write(text)

# Write updated checklist
with open(CHECKLIST_PATH, "w", encoding="utf-8", newline="\n") as cf:
    cf.write(text)

print(f"Updated checklist written to {CHECKLIST_PATH}")
print(f"Backup saved to {backup_path}")
print(f"Progress pct updated: {n1>0 or n2>0}")
print(f"Completed IDs applied: {len(completed_ids)}")
