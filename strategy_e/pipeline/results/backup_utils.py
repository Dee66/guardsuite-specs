import os
from datetime import datetime

def write_backup(path: str, content: str) -> str:
    """
    Writes a deterministic timestamped backup for a file being repaired.
    Returns the backup file path.
    Backup file lives under strategy_e/pipeline/results/backups/.
    """
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    name = os.path.basename(path)
    backup_dir = os.path.join("strategy_e", "pipeline", "results", "backups")
    os.makedirs(backup_dir, exist_ok=True)

    backup_path = os.path.join(backup_dir, f"{name}.backup.{ts}.yml")

    with open(backup_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    return backup_path
