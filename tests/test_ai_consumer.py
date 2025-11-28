import json
import subprocess
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None


def run_cmd(args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_ai_consumer_runs_and_outputs_analysis(tmp_path):
    repo_index = Path("repos_index.yml")
    # Ensure repos_index exists; aggregator will create it if missing
    if not repo_index.exists():
        run_cmd(["python3", "scripts/aggregate_and_analyze.py"])

    out = tmp_path / "ai_analysis_test.yml"
    # Run the ai_consumer against the repo index
    run_cmd(["python3", "scripts/ai_consumer.py", str(repo_index), str(out)])
    assert out.exists(), "ai_consumer did not produce output file"

    text = out.read_text(encoding="utf-8")
    if yaml:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)

    assert isinstance(data, dict)
    assert "analysis" in data, "Output missing top-level 'analysis'"
    assert isinstance(data["analysis"], dict)
