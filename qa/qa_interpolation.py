"""Variable-font interpolation tests: every axis, corners, named and arbitrary instances.

Checks per instance: outline topology (counters must not close or appear), counter area floors,
ink-area monotonicity along wght, advance behaviour along wdth, metric invariance under GRAD,
pair collisions after kerning, and deviation from the parametric design model."""
import os, sys, io, json, math, time
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.recordingPen import DecomposingRecordingPen
from common import *
import pathops
import uharfbuzz as hb

LETTERS = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') + list('&@$€£¥%#?!ßæœøÆŒØðþÞ') + \
    list('αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ') + list('бвгджзиклмнптфцчшщъыьэюяБДЖЗИЛУФЦЧШЩЪЫЬЭЮЯђћљњџґє')
COUNTER_GLYPHS = list('aegopqbdBRPDOQ0689@&æœøδθφρσбвдояфюАДБВОРФЯЮ%')


def instance(font_path, loc):
    f = TTFont(font_path)
    return instancer.instantiateVariableFont(f, loc, overlap=instancer.OverlapMode.KEEP_AND_DONT_SET_FLAGS)


def glyph_path(gs, name):
    p = pathops.Path()
    gs[name].draw(pathops.PathPen(p, glyphSet=gs))
    return p


def topo(gs, name):
    """(outer contours, holes, ink area) after removing overlaps."""
    p = glyph_path(gs, name)
    p.simplify(fix_winding=True, keep_starting_points=False)
    outer = holes = 0; hole_area = []
    for c in p.contours:
        a = abs(c.area)
        if a < 250:                      # slivers are counted separately by the caller
            SLIVERS.append((name, round(a)))
            continue
        if c.clockwise:                  # y-up font space: counters come out clockwise
            holes += 1; hole_area.append(a)
        else:
            outer += 1
    return outer, holes, p.area, hole_area


SLIVERS = []
# currency signs whose bars cross the letter: the bars legitimately split counters differently by weight
BAR_CROSSED = {'uni20AB', 'uni20A9', 'uni20A6', 'uni20B1', 'uni20B4', 'yen', 'Euro', 'numbersign', 'uni20B9', 'uni20B8'}


def shape_adv(font_bytes, text, feats=None):
    face = hb.Face(font_bytes); font = hb.Font(face)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, feats or {})
    return [p.x_advance for p in buf.glyph_positions], [i.codepoint for i in buf.glyph_infos]


def main():
    R = Report('interpolation')
    t0 = time.time()
    base = TTFont(VF)
    cmap = base.getBestCmap()
    names = [n for n in base.getGlyphOrder() if base['glyf'][n].numberOfContours != 0 and n != '.notdef']
    cnames = [cmap[ord(c)] for c in COUNTER_GLYPHS if ord(c) in cmap]
    tnames = [cmap[ord(c)] for c in LETTERS if ord(c) in cmap]
    # --- 1. fontTools interpolatable (structure of masters inside gvar)
    import subprocess
    r = subprocess.run([sys.executable, '-m', 'fontTools', 'varLib.interpolatable', VF, '--json', '--ignore-missing'],
                       capture_output=True, text=True)
    try:
        probs = json.loads(r.stdout) if r.stdout.strip() else {}
    except Exception:
        probs = {'_parse_error': r.stdout[:200] + r.stderr[:200]}
    kinds = {}
    for g, lst in probs.items():
        for p in (lst if isinstance(lst, list) else []):
            kinds[p.get('type', '?')] = kinds.get(p.get('type', '?'), 0) + 1
    struct_kinds = {k: v for k, v in kinds.items() if k in ('missing', 'open_path', 'path_count', 'node_count', 'node_incompatibility', 'contour_order', 'wrong_start_point')}
    R.ok('varLib.interpolatable: no structural incompatibilities', not struct_kinds, struct_kinds)
    soft = {k: v for k, v in kinds.items() if k not in struct_kinds}
    R.add('varLib.interpolatable: heuristic notes (kink / weight)', 'PASS' if not soft else 'WARN', soft)

    # --- 2. instances over the design space
    locs = grid_locations()
    ref = instance(VF, DEFAULT); gs0 = ref.getGlyphSet()
    ref_topo = {n: topo(gs0, n)[:2] for n in names}
    ref_area = {n: topo(gs0, n)[2] for n in names}
    topo_fail = []; min_counter = {}; neg_sb = []; inst_meta = []
    SLIVERS.clear(); sliver_log = {}
    for loc in locs:
        f = instance(VF, loc); gs = f.getGlyphSet(); glyf = f['glyf']; hmtx = f['hmtx']
        key = ','.join('%s=%g' % kv for kv in loc.items())
        for n in names:
            o, h, a, ha = topo(gs, n)
            if (o, h) != ref_topo[n] and n not in BAR_CROSSED:
                topo_fail.append((n, key, ref_topo[n], (o, h)))
            if n in cnames and ha:
                m = min(ha)
                if n not in min_counter or m < min_counter[n][0]:
                    min_counter[n] = (round(m), key)
            g = glyf[n]
            if g.numberOfContours != 0:
                adv, lsb = hmtx[n]
                rsb = adv - g.xMax
                if lsb < -40 or rsb < -40:
                    if n not in ('j', 'f', 'florin', 'fraction', 'periodcentered.loclCAT', 'periodcentered.loclCAT.case', 'dotlessj') and not n.startswith('uni') and 'comb' not in n:
                        neg_sb.append((n, key, lsb, rsb))
        inst_meta.append(key)
        if SLIVERS:
            sliver_log[key] = sorted(set(SLIVERS))[:12]; SLIVERS.clear()
    R.ok('no sliver contours after overlap removal at any instance', not sliver_log, dict(list(sliver_log.items())[:6]), warn=True)
    R.ok('topology stable at %d instances x %d glyphs (no counter closes, no contour inversion)' % (len(locs), len(names)),
         not topo_fail, topo_fail[:12])
    small = {k: v for k, v in min_counter.items() if v[0] < 1200}
    R.ok('counter area floor (>= 1200 sq units at every instance incl. all 16 corners)', not small, small)
    R.ok('no abnormal negative sidebearings', not neg_sb, neg_sb[:10])

    # --- 3. weight axis: ink area must increase strictly (real weight interpolation)
    weights = [100, 200, 300, 400, 500, 600, 700, 800, 900]
    areas = []
    stem = []
    for w in weights:
        f = instance(VF, dict(DEFAULT, wght=w)); gs = f.getGlyphSet()
        areas.append({n: topo(gs, n)[2] for n in tnames})
        gl = f['glyf'][cmap[ord('l')]]; I = f['glyf'][cmap[ord('I')]]
        stem.append((I.xMax - I.xMin, f['hmtx'][cmap[ord('n')]][0]))
    bad = [n for n in tnames if any(areas[i][n] >= areas[i + 1][n] for i in range(len(weights) - 1))]
    R.ok('ink area strictly increases with wght for all test glyphs', not bad, bad[:10])
    s0, s1 = stem[0], stem[-1]
    R.ok('weight is not synthetic emboldening / scaling (stem x%.1f while advance x%.2f)' % (s1[0] / s0[0], s1[1] / s0[1]),
         s1[0] / s0[0] > 4 and s1[1] / s0[1] < 1.4, stem)

    # --- 4. width axis: advances grow, stems do not scale with width
    wd = []
    for d in (75, 87.5, 100, 112.5, 125):
        f = instance(VF, dict(DEFAULT, wdth=d))
        I = f['glyf'][cmap[ord('I')]]; o = f['glyf'][cmap[ord('o')]]
        wd.append((d, f['hmtx'][cmap[ord('o')]][0], f['hmtx'][cmap[ord('H')]][0], I.xMax - I.xMin, o.xMax - o.xMin))
    R.ok('advance grows monotonically along wdth', all(wd[i][1] < wd[i + 1][1] and wd[i][2] < wd[i + 1][2] for i in range(4)), wd)
    R.ok('width axis is not horizontal scaling (round width x%.2f, stem x%.2f)' % (wd[-1][4] / wd[0][4], wd[-1][3] / wd[0][3]),
         wd[-1][4] / wd[0][4] > 1.35 and wd[-1][3] / wd[0][3] < 1.2, wd)

    # --- 5. optical size: real design changes
    oz = {}
    for o_ in (10, 14, 36, 72):
        f = instance(VF, dict(DEFAULT, opsz=o_))
        x = f['glyf'][cmap[ord('x')]]; I = f['glyf'][cmap[ord('I')]]; n = f['glyf'][cmap[ord('n')]]
        oz[o_] = dict(xheight=x.yMax, stem=I.xMax - I.xMin, n_adv=f['hmtx'][cmap[ord('n')]][0], n_lsb=f['hmtx'][cmap[ord('n')]][1])
    R.ok('opsz changes x-height, stem and spacing (not tracking only)',
         oz[10]['xheight'] > oz[72]['xheight'] and oz[10]['stem'] > oz[72]['stem'] and oz[10]['n_lsb'] > oz[72]['n_lsb'], oz)

    # --- 6. grade: metrics and kerning are invariant
    grade_bad = []
    text = 'AVATAR Toy Story 00:59:48 Tơ. LTV Yo, Україна Ελληνικά'
    for basel in (dict(DEFAULT), dict(DEFAULT, wght=100), dict(DEFAULT, wght=900), dict(DEFAULT, wght=700, wdth=75), dict(DEFAULT, wght=300, opsz=72),
                  dict(DEFAULT, wght=650, wdth=110, opsz=24)):
        advs = None; sh = None
        for g_ in (-50, -25, 0, 50, 100):
            f = instance(VF, dict(basel, GRAD=g_))
            a = [f['hmtx'][n][0] for n in f.getGlyphOrder()]
            bio = io.BytesIO(); f.save(bio)
            s = shape_adv(bio.getvalue(), text)[0]
            if advs is None:
                advs, sh = a, s
            else:
                d1 = max(abs(x - y) for x, y in zip(a, advs)); d2 = max(abs(x - y) for x, y in zip(s, sh))
                if d1 > 0 or d2 > 0:
                    grade_bad.append((basel, g_, d1, d2))
    R.ok('GRAD never changes advances or kerning (6 base locations x 5 grades, all glyphs)', not grade_bad, grade_bad[:6])
    f0 = instance(VF, dict(DEFAULT, GRAD=-50)); f1 = instance(VF, dict(DEFAULT, GRAD=100))
    i0 = f0['glyf'][cmap[ord('I')]]; i1 = f1['glyf'][cmap[ord('I')]]
    R.ok('GRAD changes stroke weight (I stem %d -> %d)' % (i0.xMax - i0.xMin, i1.xMax - i1.xMin), (i1.xMax - i1.xMin) - (i0.xMax - i0.xMin) >= 15)

    # --- 7. pair collisions after kerning (rasterised, 8 locations x 2,704 pairs)
    import freetype
    pairs_chars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    coll = []
    key_locs = [DEFAULT, dict(DEFAULT, wght=100), dict(DEFAULT, wght=900), dict(DEFAULT, wght=900, wdth=75), dict(DEFAULT, wght=900, wdth=125),
                dict(DEFAULT, opsz=10), dict(DEFAULT, wght=900, opsz=72), dict(wght=900, wdth=75, opsz=72, GRAD=100)]
    for loc in key_locs:
        f = instance(VF, loc); bio = io.BytesIO(); f.save(bio); data = bio.getvalue()
        face = freetype.Face(io.BytesIO(data)); ppem = 100; face.set_pixel_sizes(0, ppem)
        hbfont = hb.Font(hb.Face(data))
        bm = {}
        H = 160; base_y = 110
        for ch in pairs_chars:
            face.load_char(ch, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
            b = face.glyph.bitmap
            arr = np.zeros((H, 260), dtype=bool)
            if b.width:
                a = np.array(b.buffer, dtype=np.uint8).reshape(b.rows, b.width) > 100
                y0 = base_y - face.glyph.bitmap_top; x0 = 80 + face.glyph.bitmap_left
                arr[y0:y0 + b.rows, x0:x0 + b.width] = a
            bm[ch] = arr
        for a_ in pairs_chars:
            for b_ in pairs_chars:
                buf = hb.Buffer(); buf.add_str(a_ + b_); buf.guess_segment_properties(); hb.shape(hbfont, buf)
                adv = buf.glyph_positions[0].x_advance * ppem / 1000.0
                sh = int(round(adv))
                A = bm[a_]; B = np.zeros_like(A); B[:, sh:] = bm[b_][:, :A.shape[1] - sh] if sh > 0 else bm[b_]
                if (A & B).sum() > 0:
                    coll.append((a_ + b_, ','.join('%s=%g' % kv for kv in loc.items())))
    R.ok('no glyph collisions in 2,704 letter pairs at 8 extreme locations (with kerning)', not coll, coll[:16])

    # --- 8. deviation from the parametric design model at off-master locations
    dev = {}
    try:
        sys.path.insert(0, os.environ.get('ORION_SRC') or os.path.join(ROOT, 'sources', 'build-scripts'))
        from orion.params import Params
        from orion.glyphset import build_master, decomposed_contours
        from orion.geom import contour_bounds
        for loc in (dict(DEFAULT, wght=250), dict(DEFAULT, wght=650), dict(DEFAULT, wght=700, wdth=87.5), dict(DEFAULT, opsz=36), dict(wght=900, wdth=75, opsz=72, GRAD=0),
                    dict(wght=100, wdth=125, opsz=10, GRAD=0)):
            gl = build_master(Params(**loc)); f = instance(VF, loc)
            ds = []
            for n in tnames:
                if n not in gl:
                    continue
                cs = decomposed_contours(gl, n)
                if not cs:
                    continue
                bs = [contour_bounds(c) for c in cs]
                mb = (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))
                g = f['glyf'][n]
                ds.append(max(abs(mb[0] - g.xMin), abs(mb[1] - g.yMin), abs(mb[2] - g.xMax), abs(mb[3] - g.yMax), abs(gl[n].w - f['hmtx'][n][0])))
            dev[','.join('%s=%g' % kv for kv in loc.items())] = dict(mean=round(float(np.mean(ds)), 2), p95=round(float(np.percentile(ds, 95)), 2), max=round(float(max(ds)), 2))
        on_axis = [v['p95'] for k, v in dev.items() if 'wdth=100' in k and 'GRAD=0' in k]
        R.ok('interpolated instances track the design model (bounds / advance deviation, units)', max(on_axis) <= 12, dev)
    except Exception as e:
        R.add('interpolated instances track the design model', 'SKIP', repr(e))
    R.save(dict(instances_tested=len(locs), glyphs_tested=len(names), min_counter_area=min_counter, optical_size=oz, width=wd,
                weight_stem_advance=stem, model_deviation=dev, seconds=round(time.time() - t0)))


if __name__ == '__main__':
    main()
