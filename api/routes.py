"""Routing registry for GuardSpecs scaffold."""

from api import products
from api.bootstrap_api import (
    create_bootstrap,
    get_bootstrap,
    list_bootstraps,
    regenerate_bootstrap,
)
from api.ci_integration import (
    ci_regenerate_all,
    ci_structural_check,
    ci_validate_products,
)
from api.webhook_ingest import ingest_scan_result
from api.validate import validate_product

routes = {
    "GET /products": products.list_products,
    "GET /products/<id>": products.get_product,
    "POST /products/<id>": products.create_product,
    "PATCH /products/<id>": products.update_product,
    "POST /validate/<id>": validate_product,
    "GET /bootstrap": list_bootstraps,
    "GET /bootstrap/<id>": get_bootstrap,
    "POST /bootstrap/<id>": create_bootstrap,
    "GET /products/<id>/bootstrap": get_bootstrap,
    "POST /products/<id>/bootstrap/generate": regenerate_bootstrap,
    "POST /webhooks/scan-result": ingest_scan_result,
    "POST /ci/validate": ci_validate_products,
    "POST /ci/bootstrap/generate": ci_regenerate_all,
    "POST /ci/structural-check": ci_structural_check,
}
