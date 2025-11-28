# AI Output Contract

This document specifies the expected AI output schema produced after analyzing a repo or the aggregated `repos_index`.

Top-level object (mapping):
- analysis: mapping repo_name -> { task_id -> analysis_entry }
- missing_transition: list of { repo: string, task_id: string, reason: string }
- semantic_violations: list of { repo: string, file: string, violation: string }
- spec_coverage_delta: mapping repo_name -> { previous: float, current: float }
- recommendation: list of actionable suggestions (strings or structured objects)
- confidence: mapping repo_name -> float (0..100)

analysis_entry fields:
- metrics: copy of the task's metrics
- interpretation: brief structured explanation of what's missing or done
- remediation: suggested code/tests/docs to reach done state
- confidence: float 0..100

Rules:
- All fields must be explicit; do not fabricate missing evidence.
- If the AI cannot determine a field, return `null` for that field and include `missing_evidence` in the `analysis_entry`.

Example:
{
  "analysis": {
    "my-repo": {
      "CORE-001": {
        "metrics": {...},
        "interpretation": "Tests missing; implementation files absent; spec_coverage 0%.",
        "remediation": ["Add src/pipelines/ingest.py","Add tests/test_ingest.py::test_ingest_success"],
        "confidence": 35
      }
    }
  },
  "missing_transition": [],
  "semantic_violations": [],
  "spec_coverage_delta": {"my-repo": {"previous": 60, "current": 55}},
  "recommendation": ["Prioritize CORE-001 test coverage"],
  "confidence": {"my-repo": 40}
}
