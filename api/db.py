"""Simple JSON-backed metadata store for GuardSpecs scaffold."""

import json
from pathlib import Path
from typing import Any, Dict

DB_PATH = Path("db/products.json")


def load_db() -> Dict[str, Any]:
    """Load product metadata from disk (returns empty dict if missing)."""
    if not DB_PATH.exists():
        return {}
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def save_db(data: Dict[str, Any]) -> None:
    """Persist product metadata to disk, ensuring directory exists."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
