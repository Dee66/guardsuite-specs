from src.pipelines.ingest import ingest


def test_ingest_success():
    assert ingest({}) is True
