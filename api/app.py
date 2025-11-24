"""Core GuardSpecs application scaffold."""

import logging
from typing import Any, Dict

from api.config import load_config
from api.routes import routes


def create_app() -> Dict[str, Any]:
    """Create the GuardSpecs application container."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("guard-specs")
    logger.info("Starting GuardSpecs service scaffold")

    config = load_config()
    app = {
        "routes": routes,
        "config": config,
    }
    logger.debug("Loaded config: %%s", config)
    return app
