"""Fast single-location TTF build + proof rendering used during design iteration."""
from __future__ import annotations
import sys, os
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.pointPen import PointToSegmentPen
from .geom import G, WARN
from .params import Params
from . import parts


def draw_points(contours, ppen):
    for c in contours:
        ppen.beginPath()
        for s in c:
            if s[0] == 'l':
                ppen.addPoint(s[1], 'line')
            else:
                ppen.addPoint(s[1]); ppen.addPoint(s[2]); ppen.addPoint(s[3], 'curve', smooth=False)
        ppen.endPath()


def make(P, name):
    g = G(P, name)
    parts.REG[name][0](g)
    return g


def quick_ttf(P, path, names=None, glyphs=None):
    from .glyphset import build_master, decomposed_contours, cmap_for
    glyphs = glyphs or build_master(P)
    order = ['.notdef'] + [n for n in glyphs if n != '.notdef']
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap_for(glyphs))
    tt = {}; metrics = {}
    for n in order:
        pen = TTGlyphPen(None)
        if n in glyphs:
            draw_points(decomposed_contours(glyphs, n), PointToSegmentPen(Cu2QuPen(pen, 1.0, reverse_direction=True)))
            metrics[n] = int(round(glyphs[n].w))
        else:
            metrics[n] = 500
        tt[n] = pen.glyph()
    fb.setupGlyf(tt)
    fb.setupHorizontalMetrics({n: (w, tt[n].xMin if tt[n].numberOfContours else 0) for n, w in metrics.items()})
    fb.setupHorizontalHeader(ascent=980, descent=-250)
    fb.setupNameTable({'familyName': 'OrionQuick', 'styleName': 'Regular'})
    fb.setupOS2(sTypoAscender=980, sTypoDescender=-250, usWinAscent=1100, usWinDescent=300)
    fb.setupPost()
    fb.save(path)
    return glyphs


def sheet(lines, locs, out, size=64, pad=24, names=None, bg=255, fg=0, width=None):
    """Render lines of text for each location into one PNG (FreeType via Pillow)."""
    from PIL import Image, ImageDraw, ImageFont
    rows = []
    import tempfile; tmp = os.path.join(tempfile.gettempdir(), 'orionquick')
    os.makedirs(tmp, exist_ok=True)
    for i, loc in enumerate(locs):
        P = Params(**loc)
        path = '%s/q%d.ttf' % (tmp, i)
        quick_ttf(P, path, names)
        f = ImageFont.truetype(path, size)
        for ln in lines:
            rows.append((f, ln, loc))
    lh = int(size * 1.32)
    W = width or 2000
    img = Image.new('L', (W, pad * 2 + lh * len(rows)), bg)
    d = ImageDraw.Draw(img)
    for r, (f, ln, loc) in enumerate(rows):
        d.text((pad, pad + r * lh), ln, font=f, fill=fg)
    img.save(out)
    if WARN:
        print('WARN', sorted(set(WARN))[:20]); WARN.clear()
    return out
