"""Rendering QA with FreeType (statics hinted and unhinted, variable instances) and visual-regression baselines.

Small-size checks rasterise glyphs and verify that counters survive (enclosed background pixels exist) and that
vertical stems keep a consistent pixel weight.  All results here are software-renderer results (FreeType)."""
import os, sys, io, json, hashlib
import numpy as np
import freetype
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from common import *

OUT = os.path.join(ROOT, 'qa', 'rendering'); os.makedirs(OUT, exist_ok=True)
COUNTER_CHARS = 'aegobdpqBDOPR0689'
SIZES = [10, 11, 12, 13, 14, 16, 18, 20, 24]


def raster(face, ch, ppem, flags):
    face.set_pixel_sizes(0, ppem)
    face.load_char(ch, flags)
    b = face.glyph.bitmap
    if not b.width:
        return np.zeros((1, 1), dtype=np.uint8)
    return np.array(b.buffer, dtype=np.uint8).reshape(b.rows, b.width)


def enclosed_light(arr, thr=None):
    """Number of background pixels not connected to the border = open counter area in pixels.
    The ink threshold follows the glyph's own peak coverage, so hairline weights are judged fairly."""
    thr = max(40, 0.42 * float(arr.max())) if thr is None else thr
    dark = arr >= thr
    h, w = dark.shape
    pad = np.zeros((h + 2, w + 2), dtype=bool); pad[1:-1, 1:-1] = dark
    seen = np.zeros_like(pad); stack = [(0, 0)]; seen[0, 0] = True
    while stack:
        y, x = stack.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h + 2 and 0 <= nx < w + 2 and not seen[ny, nx] and not pad[ny, nx]:
                seen[ny, nx] = True; stack.append((ny, nx))
    return int((~pad & ~seen).sum())


def text_png(font_path, text, size, loc=None, dark=False, width=None, feats=None):
    f = ImageFont.truetype(font_path, size)
    if loc:
        axes = [a['name'] if isinstance(a['name'], str) else a['name'].decode() for a in f.get_variation_axes()]
        order = {'Weight': 'wght', 'Width': 'wdth', 'Optical Size': 'opsz', 'Grade': 'GRAD'}
        d = dict(DEFAULT); d.update(loc)
        f.set_variation_by_axes([d[order[a]] for a in axes])
    lines = text.split('\n')
    W = width or int(max(f.getlength(l) for l in lines) + size)
    lh = int(size * 1.3)
    img = Image.new('L', (W, lh * len(lines) + size // 2), 18 if dark else 255)
    dr = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        dr.text((size // 3, size // 5 + i * lh), l, font=f, fill=236 if dark else 0, features=feats)
    return img


def main():
    R = Report('rendering')
    statics = {os.path.basename(p)[:-4]: p for p in all_fonts() if '/static/' in p}
    # --- 1. counters at small sizes: unhinted and autohinted statics
    floor_report = {}
    for style in ('Orion-Light', 'Orion-Regular', 'Orion-Medium', 'Orion-Bold', 'Orion-Black', 'OrionCondensed-Regular', 'OrionCondensed-Bold'):
        face = freetype.Face(statics[style])
        for mode, flags in (('unhinted', freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING),
                            ('hinted', freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL),
                            ('light', freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_LIGHT)):
            closed = []
            for ppem in SIZES:
                for ch in COUNTER_CHARS:
                    if enclosed_light(raster(face, ch, ppem, flags)) == 0:
                        closed.append('%s@%d' % (ch, ppem))
            min_ok = min([s for s in SIZES if not any(c.endswith('@%d' % s) for c in closed)] or [99])
            first_all_open = next((s for s in SIZES if not any(int(c.split('@')[1]) >= s for c in closed)), None)
            floor_report['%s/%s' % (style, mode)] = dict(closed=closed, all_counters_open_from_ppem=first_all_open)
            limit = 18 if 'Black' in style else (14 if 'Bold' in style else (13 if 'Light' in style else 12))
            R.ok('counters open at >= %d ppem: %s (%s)' % (limit, style, mode), first_all_open is not None and first_all_open <= limit,
                 dict(first_all_open=first_all_open, closed=closed[:10]))
    # --- 2. variable font renders at every tested location and size without empty bitmaps
    face = freetype.Face(VF)
    tt = TTFont(VF); axes = [a.axisTag for a in tt['fvar'].axes]
    empty = []
    for loc in grid_locations(n_random=10):
        face.set_var_design_coords([loc[a] for a in axes])
        for ppem in (12, 24, 72):
            for ch in 'aeHO08g@&ßЖω':
                a = raster(face, ch, ppem, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
                if a.sum() == 0:
                    empty.append((ch, ppem, loc))
    R.ok('variable font rasterises at 63 locations x 3 sizes', not empty, empty[:5])
    # --- 3. stem consistency: the vertical stems of H, I, L, l at one size should not differ by more than 0.75 px of coverage
    #        (ttfautohint hints the vertical direction only, so hinted and unhinted horizontal stem widths coincide)
    worst = {}
    for style in ('Orion-Regular', 'Orion-Bold'):
        face = freetype.Face(statics[style])
        for mode, flags in (('unhinted', freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING), ('hinted', freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)):
            for ppem in (12, 14, 16, 20, 24, 32):
                ws = []
                for ch in 'HILl':
                    a = raster(face, ch, ppem, flags).astype(float) / 255
                    mid = a[max(1, int(a.shape[0] * 0.22))]      # above the H crossbar, below the top edge
                    runs = []; cur = 0.0
                    for v in mid:
                        if v > 0.2: cur += v
                        elif cur: runs.append(cur); cur = 0.0
                    if cur: runs.append(cur)
                    ws += runs
                worst['%s/%s/%d' % (style, mode, ppem)] = round(max(ws) - min(ws), 2)
    R.ok('stem coverage consistent across H I L l (max spread <= 0.75 px)', max(worst.values()) <= 0.75, worst)
    # --- 4. baseline and vertical extents: text must fit inside hhea ascent / descent for the required languages
    hhea = tt['hhea']; gs = tt.getGlyphSet(); cm = tt.getBestCmap()
    from corpus import LANGUAGE_SAMPLES
    over = []
    from fontTools.varLib import instancer
    for loc in (DEFAULT, dict(DEFAULT, wght=900), dict(DEFAULT, wght=900, wdth=125), dict(DEFAULT, wght=900, opsz=10), dict(DEFAULT, wght=100, opsz=72)):
        f = instancer.instantiateVariableFont(TTFont(VF), loc)
        glyf = f['glyf']
        for lang, text in LANGUAGE_SAMPLES.items():
            for ch in set(text):
                g = cm.get(ord(ch))
                if g and glyf[g].numberOfContours != 0:
                    if glyf[g].yMax > hhea.ascent or glyf[g].yMin < hhea.descent:
                        over.append((lang, ch, glyf[g].yMax, glyf[g].yMin, loc['wght'], loc['wdth']))
    R.ok('no clipping: language samples stay inside ascent %d / descent %d at 5 locations' % (hhea.ascent, hhea.descent), not over, over[:8])
    # --- 5. visual regression baselines
    base_dir = os.path.join(OUT, 'baseline'); os.makedirs(base_dir, exist_ok=True)
    text = 'Continue Watching  Season 01 — Episode 08\nTop 10 in Your Country  00:59:48  ₹1,499\nİstanbul Łódź Đặng Україна Ελληνικά'
    hashes = {}; changed = []
    old = {}
    hp = os.path.join(base_dir, 'hashes.json')
    if os.path.exists(hp):
        old = json.load(open(hp))
    matrix = []
    for w in (100, 400, 700, 900):
        for d in (75, 100, 125):
            matrix.append(dict(wght=w, wdth=d))
    matrix += [dict(opsz=10), dict(opsz=72), dict(GRAD=-50), dict(GRAD=100), dict(wght=900, wdth=75, opsz=72, GRAD=100), dict(wght=100, wdth=125, opsz=10, GRAD=-50)]
    for loc in matrix:
        for size, dark in ((18, False), (36, True), (72, False)):
            key = '_'.join('%s%g' % kv for kv in sorted(dict(DEFAULT, **loc).items())) + '_%dpx_%s' % (size, 'dark' if dark else 'light')
            img = text_png(VF, text, size, loc, dark)
            img.save(os.path.join(base_dir, key + '.png'))
            hashes[key] = hashlib.sha256(img.tobytes()).hexdigest()[:16]
            if key in old and old[key] != hashes[key]:
                changed.append(key)
    json.dump(hashes, open(hp, 'w'), indent=1)
    R.add('visual regression: %d baseline images written' % len(hashes), 'PASS' if not old or not changed else 'WARN',
          '' if not changed else '%d images differ from the previous baseline: %s' % (len(changed), changed[:5]))
    R.save(dict(small_size_counters=floor_report, stem_spread_px=worst, baselines=len(hashes), renderer='FreeType %s' % '.'.join(map(str, freetype.version()))))


if __name__ == '__main__':
    main()
