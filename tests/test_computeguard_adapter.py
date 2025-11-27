from strategy_e.adapters.computeguard_adapter import evaluate


def test_computeguard_adapter_basic():
    resource = {
        "plan_id": "sample",
        "resources": [{"content": "short\nlonger line content"}],
    }
    result = evaluate(
        resource,
        rules=[{"validation": {"checks": [{"type": "line_length", "max": 10}]}}],
        dry_run=True,
    )
    assert isinstance(result, dict)
    assert "violations" in result
