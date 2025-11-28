#!/usr/bin/env python3
"""Aggregate repositories and run AI consumer end-to-end.

Usage:
  python3 scripts/aggregate_and_analyze.py --repos . --out-repos repos_index.yml --out-ai ai_analysis.yml [--prev prev_repos_index.yml] [--llm]

This script calls into `repo-scanner.py` and `scripts/ai_consumer.py` without
performing network actions. LLM mode is opt-in and requires environment variables.
"""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--repos", nargs="+", default=["."], help="List of repo paths to aggregate")
    p.add_argument("--out-repos", default="repos_index.yml")
    p.add_argument("--out-ai", default="ai_analysis.yml")
    p.add_argument("--prev", default=None, help="Optional previous repos_index to compute deltas")
    p.add_argument("--llm", action="store_true", help="Enable optional LLM enrichment if environment is configured")
    args = p.parse_args(argv)

    # load repo-scanner functions
    ns = runpy.run_path(str(Path(__file__).resolve().parents[0] / "../repo-scanner.py"))
    aggregate_all_repos = ns.get("aggregate_all_repos")
    save_repos_index_with_history = ns.get("save_repos_index_with_history")

    if not aggregate_all_repos or not save_repos_index_with_history:
        print("repo-scanner functions not available", file=sys.stderr)
        raise SystemExit(2)

    repos_index = aggregate_all_repos(args.repos)
    save_repos_index_with_history(repos_index, args.out_repos)

    # run AI consumer
    ns2 = runpy.run_path(str(Path(__file__).resolve().parents[0] / "ai_consumer.py"))
    analyze_repos_index = ns2.get("analyze_repos_index")
    save_output = ns2.get("save_output")
    compute_delta = ns2.get("compute_spec_coverage_delta")

    if compute_delta and args.prev:
        prev = None
        try:
            import yaml, json
            pp = Path(args.prev)
            if pp.exists():
                if yaml:
                    prev = yaml.safe_load(pp.read_text(encoding="utf-8"))
                else:
                    prev = json.loads(pp.read_text(encoding="utf-8"))
        except Exception:
            prev = None
        # attach delta into analysis input by computing and adding to repos_index
        delta = compute_delta(prev or {}, repos_index)
        # store delta in a special key for the consumer to pick up
        repos_index["_previous_delta"] = delta

    # pass through llm flag to AI consumer (consumer will no-op unless environment/configured)
    analysis = analyze_repos_index(repos_index, enable_llm=args.llm)
    save_output(analysis, args.out_ai)
    print(f"Wrote {args.out_repos} and {args.out_ai}")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
