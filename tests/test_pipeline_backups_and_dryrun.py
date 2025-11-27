import os
from pathlib import Path
from strategy_e.pipeline.executor.pipeline_executor import run_pipeline_on_text


def test_dry_run_produces_no_backup(tmp_path):
    f = tmp_path / "sample.yml"
    f.write_text("a: 1\n", encoding="utf-8")

    result = run_pipeline_on_text(
        f.read_text(),
        rules={},
        path=str(f),
        dry_run=True,
    )

    assert result["dry_run"] is True
    assert result["backup_path"] is None
    # File must be unchanged
    assert f.read_text() == "a: 1\n"


def test_real_run_creates_backup_and_changes_file(tmp_path):
    f = tmp_path / "sample.yml"
    f.write_text("a: 1 \n\n\n", encoding="utf-8")

    rules = {"repair": {"steps": [{"operation": "trim_trailing_whitespace"}]}}

    result = run_pipeline_on_text(
        f.read_text(),
        rules=rules,
        path=str(f),
        dry_run=False,
    )

    # Backup must exist
    assert result["backup_path"] is not None
    assert os.path.exists(result["backup_path"])

    # File must be updated
    assert f.read_text() == "a: 1\n"
