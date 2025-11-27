#!/usr/bin/env python3
"""Simple perf harness: measure runtime of a representative command.

By default this runs a small Python timeit to produce quick timing numbers. It writes
`ai_reports/perf_results.json` with run times, mean and stdev.

Usage:
  python3 tools/perf_harness.py --cmd "python -m timeit -n100 -r3 'sum(range(100))'"

If no command provided, runs a default microbenchmark.
"""
from pathlib import Path
import subprocess
import json
import argparse
import statistics
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "ai_reports"
AI.mkdir(parents=True, exist_ok=True)


def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cmd", help="Command to benchmark (shell) ")
    p.add_argument("--runs", type=int, default=5, help="Number of iterations")
    args = p.parse_args()

    cmd = args.cmd or "python -m timeit -n100 -r3 'sum(range(1000))'"
    results = []
    outputs = []
    for i in range(args.runs):
        rc, out = run_cmd(cmd)
        results.append(rc)
        outputs.append(out)

    # attempt to parse timeit output for numeric times
    times = []
    for out in outputs:
        # look for like: '100 loops, best of 3: 1.23 usec per loop' or '1.23 sec per loop'
        import re
        m = re.search(r"([0-9]+\.?[0-9]*)\s*(usec|ms|sec) per loop", out)
        if m:
            val = float(m.group(1))
            unit = m.group(2)
            if unit == 'usec':
                val = val / 1e6
            elif unit == 'ms':
                val = val / 1e3
            # sec remains
            times.append(val)

    summary = {
        "generated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "command": cmd,
        "runs": args.runs,
        "raw_outputs": outputs,
        "exit_codes": results,
    }
    if times:
        summary["times_seconds"] = times
        summary["mean_seconds"] = statistics.mean(times)
        summary["stdev_seconds"] = statistics.stdev(times) if len(times) > 1 else 0.0

    out_path = AI / "perf_results.json"
    out_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    print("Wrote perf results to", out_path)


if __name__ == '__main__':
    main()
