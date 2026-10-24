"""Rendered smoke test for the Chinese-first research asset website.

Uses inlined local resources and intercepts authored SVG requests: no public
network access required. Not proof that GitHub Pages deployment is healthy.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,re
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
    content_type='image/svg+xml' if path.suffix=='.svg' else 'application/octet-stream'
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
        page.route('https://ora.local/asset.html*',lambda route:route.fulfill(status=200,body=page_html('asset.html'),content_type='text/html'))
        page.set_content(page_html('index.html'),wait_until='load')
        page.locator('.ora-resource-card').first.wait_for()
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        assert page.locator('h1').inner_text().startswith('让已有的经验')
        assert page.locator('.ora-resource-card').count()==9
        assert page.locator('.ora-resource-card .ora-curated img').count()==6
        assert page.locator('.ora-resource-card .ora-curated img').evaluate_all(
            '(nodes)=>nodes.every(n=>n.complete&&n.naturalWidth>0)')
        page.locator('#catalog-more').click()
        assert page.locator('.ora-resource-card').count()==21
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

        page.goto('https://ora.local/asset.html?id=supermimic-site',wait_until='load')
        page.locator('.ora-lesson').first.wait_for()
        assert 'SuperMimic' in page.locator('h1').inner_text()
        assert page.locator('.ora-lesson').count()==3
        assert page.locator('.ora-case-study').count()==1
        assert page.locator('.ora-study-grid section').count()==2
        assert page.locator('.ora-detail-links a').count()>=2
        assert 'catalog/entries/supermimic-site.json' in page.locator('.ora-detail-links a').last.get_attribute('href')
        assert page.locator('.ora-detail-preview .ora-curated img').evaluate('(n)=>n.complete&&n.naturalWidth>0')
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('detail',label)
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
        print('PASS',label,'21 resources, filters, bilingual UI, detail, quality tool, mobile layout')
        page.close()
    browser.close()
