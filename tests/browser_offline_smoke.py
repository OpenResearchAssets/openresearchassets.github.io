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
        assert page.locator('h1').inner_text().startswith('让已有的经验')
        assert page.locator('.ora-start-path').count()==3, (label, 'missing first-use paths')
        assert page.locator('.ora-start-path').nth(0).get_attribute('href')=='asset.html?id=experiment-planning'
        assert page.locator('.ora-start-path').nth(1).get_attribute('href')=='for-agents/'
        assert page.locator('.ora-start-path').nth(2).get_attribute('href')=='contribute.html'
        assert '用一份科研工作流' in page.locator('.ora-start').inner_text()
        assert page.locator('.ora-rights-notice').count()==1
        assert '异议' in page.locator('.ora-rights-notice').inner_text()
        assert 'asset-removal.yml' in page.locator('.ora-rights-notice a').get_attribute('href')
        assert page.locator('.ora-resource-card').count()==9
        assert page.locator('.ora-resource-card').first.locator('.ora-external img').count()==1
        assert 'depth-anything-3.github.io/assets/teaser.png' in page.locator('.ora-resource-card').first.locator('img').get_attribute('src')
        assert '真实来源视觉参考' in page.locator('#reference-status').inner_text()
        assert page.locator('.ora-resource-card .ora-verified img').count()==6
        page.wait_for_function("()=>[...document.querySelectorAll('.ora-resource-card .ora-verified img')].every(n=>n.complete&&n.naturalWidth>0)")
        assert page.locator('.ora-resource-card .ora-curated img').count()==0
        page.locator('#catalog-more').click()
        assert page.locator('.ora-resource-card').count()==22
        page.locator('#facet-kind').select_option('website-reference')
        assert page.locator('.ora-resource-card').count()==3
        page.locator('#facet-kind').select_option('')
        page.locator('#reference-search').fill('RoboRender')
        assert page.locator('.ora-resource-card').count()==2
        page.locator('#facet-reset').click()
        assert page.locator('.ora-resource-card').count()==9
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        assert page.locator('h1').inner_text().startswith('Make knowledge useful')
        assert 'Explore a research workflow' in page.locator('.ora-start').inner_text()
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
        assert page.locator('.assets-grid .asset-card img').evaluate_all('(nodes)=>nodes.every(n=>n.complete&&n.naturalWidth>0)')
        assert page.locator('.showcase img').evaluate_all('(nodes)=>nodes.every(n=>n.complete&&n.naturalWidth>0)')
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(ROOT/'tests'/f'_local_home_{label}.png'),full_page=True)

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
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),(
                label,asset_id,'horizontal page overflow')
            assert page.locator('.ora-lesson').count()==(1 if asset_id in cases else 3),(
                label,asset_id,'repeated generic lessons')
            if asset_id in cases:
                expected='.ora-paper-fig' if asset_id.endswith('teaser') else '.ora-site-capture'
                assert page.locator('.ora-detail-preview '+expected+' img').count()==1,(label,asset_id,'wrong source identity')
                assert page.locator('.ora-case-study').count()==1,(label,asset_id,'missing editorial')
                assert page.locator('.ora-study-grid section').count()==2
                assert page.locator('.ora-case-check li').count()>=2
                assert page.locator('.ora-disclosure').is_visible()
                assert page.locator('.ora-detail-preview img').count()==1
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
        for name in ('principles.html','contribute.html','for-agents/index.html'):
            page.set_content(page_html(name),wait_until='load')
            assert page.locator('html').get_attribute('lang')=='zh-CN'
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),name
        assert not errors,(label,errors)
        print('PASS',label,'22 detail pages, 6 curated case studies, 4 asset kinds, bilingual and responsive UI')
        page.close()
    browser.close()
