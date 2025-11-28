#!/usr/bin/env python3
"""Simple declarative rule engine to evaluate checklist evidence rules.

Reads:
 - tools/rules_definitions.json
 - ai_reports/evidence_summary.json
 - ai_reports/checklist_evidence_map.json (optional baseline)

Produces:
 - ai_reports/checklist_evidence_map.json (updated)
 - ai_reports/checklist_evidence_engine_log.json (details of rule evaluations)
 - ai_reports/checklist_update_suggestions.json (which checklist IDs can be marked done)

This engine is intentionally small and deterministic.
"""
import json
from pathlib import Path
import hashlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "ai_reports"
RULES = Path(__file__).resolve().parents[1] / "tools" / "rules_definitions.json"

# helpers

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(p, data):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def file_exists(p):
    return Path(ROOT / p).exists()


def file_last_commit_in_summary(evidence_summary, filepath):
    return evidence_summary.get("files", {}).get(filepath, {}).get("last_commit")


def pytest_exit_code_from_summary(evidence_summary):
    # Prefer structured JUnit XML if present
    junit = Path(AI / "pytest_full_results.xml")
    if junit.exists():
        try:
            tree = ET.parse(str(junit))
            root = tree.getroot()
            # testsuite(s) may be nested; sum failures/errors
            failures = 0
            errors = 0
            for ts in root.findall('.//testsuite'):
                failures += int(ts.attrib.get('failures', 0))
                errors += int(ts.attrib.get('errors', 0))
            # return 0 when no failures/errors, else return 1
            return 0 if (failures == 0 and errors == 0) else 1
        except Exception:
            pass
    return evidence_summary.get("pytest_exit_code")


def adapter_pytest_passed(adapter_pytest_path):
    # Prefer junit xml adapter results if present
    junit = Path(AI / "adapter_pytest_results.xml")
    if junit.exists():
        try:
            tree = ET.parse(str(junit))
            root = tree.getroot()
            failures = 0
            errors = 0
            for ts in root.findall('.//testsuite'):
                failures += int(ts.attrib.get('failures', 0))
                errors += int(ts.attrib.get('errors', 0))
            return (failures == 0 and errors == 0)
        except Exception:
            pass

    # fallback: check plain text summary
    p = ROOT / adapter_pytest_path
    if not p.exists():
        return False
    s = p.read_text(encoding="utf-8", errors="ignore")
    # heuristics: look for '0 failed' or 'passed' summary
    if "0 failed" in s or "passed" in s.lower():
        if "failed" in s.lower() and not "0 failed" in s:
            return False
        return True
    return False


if __name__ == "__main__":
    rules = load_json(RULES)
    esummary_path = AI / "evidence_summary.json"
    if not esummary_path.exists():
        raise SystemExit("evidence_summary.json missing; run collector first")
    esummary = load_json(esummary_path)

    cmap_path = AI / "checklist_evidence_map.json"
    if cmap_path.exists():
        cmap = load_json(cmap_path)
    else:
        cmap = {"generated_at": None, "mappings": {}}

    log = {"evaluated_at": None, "results": {}}
    suggestions = {"suggested_mark_done": [], "notes": []}

    for rid, rule in rules.get("rules", {}).items():
        rtype = rule.get("type")
        params = rule.get("params", {})
        result = {"rule_id": rid, "type": rtype, "satisfied": False, "evidence": [], "rationale": None}

        if rtype == "pytest_exit_code":
            code = pytest_exit_code_from_summary(esummary)
            result["evidence"].append({"pytest_exit_code": code})
            if isinstance(code, int) and code == 0:
                result["satisfied"] = True
                result["rationale"] = "pytest_exit_code == 0"
        elif rtype == "file_exists_and_commit":
            path = params.get("path")
            exists = file_exists(path)
            last_commit = file_last_commit_in_summary(esummary, path)
            result["evidence"].append({"file_exists": exists, "last_commit": last_commit, "path": path})
            if exists and last_commit:
                result["satisfied"] = True
                result["rationale"] = "file exists and last_commit recorded"
        elif rtype == "file_exists":
            path = params.get("path")
            exists = file_exists(path)
            result["evidence"].append({"file_exists": exists, "path": path})
            if exists:
                result["satisfied"] = True
                result["rationale"] = "file exists"
        elif rtype == "adapters_checks":
            # check that files exist and adapter pytest passed
            paths = params.get("paths", [])
            all_exist = all(file_exists(p) for p in paths)
            apath = params.get("pytest_path")
            apassed = adapter_pytest_passed(apath)
            # also check adapters flake8 exit code from evidence_summary
            adapters_flake_ok = False
            try:
                adapters_flake_exit = esummary.get("adapters_flake8_exit_code")
                adapters_flake_ok = (adapters_flake_exit == 0)
            except Exception:
                adapters_flake_ok = False
            result["evidence"].append({"files_exist": all_exist, "adapter_pytest_passed": apassed, "paths": paths, "pytest_path": apath})
            if all_exist and apassed and adapters_flake_ok:
                result["satisfied"] = True
                result["rationale"] = "adapter files exist, adapter pytest passed, and adapter flake8 passed"
            elif all_exist and apassed and not adapters_flake_ok:
                result["satisfied"] = False
                result["rationale"] = "adapter files present and tests passed but adapters flake8 reported issues"
            elif all_exist and not apassed:
                result["satisfied"] = False
                result["rationale"] = "adapter files present but adapter pytest did not clearly pass"
            else:
                result["satisfied"] = False
                result["rationale"] = "adapter files missing"
        else:
            result["rationale"] = "unknown rule type"

        log["results"][rid] = result

        # update cmap mappings
        mapping = cmap.get("mappings", {}).get(rid, {"evidence": [], "status": "missing", "rationale": None})
        # append evidence
        mapping["evidence"].extend(result.get("evidence", []))
        if result.get("satisfied"):
            mapping["status"] = "done"
            mapping["rationale"] = result.get("rationale")
            suggestions["suggested_mark_done"].append(rid)
        else:
            # if previously done, keep it; else set partial/missing
            if mapping.get("status") not in ("done",):
                mapping["status"] = "partial" if result.get("rationale") else "missing"
                mapping["rationale"] = result.get("rationale")
        cmap.setdefault("mappings", {})[rid] = mapping

    # finalize and save
    from datetime import datetime

    now = datetime.utcnow().isoformat() + "Z"
    cmap["generated_at"] = now
    log["evaluated_at"] = now
    save_json(AI / "checklist_evidence_map.json", cmap)
    save_json(AI / "checklist_evidence_engine_log.json", log)
    save_json(AI / "checklist_update_suggestions.json", suggestions)

    print("Rule engine completed. Updated ai_reports/checklist_evidence_map.json and created suggestions.")
