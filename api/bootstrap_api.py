"""High-level bootstrap API helpers wiring the generator and storage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from api.bootstrap_generator import BOOTSTRAP_DIR, generate_bootstrap


def _artifact_path(pid: str) -> Path:
    return BOOTSTRAP_DIR / f"{pid}.bootstrap.json"


def list_bootstraps() -> Dict[str, Any]:
    artifacts: List[Dict[str, Any]] = []
    if BOOTSTRAP_DIR.exists():
        for artifact_file in sorted(BOOTSTRAP_DIR.glob("*.bootstrap.json")):
            artifacts.append(json.loads(artifact_file.read_text(encoding="utf-8")))
    return {"bootstraps": artifacts}


def get_bootstrap(pid: str) -> Dict[str, Any]:
    path = _artifact_path(pid)
    if not path.exists():
        return {"bootstrap": None, "errors": ["Bootstrap not generated"]}
    return {"bootstrap": json.loads(path.read_text(encoding="utf-8")), "errors": []}


def create_bootstrap(pid: str) -> Dict[str, Any]:
    artifact, errors = generate_bootstrap(pid)
    return {"bootstrap": artifact, "errors": errors}


def regenerate_bootstrap(pid: str) -> Dict[str, Any]:
    """Alias for create_bootstrap used by the CLI."""

    return create_bootstrap(pid)
