# -*- coding: utf-8 -*-
"""Shared helpers for the Orion specimens. Every specimen is an HTML page that loads the built variable font
(fonts/variable/Orion-VF.woff2) and is rasterised by headless Chromium — nothing is drawn from the generator directly."""
import os, html
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.dirname(HERE)
ROOT = os.path.dirname(SPEC)
HTML_DIR = os.path.join(SPEC, 'html')
VF = os.path.join(ROOT, 'fonts', 'variable', 'Orion-VF.woff2')

BASE_CSS = """
@font-face { font-family: 'Orion'; src: url('../../fonts/variable/Orion-VF.woff2') format('woff2'); font-weight: 100 900; font-stretch: 75% 125%; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { background: #0B0D12; }
body { font-family: 'Orion', sans-serif; font-optical-sizing: none; font-kerning: normal; -webkit-font-smoothing: antialiased;
       color: #F2F2F2; background: #0B0D12; font-variation-settings: 'wght' 400, 'wdth' 100, 'opsz' 14, 'GRAD' 0; }
body.light { color: #14161A; background: #FFFFFF; }
.tag { font-variation-settings: 'wght' 600, 'wdth' 100, 'opsz' 14, 'GRAD' 0; font-size: 15px; letter-spacing: 0.14em; text-transform: uppercase; color: #8E95A3; }
.light .tag { color: #636A76; }
.note { font-size: 16px; line-height: 24px; color: #8E95A3; font-variation-settings: 'wght' 400, 'wdth' 100, 'opsz' 14, 'GRAD' 0; }
.light .note { color: #636A76; }
.foot { position: absolute; left: 96px; right: 96px; bottom: 40px; display: flex; justify-content: space-between; font-size: 15px; color: #6B7280;
        font-variation-settings: 'wght' 500, 'wdth' 100, 'opsz' 12, 'GRAD' 0; letter-spacing: 0.04em; }
"""


def fv(wght=400, wdth=100, opsz=14, grad=0):
    return "font-variation-settings:'wght' %g,'wdth' %g,'opsz' %g,'GRAD' %g" % (wght, wdth, min(72, max(10, opsz)), grad)


def tok(p, extra=''):
    """inline style for a preset dict from orion-type-presets.json"""
    feat = "font-feature-settings:'tnum' 1;" if 'tnum' in p.get('features', '') else ''
    return "font-size:%gpx;line-height:%gpx;letter-spacing:%gem;%s;%s%s" % (
        p['fontSize'], p['lineHeight'], p['letterSpacing'], fv(p['wght'], p['wdth'], p['opsz'], p['GRAD']), feat, extra)


def esc(s):
    return html.escape(s, quote=False)


def page(title, body, css='', cls='', width=1920, height=1080):
    return ("<!DOCTYPE html>\n<html lang='en'><head><meta charset='utf-8'><title>Orion — %s</title>\n<style>%s\n"
            "body { width: %dpx; %s position: relative; overflow: hidden; }\n%s</style></head>\n<body class='%s'>\n%s\n</body></html>\n" %
            (esc(title), BASE_CSS, width, ('height: %dpx;' % height) if height else 'min-height: 400px;', css, cls, body))


def fmt(s, args):
    """Fill %s placeholders in a CSS string that also contains literal percent signs."""
    parts = s.split('%s')
    assert len(parts) == len(args) + 1, (len(parts) - 1, len(args))
    out = [parts[0]]
    for a, p in zip(args, parts[1:]):
        out += [str(a), p]
    return ''.join(out)
