import hashlib
import json

import api.bootstrap_api as bootstrap_api
import api.bootstrap_generator as bootstrap_generator
from api import db


def _seed_db(db_path, payload):
    db_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _sample_product(spec: str = "spec: one"):
    return {
        "spec_yaml": spec,
        "checklist_yaml": "items:\n  - do_thing",
        "gpt_instructions_yaml": "goal: test",
    }


def test_generate_bootstrap_creates_artifact(tmp_path, monkeypatch):
    db_path = tmp_path / "products.json"
    bootstrap_dir = tmp_path / "bootstrap"
    bootstrap_dir.mkdir()
    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(bootstrap_generator, "BOOTSTRAP_DIR", bootstrap_dir)
    monkeypatch.setattr(bootstrap_api, "BOOTSTRAP_DIR", bootstrap_dir)

    payload = {"alpha": _sample_product("spec: deterministic")}
    _seed_db(db_path, payload)

    artifact, errors = bootstrap_generator.generate_bootstrap("alpha")
    assert not errors
    assert artifact is not None
    material = (
        payload["alpha"]["spec_yaml"],
        payload["alpha"]["checklist_yaml"],
        payload["alpha"]["gpt_instructions_yaml"],
    )
    expected_version = hashlib.sha256("".join(material).encode("utf-8")).hexdigest()[:8]
    assert artifact["version"] == expected_version
    assert isinstance(artifact["timestamp"], str)

    disk_artifact = json.loads(
        (bootstrap_dir / "alpha.bootstrap.json").read_text(encoding="utf-8")
    )
    assert disk_artifact == artifact


def test_create_bootstrap_requires_product(tmp_path, monkeypatch):
    db_path = tmp_path / "products.json"
    bootstrap_dir = tmp_path / "bootstrap"
    bootstrap_dir.mkdir()
    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(bootstrap_generator, "BOOTSTRAP_DIR", bootstrap_dir)
    monkeypatch.setattr(bootstrap_api, "BOOTSTRAP_DIR", bootstrap_dir)

    result = bootstrap_api.create_bootstrap("missing")
    assert result == {"bootstrap": None, "errors": ["Product not found"]}


def test_list_bootstraps_returns_sorted_artifacts(tmp_path, monkeypatch):
    db_path = tmp_path / "products.json"
    bootstrap_dir = tmp_path / "bootstrap"
    bootstrap_dir.mkdir()
    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(bootstrap_generator, "BOOTSTRAP_DIR", bootstrap_dir)
    monkeypatch.setattr(bootstrap_api, "BOOTSTRAP_DIR", bootstrap_dir)

    payload = {
        "beta": _sample_product("spec: beta"),
        "alpha": _sample_product("spec: alpha"),
    }
    _seed_db(db_path, payload)

    bootstrap_api.create_bootstrap("beta")
    bootstrap_api.create_bootstrap("alpha")

    listing = bootstrap_api.list_bootstraps()
    assert [item["product"] for item in listing["bootstraps"]] == ["alpha", "beta"]
