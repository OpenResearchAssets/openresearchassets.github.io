"""Local HTTP Chromium smoke test; no external website requests required."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
httpd=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
port=httpd.server_port
Thread(target=httpd.serve_forever,daemon=True).start()

try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu'])
        for w,h,label in [(1440,900,'desktop'),(390,844,'mobile')]:
            page=browser.new_page(viewport={'width':w,'height':h})
            issues=[]
            page.on('pageerror',lambda e:issues.append(str(e)))
            page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
            page.locator('.ora-resource-card').first.wait_for()
            assert page.locator('.ora-resource-card').count()==9
            page.locator('#catalog-more').click()
            assert page.locator('.ora-resource-card').count()==19
            page.locator('#facet-kind').select_option('visual-reference')
            assert page.locator('.ora-resource-card').count()==3
            page.locator('#facet-reset').click()
            page.locator('#reference-search').fill('RoboRender')
            assert page.locator('.ora-resource-card').count()==2
            page.locator('#facet-reset').click()
            page.locator('.lang-toggle').click()
            assert page.locator('html').get_attribute('lang')=='en'
            page.locator('.lang-toggle').click()
            assert page.locator('html').get_attribute('lang')=='zh-CN'
            if w<720:
                page.locator('.menu-toggle').click()
                assert page.locator('#site-nav').is_visible()
                page.keyboard.press('Escape')
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2')
            page.screenshot(path=str(ROOT.parent/f'OpenResearchAssets_{label}.png'),full_page=True)
            page.goto(f'http://127.0.0.1:{port}/asset.html?id=roborender-teaser')
            page.locator('.ora-lesson').first.wait_for()
            assert page.locator('.ora-lesson').count()==3
            assert 'RoboRender' in page.locator('h1').inner_text()
            page.goto(f'http://127.0.0.1:{port}/quality.html')
            assert page.locator('.audit-question').count()==8
            page.locator('.audit-question input').nth(1).check()
            page.locator('#generate-report').click()
            assert '已标记 1 项问题' in page.locator('#audit-report').inner_text()
            assert not issues,issues
            print('PASS',label,'search/facets, bilingual mode, detail, quality checklist, overflow')
            page.close()
        browser.close()
finally:
    httpd.shutdown()
