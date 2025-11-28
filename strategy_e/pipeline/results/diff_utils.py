from difflib import unified_diff


def generate_unified_diff(
    before: str, after: str, before_label="before", after_label="after"
):
    """
    Returns a deterministic unified diff string.
    Always uses LF line endings and sorted diff headers.
    """
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)

    diff = unified_diff(
        before_lines,
        after_lines,
        fromfile=before_label,
        tofile=after_label,
        lineterm="",
    )
    return "\n".join(diff)
