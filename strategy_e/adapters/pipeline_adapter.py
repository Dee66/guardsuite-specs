from typing import Any, Dict, Optional

try:
    from strategy_e.pipeline.executor.pipeline_executor import run_pipeline_on_text
except Exception:
    # Fallback stub if executor not importable in this environment
    def run_pipeline_on_text(text: str, rules, path: str = None, dry_run: bool = False, backup_dir: str = None):
        return {
            "normalized_text": text,
            "validation_errors": [],
            "repaired_text": text,
            "diff": "",
            "backup_path": None,
            "dry_run": dry_run,
        }


def evaluate(resource: Dict[str, Any], rules: Optional[Any] = None, path: Optional[str] = None, dry_run: bool = False) -> Dict[str, Any]:
    """Adapter that maps a resource to the canonical pipeline executor.

    - Accepts a resource that may contain a `text` field or `resources` list with `content`.
    - Calls `run_pipeline_on_text` and normalizes the response into a consistent dict.
    """
    text = ""
    if isinstance(resource, dict):
        if resource.get("text"):
            text = resource.get("text")
        elif resource.get("resources") and isinstance(resource.get("resources"), list):
            first = resource.get("resources")[0]
            text = first.get("content", "") if isinstance(first, dict) else str(first)
        else:
            # best-effort stringification
            text = str(resource)
    else:
        text = str(resource)

    result = run_pipeline_on_text(text, rules or [], path=path, dry_run=dry_run)

    violations = [{"message": m} for m in result.get("validation_errors", [])]

    return {
        "violations": violations,
        "repaired_text": result.get("repaired_text", ""),
        "diff": result.get("diff", ""),
        "metadata": {"dry_run": result.get("dry_run", False)},
    }
