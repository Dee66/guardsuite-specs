from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_release_metadata_is_consistent():
    specs = [
        p
        for p in PRODUCTS.glob("*.yml")
        if not p.name.endswith("_worksheet.yml") and p.name != "guardsuite_master_spec.yml"
    ]
    assert specs, "No product specs found"

    validated = 0
    for path in specs:
        data = load_yaml(path)
        if not data:
            continue

        release = data.get("release_metadata")
        assert release, f"release_metadata missing in {path}"
        assert release.get("release_channel") in {"stable", "beta", "incubating"}, (
            f"release_channel must be stable|beta|incubating in {path}"
        )

        url = release.get("release_notes_url", "")
        assert url.startswith("https://shieldcraft-ai.com/"), (
            f"release_notes_url must use shieldcraft-ai.com domain in {path}"
        )
        version_str = str(data.get("version", ""))
        assert version_str and url.endswith(version_str), (
            f"release_notes_url must end with product version {version_str} in {path}"
        )

        published_date = release.get("published_date")
        assert published_date, f"published_date missing in {path}"
        parts = published_date.split("-")
        assert len(parts) == 3 and all(part.isdigit() for part in parts), (
            f"published_date must be YYYY-MM-DD format in {path}"
        )
        validated += 1

    assert validated > 0, "No product release metadata validated"