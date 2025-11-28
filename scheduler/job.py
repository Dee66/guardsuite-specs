"""Periodic bootstrap regeneration scheduler."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List

from api.bootstrap_generator import BOOTSTRAP_DIR, generate_bootstrap
from api.db import load_db

DEFAULT_INTERVAL = 15 * 60
INTERVAL_SECONDS = int(os.environ.get("GUARDSPEC_SCHEDULER_INTERVAL", DEFAULT_INTERVAL))


def _artifact_path(pid: str) -> Path:
    return BOOTSTRAP_DIR / f"{pid}.bootstrap.json"


def _needs_persist(
    current: Dict[str, Any] | None, new_artifact: Dict[str, Any]
) -> bool:
    if current is None:
        return True
    return current.get("version") != new_artifact.get("version")


def run_once() -> Dict[str, List[str]]:
    """Run a single scheduler iteration and report which products changed."""

    db = load_db()
    written: List[str] = []
    skipped: List[str] = []
    for pid in sorted(db.keys()):
        artifact, errors = generate_bootstrap(pid, persist=False)
        if errors or artifact is None:
            continue

        path = _artifact_path(pid)
        current = None
        if path.exists():
            current = json.loads(path.read_text(encoding="utf-8"))

        if _needs_persist(current, artifact):
            BOOTSTRAP_DIR.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8"
            )
            written.append(pid)
        else:
            skipped.append(pid)

    return {"written": written, "skipped": skipped}


def run_scheduler() -> None:
    """Continuously regenerate bootstraps on the configured interval."""

    while True:
        run_once()
        time.sleep(INTERVAL_SECONDS)
