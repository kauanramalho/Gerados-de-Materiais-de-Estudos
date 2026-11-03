"""Exercise native anchor clicks in the self-contained HTML without content JavaScript."""
import json
from pathlib import Path
import shutil
import time
from urllib.parse import unquote, urlparse


def check_html_clicks(html_path, plan):
    from playwright.sync_api import sync_playwright, Error
    failures, clicks = [], 0
    with sync_playwright() as pw:
        executable = shutil.which('chromium') or shutil.which('google-chrome') or pw.chromium.executable_path
        if not Path(executable).is_file():
            raise ValueError('Chromium ausente para testar cliques')
        browser = pw.chromium.launch(executable_path=executable, headless=True, args=['--no-sandbox'])
        try:
            page = browser.new_page(java_script_enabled=False, viewport={'width': 1280, 'height': 900})
            page.set_default_timeout(5000)
            html = Path(html_path).read_text(encoding='utf-8')
            # Inline styles avoid asynchronous style onload handlers: content JS is disabled.
            styles = '<style>html{scroll-behavior:auto!important;}*{animation:none!important;transition:none!important;}</style>'
            html = html.replace('</head>', styles + '</head>', 1) if '</head>' in html else styles + html
            origin = 'https://atelie.invalid/material.html'
            page.route('**/*', lambda route: route.fulfill(status=200, content_type='text/html; charset=utf-8', body=html)
                       if route.request.url.split('#')[0] == origin else route.abort())
            page.goto(origin, wait_until='load', timeout=15000)
            for edge in plan['links']:
                anchor = page.locator('[id=' + json.dumps(edge['source'], ensure_ascii=False) + ']')
                parts = ['.toc-number', '.toc-label', '.toc-page'] if edge['role'] == 'toc' else [None]
                for selector in parts:
                    element = anchor.locator(selector) if selector else anchor
                    try:
                        element.scroll_into_view_if_needed(timeout=10000)
                        count = element.evaluate('(e)=>Array.from(e.getClientRects()).filter(r=>r.width>0&&r.height>0).length')
                        if not count:
                            failures.append(f'Sem área visível: {edge["source"]}')
                        for index in range(count):
                            element.scroll_into_view_if_needed(timeout=10000)
                            rects = element.evaluate('(e)=>Array.from(e.getClientRects()).filter(r=>r.width>0&&r.height>0).map(r=>({x:r.x,y:r.y,w:r.width,h:r.height}))')
                            rect = rects[index]
                            page.mouse.click(rect['x'] + rect['w']/2, rect['y'] + rect['h']/2)
                            clicks += 1
                            target = page.locator('[id=' + json.dumps(edge['target'], ensure_ascii=False) + ']')
                            arrived = False
                            deadline = time.monotonic() + 5
                            while time.monotonic() < deadline:
                                actual = unquote(urlparse(page.url).fragment)
                                box = target.bounding_box(timeout=2000)
                                if actual == edge['target'] and box and -2 <= box['y'] < 900:
                                    arrived = True
                                    break
                                page.wait_for_timeout(20)
                            if not arrived:
                                failures.append(f'Clique não levou ao destino visível: {edge["source"]} → {edge["target"]}')
                    except Error as error:
                        failures.append(f'Elemento não clicável/localizável: {edge["source"]}: {str(error).splitlines()[0]}')
                    if failures:
                        break
                if failures:
                    break
            return {'passed': not failures, 'clicks': clicks, 'links': len(plan['links']),
                    'errors': failures, 'chromium': browser.version}
        finally:
            browser.close()
