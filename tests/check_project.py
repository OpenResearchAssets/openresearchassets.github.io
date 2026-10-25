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
pages=['index.html','asset.html','for-agents/index.html','quality.html','principles.html','contribute.html','examples.html','examples/sample-project.html','examples/roborender.html']
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
if len(entries)!=40:errors.append('catalog: expected 40 sourced research records')
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
                'supermimic.github.io','raw.githubusercontent.com','instruct-pix2pix.timothybrooks.com','opengraph.githubassets.com'
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
# Keep the independent project's canonical organization URLs consistent.
# The org Pages root is not the old personal /OpenResearchAssets/ project path.
legacy = ('https://' + 'suchenl.github.io/OpenResearchAssets/',
          'https://github.com/' + 'Suchenl/OpenResearchAssets')
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.html','.js','.json','.txt','.yml','.yaml','.py'}:
        relative = p.relative_to(ROOT)
        if any(part in {'__pycache__','.git'} for part in relative.parts):continue
        try:content = p.read_text(encoding='utf-8')
        except UnicodeError:continue
        if any(old in content for old in legacy):
            errors.append(f'{relative}: obsolete Suchenl project URL')

# Community vision is an editable illustration, not a pasted screenshot.
for vision in (ROOT/'assets/diagrams/community-trajectory.svg',
               ROOT/'assets/diagrams/community-trajectory.en.svg'):
    if not vision.is_file():
        errors.append(f'missing editable community vision SVG: {vision.name}')
        continue
    try:
        r = ET.parse(vision)
        nodes = list(r.iter())
        if sum(el.tag.split('}')[-1]=='text' for el in nodes) < 6:
            errors.append(f'{vision.name}: text is not independently editable')
        if any(el.tag.split('}')[-1]=='image' for el in nodes):
            errors.append(f'{vision.name}: embedded raster is not allowed')
    except ET.ParseError as err:
        errors.append(f'{vision.name}: SVG parse error: {err}')

# P0: first-visit entry points and general research-asset contribution must be accessible.
home_html=(ROOT/'index.html').read_text(encoding='utf-8')
contribute_html=(ROOT/'contribute.html').read_text(encoding='utf-8')
if home_html.count('class="ora-main-path"')!=2:
    errors.append('homepage: expected Gallery and Skills entry points')
if contribute_html.count('class="ora-start-path"')!=3:
    errors.append('contribution page: expected three contribution paths')
for page_name,html in [('index.html',home_html),('contribute.html',contribute_html)]:
    if any(text not in html for text in ('data-i18n-zh=', 'data-i18n-en=')):
        errors.append(f'{page_name}: missing bilingual first-use text')
if 'id="gallery"' not in home_html or 'id="skills"' not in home_html:
    errors.append('homepage: gallery or skills route missing')
if 'id="popular-skills"' not in home_html or 'id="practice-skills"' not in home_html:
    errors.append('homepage: popular and practice tracks not separate')
if 'href="for-agents/"' not in home_html or 'href="contribute.html"' not in home_html:
    errors.append('homepage: missing agent or contribution entry')
if 'id="methods"' not in contribute_html:
    errors.append('contribution page: missing methods and workflows')
correction = ROOT/'.github/ISSUE_TEMPLATE/catalog-correction.md'
if not correction.is_file():
    errors.append('missing general asset correction issue template')
elif 'catalog-correction.md' not in contribute_html:
    errors.append('contribution page: no direct correction entry')
template=(ROOT/'.github/ISSUE_TEMPLATE/asset-request.md').read_text(encoding='utf-8')
if not all(word in template for word in ('工作流','工具','来源','授权')):
    errors.append('asset proposal template: still too narrow for research assets')

# P1 worked examples use concrete editable vector assets and never pretend to report results.
import csv
for slug in ('method-figure','experiment-design','project-homepage'):
    for locale in ('zh','en'):
        svg=ROOT/'assets/examples'/f'{slug}.{locale}.svg'
        guide=ROOT/'examples'/f'{slug}.{locale}.md'
        if not guide.is_file():errors.append(f'missing worked example guide: {guide}')
        elif len(guide.read_text(encoding='utf-8'))<1200:
            errors.append(f'worked example is too thin: {guide}')
        if not svg.is_file():
            errors.append(f'missing worked example SVG: {svg}')
            continue
        try:
            nodes=list(ET.parse(svg).iter())
            if sum(n.tag.split('}')[-1]=='text' for n in nodes)<10:
                errors.append(f'{svg}: labels are not independently editable')
            if any(n.tag.split('}')[-1]=='image' for n in nodes):
                errors.append(f'{svg}: embedded raster data is prohibited')
        except ET.ParseError as e:errors.append(f'{svg}: invalid SVG: {e}')
for p in ('examples/README.md','examples/research-brief.md','examples/evidence-register.csv',
          'examples/sample-project.html','examples.html','css/examples.css'):
    if not (ROOT/p).is_file():errors.append(f'missing worked example artifact: {p}')
with (ROOT/'examples/evidence-register.csv').open(encoding='utf-8',newline='') as sheet:
    rows=list(csv.DictReader(sheet))
    if len(rows)<3:errors.append('evidence register: expected multiple falsifiable comparisons')
    for row in rows:
        if row.get('result_value') or row.get('uncertainty_or_ci') or row.get('raw_evidence_url'):
            errors.append('example register: must not contain fictional measurements or URLs')
case_page=(ROOT/'examples.html').read_text(encoding='utf-8')
if case_page.count('class="ora-example"')!=3:errors.append('worked example landing: expected three cases')
if 'examples/sample-project.html' not in case_page or 'examples/evidence-register.csv' not in case_page:
    errors.append('worked example landing: missing concrete deliverables')
if 'examples/roborender.html' in home_html:
    errors.append('homepage: deep paper analysis must not be the main entry')

# P1 real-paper integrity: values must match the authors' table and remain author-reported.
paper_dir=ROOT/'examples'
paper_svg=[ROOT/'assets/examples'/name for name in ('roborender-method.svg','roborender-evidence.svg','roborender-method.en.svg','roborender-evidence.en.svg')]
for svg in paper_svg:
    if not svg.exists():
        errors.append(f'missing real-paper analysis SVG: {svg}')
        continue
    try:
        nodes=list(ET.parse(svg).iter())
        if sum(x.tag.split('}')[-1]=='text' for x in nodes)<12:
            errors.append(f'poorly editable real-case diagram: {svg.name}')
        if any(x.tag.split('}')[-1]=='image' for x in nodes):
            errors.append(f'real-case diagram contains embedded raster: {svg.name}')
    except ET.ParseError as exc:errors.append(f'{svg.name}: {exc}')
expected_rows=[
    ('mug',40,60,80),('bowl',30,20,80),('apple',10,20,60),('egg',0,30,50),
    ('open_fridge',0,0,70),('open_drawer',0,0,90),('pick_radio',0,30,70),
    ('place_marker',0,0,70)]
with (paper_dir/'roborender-results.csv').open(encoding='utf-8',newline='') as handle:
    observed=list(csv.DictReader(handle))
if len(observed)!=8:
    errors.append('real-paper result CSV: expected exactly 8 author-reported tasks')
else:
    for obs,expected in zip(observed,expected_rows):
        try:
            actual=(obs['task_id'],int(obs['simulation_success_pct']),int(obs['simulation_dr_success_pct']),int(obs['roborender_success_pct']))
        except (KeyError,ValueError) as exc:
            errors.append(f'real-paper CSV schema or values: {exc}')
            continue
        if actual!=expected:errors.append(f'real-paper CSV deviates from official table: {actual} vs {expected}')
        if obs.get('provenance')!='author-reported' or obs.get('independent_replication')!='no':
            errors.append('real-paper data must be explicitly labelled author-reported, not independently replicated')
    if sum(int(x['roborender_success_pct']) for x in observed)!=570:
        errors.append('real-paper: reported average must be 71.25%, rounded to 71%')
for name in ('examples/roborender.html','examples/roborender-provenance.md','css/real-case.css'):
    if not (ROOT/name).is_file():errors.append(f'missing source-traceable case file: {name}')
real_page=(ROOT/'examples/roborender.html').read_text(encoding='utf-8')
if real_page.count('<tr>')<9:errors.append('real-paper website: per-task data table incomplete')
if any(path not in real_page for path in ('roborender-provenance.md','roborender-results.csv','roborender-method.svg','roborender-evidence.svg')):
    errors.append('real-paper page: missing provenance or editables')
if 'independently reproduced' not in real_page or '非我们的独立复现' not in real_page:
    errors.append('real-paper page: missing clear bilingual reproduction boundary')
if 'examples/roborender.html' not in case_page:
    errors.append('real-paper case not linked from examples index')

# Curated Skills: popularity snapshots are dated and practice items link to public work.
popular=[e for e in entries if e.get('curation',{}).get('track')=='popular']
practice=[e for e in entries if e.get('curation',{}).get('track')=='practice']
if len(popular)!=4 or len(practice)!=2:
    errors.append('curation: expected four sourced popular items and two practiced workflows')
for e in popular:
    c=e['curation']
    if not re.fullmatch(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+',c.get('github_repo','')):
        errors.append(f"{e['id']}: invalid GitHub repo")
    if not isinstance(c.get('stars_snapshot'),int) or c['stars_snapshot']<0:
        errors.append(f"{e['id']}: missing Star snapshot")
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',c.get('stars_checked_on','')):
        errors.append(f"{e['id']}: missing Star checked date")
    if e['links']['source'] != 'https://github.com/'+c['github_repo']:
        errors.append(f"{e['id']}: Star target does not match original source")
for e in practice:
    c=e['curation']
    if not c.get('evidence'):errors.append(f"{e['id']}: missing practice evidence")
    for evidence in c.get('evidence',[]):
        if not (ROOT/evidence).is_file():errors.append(f"{e['id']}: missing evidence {evidence}")
# Gallery gate: new additions are original externally hosted images with explicit attribution.
new_visual_ids={'vggt-architecture','dreamdojo-overview','videomimic-real2sim','videomimic-approach','wonderzoom-teaser'}
if not new_visual_ids.issubset(set(ids)):
    errors.append('new curated visual references are missing')
for entry in entries:
    if entry['id'] not in new_visual_ids:continue
    if entry['kind']!='visual-reference' or entry.get('visual',{}).get('kind')!='external-reference-image':
        errors.append(f"{entry['id']}: visual original not represented accurately")
    if entry.get('curation',{}).get('source_verification')!='author-site-and-repository-path':
        errors.append(f"{entry['id']}: original source verification absent")
    identity=entry.get('figureIdentity',{})
    if identity.get('type')!='project-website-figure' or not identity.get('original_name'):
        errors.append(f"{entry['id']}: image identity not precise")
    if not entry.get('links',{}).get('officialFigure','').startswith('https://github.com/'):
        errors.append(f"{entry['id']}: original image link missing")
    if entry.get('rights',{}).get('reuse')!='reference-only':
        errors.append(f"{entry['id']}: third-party image incorrectly relicensed")
if any(entry['id']=='visualmimic-method' for entry in entries):
    errors.append('generic dense diagram must not pass strict design curation')

# Visual diversity: real teaser/results/ablation/site evidence; never relabel a site frame as a screenshot.
new_diverse={
 'teaser':['instruct-pix2pix-teaser','gridar-teaser'],
 'results':['ultraedit-qualitative','fastnerf-zoom-results'],
 'ablation':['specialist-diffusion-ablation','egoengine-ablation'],
 'project-site':['nerfies-project-site','hypernerf-project-site']
}
for visual_type,expected in new_diverse.items():
    for asset_id in expected:
        matched=next((v for v in entries if v['id']==asset_id),None)
        if not matched:
            errors.append(f'new Gallery asset missing: {asset_id}')
            continue
        if matched.get('curation',{}).get('visual_category')!=visual_type:
            errors.append(f'{asset_id}: visual category mismatch')
        if matched.get('rights',{}).get('reuse')!='reference-only':
            errors.append(f'{asset_id}: third-party artwork was incorrectly relicensed')
        identity=matched.get('figureIdentity',{})
        expected_identity='project-website-media' if visual_type=='project-site' else 'project-website-figure'
        if identity.get('type')!=expected_identity:
            errors.append(f'{asset_id}: website media and captured website screenshot are different')
        if matched.get('visual',{}).get('kind')!='external-reference-image':
            errors.append(f'{asset_id}: expected source-hosted image link, not a local copy')
        if not matched.get('links',{}).get('officialFigure','').startswith('https://'):
            errors.append(f'{asset_id}: original figure link missing')
        if not matched.get('caseStudy',{}).get('composition',{}).get('zh'):
            errors.append(f'{asset_id}: no design insight recorded')
if not all(f'data-task-query="{s}"' in home_html for s in ('teaser','qualitative-results','ablation','project-website')):
    errors.append('homepage lacks four visual-category discovery paths')

if 'function renderSkills()' not in (ROOT/'js/catalog.js').read_text(encoding='utf-8'):
    errors.append('homepage: curated skills must use the canonical catalog')

if errors:
    for e in errors:print('FAIL:',e)
    raise SystemExit(1)
print(f'PASS: {len(entries)} catalog entries, provenance, bilingual fields, source links, original SVG, page references and JS syntax')
