"""
Rule: normalize_markdown_formatting
Purpose:
  Ensure markdown files follow canonical whitespace + header formatting.
"""


def normalize(text: str) -> str:
    lines = [ln.rstrip() for ln in text.splitlines()]
    return "\n".join(lines).strip() + "\n"
