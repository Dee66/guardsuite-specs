#!/usr/bin/env python3
import yaml
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, deque

ROOT = Path.cwd()
OUT = ROOT / 'workspace' / 'strategy_d' / 'phase11' / 'cross_product_semantic_validation_report.md'
OUT.parent.mkdir(parents=True, exist_ok=True)
PROD_DIR = ROOT / 'products'
products = sorted([p.name for p in PROD_DIR.iterdir() if p.is_dir()])

# load product metadata
meta_map = {}
errors = []
warnings = []
infos = []

for prod in products:
    p = PROD_DIR / prod / 'metadata' / 'product.yml'
    if not p.exists():
        errors.append((prod, 'metadata_missing'))
        meta_map[prod] = None
        continue
    try:
        data = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
    except Exception as e:
        errors.append((prod, f'metadata_parse_error: {e}'))
        meta_map[prod] = None
        continue
    if not isinstance(data, dict):
        warnings.append((prod, 'metadata_root_not_mapping'))
        meta_map[prod] = {}
        continue
    meta_map[prod] = data

# helper

def get_related(prod_meta):
    if not prod_meta:
        return []
    r = prod_meta.get('related_products')
    if r is None:
        return []
    if isinstance(r, list):
        return [str(x) for x in r]
    return [str(r)]

# build graph
graph = defaultdict(list)
rev_graph = defaultdict(list)
for prod in products:
    data = meta_map.get(prod)
    rels = get_related(data)
    for r in rels:
        graph[prod].append(r)
        rev_graph[r].append(prod)

# checks: referenced product existence, bidirectional links
missing_refs = []
non_bidirectional = []
for a in sorted(products):
    for b in sorted(graph.get(a, [])):
        if b not in products:
            missing_refs.append((a, b))
        else:
            # check b lists a
            if a not in graph.get(b, []):
                non_bidirectional.append((a, b))

# core dependency check: look for guardsuite-core references
no_core_ref = []
for prod in products:
    data = meta_map.get(prod) or {}
    ok = False
    # check versioning.core_dependency_pin
    versioning = data.get('versioning') if isinstance(data.get('versioning'), dict) else None
    if versioning:
        core_pin = versioning.get('core_dependency_pin')
        if core_pin and 'guardsuite-core' in str(core_pin):
            ok = True
    # check references
    refs = data.get('references') if isinstance(data.get('references'), dict) else None
    if refs:
        if any('guardsuite-core' in str(v) for v in refs.values()):
            ok = True
    if not ok:
        no_core_ref.append(prod)

# guardboard/guardscore integration expectations
integration_issues = []
if 'guardboard' in products and 'guardscore' in products:
    gb = meta_map.get('guardboard') or {}
    gs = meta_map.get('guardscore') or {}
    # check guardboard mentions guardscore in related or in metadata
    gb_ok = False
    if 'guardscore' in (gb.get('related_products') or []):
        gb_ok = True
    if gb.get('guardscore_integration'):
        gb_ok = True
    if not gb_ok:
        integration_issues.append(('guardboard', 'guardscore_integration_missing'))
    # check guardscore mentions guardboard
    gs_ok = False
    if 'guardboard' in (gs.get('related_products') or []):
        gs_ok = True
    if gs.get('guardboard_integration'):
        gs_ok = True
    if not gs_ok:
        integration_issues.append(('guardscore', 'guardboard_integration_missing'))

# master_spec completeness: check guardsuite_master_spec lists products (if it has a products field)
master_issues = []
if 'guardsuite_master_spec' in products:
    ms = meta_map.get('guardsuite_master_spec') or {}
    listed = ms.get('products')
    if isinstance(listed, list):
        missing_in_master = sorted([p for p in products if p not in listed])
        if missing_in_master:
            master_issues.append(('guardsuite_master_spec', 'missing_products', missing_in_master))
    else:
        # if no products list, mark as info
        infos.append(('guardsuite_master_spec', 'no_products_list'))

# construct dependency graph reachability and cycles
# Graph uses nodes = products; edges from A to B if A -> B
nodes = set(products)
# detect cycles via DFS
visited = {}
stack = []
cycles = []

def dfs(node, path):
    if node not in nodes:
        return
    if node in visited:
        if visited[node] == 1:
            # back-edge found
            if node in path:
                idx = path.index(node)
                cycles.append(path[idx:] + [node])
        return
    visited[node] = 1
    path.append(node)
    for nbr in graph.get(node, []):
        dfs(nbr, path)
    path.pop()
    visited[node] = 2

for n in sorted(products):
    if n not in visited:
        dfs(n, [])

# reachability from roots (nodes with no incoming edges)
in_degrees = {n: len(rev_graph.get(n, [])) for n in products}
roots = [n for n,deg in sorted(in_degrees.items()) if deg == 0]
reachable = set()
for r in roots:
    q = [r]
    while q:
        cur = q.pop()
        if cur in reachable:
            continue
        reachable.add(cur)
        for nbr in graph.get(cur, []):
            if nbr in products:
                q.append(nbr)
unreachable = sorted([n for n in products if n not in reachable])

# nodes depending on non-existent products
depends_on_nonexistent = defaultdict(list)
for a in products:
    for b in graph.get(a, []):
        if b not in products:
            depends_on_nonexistent[a].append(b)

# package report
lines = []
now = datetime.now(timezone.utc).isoformat()
lines.append('# Strategy-D Phase 11: Cross-Product Semantic Validation Report')
lines.append('')
lines.append(f'- Generated: {now}')
lines.append('')
lines.append('## Summary')
lines.append('')
lines.append(f'- Products scanned: {len(products)}')
lines.append(f'- Roots (no incoming edges): {roots or []}')
lines.append(f'- Cycles detected: {len(cycles)}')
lines.append(f'- Unreachable nodes from roots: {len(unreachable)}')
lines.append('')
lines.append('## Severity tallies')
lines.append('')
lines.append(f'- Errors: {len(missing_refs) + sum(1 for e in errors)}')
lines.append(f'- Warnings: {len(non_bidirectional) + len(no_core_ref) + len(integration_issues)}')
lines.append(f'- Info: {len(infos)}')
lines.append('')
lines.append('## Missing / Invalid References (Errors)')
lines.append('')
if missing_refs:
    lines.append('| Product | Referenced |')
    lines.append('| --- | --- |')
    for a,b in sorted(missing_refs):
        lines.append(f'| {a} | {b} |')
else:
    lines.append('- None')
lines.append('')

lines.append('## Non-bidirectional Related-Product Links (Warnings)')
lines.append('')
if non_bidirectional:
    lines.append('| From | To |')
    lines.append('| --- | --- |')
    for a,b in sorted(non_bidirectional):
        lines.append(f'| {a} | {b} |')
else:
    lines.append('- None')
lines.append('')

lines.append('## Products without a guardsuite-core reference (Warnings)')
lines.append('')
if no_core_ref:
    for p in sorted(no_core_ref):
        lines.append(f'- {p}')
else:
    lines.append('- None')
lines.append('')

lines.append('## GuardBoard / GuardScore integration expectations (Warnings/Info)')
lines.append('')
if integration_issues:
    for p,issue in sorted(integration_issues):
        lines.append(f'- {p}: {issue}')
else:
    lines.append('- None')
lines.append('')

lines.append('## Master spec completeness')
lines.append('')
if master_issues:
    for item in master_issues:
        lines.append(f'- {item[0]}: missing products: {item[2]}')
else:
    lines.append('- None or no explicit product list present')
lines.append('')

lines.append('## Dependency Graph Cycles (Errors)')
lines.append('')
if cycles:
    for cyc in cycles:
        lines.append('- Cycle: ' + ' -> '.join(cyc))
else:
    lines.append('- None')
lines.append('')
lines.append('## Unreachable Nodes from Roots (Warning)')
lines.append('')
if unreachable:
    for n in unreachable:
        lines.append(f'- {n}')
else:
    lines.append('- None')
lines.append('')
lines.append('## Dependencies on non-existent products (Errors)')
lines.append('')
if depends_on_nonexistent:
    lines.append('| Product | Depends On (missing) |')
    lines.append('| --- | --- |')
    for a in sorted(depends_on_nonexistent.keys()):
        lines.append(f'| {a} | {", ".join(sorted(depends_on_nonexistent[a]))} |')
else:
    lines.append('- None')
lines.append('')
lines.append('## Full Dependency Graph (by product)')
lines.append('')
for p in sorted(products):
    nbrs = sorted([n for n in graph.get(p, []) if n in products])
    lines.append(f'- {p}: {nbrs}')
lines.append('')
lines.append('## Notes and Suggested Repairs')
lines.append('')
lines.append('- Fix missing referenced products listed under Missing/Invalid References.')
lines.append('- Consider adding bidirectional related_products entries where appropriate.')
lines.append('- Ensure every product references `guardsuite-core` where expected (see warnings).')
lines.append('- Address cycles in the dependency graph (errors) to break circular dependencies.')
lines.append('')
OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('WROTE', OUT)