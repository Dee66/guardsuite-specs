def apply_repair_steps(text: str, steps: list) -> str:
    """
    Applies real repair operations:
    - trim_trailing_whitespace
    - collapse_blank_lines
    - ensure_final_newline
    Additional operations may be added in later phases.
    Deterministic and reversible (backup is taken before writing).
    """
    for step in steps:
        op = step.get("operation")

        if op == "trim_trailing_whitespace":
            # Trim trailing whitespace on each line
            lines = [line.rstrip() for line in text.splitlines()]
            # Remove trailing blank lines at end
            while lines and lines[-1] == "":
                lines.pop()
            text = "\n".join(lines)
            # Ensure final newline
            if not text.endswith("\n"):
                text = text + "\n"

        if op == "collapse_blank_lines":
            lines = []
            blank = False
            for line in text.splitlines():
                if not line.strip():
                    if not blank:
                        lines.append("")
                    blank = True
                else:
                    lines.append(line)
                    blank = False
            text = "\n".join(lines)

        if op == "ensure_final_newline":
            if not text.endswith("\n"):
                text = text + "\n"

    return text
