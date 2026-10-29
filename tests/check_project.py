#!/usr/bin/env python3
"""Static catalog and source checks. This does not certify a rendered site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re
import json
from datetime import date, timedelta
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
pages=['index.html','asset.html','for-agents/index.html','quality.html','principles.html','contribute.html','community.html','findings.html','examples.html','examples/sample-project.html','examples/roborender.html']
for h in pages:
    p=Links();p.feed((ROOT/h).read_text(encoding='utf-8'))
    for uri in p.refs:
        u=urlparse(uri)
        if u.scheme in ('http','https','mailto') or uri.startswith('#') or uri.startswith('data:'):continue
        target=(ROOT/h).parent/u.path
        if not target.exists():errors.append(f'{h}: missing {uri}')
# Browser i18n strings are stored in HTML attributes; malformed quoting can silently
# truncate JSON and break language switching only on a particular route.
class I18NAttributes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.invalid=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('data-i18n-zh','data-i18n-en','data-i18n-attrs'):
                try:
                    json.loads(value)
                except (ValueError,TypeError) as exc:
                    self.invalid.append(f'{tag} {key}: {exc}')
for page in pages:
    parser=I18NAttributes()
    parser.feed((ROOT/page).read_text(encoding='utf-8'))
    for error in parser.invalid:
        errors.append(f'{page}: malformed i18n attribute: {error}')
for file in [*ROOT.glob('assets/templates/*.svg'), ROOT/'assets/mark.svg']:
    try:
        tree=ET.parse(file);nodes=list(tree.iter())
        if len(nodes)<5:errors.append(f'{file}: not meaningfully editable')
        if any(n.tag.split('}')[-1]=='image' for n in nodes):errors.append(f'{file}: unexpected embedded raster image')
    except ET.ParseError as e:errors.append(f'{file}: {e}')
for name in ('teaser-story','method-flow','results-panel'):
    if not (ROOT/'assets/previews'/f'{name}.png').exists():errors.append(f'missing preview: {name}')
for js in ('js/catalog.js','js/i18n.js','js/navigation.js','js/quality.js','js/community-page.js','js/community.js'):
    run=subprocess.run(['node','--check',str(ROOT/js)],capture_output=True,text=True)
    if run.returncode:errors.append(f'{js}: JS syntax: {run.stderr}')
sync=subprocess.run(['python3',str(ROOT/'tools/sync_catalog.py'),'--check'],capture_output=True,text=True)
if sync.returncode:errors.append('derived catalog out of date: '+sync.stdout+sync.stderr)
catalog=json.loads((ROOT/'catalog/index.json').read_text(encoding='utf-8'))
if catalog.get('schema_version')!='1.0.0':errors.append('catalog: unsupported schema version')
entries=catalog.get('entries',[])
if len(entries)<39:errors.append('catalog: unexpected loss of curated assets')
core_ids={'roborender-teaser','roborender-site','robodojo-teaser','robodojo-site','supermimic-teaser','supermimic-site'}
for e in entries:
    if e.get('id') in core_ids and e.get('visual',{}).get('kind') not in ('verified-paper-figure','verified-site-screenshot'):
        errors.append(f"{e.get('id')}: case hero is not the correct paper figure or homepage")
ids=[e.get('id') for e in entries]
if any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', str(eid)) for eid in ids):errors.append('catalog: unsafe ID; expected kebab-case')
if len(ids)!=len(set(ids)):errors.append('catalog: duplicate IDs')
# Workflow diagrams are authored editable SVGs, not upstream figures or screenshots.
for item in entries:
    diagram=item.get('workflowDiagram')
    if not diagram:continue
    for language in ('zh','en'):
        rel=diagram.get('src',{}).get(language,'')
        if not re.fullmatch(r'assets/editorials/[a-z0-9.-]+[.]svg',rel):
            errors.append(f"{item['id']}: invalid {language} workflow diagram path")
            continue
        file=ROOT/rel
        if not file.is_file():
            errors.append(f"{item['id']}: missing {language} workflow SVG")
            continue
        try:
            root=ET.parse(file).getroot()
            nodes=list(root.iter())
            if len(nodes)<35 or any(n.tag.split('}')[-1]=='image' for n in nodes):
                errors.append(f"{item['id']}: workflow SVG must contain editable vector elements")
        except ET.ParseError as err:
            errors.append(f"{item['id']}: invalid workflow SVG: {err}")
        if not diagram.get('alt',{}).get(language) or not diagram.get('caption',{}).get(language):
            errors.append(f"{item['id']}: missing {language} diagram alt or caption")

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
                'supermimic.github.io','raw.githubusercontent.com','instruct-pix2pix.timothybrooks.com','opengraph.githubassets.com',
                'figures.semanticscholar.org','moveit.ai'
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
    if not e.get('topics') or not set(e['topics']).issubset(catalog['facets']['topics']):
        errors.append(f'{where}: invalid controlled topics')
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
if contribute_html.count('class="ora-submit-cta"')!=1 or contribute_html.count('class="ora-submit-guidelines-grid"')!=1:
    errors.append('contribution page: expected one submission action and one concise guideline grid')
for page_name,html in [('index.html',home_html),('contribute.html',contribute_html)]:
    if any(text not in html for text in ('data-i18n-zh=', 'data-i18n-en=')):
        errors.append(f'{page_name}: missing bilingual first-use text')
if 'id="gallery"' not in home_html or 'id="skills"' not in home_html:
    errors.append('homepage: gallery or skills route missing')
for required_id in ('facet-topic','skill-search','skill-domain','skill-topic','skill-type','skill-topic-chips','skill-more'):
    if f'id="{required_id}"' not in home_html:
        errors.append(f'missing catalog topic / capability discovery control: {required_id}')
if 'id="popular-skills"' not in home_html or 'id="practice-skills"' not in home_html:
    errors.append('homepage: popular and practice tracks not separate')
if 'href="for-agents/"' not in home_html or 'href="contribute.html"' not in home_html:
    errors.append('homepage: missing agent or contribution entry')
if 'Skills / Workflows' not in contribute_html or 'id="ora-submit-title"' not in contribute_html:
    errors.append('contribution page: must accept research skills via single public submission flow')
correction = ROOT/'.github/ISSUE_TEMPLATE/catalog-correction.md'
if not correction.is_file():
    errors.append('missing general asset correction issue template')
elif 'catalog-correction.md' not in contribute_html:
    errors.append('contribution page: no direct correction entry')
template=(ROOT/'.github/ISSUE_TEMPLATE/asset-request.md').read_text(encoding='utf-8')
if not all(word in template for word in ('工作流','工具','来源','授权')):
    errors.append('asset proposal template: still too narrow for research assets')

# Shared information architecture: 3 destinations across all entry pages.
nav_pages=['index.html','community.html','findings.html','contribute.html','asset.html',
           'quality.html','principles.html','for-agents/index.html','examples.html']
nav_js=(ROOT/'js/navigation.js').read_text(encoding='utf-8')
if 'const links=[' not in nav_js or 'renderNavigation()' not in nav_js or 'renderFooter()' not in nav_js:
    errors.append('shared navigation/footer script is not authoritative')
for page_name in nav_pages:
    markup=(ROOT/page_name).read_text(encoding='utf-8')
    if markup.count('id="site-nav"')!=1 or 'data-page=' not in markup:
        errors.append(f'{page_name}: expected one declarative navigation mount')
    if '>精选 Curated</a>' in markup or '>社区 Community</a>' in markup:
        errors.append(f'{page_name}: legacy per-page nav markup remains')
if home_html.index('id="assets"')>home_html.index('id="skills"'):
    errors.append('homepage: Gallery editable templates should precede Skills')
if 'id="philosophy"' in home_html or 'id="join"' in home_html:
    errors.append('homepage: secondary tools/contribution marketing sections should not dominate Curated')
if 'ora-community-principle' in (ROOT/'community.html').read_text(encoding='utf-8'):
    errors.append('Community: duplicate curatorial explainer still occupies the feed')
if 'catalog-correction.md' not in contribute_html:
    errors.append('Contribute: correction link lost')

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

# Actionable dossiers are source-inspected, not evidence of executing the original Skill.
reviewed=[e for e in entries if e.get('execution',{}).get('scope')=='source-metadata-reviewed-not-executed']
if len(reviewed)<13:errors.append('expected at least 13 source-reviewed individual Skill dossiers')
for e in reviewed:
    ex=e['execution']
    if e.get('curation',{}).get('star_scope')!='parent-repository':
        errors.append(f"{e['id']}: inaccurate single Skill star attribution")
    if not e.get('links',{}).get('source','').endswith('/SKILL.md'):
        errors.append(f"{e['id']}: source must link actual SKILL.md")
    if not re.fullmatch(r'[a-f0-9]{40}',ex.get('source_file_sha','')):
        errors.append(f"{e['id']}: missing verified file blob SHA")
    for field in ('inputs','outputs','requirements','steps','checks'):
        if not all(ex.get(field,{}).get(lang) for lang in ('zh','en')):
            errors.append(f"{e['id']}: missing bilingual {field}")
# Homepage is an editorial task-diverse preview, not a duplicate-star leaderboard.
showcase=[e for e in entries if e.get('curation',{}).get('homepage_order') is not None]
if len(showcase)!=8 or sorted(x['curation']['homepage_order'] for x in showcase)!=list(range(1,9)):
    errors.append('skill homepage: expected exactly eight distinct curated preview positions')
if len({e['id'] for e in showcase})!=8 or not all(e.get('curation',{}).get('track')=='popular' for e in showcase):
    errors.append('skill homepage: invalid editorial selections')
# Curated Skills: popularity snapshots are dated and practice items link to public work.
popular=[e for e in entries if e.get('curation',{}).get('track')=='popular']
practice=[e for e in entries if e.get('curation',{}).get('track')=='practice']
if len(popular)<4 or len(practice)<2:
    errors.append('curation: popular and practice tracks unexpectedly regressed')
for e in popular:
    c=e['curation']
    if not re.fullmatch(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+',c.get('github_repo','')):
        errors.append(f"{e['id']}: invalid GitHub repo")
    if not isinstance(c.get('stars_snapshot'),int) or c['stars_snapshot']<0:
        errors.append(f"{e['id']}: missing Star snapshot")
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',c.get('stars_checked_on','')):
        errors.append(f"{e['id']}: missing Star checked date")
    if not e['links']['source'].startswith('https://github.com/'+c['github_repo']):
        errors.append(f"{e['id']}: Star target does not match original source")
    if e['links']['source'] != 'https://github.com/'+c['github_repo'] and c.get('star_scope')!='parent-repository':
        errors.append(f"{e['id']}: specific skill must label stars as parent-repository scope")
if not any(e.get('id')=='skill-source-intake' for e in practice):
    errors.append('Missing published and audited skill source intake workflow')
if not any(e.get('id')=='catalog-skill-trials' for e in practice):
    errors.append('Missing real executed catalog Skill trials in practice notes')
for trial_id in ('kdense-scientific-visualization','openai-jupyter-notebook'):
    target=next((e for e in entries if e['id']==trial_id),None)
    if not target or not target.get('trial',{}).get('run_url','').startswith('https://github.com/OpenResearchAssets/openresearchassets.github.io/actions/runs/'):
        errors.append(f'{trial_id}: missing original public CI trial evidence')
    elif target['trial'].get('native_agent_skill_invocation') is not False:
        errors.append(f'{trial_id}: false native Agent Skill claim')
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

# Curatorial rejection and direct original access.
if 'gridar-teaser' in ids:errors.append('GridAR rejected by editorial review but remains in catalog')
if (ROOT/'catalog/entries/gridar-teaser.json').exists():
    errors.append('Rejected GridAR record must not be indexed or retained as a candidate')
if 'id="featured-project-sites"' not in home_html:
    errors.append('Homepage lacks directly accessible original interactive project sites')
site_js=(ROOT/'js/catalog.js').read_text(encoding='utf-8')
if 'function renderFeaturedSites()' not in site_js or 'ora-open-source' not in site_js:
    errors.append('Gallery cards lack first-class source-site navigation')

# Visual diversity: real teaser/results/ablation/site evidence; never relabel a site frame as a screenshot.
new_diverse={
 'teaser':['instruct-pix2pix-teaser'],
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

# Community: verify authenticated GitHub reactions use stable per-asset terms.
community_cfg=ROOT/'config/community.json'
community_js_path=ROOT/'js/community.js'
asset_html=(ROOT/'asset.html').read_text(encoding='utf-8')
if not community_cfg.is_file() or not community_js_path.is_file():
    errors.append('Missing configured giscus community files')
else:
    community=json.loads(community_cfg.read_text(encoding='utf-8'))
    community_js=community_js_path.read_text(encoding='utf-8')
    if community.get('enabled') is True:
        if community.get('repo')!='OpenResearchAssets/openresearchassets.github.io':
            errors.append('Giscus repo is not the curated public repository')
        if not re.fullmatch(r'R_[A-Za-z0-9_-]+',community.get('repo_id','')):
            errors.append('Invalid GitHub repository node ID for giscus')
        if community.get('category')!='Assets' or not re.fullmatch(r'DIC_[A-Za-z0-9_-]+',community.get('category_id','')):
            errors.append('Invalid Assets discussion category ID for giscus')
        if "mapping:'specific'" not in community_js or "term:'ora-asset:'+id" not in community_js:
            errors.append('Giscus must use stable per-asset discussion mapping, not pathname')
        if 'id="ora-community"' not in asset_html or 'src="js/community.js"' not in asset_html:
            errors.append('Asset page missing community script or mounting section')
        if 'window.ORA_COMMUNITY?.mount(e.id)' not in site_js:
            errors.append('Asset detail does not mount per-entry giscus')
    else:
        errors.append('Giscus configured but unexpectedly disabled')
if 'template=submit-asset.yml' not in home_html or not (ROOT/'.github/ISSUE_TEMPLATE/submit-asset.yml').is_file():
    errors.append('Public submission entry is missing')

community_html=(ROOT/'community.html').read_text(encoding='utf-8')
community_js=(ROOT/'js/community-page.js').read_text(encoding='utf-8')
if not all(x in community_html for x in ('id="community-grid"', 'id="community-sort"', 'id="community-kind"', 'js/community-page.js')):
    errors.append('Community page lacks live feed and working filter controls')
if not all(x in community_js for x in ('api.github.com/repos/OpenResearchAssets/openresearchassets.github.io/issues','reactions',"'[投稿]'")):
    errors.append('Community must read real form submissions and GitHub reactions')
if not all(x in home_html for x in ('href="community.html"','href="#gallery"')):
    errors.append('Curated homepage must link prominently to Community and Gallery')
if 'template=submit-asset.yml' not in contribute_html:
    errors.append('Contribute page must link the public Issue Form')
# Findings is the third content destination, fed by provenance-bearing snapshots.
findings_html=(ROOT/'findings.html').read_text(encoding='utf-8')
findings_js=(ROOT/'js/findings.js').read_text(encoding='utf-8')
if not all(value in findings_html for value in ('data-page="findings"','id="findings-feeds"','js/findings.js','findings.css')):
    errors.append('Findings: public discovery page missing source-based feed mount or styles')
if not all(value in nav_js for value in ("key:'curated'", "key:'community'", "key:'findings'", "key:'contribute'")):
    errors.append('Shared navigation: expected Curated, Community, Findings, and Contribute action')
if 'data/findings.json' not in findings_js:
    errors.append('Findings must load the documented static provenance snapshot')

# Catalog Git history is evidence of indexing, not of a public Issue submission.
for entry in entries:
    history=entry.get('catalogHistory',{})
    ident=entry.get('sourceIdentity',{})
    # Validate new and historical records without freezing the acceptable dates to the
    # initial October intake. Git history, not this field alone, is the provenance.
    recorded = history.get('first_recorded_on', '')
    try:
        indexed_on = date.fromisoformat(recorded)
        valid_index_date = (
            recorded == indexed_on.isoformat()
            and date(2026, 10, 24) <= indexed_on <= date.today() + timedelta(days=1)
        )
    except (TypeError, ValueError):
        valid_index_date = False
    if not valid_index_date:
        errors.append(f"{entry['id']}: unverified first-indexed date")
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}',history.get('committed_by','')):
        errors.append(f"{entry['id']}: missing Git commit account")
    if not re.fullmatch(r'https://github[.]com/OpenResearchAssets/openresearchassets[.]github[.]io/commit/[a-f0-9]{40}',history.get('commit_url','')):
        errors.append(f"{entry['id']}: missing first-index commit evidence")
    if ident.get('origin') not in ('project-original','github-source','external-site'):
        errors.append(f"{entry['id']}: missing source identity")
    if ident.get('origin')=='github-source' and not ident.get('repository_url','').startswith('https://github.com/'):
        errors.append(f"{entry['id']}: untraceable original repository")
    if entry.get('kind') in ('visual-reference','website-reference') and (not entry.get('caseStudy') or not entry.get('figureIdentity')):
        errors.append(f"{entry['id']}: gallery case study or image identity missing")

if errors:
    for e in errors:print('FAIL:',e)
    raise SystemExit(1)
print(f'PASS: {len(entries)} catalog entries, provenance, bilingual fields, source links, original SVG, page references and JS syntax')
