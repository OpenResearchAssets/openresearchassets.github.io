#!/usr/bin/env python3
"""Static catalog and source checks. This does not certify a rendered site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json
import subprocess
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.refs.append(v)
errors=[]
pages=['index.html','asset.html','for-agents/index.html','quality.html','principles.html','contribute.html']
for h in pages:
    p=Links();p.feed((ROOT/h).read_text(encoding='utf-8'))
    for uri in p.refs:
        u=urlparse(uri)
        if u.scheme in ('http','https','mailto') or uri.startswith('#') or uri.startswith('data:'):continue
        target=(ROOT/h).parent/u.path
        if not target.exists():errors.append(f'{h}: missing {uri}')
for file in [*ROOT.glob('assets/templates/*.svg'), ROOT/'assets/mark.svg']:
    try:
        tree=ET.parse(file);nodes=list(tree.iter())
        if len(nodes)<5:errors.append(f'{file}: not meaningfully editable')
        if any(n.tag.split('}')[-1]=='image' for n in nodes):errors.append(f'{file}: unexpected embedded raster image')
    except ET.ParseError as e:errors.append(f'{file}: {e}')
for name in ('teaser-story','method-flow','results-panel'):
    if not (ROOT/'assets/previews'/f'{name}.png').exists():errors.append(f'missing preview: {name}')
for js in ('js/catalog.js','js/i18n.js','js/navigation.js','js/quality.js'):
    run=subprocess.run(['node','--check',str(ROOT/js)],capture_output=True,text=True)
    if run.returncode:errors.append(f'{js}: JS syntax: {run.stderr}')
sync=subprocess.run(['python3',str(ROOT/'tools/sync_catalog.py'),'--check'],capture_output=True,text=True)
if sync.returncode:errors.append('derived catalog out of date: '+sync.stdout+sync.stderr)
catalog=json.loads((ROOT/'catalog/index.json').read_text(encoding='utf-8'))
if catalog.get('schema_version')!='1.0.0':errors.append('catalog: unsupported schema version')
entries=catalog.get('entries',[])
if len(entries)<19:errors.append('catalog: missing baseline 19 entries')
ids=[e.get('id') for e in entries]
import re
if any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', str(eid)) for eid in ids):errors.append('catalog: unsafe ID; expected kebab-case')
if len(ids)!=len(set(ids)):errors.append('catalog: duplicate IDs')
for rid in ('roborender-teaser','roborender-site','robodojo-teaser','robodojo-site','supermimic-teaser','supermimic-site'):
    if rid not in ids:errors.append('missing primary case '+rid)
for e in entries:
    where=e.get('id')
    if e.get('kind') not in catalog['facets']['kinds']:errors.append(f'{where}: unknown kind')
    for field,group in (('stages','stages'),('domains','domains')):
        values=e.get(field,[])
        if not values or not set(values).issubset(catalog['facets'][group]):errors.append(f'{where}: invalid {field}')
    if not e.get('tasks'):errors.append(f'{where}: missing task tags')
    for name in ('description','keywords'):
        val=e.get(name,{})
        if not all(val.get(language) for language in ('zh','en')):errors.append(f'{where}: missing bilingual {name}')
    for name in ('use_when','learn','avoid'):
        val=e.get('applicability',{}).get(name,{})
        if not all(val.get(language) for language in ('zh','en')):errors.append(f'{where}: missing bilingual {name}')
    src=e.get('links',{}).get('source','')
    if not src.startswith('https://'):errors.append(f'{where}: missing official HTTPS source')
    if e.get('parent') and e['parent'] not in ids:errors.append(f'{where}: broken related asset')
    if e.get('rights',{}).get('preview')=='original-svg':
        target=e.get('links',{}).get('editable','')
        if not target.startswith('assets/templates/') or not (ROOT/target).exists():errors.append(f'{where}: missing editable source')
for f in ('LICENSE','CONTRIBUTING.md','docs/ASSET_POLICY.md','docs/ASSET_SCHEMA.md','docs/QUALITY_STANDARD.md','docs/PRODUCT_STRATEGY.md','skills/quality-critic/SKILL.md','llms.txt','for-agents/README.md'):
    if not (ROOT/f).exists():errors.append(f'missing {f}')
index=(ROOT/'index.html').read_text(encoding='utf-8')
if 'js/catalog.js' not in index or 'data/references.js' in index:errors.append('index not connected to canonical catalog')
if errors:
    for e in errors:print('FAIL:',e)
    raise SystemExit(1)
print(f'PASS: {len(entries)} catalog entries, provenance, bilingual fields, source links, original SVG, page references and JS syntax')
