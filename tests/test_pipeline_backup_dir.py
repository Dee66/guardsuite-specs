import os
from pathlib import Path
from strategy_e.pipeline.executor.pipeline_executor import run_pipeline_on_text


def test_backup_written_to_custom_dir(tmp_path):
    target = tmp_path / "example.yml"
    target.write_text("key: value  \n", encoding="utf-8")

    custom_dir = tmp_path / "my_backups"

    rules = {
        "repair": {
            "steps": [{"operation": "trim_trailing_whitespace"}]
        }
    }

    result = run_pipeline_on_text(
        target.read_text(),
        rules,
        path=str(target),
        dry_run=False,
        backup_dir=str(custom_dir),
    )

    assert result["backup_path"] is not None
    assert str(custom_dir) in result["backup_path"]
    assert Path(result["backup_path"]).exists()


def test_backup_dir_not_used_in_dry_run(tmp_path):
    target = tmp_path / "example.yml"
    target.write_text("key: value\n", encoding="utf-8")

    custom_dir = tmp_path / "unused"

    result = run_pipeline_on_text(
        target.read_text(),
        rules={},
        path=str(target),
        dry_run=True,
        backup_dir=str(custom_dir),
    )

    assert result["backup_path"] is None
    assert not custom_dir.exists()
