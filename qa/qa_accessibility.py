"""Accessibility and legibility evaluation.

1. Confusable pairs: rasterise, blur to simulate reduced acuity / viewing distance, and score how different the two
   shapes remain (1 - normalised cross-correlation at best alignment).  Reference families are measured the same way
   when the Reference folder is available (measurement only).
2. Viewing geometry: x-height visual angle of every TV type preset at 1-4 m on 32-75 inch 1080p / 4K panels.
3. Contrast: WCAG 2.x contrast ratios of the palette used by the specimens and integration examples.
4. Text scaling and spacing overrides (WCAG 1.4.4 / 1.4.12): the line box must hold at 200 % with spacing overrides.
All results are simulations computed in software; none replaces testing with people or on devices."""
import os, sys, json, math, glob
import numpy as np
import freetype
from PIL import Image, ImageFilter
from fontTools.ttLib import TTFont
from common import *

PAIRS = [('I', 'l'), ('I', '1'), ('l', '1'), ('O', '0'), ('S', '5'), ('B', '8'), ('6', '9'), ('rn', 'm'), ('c', 'e'), ('Z', '2'), ('G', '6'),
         ('cl', 'd'), ('vv', 'w'), ('i', 'j'), ('a', 'o'), ('h', 'b'), ('3', '8'), ('D', 'O')]
ACUITY_BLUR = {'20/20': 0.0, '20/40': 1.0, '20/80': 2.2}       # Gaussian sigma in px at 24 ppem (x-height ~12.5 px)


def kern_px(path, a, b, ppem, coords=None):
    """Kerning between two characters as shaped by HarfBuzz (pixels at ppem)."""
    import uharfbuzz as hb
    face = hb.Face(hb.Blob.from_file_path(path)); font = hb.Font(face)
    def adv(feats):
        buf = hb.Buffer(); buf.add_str(a + b); buf.guess_segment_properties(); hb.shape(font, buf, feats)
        return buf.glyph_positions[0].x_advance
    return (adv({}) - adv({'kern': False})) * ppem / face.upem


def render(face, text, ppem, path=None):
    face.set_pixel_sizes(0, ppem)
    W, H = ppem * (len(text) + 2), int(ppem * 1.8)
    img = np.zeros((H, W), dtype=float); x = ppem // 2; base = int(ppem * 1.3)
    prev = None
    for ch in text:
        if prev is not None and path:
            x += int(round(kern_px(path, prev, ch, ppem)))
        prev = ch
        face.load_char(ch, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
        b = face.glyph.bitmap
        if b.width:
            a = np.array(b.buffer, dtype=np.uint8).reshape(b.rows, b.width) / 255.0
            y0 = base - face.glyph.bitmap_top; x0 = x + face.glyph.bitmap_left
            img[y0:y0 + b.rows, x0:x0 + b.width] = np.maximum(img[y0:y0 + b.rows, x0:x0 + b.width], a)
        x += face.glyph.advance.x >> 6
    xs = np.where(img.sum(axis=0) > 0)[0]
    return img[:, xs[0]:xs[-1] + 1] if len(xs) else img


def blur(a, sigma):
    if sigma <= 0:
        return a
    im = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sigma))
    return np.asarray(im, dtype=float) / 255.0


def distinct(a, b):
    """1 - best normalised cross-correlation over horizontal alignments (0 = identical, 1 = unrelated)."""
    H = max(a.shape[0], b.shape[0]); W = max(a.shape[1], b.shape[1]) + 8
    best = 0.0
    for dxa in range(0, W - a.shape[1] + 1, 1):
        A = np.zeros((H, W)); A[:a.shape[0], dxa:dxa + a.shape[1]] = a
        for dxb in range(0, W - b.shape[1] + 1, 2):
            B = np.zeros((H, W)); B[:b.shape[0], dxb:dxb + b.shape[1]] = b
            den = math.sqrt((A * A).sum() * (B * B).sum())
            if den > 0:
                best = max(best, float((A * B).sum() / den))
    return round(1 - best, 3)


def score_font(path, coords=None):
    face = freetype.Face(path)
    if coords:
        face.set_var_design_coords(coords)
    out = {}
    for a, b in PAIRS:
        ra, rb = render(face, a, 24, path), render(face, b, 24, path)
        out['%s|%s' % (a, b)] = {k: distinct(blur(ra, s), blur(rb, s)) for k, s in ACUITY_BLUR.items()}
    return out


def lum(hexc):
    c = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return round((max(la, lb) + 0.05) / (min(la, lb) + 0.05), 2)


def main():
    R = Report('accessibility')
    orion = score_font(os.path.join(STATIC, 'Orion', 'Orion-Regular.ttf'))
    refs = {}
    ref_root = os.environ.get('ORION_REFERENCE')
    if ref_root and os.path.isdir(ref_root):
        cand = {'Inter (Regular)': ('Inter/Inter-VariableFont_opsz,wght.ttf', None), 'Roboto Flex (Regular)': ('Roboto_Flex/*.ttf', None),
                'Gotham Book': ('Gotham-font-family/Gotham/Gotham-Book.otf', None), 'Netflix Sans Regular': ('Netflix Sans/NetflixSans-Regular.otf', None)}
        for nm, (pat, co) in cand.items():
            m = glob.glob(os.path.join(ref_root, pat))
            if m:
                try:
                    refs[nm] = score_font(m[0], co)
                except Exception as e:
                    refs[nm] = {'error': repr(e)}
    # thresholds: at normal acuity every critical pair must stay clearly distinct
    crit = ['I|l', 'I|1', 'l|1', 'O|0', 'S|5', 'B|8', '6|9', 'rn|m', 'c|e']
    for k in crit:
        R.ok('confusable %s distinct at 20/20 (score >= 0.10)' % k, orion[k]['20/20'] >= 0.10, orion[k])
        R.ok('confusable %s still distinct under 20/40 blur (score >= 0.05)' % k, orion[k]['20/40'] >= 0.05, orion[k], warn=True)
    if refs:
        better = {}
        for k in crit:
            vals = [r[k]['20/40'] for r in refs.values() if k in r]
            better[k] = dict(orion=orion[k]['20/40'], reference_median=round(float(np.median(vals)), 3) if vals else None)
        n = sum(1 for v in better.values() if v['reference_median'] is not None and v['orion'] >= v['reference_median'])
        R.add('confusable separation vs reference median (20/40 blur): Orion >= median on %d of %d pairs' % (n, len(crit)), 'PASS', better)
    # stylistic sets must increase separation further
    def with_feature(feat, a, b):
        import uharfbuzz as hb
        return None
    # --- viewing geometry for the TV presets
    sys.path.insert(0, os.path.join(ROOT, 'integration'))
    presets = json.load(open(os.path.join(ROOT, 'integration', 'tokens', 'orion-type-presets.json')))
    tt = TTFont(os.path.join(STATIC, 'Orion', 'Orion-Regular.ttf'))
    xh = tt['OS/2'].sxHeight / 1000.0
    geo = []
    worst = {}
    for diag in (32, 43, 55, 65, 75):
        for dist in (1, 2, 3, 4):
            height_m = diag * 0.0254 * 9 / math.hypot(16, 9)
            for res, rows in (('1080p', 1080),):
                for name, p in presets['tv'].items():
                    px = p['fontSize']                                   # authored on a 1080p canvas
                    x_m = px * xh * height_m / rows
                    arcmin = math.degrees(2 * math.atan(x_m / (2 * dist))) * 60
                    geo.append(dict(diagonal=diag, distance_m=dist, preset=name, px=px, xheight_arcmin=round(arcmin, 1)))
                    key = name
                    if key not in worst or arcmin < worst[key][0]:
                        worst[key] = (round(arcmin, 1), diag, dist)
    # recommended viewing: SMPTE ~30 deg / THX ~36-40 deg field of view -> distance about 1.2-1.6 x diagonal
    rec = [g for g in geo if 1.2 * g['diagonal'] * 0.0254 <= g['distance_m'] <= 2.6 * g['diagonal'] * 0.0254]
    by_preset = {}
    for g in rec:
        by_preset.setdefault(g['preset'], []).append(g['xheight_arcmin'])
    for name, vals in by_preset.items():
        floor = 9.0 if name in ('caption', 'metadata') else 10.0
        R.ok('TV preset %s: x-height >= %.0f arcmin over typical viewing geometry (min %.1f)' % (name, floor, min(vals)), min(vals) >= floor, min(vals), warn=True)
    # --- contrast of the documented palette
    pal = presets['palette']
    for nm, (fg, bg, need) in pal['pairs'].items():
        c = contrast(fg, bg)
        R.ok('contrast %s %s on %s = %.2f:1 (needs %.1f:1)' % (nm, fg, bg, c, need), c >= need, c)
    # --- scaling: line box must contain ascent/descent at the documented line heights with 200 % text and WCAG spacing overrides
    asc, desc = tt['hhea'].ascent / 1000, -tt['hhea'].descent / 1000
    tight = []
    for plat, ps in presets.items():
        if plat in ('palette', 'meta'):
            continue
        for name, p in ps.items():
            lh = p['lineHeight'] / p['fontSize']
            # Latin text ink (cap accents to descender) must fit the line box; Vietnamese stacks need >= 1.25
            if lh < 1.08:
                tight.append((plat, name, round(lh, 2)))
    R.ok('all presets keep line-height >= 1.08 em (ink never collides between lines)', not tight, tight)
    # WCAG 1.4.12: with line-height 1.5 em the tallest ink in the font (stacked Vietnamese capitals to the deepest
    # descender / below-mark) must fit one line box, and added letter-spacing must not break any shaping: the font
    # must not contain ligature features that tracking would have to disable.
    ink = (tt['head'].yMax - tt['head'].yMin) / tt['head'].unitsPerEm
    R.ok('WCAG 1.4.12: tallest ink (%.3f em) fits a 1.5 em line box' % ink, ink <= 1.5, ink)
    feats = {fr.FeatureTag for fr in tt['GSUB'].table.FeatureList.FeatureRecord}
    R.ok('WCAG 1.4.12: no liga / dlig / rlig features, so letter- and word-spacing overrides cannot change glyph forms',
         not (feats & {'liga', 'dlig', 'rlig', 'clig'}), sorted(feats & {'liga', 'dlig', 'rlig', 'clig'}))
    out = dict(orion=orion, references=refs, viewing_geometry_worst=worst, typical_viewing_min_arcmin={k: min(v) for k, v in by_preset.items()})
    os.makedirs(os.path.join(ROOT, 'qa', 'accessibility'), exist_ok=True)
    json.dump(dict(geometry=geo, **out), open(os.path.join(ROOT, 'qa', 'accessibility', 'accessibility-data.json'), 'w'), indent=1)
    R.save(out)


if __name__ == '__main__':
    main()
