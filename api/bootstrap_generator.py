"""Deterministic bootstrap generator for GuardSpecs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from api.db import load_db

BOOTSTRAP_DIR = Path("bootstrap")
BOOTSTRAP_DIR.mkdir(parents=True, exist_ok=True)


def _hash_inputs(spec: str, checklist: str, instructions: str) -> str:
    concatenated = (spec or "") + (checklist or "") + (instructions or "")
    digest = hashlib.sha256(concatenated.encode("utf-8")).hexdigest()
    return digest[:8]


def generate_bootstrap(
    pid: str, *, persist: bool = True
) -> Tuple[Dict[str, Any] | None, List[str]]:
    db = load_db()
    product = db.get(pid)
    if not product:
        return None, ["Product not found"]

    spec = product.get("spec_yaml", "")
    checklist = product.get("checklist_yaml", "")
    instructions = product.get("gpt_instructions_yaml", "")

    version = _hash_inputs(spec, checklist, instructions)
    timestamp = datetime.now(timezone.utc).isoformat()

    artifact = {
        "product": pid,
        "timestamp": timestamp,
        "version": version,
        "spec": spec,
        "checklist": checklist,
        "gpt_instructions": instructions,
        "architect_session_state": {
            "last_checklist_item": None,
            "last_instruction_version": 0,
            "last_implementor_status": None,
        },
        "incomplete": False,
        "validation_errors": [],
    }

    if persist:
        path = BOOTSTRAP_DIR / f"{pid}.bootstrap.json"
        path.write_text(
            json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8"
        )

    return artifact, []
