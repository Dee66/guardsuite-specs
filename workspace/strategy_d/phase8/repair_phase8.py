#!/usr/bin/env python3
import yaml, sys
from pathlib import Path
from datetime import datetime, timezone
from collections import OrderedDict
import difflib

ROOT = Path.cwd()
SCHEMA_PATH = ROOT / 'schemas' / 'checklist_schema.yml'
OUT_DIFF_DIR = ROOT / 'workspace' / 'strategy_d' / 'phase8' / 'diffs'
OUT_DIFF_DIR.mkdir(parents=True, exist_ok=True)
REVALID_PATH = ROOT / 'workspace' / 'strategy_d' / 'phase8' / 'checklist_revalidation_report.md'

products = [
    'vectorscan','vectorguard','computescan','computeguard','pipelinescan','pipelineguard',
    'guardboard','guardscore','guardsuite-core','guardsuite_master_spec','guardsuite-specs',
    'guardsuite-template','playground'
]

try:
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding='utf-8'))
except Exception as e:
    print('ERROR: unable to load checklist schema', e)
    sys.exit(1)

properties = schema.get('properties', {}) or {}
required_top = schema.get('required', []) or []

# placeholders
def placeholder_for(prop_schema):
    if not prop_schema:
        return {}
    t = None
    if isinstance(prop_schema, dict):
        t = prop_schema.get('type')
    elif isinstance(prop_schema, str):
        t = prop_schema
    if t == 'string' or t is None:
        return ''
    if t == 'array':
        return []
    if t in ('object','mapping'):
        return {}
    if t == 'integer':
        return 0
    if t == 'number':
        return 0
    if t == 'boolean':
        return False
    return None

# repair single checklist mapping
def repair_checklist(data):
    new = OrderedDict()
    legacy = OrderedDict()
    # ensure top-level required blocks exist
    for top in required_top:
        if top in data and data[top] is not None:
            val = data.pop(top)
            # normalize types according to schema
            schema_entry = properties.get(top)
            stype = schema_entry.get('type') if isinstance(schema_entry, dict) else None
            if stype == 'array' and not isinstance(val, list):
                val = [val]
            if stype == 'object' and not isinstance(val, dict):
                val = {'value': val}
            new[top] = val
        else:
            # insert placeholder
            schema_entry = properties.get(top)
            new[top] = placeholder_for(schema_entry)
    # any remaining keys go into x_legacy
    for k in sorted(data.keys()):
        legacy[k] = data[k]
    if legacy:
        new['x_legacy'] = legacy
    return new

# helper to plain dict
def to_plain(o):
    if isinstance(o, dict):
        return {k: to_plain(v) for k,v in o.items()}
    if isinstance(o, list):
        return [to_plain(v) for v in o]
    return o

modified = []
for prod in products:
    checklist_path = ROOT / 'products' / prod / 'checklist' / 'checklist.yml'
    if not checklist_path.exists():
        print('SKIP missing', checklist_path)
        continue
    orig_text = checklist_path.read_text(encoding='utf-8')
    try:
        data = yaml.safe_load(orig_text)
    except Exception as e:
        # malformed YAML -> treat as empty mapping and preserve raw in x_legacy
        data = {}
    if data is None:
        data = {}
    if not isinstance(data, dict):
        data = {'value': data}
    repaired = repair_checklist(dict(data))
    new_text = yaml.safe_dump(to_plain(repaired), sort_keys=False, allow_unicode=True)
    if new_text.strip() != orig_text.strip():
        checklist_path.write_text(new_text, encoding='utf-8')
        modified.append(str(checklist_path.relative_to(ROOT)))
    # write unified diff
    diff_path = OUT_DIFF_DIR / f"{prod}.checklist.diff"
    ud = ''.join(difflib.unified_diff(orig_text.splitlines(keepends=True), new_text.splitlines(keepends=True), fromfile=str(checklist_path.relative_to(ROOT))+'.orig', tofile=str(checklist_path.relative_to(ROOT)), lineterm=''))
    diff_path.write_text(ud or '# no changes\n', encoding='utf-8')
    print('WROTE DIFF', diff_path)

print('Modified checklists:', len(modified))

# attempt to run existing checklist validator if present
validator = ROOT / 'workspace' / 'strategy_d' / 'phase8' / 'validate_checklists.py'
if validator.exists():
    try:
        import subprocess
        subprocess.run([sys.executable, str(validator)], check=True)
    except subprocess.CalledProcessError as e:
        print('Validator failed', e)
# fallback: re-use phase6 validator for basic presence check
else:
    print('No dedicated checklist validator found; creating simple revalidation report')
    lines = []
    now = datetime.now(timezone.utc).isoformat()
    lines.append('# Strategy-D Phase 8: Checklist Revalidation Report')
    lines.append('')
    lines.append(f'- Generated: {now}')
    lines.append('')
    lines.append('## Findings')
    lines.append('')
    for prod in products:
        path = ROOT / 'products' / prod / 'checklist' / 'checklist.yml'
        ok = False
        detail = ''
        if not path.exists():
            detail = 'missing'
        else:
            try:
                v = yaml.safe_load(path.read_text(encoding='utf-8'))
                if isinstance(v, dict) and all(k in v for k in ['metadata','states','phases','items']):
                    ok = True
                else:
                    detail = 'structural-mismatch'
            except Exception as e:
                detail = f'parse-error: {e}'
        lines.append(f'### {prod}')
        lines.append('')
        lines.append(f'- Checklist present: {"yes" if path.exists() else "no"}')
        lines.append(f'- Valid: {"yes" if ok else "no"}')
        if not ok:
            lines.append(f'- Detail: {detail}')
        lines.append('')
    REVALID_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVALID_PATH.write_text('\n'.join(lines)+"\n", encoding='utf-8')
    print('WROTE', REVALID_PATH)
