"""GuardSpecs configuration loader."""

import os
from typing import Dict


def load_config() -> Dict[str, str]:
    """Load basic environment-driven configuration."""
    return {
        "ENV": os.environ.get("ENV", "development"),
    }
