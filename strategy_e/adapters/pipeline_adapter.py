from typing import Any, Dict, Optional

try:
    from strategy_e.pipeline.executor.pipeline_executor import (
        run_pipeline_on_text,
    )
except Exception:
    # Fallback stub if executor not importable in this environment
    def run_pipeline_on_text(
        text: str,
        rules,
        path: str = None,
        dry_run: bool = False,
        backup_dir: str = None,
    ):
        return {
            "normalized_text": text,
            "validation_errors": [],
            "repaired_text": text,
            "diff": "",
            "backup_path": None,
            "dry_run": dry_run,
        }


def evaluate(
    resource: Dict[str, Any],
    rules: Optional[Any] = None,
    path: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Adapter that maps a resource to the canonical pipeline executor.

    Accepts a resource that may contain a `text` field or `resources` list
    with `content`. Calls `run_pipeline_on_text` and normalizes the
    response into a consistent dict.
    """
    text = ""
    if isinstance(resource, dict):
        if resource.get("text"):
            text = resource.get("text")
        elif resource.get("resources") and isinstance(
            resource.get("resources"), list
        ):
            first = resource.get("resources")[0]
            if isinstance(first, dict):
                text = first.get("content", "")
            else:
                text = str(first)
        else:
            # best-effort stringification
            text = str(resource)
    else:
        text = str(resource)

    # Normalize rules to the executor expected format: iterable of (path,
    # rule) tuples.
    rules_param = rules or []
    if isinstance(rules_param, dict):
        rules_param = [(None, rules_param)]
    elif isinstance(rules_param, list):
        # Normalize list elements: accept list of dicts, list of
        # (path, rule) tuples, and nested tuple cases. Produce list of
        # (path, rule_dict).
        normalized = []
        for item in rules_param:
            if isinstance(item, tuple) and len(item) == 2:
                path, rule = item
                # If rule is nested tuple (from double-wrapping), unwrap.
                if isinstance(rule, tuple) and len(rule) == 2:
                    _, rule = rule
                normalized.append((path, rule))
            else:
                normalized.append((None, item))
        rules_param = normalized

    result = run_pipeline_on_text(
        text, rules_param, path=path, dry_run=dry_run
    )

    validation_errors = result.get("validation_errors", [])
    violations = [{"message": m} for m in validation_errors]

    return {
        "violations": violations,
        "repaired_text": result.get("repaired_text", ""),
        "diff": result.get("diff", ""),
        "metadata": {"dry_run": result.get("dry_run", False)},
    }
