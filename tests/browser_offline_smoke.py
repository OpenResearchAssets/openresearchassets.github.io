"""Browser QA without local HTTP. Requires Playwright and Chromium.
Replaces repo-owned links, scripts, styles and assets with inlined equivalents.
Does not verify the public CDN or HTTP deployment.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64
import re

ROOT=Path(__file__).resolve().parents[1]

def inline(name):
    html=(ROOT/name).read_text(encoding='utf-8')
    html=re.sub(r'<link rel="stylesheet" href="([^"]+)">',
                lambda m:'<style>'+(ROOT/m[1]).read_text(encoding='utf-8')+'</style>',html)
    html=re.sub(r'<script src="([^"]+)"></script>',
                lambda m:'<script>'+(ROOT/m[1]).read_text(encoding='utf-8')+'</script>',html)
    def img(m):
        path=ROOT/m[1]
        mime='image/svg+xml' if path.suffix=='.svg' else 'image/png'
        return 'src="data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')+'"'
    return re.sub(r'src="(assets/[^"]+)"',img,html)

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,
                               args=['--no-sandbox','--disable-gpu'])
    for width,height,name in ((1440,900,'desktop'),(390,844,'mobile')):
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(inline('index.html'),wait_until='load')
        assert page.locator('.reference-card').count()==8
        assert page.locator('img').evaluate_all('(nodes)=>nodes.every(n=>n.complete&&n.naturalWidth>0)')
        page.locator('[data-filter="Research"]').click()
        assert page.locator('.reference-card').count()==3
        page.locator('[data-filter="All"]').click()
        page.locator('#reference-search').fill('RoboRender')
        assert page.locator('.reference-card').count()==1
        if width<721:
            page.locator('.menu-toggle').click()
            assert page.locator('#site-nav').is_visible()
            page.keyboard.press('Escape')
            assert not page.locator('#site-nav').is_visible()
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
        page.set_content(inline('quality.html'),wait_until='load')
        assert page.locator('.audit-question').count()==8
        page.locator('.audit-question input').nth(1).check()
        page.locator('#generate-report').click()
        assert '1 selected issue' in page.locator('#audit-report').inner_text()
        page.locator('#artifact-type').select_option('table')
        assert page.locator('.audit-question').count()==8
        for subpage in ('principles.html','contribute.html'):
            page.set_content(inline(subpage),wait_until='load')
            if width<721:
                page.locator('.menu-toggle').click()
                assert page.locator('#site-nav').is_visible()
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
        assert not errors,errors
        print(f'PASS {name}: rendering, filter, review, navigation, no JS errors')
        page.close()
    browser.close()
