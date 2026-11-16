#!/usr/bin/env python3
"""Build every Orion specimen: writes specimens/html/*.html and rasterises each page with headless Chromium (Playwright).

    python3 specimens/src/build_specimens.py [name-filter]

The pages load ../../fonts/variable/Orion-VF.woff2, so the PNGs show the shipped binary, shaped by HarfBuzz and
rasterised by Skia/FreeType inside Chromium (software rendering; not a photograph of a TV)."""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pages_sheets, pages_axes, pages_ui
from playwright.async_api import async_playwright

PAGES = pages_sheets.PAGES + pages_axes.PAGES + pages_ui.PAGES
flt = sys.argv[1] if len(sys.argv) > 1 else ''


async def main():
    os.makedirs(HTML_DIR, exist_ok=True)
    async with async_playwright() as pw:
        kw = {}
        for exe in ('/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'):
            if os.path.exists(exe):
                kw['executable_path'] = exe; break
        br = await pw.chromium.launch(args=['--no-sandbox', '--font-render-hinting=none', '--allow-file-access-from-files'], **kw)
        for rel, fn, scale in PAGES:
            if flt and flt not in rel:
                continue
            html_text = fn()
            name = rel.split('/')[-1]
            hp = os.path.join(HTML_DIR, name + '.html'); open(hp, 'w', encoding='utf-8').write(html_text)
            out = os.path.join(SPEC, rel + '.png'); os.makedirs(os.path.dirname(out), exist_ok=True)
            w = 1440 if 'mobile-ui' in rel else 1920
            ctx = await br.new_context(viewport={'width': w, 'height': 940 if 'mobile-ui' in rel else 1080}, device_scale_factor=scale)
            pg = await ctx.new_page()
            await pg.goto('file://' + hp)
            await pg.evaluate('document.fonts.ready')
            ok = await pg.evaluate("document.fonts.check(\"700 40px Orion\")")
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=out, full_page=True)
            await ctx.close()
            print('%-48s font loaded: %s' % (rel + '.png', ok))
        await br.close()

asyncio.run(main())
