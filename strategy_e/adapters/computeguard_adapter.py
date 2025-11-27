from typing import Any, Dict, Optional

from strategy_e.adapters.pipeline_adapter import evaluate as pipeline_evaluate


def evaluate(
    resource: Dict[str, Any],
    rules: Optional[Any] = None,
    path: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Computeguard-specific adapter.

    Performs lightweight input validation against expected product fields,
    then delegates to the canonical pipeline adapter.
    """
    if not isinstance(resource, dict):
        raise ValueError("resource must be a mapping type")

    # Lightweight precondition: product schemas require `plan_id` and
    # `resources`.
    if not resource.get("plan_id"):
        raise ValueError("resource missing required field: plan_id")
    if not resource.get("resources"):
        raise ValueError("resource missing required field: resources")

    # Normalize rules to executor expected format: iterable of
    # (path, rule) tuples.
    rules_param = rules or []
    if isinstance(rules_param, dict):
        rules_param = [(None, rules_param)]
    elif isinstance(rules_param, list):
        rules_param = [(None, r) for r in rules_param]

    return pipeline_evaluate(
        resource, rules=rules_param, path=path, dry_run=dry_run
    )
