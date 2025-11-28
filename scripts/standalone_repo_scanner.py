#!/usr/bin/env python3
"""Standalone repository scanner

Place this script inside any repository you want to scan (or copy it to another repo).

It will:
- For each provided repo path, optionally run `tools/full_audit.py` if present (using the same Python executable).
- Copy the repo's `ai_reports/` directory (if present) into an output folder `ai_reports_multi/<repo-name>/`.
- Record `full_audit` stdout, `git HEAD`, and produce `scan_summary.json` + `scan_summary.csv` in the output folder.

Usage examples:
  python3 scripts/standalone_repo_scanner.py --repos /path/to/repo
  python3 scripts/standalone_repo_scanner.py --repos /path/to/repo1,/path/to/repo2 --out-dir /tmp/scan_out

This file is intentionally self-contained and avoids depending on project-specific constants.
"""
from pathlib import Path
import subprocess
import argparse
import shutil
import json
import csv
import sys
from datetime import datetime
import re


def run_full_audit_if_present(repo_path: Path):
    # Prefer repo-local `tools/full_audit.py` if present; otherwise use embedded runner.
    fa = repo_path / "tools" / "full_audit.py"
    if fa.exists():
        # run the repo-local full_audit.py
        try:
            p = subprocess.run([sys.executable, str(fa)], cwd=str(repo_path), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            return p.returncode, p.stdout
        except Exception as e:
            return -1, f"error_running_full_audit: {e}"
    # No repo-local audit; run the embedded implementation
    rc, out = run_embedded_full_audit(repo_path)
    # prefix output to indicate embedded implementation was used
    prefixed = "embedded_full_audit\n" + (out or "")
    return rc, prefixed


def run_embedded_full_audit(repo_path: Path):
    """Embedded, self-contained full audit runner.

    This runs a best-effort set of checks without importing repo-local tooling:
    - Runs `pytest` (captures JUnit XML and stdout)
    - Runs adapter tests under any `adapters` test paths
    - Runs `flake8` (system or `python -m flake8`)
    - Performs simple determinism: run pytest twice and record hashes
    - Writes outputs under `ai_reports/` in the repo and returns (rc, combined_stdout)
    """
    out_lines = []
    ai_reports = repo_path / "ai_reports"
    ai_reports.mkdir(parents=True, exist_ok=True)

    # 1) Run pytest full suite with JUnit XML
    junit_path = ai_reports / "pytest_full_results.xml"
    pytest_cmd = [sys.executable, "-m", "pytest", "--junitxml", str(junit_path), "-q"]
    rc_py, out_py = run_command(pytest_cmd, repo_path)
    out_lines.append(f"PYTEST_RC: {rc_py}\n")
    (ai_reports / "pytest_output.txt").write_text(out_py or "", encoding="utf-8", newline="\n")

    # 2) Run adapter tests if any adapters/tests directory exists
    adapters_test_paths = list(repo_path.glob("**/adapters/tests"))
    adapters_rc = None
    adapters_out = ""
    if adapters_test_paths:
        # run pytest only for adapter tests
        paths = [str(p) for p in adapters_test_paths]
        rc_a, out_a = run_command([sys.executable, "-m", "pytest", "-q"] + paths, repo_path)
        adapters_rc = rc_a
        adapters_out = out_a or ""
        (ai_reports / "adapter_pytest_output.txt").write_text(adapters_out, encoding="utf-8", newline="\n")

    # 3) Run flake8 if available
    flake_rc = None
    flake_out = ""
    if shutil.which("flake8"):
        flake_rc, flake_out = run_command(["flake8"], repo_path)
    else:
        flake_rc, flake_out = run_command([sys.executable, "-m", "flake8"], repo_path)
    (ai_reports / "flake8.txt").write_text(flake_out or "", encoding="utf-8", newline="\n")

    # 4) Simple determinism: run pytest one more time and record stdout hash
    rc_py2, out_py2 = run_command(pytest_cmd, repo_path)
    (ai_reports / "pytest_output_run2.txt").write_text(out_py2 or "", encoding="utf-8", newline="\n")

    import hashlib

    def sha_of(s: str):
        return hashlib.sha256((s or "").encode("utf-8")).hexdigest()

    det = {
        "first_run_sha": sha_of(out_py),
        "second_run_sha": sha_of(out_py2),
    }
    (ai_reports / "determinism.json").write_text(json.dumps(det, sort_keys=True, indent=2), encoding="utf-8", newline="\n")

    # 5) Evidence summary
    summary = {
        "repo": str(repo_path),
        "generated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "pytest_exit_code": rc_py,
        "pytest2_exit_code": rc_py2,
        "adapters_pytest_exit_code": adapters_rc,
        "flake8_exit_code": flake_rc,
    }
    (ai_reports / "evidence_summary.json").write_text(json.dumps(summary, sort_keys=True, indent=2), encoding="utf-8", newline="\n")

    combined = "\n".join(out_lines) + "\n" + (out_py or "")
    # Use pytest exit code as representative
    return rc_py, combined


def run_command(cmd, cwd: Path):
    try:
        p = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return p.returncode, p.stdout
    except (OSError, subprocess.SubprocessError) as e:
        return -1, f"error_running_command: {e}"


def bootstrap_venv(repo_path: Path, venv_dir: Path, dest_ai_reports: Path):
    """Create a venv at `venv_dir` and install dependencies if possible.

    Writes `bootstrap.log` and `bootstrap_summary.json` into `dest_ai_reports`.
    Returns (rc, message, venv_python_path)
    """
    dest_ai_reports.mkdir(parents=True, exist_ok=True)
    log_path = dest_ai_reports / "bootstrap.log"
    summary_path = dest_ai_reports / "bootstrap_summary.json"

    # If venv already exists, reuse it (do not recreate)
    try:
        if not venv_dir.exists():
            rc_make, out_make = run_command([sys.executable, "-m", "venv", str(venv_dir)], repo_path)
        else:
            rc_make, out_make = 0, "venv exists; skipping creation"

        venv_python = venv_dir / "bin" / "python"
        if not venv_python.exists():
            # fallback: maybe windows layout, try Scripts
            venv_python = venv_dir / "Scripts" / "python.exe"

        out_lines = []
        out_lines.append(f"venv_create_rc: {rc_make}\n")
        out_lines.append(out_make or "")

        # Upgrade pip/setuptools/wheel first
        rc_upg, out_upg = run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], repo_path)
        out_lines.append(f"pip_upgrade_rc: {rc_upg}\n")
        out_lines.append(out_upg or "")

        # Install requirements if present
        req = repo_path / "requirements.txt"
        pyproject = repo_path / "pyproject.toml"
        install_rc = None
        install_out = ""
        if req.exists():
            install_rc, install_out = run_command([str(venv_python), "-m", "pip", "install", "-r", str(req)], repo_path)
            out_lines.append(f"install_requirements_rc: {install_rc}\n")
            out_lines.append(install_out or "")
        elif pyproject.exists():
            # best-effort: attempt pip install .
            install_rc, install_out = run_command([str(venv_python), "-m", "pip", "install", "."], repo_path)
            out_lines.append(f"pip_install_dot_rc: {install_rc}\n")
            out_lines.append(install_out or "")
        else:
            out_lines.append("no requirements.txt or pyproject.toml found; skipping install\n")

        # Write log and summary
        log_path.write_text("\n".join(out_lines), encoding="utf-8", newline="\n")
        summary = {
            "venv_dir": str(venv_dir),
            "venv_python": str(venv_python),
            "venv_create_rc": rc_make,
            "pip_upgrade_rc": rc_upg,
            "install_rc": install_rc,
        }
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8", newline="\n")

        # Interpret success if pip upgrade succeeded
        if rc_upg == 0:
            return 0, "bootstrap_success", str(venv_python)
        else:
            return -1, "bootstrap_partial", str(venv_python)
    except Exception as e:
        # best-effort error reporting
        try:
            log_path.write_text(f"bootstrap_exception: {e}\n", encoding="utf-8", newline="\n")
        except Exception:
            pass
        return -1, f"bootstrap_exception: {e}", None


def fallback_audit(repo_path: Path, dest_ai_reports: Path):
    """Perform a minimal, self-healing audit if `tools/full_audit.py` is absent.

    - Runs `python -m pytest` if available and records output.
    - Runs `flake8` if available and records output.
    - Writes a simple `evidence_summary.json`.
    """
    dest_ai_reports.mkdir(parents=True, exist_ok=True)
    start_ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Pytest
    pytest_exit = None
    pytest_out = ""
    pytest_collected = None
    # Try running via `python -m pytest`; if pytest is not installed this will return non-zero.
    rc, out = run_command([sys.executable, "-m", "pytest", "--maxfail=1", "--disable-warnings", "-q"], repo_path)
    pytest_exit = rc
    pytest_out = out or ""
    (dest_ai_reports / "pytest_output.txt").write_text(pytest_out, encoding="utf-8", newline="\n")

    # Detect collected tests from pytest output if present
    m = re.search(r"collected\s+(\d+)\s+items", pytest_out)
    if not m:
        m = re.search(r"collected\s+(\d+)\s+tests", pytest_out)
    if m:
        try:
            pytest_collected = int(m.group(1))
        except Exception:
            pytest_collected = None
    else:
        # sometimes pytest prints 'collected 0 items' or different phrasing
        if "collected 0" in pytest_out:
            pytest_collected = 0

    # Flake8
    flake_exit = None
    flake_out = ""
    # prefer system flake8 or python -m flake8
    if shutil.which("flake8"):
        rcf, outf = run_command(["flake8"], repo_path)
    else:
        rcf, outf = run_command([sys.executable, "-m", "flake8"], repo_path)

    flake_exit = rcf
    flake_out = outf or ""
    (dest_ai_reports / "flake8.txt").write_text(flake_out, encoding="utf-8", newline="\n")

    # Build a small evidence summary
    summary = {
        "generated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "repo": str(repo_path),
        "pytest_exit_code": pytest_exit,
        "pytest_collected": pytest_collected,
        "flake8_exit_code": flake_exit,
        "scan_started_at": start_ts,
    }
    (dest_ai_reports / "evidence_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8", newline="\n")

    # If neither tool appears available, attempt to bootstrap a venv and retry
    tools_available = (pytest_exit is not None and pytest_exit != -1) or (flake_exit is not None and flake_exit != -1)
    if not tools_available:
        # attempt a best-effort bootstrap into .scanner_venv
        venv_dir = repo_path / ".scanner_venv"
        b_rc, b_msg, venv_python = bootstrap_venv(repo_path, venv_dir, dest_ai_reports)
        (dest_ai_reports / "bootstrap_summary.json").write_text(json.dumps({"rc": b_rc, "msg": b_msg, "venv_python": venv_python}, sort_keys=True), encoding="utf-8", newline="\n")

        if b_rc == 0 and venv_python:
            # retry pytest and flake8 inside the venv
            rc2, out2 = run_command([venv_python, "-m", "pytest", "--maxfail=1", "--disable-warnings", "-q"], repo_path)
            (dest_ai_reports / "pytest_output_after_bootstrap.txt").write_text(out2 or "", encoding="utf-8", newline="\n")
            rcf2, outf2 = run_command([venv_python, "-m", "flake8"], repo_path)
            (dest_ai_reports / "flake8_after_bootstrap.txt").write_text(outf2 or "", encoding="utf-8", newline="\n")

            # update summary
            summary_after = {
                "pytest_exit_code_after_bootstrap": rc2,
                "flake8_exit_code_after_bootstrap": rcf2,
            }
            (dest_ai_reports / "evidence_summary_after_bootstrap.json").write_text(json.dumps(summary_after, indent=2, sort_keys=True), encoding="utf-8", newline="\n")

            # Treat as success if either tool produced output
            if rc2 is not None or rcf2 is not None:
                return 0, "fallback_after_bootstrap"

    # Return an aggregate exit code: 0 if at least one tool ran (even if tests failed), else -1
    if pytest_exit is not None or flake_exit is not None:
        return 0, "fallback_audit_completed"
    return -1, "fallback_audit_no_tools"


def collect_ai_reports(repo_path: Path, dest_dir: Path):
    src = repo_path / "ai_reports"
    # Ensure destination parent exists
    dest_dir.parent.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        # Create an empty ai_reports folder in the destination with a placeholder
        dest_dir.mkdir(parents=True, exist_ok=True)
        placeholder = dest_dir / "_MISSING_ai_reports_PLACEHOLDER.txt"
        placeholder.write_text("source ai_reports not found in repo; placeholder created by scanner\n", encoding="utf-8", newline="\n")
        return False, "no_ai_reports"

    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(src, dest_dir)
    return True, None


def git_head(repo_path: Path):
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(repo_path), text=True).strip()
        return out
    except (subprocess.CalledProcessError, OSError):
        return None


def scan_repos(repos, out_root: Path):
    out_root.mkdir(parents=True, exist_ok=True)
    summary = []

    for r in repos:
        repo_path = Path(r).expanduser().resolve()
        if not repo_path.exists():
            print(f"Skipping missing repo: {repo_path}")
            continue

        repo_name = repo_path.name
        dest = out_root / repo_name
        dest.mkdir(parents=True, exist_ok=True)

        start_ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        rc, output = run_full_audit_if_present(repo_path)
        if output is None:
            output = ""

        # write console output deterministically
        (dest / "full_audit_stdout.txt").write_text(output, encoding="utf-8", newline="\n")

        # If full_audit.py was missing, create a marker file so the output tree is self-healing
        if output == "full_audit_missing" or rc is None:
            (dest / "NO_FULL_AUDIT.txt").write_text("tools/full_audit.py not present in target repo; scanner skipped running it\n", encoding="utf-8", newline="\n")

        # If there was an error running full_audit, record it explicitly
        if isinstance(output, str) and output.startswith("error_running_full_audit"):
            (dest / "FULL_AUDIT_ERROR.txt").write_text(output, encoding="utf-8", newline="\n")

        collected, reason = collect_ai_reports(repo_path, dest / "ai_reports")

        # If ai_reports were not found/collected, attempt a self-healing fallback audit
        if not collected:
            fb_rc, fb_reason = fallback_audit(repo_path, dest / "ai_reports")
            if fb_rc == 0:
                collected = True
                reason = None
            else:
                # leave collected False and record fallback reason
                reason = fb_reason

        head = git_head(repo_path)

        entry = {
            "repo": str(repo_path),
            "repo_name": repo_name,
            "scan_started_at": start_ts,
            "full_audit_exit_code": rc,
            "collected_ai_reports": collected,
            "collect_error": reason,
            "git_head": head,
        }

        summary.append(entry)

    # write combined JSON and CSV (deterministic JSON)
    summary_path = out_root / "scan_summary.json"
    with open(summary_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"generated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), "repos": summary}, f, indent=2, sort_keys=True)

    csv_path = out_root / "scan_summary.csv"
    with open(csv_path, "w", encoding="utf-8", newline="\n") as cf:
        writer = csv.writer(cf)
        writer.writerow(["repo_name", "repo", "scan_started_at", "full_audit_exit_code", "collected_ai_reports", "git_head"])
        for e in summary:
            writer.writerow([e["repo_name"], e["repo"], e["scan_started_at"], e["full_audit_exit_code"], e["collected_ai_reports"], e["git_head"]])

    print(f"Scan complete. Summary: {summary_path} | CSV: {csv_path}")


def main():
    p = argparse.ArgumentParser(description="Standalone scanner: run tools/full_audit.py (if present) and collect ai_reports/. Run without args to scan the current working directory.")
    p.add_argument("--repos", help="Comma-separated list of repo paths to scan (optional). If omitted, the current directory is scanned.", default=None)
    p.add_argument("--out-dir", help="Output directory for collected ai_reports (default: ./ai_reports_multi)", default="ai_reports_multi")
    args = p.parse_args()

    repos = []
    if args.repos:
        repos = [r.strip() for r in args.repos.split(",") if r.strip()]
    else:
        # Default behavior: scan current working directory
        repos = [str(Path.cwd())]

    out_root = Path(args.out_dir).expanduser().resolve()
    scan_repos(repos, out_root)


if __name__ == "__main__":
    main()
