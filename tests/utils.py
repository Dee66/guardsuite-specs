from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "products"
EXCLUDED_FILES = {"guardsuite_master_spec.yml", "guardsuite-template.yml", "pillar-template.yml"}


@dataclass(frozen=True)
class ProductSpecRecord:
    path: Path
    data: dict

    @property
    def file_id(self) -> str:
        return self.path.stem

    @property
    def product_id(self) -> str:
        return str(self.data.get("id", self.file_id))


def _load_canonical_product_specs() -> List[ProductSpecRecord]:
    records: List[ProductSpecRecord] = []
    for path in sorted(PRODUCTS_DIR.glob("*.yml")):
        if path.name.endswith("_worksheet.yml") or path.name in EXCLUDED_FILES:
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not data:
            continue
        records.append(ProductSpecRecord(path=path, data=data))
    return records


PRODUCT_SPEC_RECORDS: List[ProductSpecRecord] = _load_canonical_product_specs()
PRODUCT_SPEC_IDS = [record.file_id for record in PRODUCT_SPEC_RECORDS]
CANONICAL_PRODUCT_IDS = {record.product_id for record in PRODUCT_SPEC_RECORDS}
PRODUCTS_BY_ID = {record.product_id: record for record in PRODUCT_SPEC_RECORDS}

# Some historical references still use legacy identifiers. Map them here so tests can
# validate related_products entries without forcing wholesale spec renames.
KNOWN_PRODUCT_ALIASES = {
    "guardsuite-specs": "guard-specs",
}
