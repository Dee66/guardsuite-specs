from src.pipelines.stages import stage_order


def test_stage_order():
    so = stage_order()
    assert isinstance(so, list)
    assert "ingest" in so
