from strategy_e.adapters.pipeline_adapter import evaluate


def test_pipeline_adapter_basic():
    resource = {
        "plan_id": "test-plan",
        "resources": [{"content": "short\nline"}],
    }
    result = evaluate(
        resource,
        rules=[
            {
                "validation": {
                    "checks": [{"type": "line_length", "max": 120}]
                }
            }
        ],
        dry_run=True,
    )
    assert isinstance(result, dict)
    assert "violations" in result
