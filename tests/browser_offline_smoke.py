"""Rendered smoke test for the Chinese-first research asset website.

Uses inlined local resources and intercepts authored SVG requests: no public
network access required. Not proof that GitHub Pages deployment is healthy.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,re,json
from shutil import which
ROOT=Path(__file__).resolve().parents[1]

def page_html(name):
    path=ROOT/name
    html=path.read_text(encoding='utf-8')
    html=re.sub(r'<link(?=[^>]*rel="stylesheet")(?=[^>]*href="([^"]+)")[^>]*>',
                lambda m:'<style>'+(path.parent/m[1]).read_text(encoding='utf-8')+'</style>',html)
    html=re.sub(r'<script src="([^"]+)"></script>',
                lambda m:'<script>'+(path.parent/m[1]).read_text(encoding='utf-8')+'</script>',html)
    def img(m):
        image_path=path.parent/m[1]
        mime='image/svg+xml' if image_path.suffix=='.svg' else 'image/png'
        return 'src="data:'+mime+';base64,'+base64.b64encode(image_path.read_bytes()).decode()+'"'
    html=re.sub(r'src="((?:\.\./)?assets/[^"]+)"',img,html)
    catalog=(ROOT/'catalog/index.json').read_text(encoding='utf-8').replace('<','\\u003c')
    html=html.replace('</head>','<base href="https://ora.local/"><script type="application/json" id="ora-catalog-data">'+catalog+'</script></head>',1)
    return html

def local_asset(route):
    from urllib.parse import urlparse
    name=urlparse(route.request.url).path.lstrip('/')
    path=(ROOT/name).resolve()
    if ROOT not in path.parents or not path.is_file():
        route.abort()
        return
    content_type='image/svg+xml' if path.suffix=='.svg' else 'image/png' if path.suffix=='.png' else 'image/jpeg' if path.suffix in ('.jpg','.jpeg') else 'application/octet-stream'
    route.fulfill(status=200,body=path.read_bytes(),content_type=content_type)

with sync_playwright() as pw:
    opts={'headless':True,'args':['--no-sandbox','--disable-gpu']}
    local_chromium=which('chromium') or which('chromium-browser')
    if local_chromium:opts['executable_path']=local_chromium
    browser=pw.chromium.launch(**opts)
    for w,h,label in ((1440,900,'desktop'),(768,900,'tablet'),(390,844,'mobile'),(320,720,'small-mobile')):
        page=browser.new_page(viewport={'width':w,'height':h})
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.route('https://ora.local/assets/**',local_asset)
        page.route(re.compile(r'^https://(?:depth-anything-3\.github\.io|media\.luminis-sim\.com|tianxingchen\.github\.io|supermimic\.github\.io|raw\.githubusercontent\.com|opengraph\.githubassets\.com)/'),lambda route:route.abort())
        page.route('https://ora.local/asset.html*',lambda route:route.fulfill(status=200,body=page_html('asset.html'),content_type='text/html'))
        page.set_content(page_html('index.html'),wait_until='load')
        page.locator('.ora-resource-card').first.wait_for()
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        assert page.locator('h1').inner_text().startswith('收藏真正出色的图')
        assert [a.get_attribute('href') for a in page.locator('#site-nav a').all()]==['index.html','community.html','findings.html','contribute.html']
        assert page.locator('.nav-cta').first.get_attribute('href')=='contribute.html'
        assert page.locator('.ora-footer-links a').count()==5
        assert page.locator('.ora-main-path').count()==2
        assert page.locator('.ora-main-path').nth(0).get_attribute('href')=='#gallery'
        assert page.locator('.ora-main-path').nth(1).get_attribute('href')=='#skills'
        catalog_data=json.loads((ROOT/'catalog/index.json').read_text(encoding='utf-8'))
        popular_data=[e for e in catalog_data['entries'] if e.get('curation',{}).get('track')=='popular']
        practice_data=[e for e in catalog_data['entries'] if e.get('curation',{}).get('track')=='practice']
        assert page.locator('#popular-skills .ora-skill-card').count()==min(8,len(popular_data))
        assert page.locator('#practice-skills .ora-skill-card').count()==len(practice_data)
        assert page.locator('#popular-skills [data-star-repo]').count()==min(8,len(popular_data))
        assert page.locator('#skill-more').is_visible()==(len(popular_data)>8)
        assert f"{len(popular_data)+len(practice_data)} / " in page.locator('#skill-status').inner_text()
        # Domain, topic and capability type are independent, composable filters.
        page.locator('#skill-topic').select_option('document-parsing')
        expected_docs=sum('document-parsing' in e['topics'] for e in popular_data+practice_data)
        assert page.locator('#popular-skills .ora-skill-card').count()+page.locator('#practice-skills .ora-skill-card').count()==expected_docs
        page.locator('#skill-type').select_option('skill')
        expected_skills=sum('document-parsing' in e['topics'] and e['curation']['type']=='skill' for e in popular_data+practice_data)
        assert page.locator('#popular-skills .ora-skill-card').count()+page.locator('#practice-skills .ora-skill-card').count()==expected_skills
        page.locator('#skill-reset').click()
        assert page.locator('#popular-skills .ora-skill-card').count()==min(8,len(popular_data))
        if len(popular_data)>8:
            page.locator('#skill-more').click()
            assert page.locator('#popular-skills .ora-skill-card').count()==len(popular_data)
        # A concrete skill's stars must explicitly be attributed to its parent repository.
        individual=page.locator('#popular-skills [data-star-scope="parent-repository"]').first
        assert individual.count()==1 and ('母仓库' in individual.inner_text())
        assert '未经本站亲测' in page.locator('#popular-skills').inner_text()
        assert '公开实践证据' in page.locator('#practice-skills').inner_text()
        assert page.locator('.ora-rights-notice').count()==1
        assert '异议' in page.locator('.ora-rights-notice').inner_text()
        assert 'asset-removal.yml' in page.locator('.ora-rights-notice a').get_attribute('href')
        assert page.locator('.ora-resource-card').count()==9
        assert page.locator('.ora-featured-site').count()==2
        assert page.locator('.ora-featured-site').nth(0).locator('.ora-open-source').get_attribute('href')=='https://nerfies.github.io/'
        assert page.locator('.ora-featured-site').nth(1).locator('.ora-open-source').get_attribute('href')=='https://hypernerf.github.io/'
        assert page.locator('.ora-featured-site').nth(0).locator('.ora-featured-preview').get_attribute('href')=='https://nerfies.github.io/'
        assert page.locator('.ora-resource-card').first.locator('.ora-external img').count()==1
        assert 'depth-anything-3.github.io/assets/teaser.png' in page.locator('.ora-resource-card').first.locator('img').get_attribute('src')
        assert '真实来源视觉参考' in page.locator('#reference-status').inner_text()
        assert page.locator('.ora-resource-card .ora-verified img').count()==6
        page.wait_for_function("()=>[...document.querySelectorAll('.ora-resource-card .ora-verified img')].every(n=>n.complete&&n.naturalWidth>0)")
        assert page.locator('.ora-resource-card .ora-curated img').count()==0
        page.locator('#facet-topic').select_option('three-d-vision')
        assert page.locator('.ora-resource-card').count()>0
        assert all('three-d-vision' in e['topics'] for e in catalog_data['entries'] if e['id'] in
                   page.locator('.ora-resource-card').evaluate_all('(cards)=>cards.map(c=>new URL(c.querySelector(".ora-open-details").href).searchParams.get("id"))'))
        page.locator('#facet-reset').click()
        # Four discovery routes must correspond to authored figure functions, not only labels.
        page.locator('[data-task-query="ablation"]').click()
        assert page.locator('.ora-resource-card').count()>=2
        assert 'Specialist Diffusion' in page.locator('#reference-grid').inner_text()
        assert 'EgoEngine' in page.locator('#reference-grid').inner_text()
        page.locator('[data-task-query="qualitative-results"]').click()
        assert 'UltraEdit' in page.locator('#reference-grid').inner_text()
        assert 'Fast Learning Radiance Fields' in page.locator('#reference-grid').inner_text()
        page.locator('[data-task-query="project-website"]').click()
        assert 'Nerfies' in page.locator('#reference-grid').inner_text()
        assert 'HyperNeRF' in page.locator('#reference-grid').inner_text()
        page.locator('#facet-reset').click()
        page.locator('#catalog-more').click()
        assert page.locator('.ora-resource-card').count()==28
        page.locator('#facet-kind').select_option('website-reference')
        assert page.locator('.ora-resource-card').count()==5
        assert page.locator('.ora-resource-card').filter(has_text='Nerfies').locator('.ora-resource-visual').get_attribute('href')=='https://nerfies.github.io/'
        assert page.locator('.ora-resource-card').filter(has_text='HyperNeRF').locator('.ora-resource-content h3 a').get_attribute('href')=='https://hypernerf.github.io/'
        assert page.locator('.ora-resource-card').filter(has_text='Nerfies').locator('.ora-open-source').get_attribute('target')=='_blank'
        page.locator('#facet-kind').select_option('')
        page.locator('#reference-search').fill('RoboRender')
        assert page.locator('.ora-resource-card').count()==2
        page.locator('#facet-reset').click()
        assert page.locator('.ora-resource-card').count()==9
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        assert page.locator('h1').inner_text().startswith('Remarkable research figures')
        assert 'Beautiful research visuals' in page.locator('.ora-main-paths').inner_text()
        assert 'Visit official site' in page.locator('.ora-featured-site').first.inner_text()
        assert 'Popular open-source picks' in page.locator('#skills').inner_text()
        assert 'Rights holders may request removal' in page.locator('.ora-rights-notice').inner_text()
        assert page.locator('.ora-resource-card').count()==9
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        if w<=720:
            page.locator('.menu-toggle').click()
            assert page.locator('#site-nav').is_visible()
            page.keyboard.press('Escape')
            assert not page.locator('#site-nav').is_visible()
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('home',label,page.evaluate('document.documentElement.scrollWidth'))
        assert page.locator('.assets-grid .asset-card').count()==5
        assert page.locator('#assets').bounding_box()['y']<page.locator('#skills').bounding_box()['y']
        assert page.locator('.assets-grid .asset-card img').evaluate_all('(nodes)=>nodes.every(n=>n.complete&&n.naturalWidth>0)')
        assert page.locator('.showcase img').evaluate_all('(nodes)=>nodes.every(n=>n.complete&&n.naturalWidth>0)')
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(ROOT/'tests'/f'_local_home_{label}.png'),full_page=True)
        if label in ('desktop','mobile'):
            page.locator('#skills').screenshot(path=str(ROOT/'tests'/f'_local_skills_{label}.png'))

        # Full catalog coverage, not a single showcase page. Main-case screenshots
        # are kept for desktop and mobile human visual review.
        cases=('roborender-teaser','roborender-site','robodojo-teaser',
               'robodojo-site','supermimic-teaser','supermimic-site')
        samples=('depth-anything-3-visual','topconf-figure-gallery','teaser-story',
                 'quality-critic-skill','experiment-planning')
        entries=json.loads((ROOT/'catalog/index.json').read_text(encoding='utf-8'))['entries']
        for entry in entries:
            asset_id=entry['id']
            page.goto('https://ora.local/asset.html?id='+asset_id,wait_until='load')
            page.locator('.ora-detail-heading h1').wait_for()
            assert asset_id in page.locator('.ora-eyebrow').text_content(),(label,asset_id,'wrong id')
            assert page.locator('.ora-detail-preview .ora-preview').count()==1,(label,asset_id,'missing preview')
            assert page.locator('.ora-detail-links a').count()>=2,(label,asset_id,'source / JSON missing')
            assert 'catalog/entries/'+asset_id+'.json' in page.locator('.ora-detail-links a').last.get_attribute('href')
            assert page.locator('.ora-detail-sidebar').is_visible()
            assert page.locator('.ora-detail-rights').count()==1
            assert 'asset-removal.yml' in page.locator('.ora-detail-rights a').get_attribute('href')
            overflow=page.evaluate('''() => ({
                width: innerWidth, actual: document.documentElement.scrollWidth,
                offenders:[...document.querySelectorAll('body *')].map(el=>({
                  tag:el.tagName,cls:el.className,txt:(el.textContent||'').trim().slice(0,60),
                  right:Math.round(el.getBoundingClientRect().right),
                  width:Math.round(el.getBoundingClientRect().width)
                })).filter(e=>e.right>innerWidth+2).slice(0,12)
            })''')
            assert overflow['actual']<=w+2, (label,asset_id,'horizontal page overflow',overflow)
            assert page.locator('.ora-lesson').count()==(1 if entry.get('caseStudy') else 3),(
                label,asset_id,'repeated generic lessons')
            if asset_id in cases:
                expected='.ora-paper-fig' if asset_id.endswith('teaser') else '.ora-site-capture'
                assert page.locator('.ora-detail-preview '+expected+' img').count()==1,(label,asset_id,'wrong source identity')
                assert page.locator('.ora-case-study').count()==1,(label,asset_id,'missing editorial')
                assert page.locator('.ora-study-grid section').count()==2
                assert page.locator('.ora-case-check li').count()>=2
                assert page.locator('.ora-disclosure').is_visible()
                assert page.locator('.ora-detail-preview img').count()==1
            elif entry.get('caseStudy'):
                assert page.locator('.ora-case-study').count()==1
                assert page.locator('.ora-detail-preview .ora-external img').count()==1
                assert entry['rights']['reuse']=='reference-only'
            else:
                assert page.locator('.ora-case-study').count()==0
            visual=page.locator('.ora-detail-preview img')
            if visual.count() and entry.get('visual',{}).get('kind')!='external-reference-image':
                visual.scroll_into_view_if_needed()
                page.wait_for_function("()=>[...document.querySelectorAll('.ora-detail-preview img')].every(n=>n.complete&&n.naturalWidth>0)")
            elif visual.count():
                assert visual.first.get_attribute('src').startswith('https://')
            if asset_id=='roborender-teaser':
                assert 'CC BY 4.0' in page.locator('.ora-detail-sidebar').inner_text()
            if asset_id=='depth-anything-3-visual':
                assert page.locator('.ora-detail-preview .ora-external img').count()==1
            if entry['kind']=='resource-index':
                assert page.locator('.ora-detail-preview .ora-external img').count()==1
            if entry['kind']=='workflow':
                cls='.ora-skill-preview' if asset_id=='quality-critic-skill' else '.ora-workflow-preview'
                assert page.locator('.ora-detail-preview '+cls).count()==1,(label,asset_id,'wrong workflow type')
                assert page.locator('.ora-detail-preview .ora-cover-step').count()>=1
            if entry['kind']=='editable-template':
                assert page.locator('.ora-detail-preview .ora-template img').count()==1
                assert 'Original site asset' in page.locator('.ora-detail-sidebar').inner_text() if page.locator('html').get_attribute('lang')=='en' else '本站原创资产' in page.locator('.ora-detail-sidebar').inner_text()
            if asset_id in cases and label in ('desktop','mobile'):
                page.screenshot(path=str(ROOT/'tests'/f'_local_case_{asset_id}_{label}.png'),full_page=True)
            if asset_id in samples and label in ('desktop','mobile'):
                page.screenshot(path=str(ROOT/'tests'/f'_local_sample_{asset_id}_{label}.png'),full_page=True)
            if asset_id in cases and label in ('desktop','mobile'):
                zh=page.locator('.ora-case-intro p').inner_text()
                page.locator('.lang-toggle').click()
                assert page.locator('html').get_attribute('lang')=='en'
                assert page.locator('.ora-case-intro p').inner_text()!=zh,(label,asset_id,'translation missing')
                assert page.locator('.ora-lesson').count()==1
                page.locator('.lang-toggle').click()
                assert page.locator('html').get_attribute('lang')=='zh-CN'
            print('CHECK',label,asset_id)
        # Retain the familiar single-detail alias for compact CI logs.
        page.goto('https://ora.local/asset.html?id=supermimic-site',wait_until='load')
        page.locator('.ora-case-study').wait_for()
        page.screenshot(path=str(ROOT/'tests'/f'_local_detail_{label}.png'),full_page=True)

        page.set_content(page_html('quality.html'),wait_until='load')
        assert page.locator('.audit-question').count()==8
        page.locator('.audit-question input').nth(1).check()
        page.locator('#generate-report').click()
        assert '已标记 1 项问题' in page.locator('#audit-report').inner_text()
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        page.locator('#generate-report').click()
        assert '1 selected issues' in page.locator('#audit-report').inner_text()
        # Language persists between pages; explicitly switch back to Chinese for the next checks.
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        # Worked cases: real image loads, bilingual links, responsive layout.
        page.set_content(page_html('examples.html'),wait_until='load')
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        assert page.locator('.ora-example').count()==3
        assert page.locator('.ora-example-visual img').count()==3
        for image in page.locator('.ora-example-visual img').all():
            image.scroll_into_view_if_needed()
            page.wait_for_function('(el)=>el.complete&&el.naturalWidth>0',arg=image.element_handle())
        assert '教学' in page.locator('.ora-example-warning').inner_text()
        assert 'examples/evidence-register.csv' in page.content()
        assert 'examples/sample-project.html' in page.content()
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('examples',label)
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        assert 'One research question' in page.locator('.ora-example-hero h1').inner_text()
        assert page.locator('.ora-example-visual img').first.get_attribute('src').endswith('.en.svg')
        for image in page.locator('.ora-example-visual img').all():
            image.scroll_into_view_if_needed()
            page.wait_for_function('(el)=>el.complete&&el.naturalWidth>0',arg=image.element_handle())
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        if label in ('desktop','mobile'):
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(ROOT/'tests'/f'_local_examples_{label}.png'),full_page=True)
        page.set_content(page_html('examples/sample-project.html'),wait_until='load')
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        assert '结果：未采集' in page.locator('main').inner_text()
        assert page.locator('.diagram img.zh').is_visible()
        if label in ('desktop','mobile'):
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(ROOT/'tests'/f'_local_sample_site_zh_{label}.png'),full_page=True)
        page.locator('#toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        assert page.locator('.diagram img.en').is_visible()
        assert 'Results: not available' in page.locator('main').inner_text()
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('sample-project',label)
        if label in ('desktop','mobile'):
            page.screenshot(path=str(ROOT/'tests'/f'_local_sample_site_{label}.png'),full_page=True)

        # Real-paper editorial case: original cited figure, native editable diagrams,
        # transcribed author results, bilingual disclosure, and responsive layout.
        page.set_content(page_html('examples/roborender.html'),wait_until='load')
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        assert page.locator('.rc-table tbody tr').count()==8
        assert page.locator('.rc-table tfoot').inner_text().strip().endswith('71%')
        assert '非我们的独立复现' in page.locator('.rc-disclaimer').inner_text()
        assert page.locator('.rc-source-figure img').count()==1
        assert page.locator('.rc-figure img').count()==2
        for paper_image in page.locator('.rc-source-figure img, .rc-figure img').all():
            paper_image.scroll_into_view_if_needed()
            page.wait_for_function('(el)=>el.complete&&el.naturalWidth>0',arg=paper_image.element_handle())
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('real-paper',label)
        if label in ('desktop','mobile'):
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(ROOT/'tests'/f'_local_real_case_zh_{label}.png'),full_page=True)
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        assert 'from an open paper' in page.locator('.rc-hero h1').inner_text()
        assert page.locator('.rc-figure img').first.get_attribute('src').endswith('.en.svg')
        for im in page.locator('.rc-figure img').all():
            im.scroll_into_view_if_needed()
            page.wait_for_function('(el)=>el.complete&&el.naturalWidth>0',arg=im.element_handle())
        assert 'have not been independently reproduced' in page.locator('.rc-disclaimer').inner_text()
        assert page.locator('.rc-table tbody tr').count()==8
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('real-paper-en',label)
        if label in ('desktop','mobile'):
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(ROOT/'tests'/f'_local_real_case_{label}.png'),full_page=True)
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='zh-CN'

        for name in ('principles.html','contribute.html','for-agents/index.html'):
            page.set_content(page_html(name),wait_until='load')
            assert page.locator('html').get_attribute('lang')=='zh-CN'
            assert page.locator('#site-nav a').count()==4
            assert page.locator('.ora-footer-links a').count()==5
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),name
            if name=='contribute.html':
                assert page.locator('.ora-submit-cta').count()==1
                assert 'submit-asset.yml' in page.locator('.ora-submit-cta').get_attribute('href')
                assert page.locator('.ora-submit-guidelines-grid>div').count()==3
                assert 'catalog-correction.md' in page.locator('.ora-submit-secondary').inner_html()
                page.locator('.lang-toggle').click()
                assert page.locator('html').get_attribute('lang')=='en'
                assert 'Share something worth discovering' in page.locator('h1').inner_text()
                assert 'Original source' in page.locator('.ora-submit-guidelines-grid').inner_text()
                page.locator('.lang-toggle').click()
                assert page.locator('html').get_attribute('lang')=='zh-CN'
        # Public Community is separate from curated Gallery. Mock GitHub API without
        # pretending that there are live submissions or their real reaction counts.
        fake_issue=lambda number,title,kind,likes,created: {
            'number':number, 'title':'[投稿] '+title, 'state':'open','labels':[],
            'created_at':created, 'user':{'login':'mock-author-'+str(number)},
            'comments':2, 'reactions':{'+1':likes},
            'body':('### 资产类型 / Asset type\n'+kind+
                    '\n\n### 作品名称 / Asset title\n'+title+
                    '\n\n### 官方来源 / Original source URL\nhttps://example.org/source'+str(number)+
                    '\n\n### 为什么值得分享或推荐？/ Why is this asset worth sharing?\nConcrete visual and practical lessons.')
        }
        test_issues=[
            fake_issue(2,'Visual asset','高审美论文图 / Research figure',3,'2026-10-26T01:00:00Z'),
            fake_issue(1,'Popular skill','高热度 Skill / Popular GitHub Skill',21,'2026-10-25T01:00:00Z')
        ]
        page.route(re.compile(r'^https://api\.github\.com/repos/OpenResearchAssets/openresearchassets\.github\.io/issues\?'),
                   lambda route:route.fulfill(status=200,body=json.dumps(test_issues),content_type='application/json'))
        page.route('https://ora.local/catalog/index.json',
                   lambda route:route.fulfill(status=200,body=(ROOT/'catalog/index.json').read_text(encoding='utf-8'),content_type='application/json'))
        page.set_content(page_html('community.html'),wait_until='load')
        page.locator('.ora-community-entry').first.wait_for()
        assert page.locator('.ora-community-entry').count()==2
        assert page.locator('#site-nav a[href="index.html"]').count()==1
        assert '👍 3' in page.locator('.ora-community-grid').inner_text()
        assert '👍 21' in page.locator('.ora-community-grid').inner_text()
        page.locator('#community-sort').select_option('popular')
        assert 'Popular skill' in page.locator('.ora-community-entry').first.inner_text()
        page.locator('#community-kind').select_option('visual')
        assert page.locator('.ora-community-entry').count()==1
        assert 'Visual asset' in page.locator('.ora-community-entry').first.inner_text()
        page.locator('#community-kind').select_option('all')
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        assert 'Original link (unverified)' in page.locator('.ora-community-entry').first.inner_text()
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('community-en',label)
        if label in ('desktop','mobile'):
            page.screenshot(path=str(ROOT/'tests'/f'_local_community_{label}.png'),full_page=True)
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        # Findings: four distinct real-source concepts, mocked ONLY in offline tests.
        example_feeds={}
        for key,name,metric in [('papers','Hugging Face Papers','upvotes'),('github','GitHub Trending','stars gained this week'),
                                ('skills','GitHub Search','total stars'),('workflows','GitHub Search','total stars')]:
            example_feeds[key]={
                'source':name,'url':'https://example.org/source','status':'ok',
                'fetched_at':'2026-10-26T01:00:00Z','metric_note':'Synthetic CI data only',
                'items':[{'title':'CI fixture '+key+' '+str(i),'url':'https://example.org/'+key+'/'+str(i),
                          'detail':'Verified source text ' * 55,'summary_source':'paper abstract' if key=='papers' else 'repository README',
                          'title_zh':'测试论文中文标题' if key=='papers' and i==1 else '', 
                          'subtitle_zh':'这是一段根据原始摘要自动翻译的内容。' if key=='papers' and i==1 else '',
                          'subtitle':'Sourced project description for visual regression',
                          'metric':metric,'value':15000+i,'author':'Example'}
                         for i in range(1,7)]}
        example_snapshot={'schema_version':'1','generated_at':'2026-10-26T02:00:00Z','feeds':example_feeds}
        page.route('https://ora.local/data/findings.json',lambda route:
                   route.fulfill(status=200,body=json.dumps(example_snapshot),content_type='application/json'))
        page.set_content(page_html('findings.html'),wait_until='load')
        page.locator('.findings-feed').first.wait_for()
        assert page.locator('#site-nav a').count()==4
        assert page.locator('#site-nav a[href="findings.html"]').get_attribute('aria-current')=='page'
        if label=='mobile':
            filter_boxes=[node.bounding_box() for node in page.locator('.findings-filter').all()]
            assert all(box and box['x']>=0 and box['x']+box['width']<=w+2 for box in filter_boxes),(
                'mobile discovery filters should all be visible without horizontal swiping',filter_boxes)
        assert page.locator('.findings-feed').count()==4
        assert page.locator('.findings-item').count()==12,('overview must display at most three per category',label)
        assert page.locator('.findings-feed-more').count()==4
        assert 'CI fixture papers' in page.locator('.findings-feed').first.inner_text()
        assert page.locator('.lang-toggle').get_attribute('data-current-lang')=='zh'
        assert page.locator('.lang-toggle .ora-lang-option.is-active').inner_text()=='中文'
        assert '测试论文中文标题' in page.locator('.findings-item').first.inner_text()
        assert '这是一段根据原始摘要自动翻译的内容。' in page.locator('.findings-item').first.inner_text()
        assert 'Trending papers' not in page.locator('.findings-feed').first.locator('h3').inner_text()
        assert page.locator('.findings-original-compare').count()>=1
        page.locator('.findings-original-compare summary').first.click()
        assert 'CI fixture papers 1' in page.locator('.findings-original-compare').first.inner_text()
        assert '15,001' in page.locator('.findings-item-metric').first.inner_text()
        assert '社区票数' in page.locator('.findings-item-metric').first.inner_text()
        if label in ('desktop','mobile'):
            page.screenshot(path=str(ROOT/'tests'/f'_local_findings_overview_{label}.png'),full_page=True)
        # Click an overview affordance, not only a category tab: focused full-width reading.
        page.locator('[data-open-feed="papers"]').first.click()
        assert page.locator('.findings-feed').count()==1
        assert page.locator('.findings-item').count()==6
        assert page.locator('.findings-feed-focused').count()==1
        assert 'feed=papers' in page.url
        assert page.locator('.findings-focus-guide').count()==1
        assert page.locator('.findings-item-rank').last.inner_text()=='06'
        assert page.locator('.findings-entry-detail').count()>=1
        page.locator('.findings-entry-detail summary').first.click()
        assert 'Verified source text' in page.locator('.findings-entry-full').first.inner_text()
        assert 'HF upvotes' not in page.locator('.findings-feed').first.inner_text() or page.locator('.findings-item-metric').count()==6
        if label in ('desktop','mobile'):
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(ROOT/'tests'/f'_local_findings_focused_{label}.png'),full_page=True)
        page.locator('.findings-back').click()
        assert page.locator('.findings-feed').count()==4
        assert page.locator('.findings-item').count()==12
        assert 'feed=' not in page.url
        page.locator('[data-feed="skills"]').click()
        assert page.locator('.findings-feed').count()==1
        assert page.locator('.findings-item').count()==6
        assert 'CI fixture skills' in page.locator('.findings-feed').first.inner_text()
        assert '累计 Stars' in page.locator('.findings-item-metric').first.inner_text()
        page.locator('[data-feed="all"]').click()
        page.locator('#findings-search').fill('workflows')
        assert page.locator('.findings-item').count()==6,('search must include non-preview entries',label)
        page.locator('#findings-search').fill('')
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        assert 'Trend desk' in page.locator('h2').inner_text()
        assert page.locator('.lang-toggle').get_attribute('data-current-lang')=='en'
        assert page.locator('.lang-toggle .ora-lang-option.is-active').inner_text()=='EN'
        assert page.locator('.findings-feed').first.locator('h3').inner_text()=='Trending papers'
        assert 'CI fixture papers 1' in page.locator('.findings-item').first.inner_text()
        assert 'Sourced project description for visual regression' in page.locator('.findings-item').first.inner_text()
        assert '测试论文中文标题' not in page.locator('.findings-item').first.inner_text()
        assert '这是一段根据原始摘要自动翻译的内容。' not in page.locator('.findings-item').first.inner_text()
        assert 'HF upvotes' in page.locator('.findings-item-metric').first.inner_text()
        assert page.locator('html').get_attribute('lang')=='en'
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('findings-en',label)
        if label in ('desktop','mobile'):
            page.screenshot(path=str(ROOT/'tests'/f'_local_findings_{label}.png'),full_page=True)
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        assert page.locator('.lang-toggle').get_attribute('data-current-lang')=='zh'
        assert page.locator('.lang-toggle .ora-lang-option.is-active').inner_text()=='中文'
        assert '测试论文中文标题' in page.locator('.findings-item').first.inner_text()
        # Real public snapshot: long GitHub repo names and paper abstracts must
        # not overflow on desktop, tablet or mobile. Not synthetic rankings.
        real_snapshot=(ROOT/'data/findings.json').read_text(encoding='utf-8')
        page.route('https://ora.local/data/findings.json',lambda route:
                   route.fulfill(status=200,body=real_snapshot,content_type='application/json'))
        page.set_content(page_html('findings.html'),wait_until='load')
        page.locator('.findings-feed').first.wait_for()
        assert page.locator('.findings-feed').count()==4
        assert page.locator('.findings-item').count()<=12
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        real_data=json.loads(real_snapshot)
        for i,key in enumerate(('papers','github','skills','workflows')):
            row=real_data['feeds'][key]['items'][0]
            if row.get('subtitle_zh') or row.get('detail_zh'):
                expected=(row.get('subtitle_zh') or row.get('detail_zh'))[:35]
                assert expected[:15] in page.locator('.findings-feed').nth(i).locator('.findings-item').first.inner_text(),(
                    'top Findings should display Chinese translated body, not original English',key,label)
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('findings-real-overview',label)
        if label in ('desktop','mobile'):
            page.screenshot(path=str(ROOT/'tests'/f'_local_findings_real_{label}.png'),full_page=True)
        page.locator('[data-feed="github"]').click()
        assert page.locator('.findings-feed-focused').count()==1
        assert page.locator('.findings-item').count()==min(8,len(json.loads(real_snapshot)['feeds']['github']['items']))
        if len(json.loads(real_snapshot)['feeds']['github']['items'])>8:
            assert page.locator('.findings-load-more').count()==1
            page.locator('.findings-load-more').click()
            assert page.locator('.findings-item').count()==len(json.loads(real_snapshot)['feeds']['github']['items'])
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('findings-real-focused',label)
        if label in ('desktop','mobile'):
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(ROOT/'tests'/f'_local_findings_real_focused_{label}.png'),full_page=True)
        assert not errors,(label,errors)
        print('PASS',label,'curated visual Gallery, verified Stars, public practice evidence, bilingual and responsive UI')
        page.close()
    browser.close()
