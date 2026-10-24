"""Rendered smoke test for the Chinese-first bilingual static website.

Uses inlined repo resources when local network navigation is blocked.
Do not infer public CDN availability from this local test.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,re

ROOT=Path(__file__).resolve().parents[1]
def page_html(name):
    html=(ROOT/name).read_text(encoding='utf-8')
    html=re.sub(r'<link(?=[^>]*rel="stylesheet")(?=[^>]*href="([^"]+)")[^>]*>',lambda m:'<style>'+(ROOT/m[1]).read_text(encoding='utf-8')+'</style>',html)
    html=re.sub(r'<script src="([^"]+)"></script>',lambda m:'<script>'+(ROOT/m[1]).read_text(encoding='utf-8')+'</script>',html)
    def img(m):
        path=ROOT/m[1];mime='image/svg+xml' if path.suffix=='.svg' else 'image/png'
        return 'src="data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()+'"'
    return re.sub(r'src="(assets/[^"]+)"',img,html)

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu'])
    for w,h,label in ((1440,900,'desktop'),(768,900,'tablet'),(390,844,'mobile'),(320,720,'small-mobile')):
        page=browser.new_page(viewport={'width':w,'height':h});errs=[]
        page.on('pageerror',lambda error:errs.append(str(error)))
        page.set_content(page_html('index.html'),wait_until='load')
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        assert page.locator('h1').inner_text().startswith('让研究成果')
        assert page.locator('.reference-card').count()==8
        assert page.locator('img').evaluate_all('(nodes)=>nodes.every(n=>n.complete&&n.naturalWidth>0)')
        page.locator('[data-filter="Research"]').click()
        assert page.locator('.reference-card').count()==3
        page.locator('[data-filter="All"]').click()
        page.locator('#reference-search').fill('RoboRender')
        assert page.locator('.reference-card').count()==1
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        assert page.locator('h1').inner_text().startswith('Make your research')
        assert page.locator('.reference-card').count()==1
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='zh-CN'
        page.locator('#reference-search').fill('')
        if w<=720:
            page.locator('.menu-toggle').click();assert page.locator('#site-nav').is_visible()
            page.keyboard.press('Escape');assert not page.locator('#site-nav').is_visible()
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2'),('home',label,page.evaluate('document.documentElement.scrollWidth'))
        page.screenshot(path=str(ROOT/'tests'/f'_local_home_{label}.png'),full_page=False)
        page.set_content(page_html('quality.html'),wait_until='load')
        assert page.locator('.audit-question').count()==8
        page.locator('.audit-question input').nth(1).check()
        page.locator('#generate-report').click()
        assert '已标记 1 项问题' in page.locator('#audit-report').inner_text()
        page.locator('.lang-toggle').click()
        assert page.locator('html').get_attribute('lang')=='en'
        page.locator('.audit-question').count()==8
        # preserve the selected checkbox and regenerate the report in English
        assert page.locator('input[type=checkbox]:checked').count()==1
        page.locator('#generate-report').click()
        assert '1 selected issues' in page.locator('#audit-report').inner_text()
        page.locator('#artifact-type').select_option('table')
        assert page.locator('.audit-question').count()==8
        for filename in ('principles.html','contribute.html'):
            page.set_content(page_html(filename),wait_until='load')
            assert page.locator('html').get_attribute('lang')=='zh-CN'
            if w<=720:
                page.locator('.menu-toggle').click();assert page.locator('#site-nav').is_visible()
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),filename
        assert not errs,(label,errs)
        print('PASS',label,'bilingual navigation, filters, self-review, layout and JS')
        page.close()
    browser.close()
