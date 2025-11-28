#!/usr/bin/env python3
"""Deterministic AI consumer scaffold.

Reads `repos_index.yml` (or JSON) and produces `ai_analysis.yml` under the
AI Output Contract. This is a rule-based scaffold (no network or LLM calls).

Usage:
  python3 scripts/ai_consumer.py repos_index.yml ai_analysis.yml

The output follows `AI_OUTPUT_CONTRACT.md` with conservative, evidence-based
interpretation and explicit `missing_evidence` when facts are unavailable.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except Exception:
    yaml = None


def load_repos_index(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"repos_index not found: {path}")
    if yaml:
        with p.open("r", encoding="utf-8") as fh:
            try:
                return yaml.safe_load(fh) or {}
            except Exception:
                pass
    # fallback to json
    with p.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _is_file_path(s: str) -> bool:
    # heuristic: contains a path separator or endswith .md/.py
    return ("/" in s) or s.endswith(".py") or s.endswith(".md")


def analyze_task(repo_path: str, task_id: str, task_score: Dict[str, Any]) -> Dict[str, Any]:
    metrics = task_score.get("metrics", {})
    details = task_score.get("details", {})

    missing_evidence: List[str] = []
    # Check implementation files existence
    for f in details.get("impl_files", []) or []:
        try:
            if not Path(f).exists():
                missing_evidence.append(str(f))
        except Exception:
            missing_evidence.append(str(f))

    # Check validation artifacts (tests) existence when they look like paths
    for a in details.get("validation_artifacts", []) or []:
        if isinstance(a, str) and _is_file_path(a):
            p = Path(repo_path) / a
            if not p.exists():
                missing_evidence.append(str(p))

    interpretation_parts: List[str] = []
    remediation: List[str] = []

    final = int(task_score.get("final_score", 0))

    if final >= 80 and not missing_evidence and metrics.get("TESTS_PASS"):
        interpretation_parts.append("Task appears complete")
    else:
        if missing_evidence:
            interpretation_parts.append("Missing evidence for required artifacts")
            for me in missing_evidence:
                remediation.append(f"Add or restore file: {me}")
        if not metrics.get("TESTS_PASS"):
            interpretation_parts.append("Targeted tests missing or not present")
            remediation.append("Add and run unit tests referenced in validation_artifacts")
        if metrics.get("SPEC_COVERAGE", 0) < 80:
            interpretation_parts.append("Low spec coverage")
            remediation.append("Increase spec coverage for the listed spec sections in project_map")

    # semantic violation example: pipeline task with low coverage
    semantic_violations: List[Dict[str, Any]] = []
    if task_score.get("task_type") == "pipeline_stage" and metrics.get("SPEC_COVERAGE", 0) < 50:
        semantic_violations.append({"task": task_id, "violation": "pipeline stage with very low spec coverage"})

    # confidence: map final score to 0..100, reduce if missing evidence
    confidence = float(final)
    if missing_evidence:
        confidence = max(0.0, confidence - 30.0)

    return {
        "metrics": metrics,
        "interpretation": "; ".join(interpretation_parts) if interpretation_parts else "insufficient evidence",
        "remediation": remediation,
        "missing_evidence": missing_evidence,
        "semantic_violations": semantic_violations,
        "confidence": int(round(confidence)),
    }


def analyze_repos_index(repos_index: Dict[str, Any], enable_llm: bool = False) -> Dict[str, Any]:
    analysis: Dict[str, Any] = {}
    missing_transition: List[Dict[str, Any]] = []
    semantic_violations: List[Dict[str, Any]] = []
    spec_coverage_delta: Dict[str, Dict[str, float]] = {}
    recommendation: List[str] = []
    confidence_map: Dict[str, float] = {}

    for repo_name, repo_data in repos_index.items():
        if str(repo_name).startswith("_"):
            # reserved keys like _previous_delta
            continue
        repo_path = repo_data.get("repo_path", ".")
        scoring = repo_data.get("scoring", {}) or {}
        analysis[repo_name] = {}
        repo_confidences: List[float] = []

        for tid, ts in scoring.items():
            entry = analyze_task(repo_path, tid, ts)
            # Optionally enrich with an LLM (opt-in)
            if enable_llm:
                try:
                    entry = llm_enrich_analysis(repo_name, tid, entry)
                except Exception:
                    # fail-safe: do not break analysis if LLM enrichment fails
                    pass

            analysis[repo_name][tid] = entry
            repo_confidences.append(float(entry.get("confidence", 0)))
            for sv in entry.get("semantic_violations", []):
                semantic_violations.append({"repo": repo_name, **sv})
            for rec in entry.get("remediation", []):
                recommendation.append(f"{repo_name}:{tid} -> {rec}")

        # repo-level confidence: average
        avg_conf = float(sum(repo_confidences) / len(repo_confidences)) if repo_confidences else 0.0
        confidence_map[repo_name] = float(round(avg_conf, 2))

        # spec_coverage_delta: try to compute per-repo average SPEC_COVERAGE
        # If a previous snapshot has been attached under repos_index['_previous_delta']
        # the caller may have already computed a delta; we will leave per-repo current
        # here and let compute_spec_coverage_delta() handle diffs when available.
        spec_coverage_delta[repo_name] = {"previous": None, "current": None}

    return {
        "analysis": analysis,
        "missing_transition": missing_transition,
        "semantic_violations": semantic_violations,
        "spec_coverage_delta": spec_coverage_delta,
        "recommendation": recommendation,
        "confidence": confidence_map,
    }


def compute_spec_coverage_delta(prev_index: Dict[str, Any], curr_index: Dict[str, Any]) -> Dict[str, Any]:
    """Compute per-repo spec coverage delta between previous and current indexes.

    Returns mapping repo_name -> {"previous": float|None, "current": float|None}
    """
    def avg_spec(idx: Dict[str, Any], repo_name: str) -> float:
        repo = idx.get(repo_name, {}) if isinstance(idx, dict) else {}
        scoring = repo.get("scoring", {}) or {}
        vals = []
        for tid, ts in scoring.items():
            try:
                vals.append(float(ts.get("metrics", {}).get("SPEC_COVERAGE", 0)))
            except Exception:
                vals.append(0.0)
        return float(sum(vals) / len(vals)) if vals else None

    out: Dict[str, Any] = {}
    for repo_name in set(list(prev_index.keys()) + list(curr_index.keys())):
        if repo_name.startswith("_"):
            continue
        prev_val = avg_spec(prev_index, repo_name)
        curr_val = avg_spec(curr_index, repo_name)
        out[repo_name] = {"previous": prev_val, "current": curr_val}
    return out


def llm_enrich_analysis(repo_name: str, task_id: str, entry: Dict[str, Any]) -> Dict[str, Any]:
    """Optional LLM enrichment hook.

    This function is a safe stub. If environment is configured with an LLM API key
    (e.g., `OPENAI_API_KEY`) and the caller opts in, this function may call out to
    a provider. By default it returns the entry unchanged.
    """
    # Do not perform network calls here; keep as a deterministic no-op stub.
    return entry


def save_output(out: Dict[str, Any], path: str) -> None:
    p = Path(path)
    if yaml:
        with p.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(out, fh, sort_keys=True)
    else:
        with p.open("w", encoding="utf-8") as fh:
            json.dump(out, fh, sort_keys=True, indent=2)


def main(argv: List[str]):
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("in_path", nargs="?", default="repos_index.yml")
    p.add_argument("out_path", nargs="?", default="ai_analysis.yml")
    p.add_argument("--llm", action="store_true", help="Enable optional LLM enrichment (opt-in)")
    args = p.parse_args(argv[1:])

    ri = load_repos_index(args.in_path)
    out = analyze_repos_index(ri, enable_llm=args.llm)
    save_output(out, args.out_path)
    print(f"Wrote {args.out_path}")


if __name__ == "__main__":
    import sys

    main(sys.argv)
