#!/usr/bin/env python3
"""Offline structure/asset/reference sanity checks, not a substitute for visual review."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import subprocess
import xml.etree.ElementTree as ET
import re
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.refs=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.refs.append(v)
errors=[]
for h in ('index.html','quality.html','principles.html','contribute.html'):
    p=Links();p.feed((ROOT/h).read_text())
    for uri in p.refs:
        u=urlparse(uri)
        if u.scheme in ('http','https','mailto') or uri.startswith('#') or uri.startswith('data:'):continue
        f=(ROOT/u.path)
        if not f.exists():errors.append(f'{h}: missing {uri}')
for file in [*ROOT.glob('assets/templates/*.svg'),ROOT/'assets/mark.svg']:
    try:
        tree=ET.parse(file);nodes=list(tree.iter())
        if len(nodes)<5:errors.append(f'{file}: not meaningfully editable')
        if any(n.tag.split('}')[-1]=='image' for n in nodes):errors.append(f'{file}: embedded image is not allowed in original vector study')
    except ET.ParseError as e:errors.append(f'{file}: {e}')
for name in ('teaser-story','method-flow','results-panel'):
    if not (ROOT/'assets/previews'/f'{name}.png').exists():errors.append(f'missing preview: {name}')
for js in ('js/site.js','js/quality.js','data/references.js'):
    run=subprocess.run(['node','--check',str(ROOT/js)],capture_output=True,text=True)
    if run.returncode:errors.append(f'{js}: invalid JS: {run.stderr}')
refs=(ROOT/'data/references.js').read_text()
for source in ('https://robodojo-benchmark.com/','https://robo-render.github.io/','https://supermimic.github.io/'):
    if source not in refs:errors.append(f'missing canonical linked reference {source}')
if len(re.findall(r"\bid:'",refs))!=8:errors.append('expected 8 reference objects in edition one')
for f in ('LICENSE','CONTRIBUTING.md','docs/ASSET_POLICY.md','docs/QUALITY_STANDARD.md','docs/PRODUCT_STRATEGY.md','skills/quality-critic/SKILL.md'):
    if not (ROOT/f).exists():errors.append(f'missing {f}')
if errors:
    for e in errors:print('FAIL:',e)
    raise SystemExit(1)
print('PASS: internal assets, editable SVG parse, JS syntax, first-edition references, key governance files')
