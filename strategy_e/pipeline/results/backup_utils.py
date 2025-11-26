from pathlib import Path
from datetime import datetime


def write_backup(path, content, backup_dir=None):
    """
    Writes a deterministic timestamped backup for a file being repaired.
    Returns the backup file path. If `backup_dir` is provided, it's used as the root; otherwise
    default location `strategy_e/pipeline/results/backups/` is used.
    """
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    name = Path(path).name

    # Determine directory
    if backup_dir is not None:
        backup_root = Path(backup_dir)
    else:
        backup_root = Path("strategy_e") / "pipeline" / "results" / "backups"

    backup_root.mkdir(parents=True, exist_ok=True)

    backup_path = backup_root / f"{name}.backup.{ts}.yml"

    with backup_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    return str(backup_path)
