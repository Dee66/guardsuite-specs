#!/usr/bin/env python3
"""Multi-repo scanner that runs the repo's full audit and collects deterministic outputs.

Usage:
  tools/repo_scanner.py --repos repo1,repo2
  tools/repo_scanner.py --repos-file repos.txt

What it does:
- For each repo path, runs `python3 tools/full_audit.py` inside the repo.
- Captures resulting `ai_reports/*` files and copies them to a central folder `ai_reports_multi/<repo-name>/`.
- Records `git rev-parse HEAD`, runtime status, and a deterministic timestamp.
- Produces `ai_reports_multi/scan_summary.json` and `scan_summary.csv`.

This script is deliberately simple and uses deterministic JSON output (sorted keys).
"""
from pathlib import Path
import subprocess
import argparse
import shutil
import json
import csv
from datetime import datetime
import sys


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "ai_reports_multi"
OUT_ROOT.mkdir(exist_ok=True)


def run_full_audit(repo_path: Path):
    # Run the repo's full_audit.py using the same python executable
    cmd = [sys.executable, "tools/full_audit.py"]
    print(f"Running full_audit in {repo_path}")
    p = subprocess.run(cmd, cwd=str(repo_path), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout


def collect_ai_reports(repo_path: Path, dest_dir: Path):
    src = repo_path / "ai_reports"
    if not src.exists():
        return False, f"no ai_reports in {repo_path}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    # copy all files (non-recursive) and directories
    for child in src.iterdir():
        dest = dest_dir / child.name
        if child.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(child, dest)
        else:
            shutil.copy2(child, dest)
    return True, None


def git_head(repo_path: Path):
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(repo_path), text=True).strip()
        return out
    except Exception:
        return None


def scan_repos(repos):
    summary = []
    for r in repos:
        repo_path = Path(r).resolve()
        if not repo_path.exists():
            print(f"Skipping missing repo: {repo_path}")
            continue

        repo_name = repo_path.name
        dest = OUT_ROOT / repo_name
        dest.mkdir(parents=True, exist_ok=True)

        start_ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        rc, output = run_full_audit(repo_path)

        # write audit console output deterministically
        (dest / "full_audit_stdout.txt").write_text(output, encoding="utf-8", newline="\n")

        collected, reason = collect_ai_reports(repo_path, dest)

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

    # write combined JSON and CSV
    summary_path = OUT_ROOT / "scan_summary.json"
    with open(summary_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"generated_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), "repos": summary}, f, indent=2, sort_keys=True)

    csv_path = OUT_ROOT / "scan_summary.csv"
    with open(csv_path, "w", encoding="utf-8", newline="\n") as cf:
        writer = csv.writer(cf)
        writer.writerow(["repo_name", "repo", "scan_started_at", "full_audit_exit_code", "collected_ai_reports", "git_head"])
        for e in summary:
            writer.writerow([e["repo_name"], e["repo"], e["scan_started_at"], e["full_audit_exit_code"], e["collected_ai_reports"], e["git_head"]])

    print(f"Scan complete. Summary: {summary_path} | CSV: {csv_path}")


def main():
    p = argparse.ArgumentParser(description="Run full_audit across multiple repos and collect ai_reports")
    p.add_argument("--repos", help="Comma-separated list of repo paths to scan")
    p.add_argument("--repos-file", help="File with one repo path per line")
    args = p.parse_args()

    repos = []
    if args.repos:
        repos = [r.strip() for r in args.repos.split(",") if r.strip()]
    if args.repos_file:
        repos_file = Path(args.repos_file)
        if repos_file.exists():
            repos += [line.strip() for line in repos_file.read_text(encoding="utf-8").splitlines() if line.strip()]

    if not repos:
        print("No repos provided. Use --repos or --repos-file")
        return

    scan_repos(repos)


if __name__ == "__main__":
    main()
