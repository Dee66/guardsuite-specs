"""Local MkDocs plugin that wires in the standard admonition Markdown extension."""

from __future__ import annotations

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin


class AdmonitionPlugin(BasePlugin):
    """Registers the standard Markdown admonition extension via a plugin hook."""

    def on_config(
        self, config: MkDocsConfig
    ) -> MkDocsConfig:  # pragma: no cover - mkdocs hook
        extensions = list(config.get("markdown_extensions", []))
        if "admonition" not in extensions:
            extensions.append("admonition")
            config["markdown_extensions"] = extensions
        return config
