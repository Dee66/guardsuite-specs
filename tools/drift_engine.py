#!/usr/bin/env python3
"""
Deterministic drift-comparison engine.

Usage: tools/drift_engine.py --ref <path-to-checksums.json> --new <path-or-dir> --out <out.json>

If --new is a directory, the engine will compute SHA-256 checksums for relevant files
under that directory (products/, rule_specs/, validation_integrity_snapshot/, canonical_state/guard_suite_state.json).
If --new is a checksums.json file, it will be read directly.

Outputs a JSON report listing added/removed/changed/unchanged files.
"""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import sys


def load_checksums(path: Path):
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('files', {})


def compute_checksums_for_repo(root: Path):
    # Collect candidate files under the repo matching the canonical areas
    patterns = [
        'canonical_state/guard_suite_state.json',
        'validation_integrity_snapshot/*.json',
        'validation_integrity_snapshot/*.md',
        'products/*/metadata/product.yml',
        'products/*/checklist/checklist.yml',
        'rule_specs/**/*.yml',
        'products/*/assets/copy/demo/plan_bad.json',
        'products/*/assets/copy/demo/plan_guard.json',
        'products/*/assets/copy/demo/demo_version.yml',
        'products/*/assets/copy/repro_notes.md',
    ]
    files = set()
    for pat in patterns:
        for p in root.glob(pat):
            if p.is_file():
                files.add(p.relative_to(root).as_posix())

    return compute_checksums_from_list(root, sorted(files))


def compute_checksums_from_list(root: Path, relpaths):
    out = {}
    for rel in relpaths:
        p = root / rel
        if p.exists() and p.is_file():
            h = hashlib.sha256()
            with p.open('rb') as fh:
                for chunk in iter(lambda: fh.read(8192), b''):
                    h.update(chunk)
            out[rel] = h.hexdigest()
        else:
            out[rel] = None
    return out


def union_keys(a, b):
    s = set(a) | set(b)
    return sorted(s)


def make_report(ref_checks, new_checks):
    keys = union_keys(ref_checks.keys(), new_checks.keys())
    added = []
    removed = []
    changed = []
    unchanged = []
    for k in keys:
        r = ref_checks.get(k)
        n = new_checks.get(k)
        if r is None and n is None:
            # both missing — treat as removed
            removed.append(k)
        elif r is None and n is not None:
            added.append(k)
        elif r is not None and n is None:
            removed.append(k)
        else:
            if r == n:
                unchanged.append(k)
            else:
                changed.append(k)

    total = len(keys)
    unchanged_count = len(unchanged)
    # Repo health drift score: percentage of unchanged files (0-100)
    score = int((unchanged_count / total) * 100) if total > 0 else 100

    report = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'summary': {
            'total_paths': total,
            'added': len(added),
            'removed': len(removed),
            'changed': len(changed),
            'unchanged': len(unchanged),
            'drift_score': score,
        },
        'details': {
            'added': sorted(added),
            'removed': sorted(removed),
            'changed': sorted(changed),
            'unchanged': sorted(unchanged),
        },
    }
    return report


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)


def write_markdown(path: Path, report):
    ts = report.get('timestamp')
    lines = []
    lines.append('# GuardSuite Drift Report')
    lines.append(f'**Generated:** {ts}')
    lines.append('')
    lines.append('## Summary')
    s = report['summary']
    lines.append(f"- Total paths considered: {s['total_paths']}")
    lines.append(f"- Added: {s['added']}")
    lines.append(f"- Removed: {s['removed']}")
    lines.append(f"- Changed: {s['changed']}")
    lines.append(f"- Unchanged: {s['unchanged']}")
    lines.append(f"- Drift score: {s['drift_score']}/100")
    lines.append('')
    lines.append('See `drift_report.json` for machine-readable details.')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')


def main(argv):
    ap = argparse.ArgumentParser(description='Drift comparison engine')
    ap.add_argument('--ref', required=True, help='Reference checksums.json')
    ap.add_argument('--new', required=True, help='New path (dir) or checksums.json file')
    ap.add_argument('--out', required=True, help='Output JSON file')
    args = ap.parse_args(argv)

    root = Path('.').resolve()
    ref_path = Path(args.ref)
    if not ref_path.exists():
        print('Reference checksums file not found:', ref_path, file=sys.stderr)
        return 2
    ref_checks = load_checksums(ref_path)

    new_path = Path(args.new)
    if new_path.is_file():
        new_checks = load_checksums(new_path)
    else:
        # treat as directory root to scan
        new_checks = compute_checksums_for_repo(new_path)

    report = make_report(ref_checks, new_checks)
    outpath = Path(args.out)
    write_json(outpath, report)
    # also write a markdown companion
    mdpath = outpath.parent / 'drift_report.md'
    write_markdown(mdpath, report)
    print('WROTE', outpath, 'and', mdpath)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
