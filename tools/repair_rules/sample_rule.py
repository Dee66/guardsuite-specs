"""Sample normalization rule for repair_runner.

This rule is intentionally simple: it replaces any trailing whitespace on lines
and ensures the normalized marker is present. It's only an example of the
`normalize(text)` interface expected by `repair_runner.load_rules()`.
"""


def normalize(text: str) -> str:
    lines = [l.rstrip() + "\n" for l in text.splitlines()]
    out = "".join(lines)
    marker = "# normalized-by-sample-rule\n"
    if not out.endswith(marker):
        if out.endswith("\n"):
            out = out + marker
        else:
            out = out + "\n" + marker
    return out
