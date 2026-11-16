"""Glyph-set assembly: draws every glyph for a design-space location, builds
accented composites from Unicode decomposition, places anchors and resolves
component metrics.  The result is identical in structure for every location."""
from __future__ import annotations
import unicodedata
from .geom import G, flatten, poly
from .params import Params
from . import parts
from . import latin_lc, latin_uc, symbols, marks, latin_ext, greek, cyrillic  # noqa: F401  (registration)
from .charset import COMPOSED, EXTRA_COMPOSITES, uni_name

MARK_BY_CP = marks.MARK_BY_CP          # combining codepoint -> mark glyph name
STACKS = marks.STACKS                  # (cp, cp) -> stacked mark glyph


def glyph_for_cp(cp):
    for n, (fn, us) in parts.REG.items():
        if cp in us:
            return n
    return None


_CP2NAME = None


def cp2name():
    global _CP2NAME
    if _CP2NAME is None:
        _CP2NAME = {}
        for n, (fn, us) in parts.REG.items():
            for u in us:
                _CP2NAME.setdefault(u, n)
    return _CP2NAME


def is_upper_base(name):
    return name in parts.UPPER


def decompose(ch):
    """Return (base_glyph, [mark glyph names]) for a precomposed character or None."""
    d = unicodedata.normalize('NFD', ch)
    if len(d) < 2:
        return None
    c2n = cp2name()
    base_cp = ord(d[0]); mcps = [ord(c) for c in d[1:]]
    base = c2n.get(base_cp)
    if base is None:
        return None
    upper = is_upper_base(base)
    greek_ = 0x370 <= base_cp <= 0x3FF
    # language-aware substitutions
    if base in ('i', 'uni0456') and any(marks.is_above(m) for m in mcps): base = 'dotlessi'
    if base in ('j', 'uni0458') and any(marks.is_above(m) for m in mcps): base = 'dotlessj'
    out = []
    i = 0
    while i < len(mcps):
        m = mcps[i]
        pair = (m, mcps[i + 1]) if i + 1 < len(mcps) else None
        if greek_ and pair == (0x308, 0x301):
            out.append('dieresistonoscomb'); i += 2; continue
        if pair in STACKS:
            out.append(STACKS[pair]); i += 2; continue
        if greek_ and m == 0x301:
            out.append('tonoscomb')
        elif m == 0x30C and base in ('d', 't', 'l', 'L'):
            out.append('caroncomb.alt')
        elif m == 0x327 and base in ('G', 'K', 'L', 'N', 'R', 'k', 'l', 'n', 'r'):
            out.append('commaaccentcomb')
        elif m == 0x327 and base == 'g':
            out.append('commaturnedabovecomb')
        elif m in MARK_BY_CP:
            out.append(MARK_BY_CP[m])
        else:
            return None
        i += 1
    if upper:
        out = [o + '.case' if (o + '.case') in parts.REG and not o.endswith('.alt') else o for o in out]
    return base, out


def default_anchors(P, name, g, upper):
    b = g.bounds()
    if b is None:
        return
    cx = (b[0] + b[2]) / 2
    if 'top' not in g.anchors:
        if upper:
            y = P.cap
        else:
            y = P.asc if b[3] > P.xh + 60 else P.xh
        g.anchors['top'] = (cx, y)
    if name in ('o', 'O', 'Omicron', 'omicron', 'uni041E', 'uni043E'):
        g.anchors['horn'] = (cx + (b[2] - b[0]) / 2 * 0.66, (b[1] + b[3]) / 2 + (b[3] - b[1]) / 2 * 0.74)
    if name in ('u', 'U'):
        g.anchors['horn'] = (b[2] - (P.V0 if upper else P.v0) * 0.42, b[3] - (P.H0 if upper else P.h0) * 0.25)
    if 'bottom' not in g.anchors:
        g.anchors['bottom'] = (cx, 0.0)
    if 'ogonek' not in g.anchors:
        if name in ('e', 'o', 'O', 'U', 'Omicron', 'omicron'):      # round bottoms: attach under the bowl
            g.anchors['ogonek'] = (cx + (b[2] - b[0]) * 0.10, 0.0)
        else:
            g.anchors['ogonek'] = (b[2] - (P.V0 if upper else P.v0) * 0.55, 0.0)


def zone_min_x(g, y0, y1):
    xs = []
    for c in g.contours:
        pts = flatten(c, 8)
        n = len(pts)
        for i in range(n):
            p, q = pts[i - 1], pts[i]
            lo, hi = min(p[1], q[1]), max(p[1], q[1])
            if hi < y0 or lo > y1:
                continue
            xs.append(min(p[0], q[0]))
    return min(xs) if xs else None


def zone_max_x(g, y0, y1):
    xs = []
    for c in g.contours:
        pts = flatten(c, 8)
        for i in range(len(pts)):
            p, q = pts[i - 1], pts[i]
            lo, hi = min(p[1], q[1]), max(p[1], q[1])
            if hi < y0 or lo > y1:
                continue
            xs.append(max(p[0], q[0]))
    return max(xs) if xs else None


def flat_bounds(glyphs, name, dx=0, dy=0, depth=0):
    g = glyphs[name]
    bs = []
    b = g.bounds()
    if b:
        bs.append((b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy))
    for cn, cx, cy in g.components:
        if depth < 4:
            cb = flat_bounds(glyphs, cn, dx + cx, dy + cy, depth + 1)
            if cb:
                bs.append(cb)
    if not bs:
        return None
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def build_master(P, only=None):
    """Draw all glyphs for one location.  Returns {name: G} in glyph order."""
    from .geom import POLY_LOG
    gbase = None
    if P.GRAD != 0:
        # grade must not move anything: metrics, anchors and component offsets come from GRAD = 0
        gbase = build_master(Params(wght=P.wght, wdth=P.wdth, opsz=P.opsz, GRAD=0))
    glyphs = {}
    for name in parts.ORDER:
        g = G(P, name)
        POLY_LOG.clear()
        parts.REG[name][0](g)
        g.polyflags = tuple(POLY_LOG)
        if gbase is not None and hasattr(g, 'dx'):
            g.translate(gbase[name].dx - g.dx); g.dx = gbase[name].dx
        glyphs[name] = g
    # --- fraction bar: placed so that numerators and denominators keep the same clearance from it.
    #     Worst cases are ink in the numerator's bottom-right corner (2) and the denominator's top-left corner (7, 5).
    f = glyphs.get('fraction')
    if f is not None and f.contours:
        if gbase is not None:
            f.translate(gbase['fraction'].fshift); f.fshift = gbase['fraction'].fshift; f.w = gbase['fraction'].w
        else:
            digs = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
            nb = [flat_bounds(glyphs, d + '.numr') for d in digs]; db = [flat_bounds(glyphs, d + '.dnom') for d in digs]
            y_n = min(b[1] for b in nb); y_d = max(b[3] for b in db)
            rsb_n = min(glyphs[d + '.dnom'].w - b[2] for d, b in zip(digs, nb)); lsb_d = min(b[0] for b in db)
            pts = flatten(f.contours[0], 2)

            def cross(y):
                xs = []
                for i in range(len(pts)):
                    (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % len(pts)]
                    if (ya - y) * (yb - y) < 0:
                        xs.append(xa + (xb - xa) * (y - ya) / (yb - ya))
                return min(xs), max(xs)
            gap = 14.0 + 0.15 * P.V0
            f.fshift = (-rsb_n + gap) - cross(y_n)[0]
            f.translate(f.fshift)
            f.w = cross(y_d)[1] + f.fshift + gap - lsb_d
    # --- widths of pure-component glyphs and fractions
    for name, g in glyphs.items():
        fr = getattr(g, 'frac', None)
        if fr:
            num, den = fr
            n = glyphs[num + '.numr']; f = glyphs['fraction']; d = glyphs[den + '.dnom']
            nw = glyphs[num + '.dnom'].w
            g.components = [(num + '.numr', 0, 0), ('fraction', nw, 0), (den + '.dnom', nw + f.w, 0)]
            g.w = nw + f.w + d.w
    for name, g in glyphs.items():
        seq = getattr(g, 'seq', None)
        if seq:
            x = 0.0; comps = []
            for item in seq:
                cn, adj = item if isinstance(item, tuple) else (item, 0.0)
                x += adj
                comps.append((cn, x, 0.0)); x += glyphs[cn].w
            g.components = comps; g.w = x
    for name, g in glyphs.items():
        tf = getattr(g, 'tf', None)
        if tf:
            base, wf_ = tf
            adv = latin_uc.fig_adv(P) * wf_
            g.components = [(base, (adv - glyphs[base].w) / 2, 0.0)]
            g.w = adv
    for name, g in glyphs.items():
        if g.w is None:
            g.w = glyphs[g.components[0][0]].w
        un = getattr(g, 'under', None)
        if un:                                   # dong: underline below the letter
            bw = glyphs[g.components[0][0]].w
            g.contours.append(poly([(bw * 0.14, -un * 2.1), (bw * 0.86, -un * 2.1), (bw * 0.86, -un * 1.1), (bw * 0.14, -un * 1.1)]))
    # --- anchors on bases
    for name, g in glyphs.items():
        if name in marks.MARKS or not g.contours:
            continue
        default_anchors(P, name, g, is_upper_base(name))
    for name, g in glyphs.items():           # component-only bases inherit anchors
        if not g.contours and g.components and name not in marks.MARKS and not g.anchors:
            cn, cx, cy = g.components[0]
            for k, (ax, ay) in glyphs[cn].anchors.items():
                if not k.startswith('_'):
                    g.anchors[k] = (ax + cx, ay + cy)
    # --- precomposed characters
    for cp in COMPOSED:
        ch = chr(cp)
        dec = decompose(ch)
        if dec is None:
            continue
        base, mk = dec
        name = uni_name(cp)
        if name in glyphs:
            continue
        g = compose(P, glyphs, name, base, mk, cp)
        glyphs[name] = g
    for name, (base, mk, cps) in EXTRA_COMPOSITES.items():
        if name not in glyphs:
            glyphs[name] = compose(P, glyphs, name, base, mk, None)
    # accented forms of the stylistic alternates
    for cp in COMPOSED:
        dec = decompose(chr(cp))
        if dec is None or dec[0] not in ALT_BASES:
            continue
        alt = ALT_BASES[dec[0]]
        name = uni_name(cp) + alt[alt.index('.'):]
        mk = dec[1]
        if alt == 'l.ss02' and 'caroncomb.alt' not in mk and False:
            pass
        glyphs[name] = compose(P, glyphs, name, alt, mk, None)
    if gbase is not None:
        for name, g in glyphs.items():
            b = gbase[name]
            g.w = b.w; g.anchors = dict(b.anchors)
            if g.components:
                g.components = list(b.components)
    return glyphs


ALT_BASES = {'a': 'a.ss03', 'I': 'I.ss01', 'l': 'l.ss02'}


def compose(P, glyphs, name, base, mks, cp):
    bg = glyphs[base]
    g = G(P, name)
    g.w = bg.w
    comps = [(base, 0.0, 0.0)]
    anchors = dict(bg.anchors)
    upper = is_upper_base(base)
    shift_base = 0.0
    for mk in mks:
        mg = glyphs[mk]
        if mk.startswith('tonoscomb') and upper:
            # Greek capital tonos stands to the left of the letter
            tb = mg.bounds()
            tw = tb[2] - tb[0]
            c = zone_min_x(bg, P.cap * 0.70, P.cap) or 0.0
            gap = 26.0 + P.V0 * 0.12
            shift = max(0.0, tw + gap - c)
            if base == 'Alpha' or base == 'A':
                shift = max(0.0, tw * 0.60 + gap - c)
            x = c + shift - gap - tb[2]
            comps = [(n, x_ + shift, y_) for n, x_, y_ in comps]
            anchors = {k: (ax + shift, ay) for k, (ax, ay) in anchors.items()}
            comps.append((mk, x, 0.0))
            g.w += shift
            continue
        if mk == 'caroncomb.alt':
            mb = mg.bounds()
            xr = zone_max_x(bg, P.xh * 0.9, P.asc if not upper else P.cap) or bg.w
            gap = 18.0 + P.v0 * 0.10
            x = xr + gap - mb[0]
            top = P.cap if upper else P.asc
            comps.append((mk, x, top - mb[3]))
            g.w = max(g.w, x + mb[2] - P.so * 0.2)
            continue
        attach = None
        for an in ('top', 'bottom', 'ogonek', 'horn'):
            if '_' + an in mg.anchors and an in anchors:
                attach = an
                break
        if attach is None:
            continue
        ax, ay = anchors[attach]; mx, my = mg.anchors['_' + attach]
        dx, dy = ax - mx, ay - my
        comps.append((mk, dx, dy))
        if attach in mg.anchors:              # stacking point moves up / down
            sx, sy = mg.anchors[attach]
            anchors[attach] = (sx + dx, sy + dy)
    g.components = comps
    g.anchors = anchors
    # widen narrow letters whose marks overhang the advance (i-circumflex, i-dieresis ...)
    lo, hi = 0.0, g.w
    for mk, dx, dy in comps[1:]:
        if mk.startswith(('ogonek', 'horn', 'tonos', 'caroncomb.alt', 'cedilla')):
            continue
        mb = glyphs[mk].bounds()
        if mb:
            lo = min(lo, mb[0] + dx - 12.0); hi = max(hi, mb[2] + dx + 12.0)
    if lo < 0 or hi > g.w:
        ext = max(-lo, hi - g.w)
        g.components = [(n, x_ + ext, y_) for n, x_, y_ in comps]
        g.anchors = {k: (ax + ext, ay) for k, (ax, ay) in g.anchors.items()}
        g.w += 2 * ext
    return g


def decomposed_contours(glyphs, name, dx=0.0, dy=0.0, depth=0):
    g = glyphs[name]
    out = []
    for c in g.contours:
        out.append([(s[0], *[(p[0] + dx, p[1] + dy) for p in s[1:]]) for s in c] if (dx or dy) else c)
    if depth < 5:
        for cn, cx, cy in g.components:
            out.extend(decomposed_contours(glyphs, cn, dx + cx, dy + cy, depth + 1))
    return out


def cmap_for(glyphs):
    cm = {}
    for n, (fn, us) in parts.REG.items():
        for u in us:
            cm[u] = n
    for cp in COMPOSED:
        n = uni_name(cp)
        if n in glyphs:
            cm.setdefault(cp, n)
    for name, (base, mk, cps) in EXTRA_COMPOSITES.items():
        for cp in cps:
            cm.setdefault(cp, name)
    return cm
