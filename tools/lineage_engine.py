#!/usr/bin/env python3
"""
Lineage-aware drift attribution engine.

Reads:
 - canonical_state/drift_report.json
 - canonical_state/guard_suite_state.json

Writes (to --out):
 - canonical_state/drift_lineage.json (machine-readable)
 - canonical_state/drift_lineage.md  (human-readable companion)

Pure read-only analysis of the repository; does not modify product files.
"""
import argparse
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import yaml
import sys


def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def find_product_for_path(manifest, relpath):
    # manifest['products'] is a list; deterministic order preserved
    owners = []
    for prod in manifest.get('products', []):
        # check product root
        root = prod.get('paths', {}).get('root')
        if root and relpath.startswith(root):
            owners.append(prod.get('id'))
            continue
        # check rule_specs paths
        for rs in prod.get('rule_specs', []):
            if rs.get('path') == relpath:
                owners.append(prod.get('id'))
    return sorted(set(owners))


def classify_file(relpath):
    # simple heuristics
    if relpath.startswith('products/') and relpath.endswith('metadata/product.yml'):
        return 'metadata'
    if relpath.startswith('products/') and relpath.endswith('checklist/checklist.yml'):
        return 'checklist'
    if relpath.startswith('rule_specs/') and relpath.endswith('.yml'):
        return 'rule_spec'
    if relpath.startswith('validation_integrity_snapshot/'):
        return 'validation_snapshot'
    if relpath.startswith('canonical_state/'):
        return 'canonical_state'
    return 'other'


def extract_rule_spec_info(root: Path, relpath: str):
    p = root / relpath
    try:
        data = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
        return {
            'rule_id': data.get('rule_id'),
            'applies_to': data.get('applies_to'),
        }
    except Exception as e:
        return {'_parse_error': str(e)}


def extract_metadata_sections(root: Path, relpath: str):
    p = root / relpath
    try:
        data = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
        if isinstance(data, dict):
            return sorted(list(data.keys()))
        return []
    except Exception:
        return []


def git_last_phase_commit_for_file(relpath: str):
    # Search git log for last commit touching file with Strategy-D or Strategy-E in message
    try:
        # use --grep to find Strategy-D or Strategy-E commits; search both
        cmd = ['git', 'log', '--pretty=format:%H|%s', '--grep=Strategy-D Phase', '--', relpath]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        if out.strip():
            # take first line as most recent matching
            line = out.splitlines()[0]
            h, msg = line.split('|', 1)
            return {'commit': h, 'message': msg, 'phase': 'Strategy-D'}
        cmd2 = ['git', 'log', '--pretty=format:%H|%s', '--grep=Strategy-E Phase', '--', relpath]
        out2 = subprocess.check_output(cmd2, stderr=subprocess.DEVNULL, text=True)
        if out2.strip():
            line = out2.splitlines()[0]
            h, msg = line.split('|', 1)
            return {'commit': h, 'message': msg, 'phase': 'Strategy-E'}
    except subprocess.CalledProcessError:
        pass
    except Exception:
        pass
    return None


def explain_lineage(relpath, owners, ftype, git_info):
    parts = []
    parts.append(f"Path: {relpath}")
    if owners:
        parts.append(f"Owner products: {', '.join(owners)}")
    else:
        parts.append("Owner products: unknown")
    parts.append(f"Type: {ftype}")
    if git_info:
        parts.append(f"Last phase commit: {git_info.get('phase')} - {git_info.get('commit')} - {git_info.get('message')}")
    else:
        parts.append("No phase-specific commit message found (fallback: unknown)")
    return '; '.join(parts)


def main(argv):
    ap = argparse.ArgumentParser(description='Lineage attribution engine')
    ap.add_argument('--drift', required=True, help='Path to canonical_state/drift_report.json')
    ap.add_argument('--manifest', required=True, help='Path to canonical_state/guard_suite_state.json')
    ap.add_argument('--out', required=True, help='Output JSON file (drift_lineage.json)')
    args = ap.parse_args(argv)

    root = Path('.').resolve()
    drift = load_json(Path(args.drift))
    manifest = load_json(Path(args.manifest))

    details = drift.get('details', {})
    changed = details.get('changed', [])
    added = details.get('added', [])
    removed = details.get('removed', [])
    all_paths = sorted(set(changed + added + removed + details.get('unchanged', [])))

    files_report = {}
    for rel in all_paths:
        ftype = classify_file(rel)
        owners = find_product_for_path(manifest, rel)
        entry = {'path': rel, 'type': ftype, 'owners': owners}
        # additional metadata for specific types
        if ftype == 'rule_spec':
            entry['rule_spec'] = extract_rule_spec_info(root, rel)
        if ftype == 'metadata' or ftype == 'checklist':
            entry['sections'] = extract_metadata_sections(root, rel)
        # git lineage
        git_info = git_last_phase_commit_for_file(rel)
        if git_info:
            entry['last_phase_commit'] = git_info
            confidence = 1.0
        else:
            entry['last_phase_commit'] = None
            confidence = 0.0
        entry['lineage_confidence'] = confidence
        entry['explanation'] = explain_lineage(rel, owners, ftype, git_info)
        files_report[rel] = entry

    # per-product summaries
    per_product = {}
    for prod in manifest.get('products', []):
        pid = prod.get('id')
        per_product[pid] = {'changed_files': [], 'added_files': [], 'removed_files': []}
    unresolved = []
    for rel, info in sorted(files_report.items()):
        if info['owners']:
            for o in info['owners']:
                if rel in details.get('changed', []):
                    per_product[o]['changed_files'].append(rel)
                if rel in details.get('added', []):
                    per_product[o]['added_files'].append(rel)
                if rel in details.get('removed', []):
                    per_product[o]['removed_files'].append(rel)
        else:
            unresolved.append(rel)

    # compute overall confidence average
    confidences = [info.get('lineage_confidence', 0.0) for info in files_report.values()]
    avg_conf = sum(confidences) / len(confidences) if confidences else 1.0

    out = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'summary': {
            'total_paths': len(all_paths),
            'products_affected': len([p for p in per_product if per_product[p]['changed_files']]),
            'unresolved_paths': len(unresolved),
            'average_confidence': avg_conf,
        },
        'files': dict(sorted(files_report.items())),
        'per_product': {k: {'changed_files': sorted(v['changed_files']), 'added_files': sorted(v['added_files']), 'removed_files': sorted(v['removed_files'])} for k, v in sorted(per_product.items())},
        'unresolved': sorted(unresolved),
    }

    outpath = Path(args.out)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, sort_keys=True)

    # write markdown companion
    mdpath = outpath.parent / 'drift_lineage.md'
    ts = out['timestamp']
    lines = [
        '# GuardSuite Drift Lineage Report',
        f'**Generated:** {ts}',
        '',
        'This report explains the origin of drift detected in the repository.',
        'See `drift_lineage.json` for machine-readable lineage mappings.',
    ]
    with mdpath.open('w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')

    print('WROTE', outpath, 'and', mdpath)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
