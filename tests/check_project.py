#!/usr/bin/env python3
"""Static catalog and source checks. This does not certify a rendered site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re
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
if len(entries)!=22:errors.append('catalog: expected 22 current assets')
core_ids={'roborender-teaser','roborender-site','robodojo-teaser','robodojo-site','supermimic-teaser','supermimic-site'}
for e in entries:
    if e.get('id') in core_ids and e.get('visual',{}).get('kind') not in ('verified-paper-figure','verified-site-screenshot'):
        errors.append(f"{e.get('id')}: case hero is not the correct paper figure or homepage")
ids=[e.get('id') for e in entries]
if any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', str(eid)) for eid in ids):errors.append('catalog: unsafe ID; expected kebab-case')
if len(ids)!=len(set(ids)):errors.append('catalog: duplicate IDs')
if 'roborender-model-architecture' in ids:errors.append('unwanted RoboRender model architecture record was reintroduced')
if 'depth-anything-3-visual' not in ids:errors.append('missing Depth Anything 3 preferred visual')
for rid in ('roborender-teaser','roborender-site','robodojo-teaser','robodojo-site','supermimic-teaser','supermimic-site','project-homepage-layout','claim-evidence-map'):
    if rid not in ids:errors.append('missing primary case '+rid)
for e in entries:
    where=e.get('id')
    visual=e.get('visual')
    if e.get('kind') in ('visual-reference','website-reference') and e.get('id') in (
        'roborender-teaser','roborender-site','robodojo-teaser','robodojo-site',
        'supermimic-teaser','supermimic-site'):
        if not visual:errors.append(f'{where}: missing reviewed case study preview')
        if not e.get('caseStudy'):errors.append(f'{where}: missing detailed visual analysis')
    if visual:
        src=visual.get('src','')
        kind=visual.get('kind')
        if kind in ('verified-paper-figure','verified-site-screenshot'):
            if not re.fullmatch(r'assets/third-party/[a-z0-9-]+/[a-z0-9-]+\.jpg',src):
                errors.append(f'{where}: invalid verified JPEG path')
            elif not (ROOT/src).is_file():errors.append(f'{where}: missing original-source JPEG {src}')
            elif (ROOT/src).read_bytes()[:3]!=bytes.fromhex('ffd8ff'):
                errors.append(f'{where}: malformed JPEG {src}')
            identity=e.get('figureIdentity',{})
            expected_type='paper-figure' if kind=='verified-paper-figure' else 'website-viewport'
            if identity.get('type')!=expected_type:errors.append(f'{where}: wrong exact image type')
            for k in ('original_name','original_source','capture_date','modifications','credit'):
                if not identity.get(k):errors.append(f'{where}: incomplete image provenance {k}')
            if kind=='verified-paper-figure' and not re.search(r'Figure 1',identity.get('original_name','')):
                errors.append(f'{where}: wrong paper figure')
        elif kind in ('licensed-source-image','licensed-paper-figure'):
            if not re.fullmatch(r'assets/third-party/[a-z0-9-]+/[a-z0-9-]+\.png',src):
                errors.append(f'{where}: unsafe third-party image path')
            elif not (ROOT/src).is_file():errors.append(f'{where}: missing authentic PNG {src}')
            elif (ROOT/src).read_bytes()[:8]!=b'\x89PNG\r\n\x1a\n':
                errors.append(f'{where}: file is not PNG {src}')
            rights=e.get('rights',{})
            if rights.get('preview')!='third-party-cc-by-4.0':errors.append(f'{where}: wrong copyright marker')
            for k in ('license_url','licensing_evidence','original_file','original_blob_sha','attribution','modifications'):
                if not rights.get(k):errors.append(f'{where}: missing source rights field {k}')
        elif kind=='external-reference-image':
            if not src.startswith('https://'):errors.append(f'{where}: remote visual must use HTTPS')
            if urlparse(src).hostname not in {
                'depth-anything-3.github.io','media.luminis-sim.com','tianxingchen.github.io',
                'supermimic.github.io','raw.githubusercontent.com','opengraph.githubassets.com'
            }:errors.append(f'{where}: untrusted remote image host {src}')
            if e.get('rights',{}).get('preview')!='external-linked-reference':
                errors.append(f'{where}: missing external rights status')
        elif kind=='authored-analysis':
            if not src.startswith('assets/editorials/') or not src.endswith('.svg'):
                errors.append(f'{where}: invalid editorial SVG path')
            else:
                img=ROOT/src
                if not img.is_file():errors.append(f'{where}: missing editorial SVG {src}')
                else:
                    try:
                        tree=ET.parse(img)
                        nodes=list(tree.iter())
                        if len(nodes)<25:errors.append(f'{where}: editorial SVG suspiciously empty')
                        if any(n.tag.split('}')[-1]=='image' for n in nodes):errors.append(f'{where}: raster pasted into SVG')
                    except ET.ParseError as err:errors.append(f'{where}: invalid SVG: {err}')
        else: errors.append(f'{where}: unsupported visual kind {kind}')
        if e.get('analysisVisual'):
            path=e['analysisVisual'].get('src','')
            if not re.fullmatch(r'assets/editorials/[a-z0-9-]+\.svg',path) or not (ROOT/path).is_file():
                errors.append(f'{where}: invalid linked analysis file')
        for field in ('alt','label'):
            if not all(visual.get(field,{}).get(lang) for lang in ('zh','en')):
                errors.append(f'{where}: missing bilingual visual {field}')
        if visual.get('kind')=='authored-analysis' and e.get('rights',{}).get('preview') != 'authored-analysis-svg':
            errors.append(f'{where}: mismatched visual license labeling')
    if e.get('caseStudy'):
        study=e['caseStudy']
        for field in ('insight','composition','reuseSteps','verification'):
            if not all(study.get(field,{}).get(lang) for lang in ('zh','en')):
                errors.append(f'{where}: missing bilingual study {field}')
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
third_party=json.loads((ROOT/'assets/third-party/manifest.json').read_text(encoding='utf-8'))
ledger_paths={item['path'] for item in third_party['items']}
for path in ROOT.glob('assets/third-party/**/*'):
    if path.is_file() and path.suffix.lower() in ('.png','.jpg','.jpeg','.webp') and str(path.relative_to(ROOT)) not in ledger_paths:
        errors.append(f'Untracked third-party image: {path}')
for item in third_party['items']:
    image=ROOT/item['path']
    if not image.is_file():errors.append(f'Missing third-party image: {item["path"]}')
    if item.get('license_url') and not item['license_url'].startswith('https://'):
        errors.append(f'Invalid media license URL: {item["path"]}')
    if not item.get('source_url','').startswith('https://'):
        errors.append(f'Missing source URL: {item["path"]}')
    if not any(e.get('visual',{}).get('src')==item['path'] for e in entries):
        errors.append(f'Unlinked third-party media: {item["path"]}')
if not (ROOT/'.github/ISSUE_TEMPLATE/asset-removal.yml').is_file():
    errors.append('missing removal request issue template')
for page in ('index.html','asset.html'):
    if 'asset-removal.yml' not in (ROOT/page).read_text(encoding='utf-8'):
        errors.append(f'{page}: missing rights holder removal link')
if 'asset-removal.yml' not in (ROOT/'js/catalog.js').read_text(encoding='utf-8'):
    errors.append('asset details missing removal contact')
for f in ('LICENSE','CONTRIBUTING.md','docs/ASSET_POLICY.md','docs/ASSET_SCHEMA.md','docs/QUALITY_STANDARD.md','docs/PRODUCT_STRATEGY.md','skills/quality-critic/SKILL.md','llms.txt','for-agents/README.md'):
    if not (ROOT/f).exists():errors.append(f'missing {f}')
index=(ROOT/'index.html').read_text(encoding='utf-8')
if 'js/catalog.js' not in index or 'data/references.js' in index:errors.append('index not connected to canonical catalog')
if errors:
    for e in errors:print('FAIL:',e)
    raise SystemExit(1)
print(f'PASS: {len(entries)} catalog entries, provenance, bilingual fields, source links, original SVG, page references and JS syntax')
