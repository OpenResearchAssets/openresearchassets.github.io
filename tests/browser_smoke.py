"""Local Chromium smoke test; no external requests required."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
httpd=ThreadingHTTPServer(("127.0.0.1",8765),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
Thread(target=httpd.serve_forever,daemon=True).start()
with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu'])
  for w,h,label in [(1440,900,'desktop'),(390,844,'mobile')]:
    page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
    issues=[]
    page.on('pageerror',lambda e: issues.append(str(e)))
    page.goto('http://127.0.0.1:8765/index.html',wait_until='load')
    assert page.locator('.reference-card').count()==8,(label,page.locator('.reference-card').count())
    page.locator('[data-filter="Research"]').click()
    assert page.locator('.reference-card').count()==3
    page.locator('[data-filter="All"]').click()
    page.locator('#reference-search').fill('RoboRender')
    assert page.locator('.reference-card').count()==1
    page.locator('#reference-search').fill('')
    assert page.locator('.reference-card').count()==8
    page.screenshot(path=str(ROOT.parent/f'OpenResearchAssets_{label}.png'),full_page=True)
    overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 2')
    assert not overflow, f'{label} has horizontal overflow'
    assert not issues,issues
    page.goto('http://127.0.0.1:8765/quality.html',wait_until='load')
    assert page.locator('.audit-question').count()==8
    page.locator('.audit-question input').nth(1).check()
    page.locator('#generate-report').click()
    assert page.locator('#audit-report').is_visible()
    assert '1 selected issue' in page.locator('#audit-report').inner_text()
    page.locator('#artifact-type').select_option('table')
    assert page.locator('.audit-question').count()==8
    page.locator('#artifact-type').select_option('paper')
    assert page.locator('.audit-question').count()==8
    page.screenshot(path=str(ROOT.parent/f'OpenResearchAssets_quality_{label}.png'),full_page=True)
    assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 2'),f'quality {label} overflow'
    print('PASS:',label,'reference search/filter, quality review, responsive overflow and browser JS errors')
    page.close()
  browser.close()
httpd.shutdown()
