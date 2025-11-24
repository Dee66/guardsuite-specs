"""In-memory helpers for CRUD product operations backed by JSON storage."""

from typing import Any, Dict, Optional

from api.db import load_db, save_db


def list_products() -> Dict[str, Any]:
    return load_db()


def get_product(pid: str) -> Optional[Dict[str, Any]]:
    db = load_db()
    return db.get(pid)


def create_product(pid: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    db = load_db()
    db[pid] = payload
    save_db(db)
    return db[pid]


def update_product(pid: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = load_db()
    if pid not in db:
        return None
    db[pid].update(payload)
    save_db(db)
    return db[pid]
