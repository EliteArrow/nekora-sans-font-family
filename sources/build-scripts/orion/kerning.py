"""Profile-based kerning.

Kerning is computed for every master from the actual outlines, so it follows
the design through weight, width, optical size and grade.

Measure.  For a pair (A, B) the horizontal gap d(y) between A's right profile
and B's left profile is sampled in 10-unit bands.  The pair's optical gap is
the power mean M = mean(d^-2)^(-1/2): close passages dominate, but only in
proportion to their length.  Each side also has a 'wall' reference (the same
mean against a flat edge).  Pairs whose profiles interlock have M larger than
the sum of the two wall references; that excess is closed with a saturating
gain (calibrated against the kerning magnitudes of the reference families).
Pairs built from equal-zone profiles (HH, OO, nn, no ...) come out at zero by
construction, so the designed sidebearings are never second-guessed.
"""
from __future__ import annotations
import math, unicodedata
import numpy as np
from .geom import flatten
from .glyphset import decomposed_contours, cmap_for
from .params import master_name, DEFAULT
from . import marks

Y0, Y1, STEP = -220, 780, 10
NB = (Y1 - Y0) // STEP
BIG = 400.0
P_EXP = -2.0

PUNCT = ['period', 'comma', 'colon', 'semicolon', 'hyphen', 'endash', 'emdash', 'quoteleft', 'quoteright', 'quotedblleft',
         'quotedblright', 'quotesinglbase', 'quotedblbase', 'quotesingle', 'quotedbl', 'parenleft', 'parenright',
         'slash', 'question', 'exclam', 'guilsinglleft', 'guilsinglright', 'guillemotleft', 'guillemotright',
         'asterisk', 'ellipsis']
QUOTES = {'quoteleft', 'quoteright', 'quotedblleft', 'quotedblright', 'quotesingle', 'quotedbl'}
DOTS = {'period', 'comma', 'ellipsis', 'quotesinglbase', 'quotedblbase'}
SKIP = {'florin', 'ordfeminine', 'ordmasculine', 'napostrophe', 'ldot', 'Ldot', 'longs', 'IJ', 'ij', 'mu'}
FIGS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero.zero']


def profiles(glyphs, name):
    """Left / right ink profile per band (inf where the band holds no ink)."""
    L = np.full(NB, np.inf); R = np.full(NB, -np.inf)
    for c in decomposed_contours(glyphs, name):
        pts = flatten(c, 5)
        n = len(pts)
        for i in range(n):
            x0, y0 = pts[i - 1]; x1, y1 = pts[i]
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            b0 = max(0, int((y0 - Y0) // STEP)); b1 = min(NB - 1, int((y1 - Y0) // STEP))
            if b1 < 0 or b0 > NB - 1:
                continue
            for b in range(b0, b1 + 1):
                ya = max(y0, Y0 + b * STEP); yb = min(y1, Y0 + (b + 1) * STEP)
                if y1 - y0 < 1e-6:
                    xa, xb = x0, x1
                else:
                    xa = x0 + (x1 - x0) * (ya - y0) / (y1 - y0); xb = x0 + (x1 - x0) * (yb - y0) / (y1 - y0)
                lo = min(xa, xb); hi = max(xa, xb)
                if lo < L[b]: L[b] = lo
                if hi > R[b]: R[b] = hi
    w = glyphs[name].w
    return L, np.where(np.isfinite(R), w - R, np.inf)


def kind_of(name, cps):
    if name in FIGS:
        return 'fig'
    if name in PUNCT:
        return 'punct'
    for cp in cps:
        cat = unicodedata.category(chr(cp))
        if cat == 'Lu':
            return 'U'
        if cat in ('Ll', 'Lo'):
            return 'L'
    if name.endswith(('.ss01',)):
        return 'U'
    if name.endswith(('.ss02', '.ss03', '.loclSRB')):
        return 'L'
    return None


def script_of(cps):
    for cp in cps:
        if 0x370 <= cp <= 0x3FF: return 'grek'
        if 0x400 <= cp <= 0x52F: return 'cyrl'
    return 'latn'


def kern_set(glyphs):
    cmap = cmap_for(glyphs)
    rev = {}
    for cp, n in cmap.items():
        rev.setdefault(n, []).append(cp)
    out = {}
    for n in glyphs:
        if n in marks.MARKS or n in SKIP:
            continue
        g = glyphs[n]
        # composites take part only when they kern exactly like their base letter
        if g.components and not g.contours and len(g.components) > 1 and base_of(glyphs, n) == n:
            continue
        k = kind_of(n, rev.get(n, []))
        if k:
            out[n] = (k, script_of(rev.get(n, [])), n)
    return out


def base_of(glyphs, name):
    """Accented composites kern like their base letter when the advance is unchanged."""
    g = glyphs[name]
    if g.components and not g.contours:
        b = g.components[0]
        if abs(b[1]) < 0.5 and abs(glyphs[b[0]].w - g.w) < 0.5 and not any(c[0] == 'caroncomb.alt' for c in g.components):
            return base_of(glyphs, b[0])
    return name


def make_classes(glyphs, kset):
    """Group glyphs whose side profiles coincide (computed on the default master)."""
    prof = {}
    def key(arr):
        a = np.where(np.isfinite(arr), np.round(arr / 10.0), 999)
        return tuple(a[::2].astype(int))
    left, right = {}, {}
    base = {}
    for n in kset:
        b = base_of(glyphs, n)
        base[n] = b
        if b not in prof:
            prof[b] = profiles(glyphs, b)
        L, R = prof[b]
        left.setdefault((kset[n][:2], key(L)), []).append(n)
        right.setdefault((kset[n][:2], key(R)), []).append(n)
    lcls = {members[0]: members for members in left.values()}
    rcls = {members[0]: members for members in right.values()}
    return lcls, rcls


def pmean(d):
    return np.mean(np.power(d, P_EXP), axis=-1) ** (1.0 / P_EXP)


GAIN = {('U', 'U'): (0.42, 120.0), ('U', 'L'): (0.40, 105.0), ('L', 'U'): (0.34, 80.0), ('L', 'L'): (0.25, 60.0),
        ('fig', 'fig'): (0.22, 50.0)}


def gain(ka, kb):
    if (ka, kb) in GAIN:
        return GAIN[(ka, kb)]
    if 'punct' in (ka, kb):
        if 'fig' in (ka, kb):
            return (0.36, 90.0)
        return (0.40, 110.0)
    return None


def allowed(a, b):
    (ka, sa, na), (kb, sb, nb) = a, b
    if ka == 'punct' and kb == 'punct':
        return (na in QUOTES and nb in DOTS) or (na in DOTS and nb in QUOTES)
    if ka in ('U', 'L') and kb in ('U', 'L'):
        return sa == sb
    if 'fig' in (ka, kb) and ({ka, kb} & {'U', 'L'}):
        return False
    return True


def master_kerning(glyphs, lcls, rcls, kset, clear=50.0, scale=1.0):
    """Raw kerning values for all class pairs on one master."""
    rnames = list(rcls); lnames = list(lcls)
    Rm = np.array([profiles(glyphs, base_of(glyphs, n))[1] for n in rnames])
    Lm = np.array([profiles(glyphs, base_of(glyphs, n))[0] for n in lnames])
    big = BIG
    Rf = np.where(np.isfinite(Rm), np.maximum(Rm, 1.0), big)
    Lf = np.where(np.isfinite(Lm), np.maximum(Lm, 1.0), big)
    # vertical zone of each side: bands holding ink (extended to the union for the pair)
    Rink = np.isfinite(Rm); Link = np.isfinite(Lm)
    out = {}
    for i, a in enumerate(rnames):
        ka = kset[a]
        zone = Rink[i][None, :] | Link                         # union zone per pair
        d = Rf[i][None, :] + Lf                                # (nL, NB)
        # mask bands outside the union zone by a neutral large value excluded from the mean
        inv = np.where(zone, np.power(d, P_EXP), 0.0)
        cnt = zone.sum(axis=1).clip(min=1)
        M = (inv.sum(axis=1) / cnt) ** (1.0 / P_EXP)
        wa = np.where(zone, np.power(Rf[i][None, :], P_EXP), 0.0).sum(axis=1) / cnt
        wb = np.where(zone, np.power(Lf, P_EXP), 0.0).sum(axis=1) / cnt
        E = wa ** (1.0 / P_EXP) + wb ** (1.0 / P_EXP)
        exc = M - E
        dmin = np.where(Rink[i][None, :] & Link, Rm[i][None, :] + Lm, np.inf).min(axis=1)
        # clearance: shapes may pass over / under each other but never come nearer than `clear`
        vmin = np.full(len(lnames), -np.inf)
        for k in range(-8, 9):
            sep = max(0.0, abs(k) * STEP - STEP)
            req2 = clear * clear - (0.8 * sep) ** 2
            if req2 <= 0:
                continue
            req = math.sqrt(req2)
            ra = np.roll(Rm[i], k)
            if k > 0: ra[:k] = np.inf
            elif k < 0: ra[k:] = np.inf
            cand = req - (ra[None, :] + Lm)
            cand = np.where(np.isfinite(cand), cand, -np.inf).max(axis=1)
            vmin = np.maximum(vmin, cand)
        for j, b in enumerate(lnames):
            kb = kset[b]
            if not allowed(ka, kb):
                continue
            gn = gain(ka[0], kb[0])
            if gn is None:
                continue
            g_, cap = gn
            x = exc[j]
            if x >= 0:
                v = -cap * math.tanh(g_ * x / cap)
            else:
                v = 36.0 * math.tanh(0.30 * (-x) / 36.0)
            # never close a facing gap below 55% of its designed value
            if np.isfinite(dmin[j]) and v < 0:
                floor = 0.50 * dmin[j]
                v = max(v, -(dmin[j] - floor))
            if np.isfinite(vmin[j]) and v < vmin[j]:
                v = min(vmin[j], 60.0) if vmin[j] > 0 else max(v, vmin[j])
            out[(a, b)] = v * scale
    return out


def build_kerning(built, log=print):
    """Return {master_name: (kerning, groups)} with one pair set for every master."""
    dn = master_name(DEFAULT)
    g0 = built[dn][1]
    kset = kern_set(g0)
    lcls, rcls = make_classes(g0, kset)
    raw = {}
    from .params import Params
    for mn, (loc, gl) in built.items():
        P = Params(**loc)
        raw[mn] = master_kerning(gl, lcls, rcls, kset, clear=0.42 * (P.sb + P.so) + 8.0)
        # r followed by n / m: a little air keeps 'rn' from reading as 'm'
        for a in rcls:
            if 'r' in rcls[a] and kset[a][:2] == ('L', 'latn'):
                for b in lcls:
                    if ('n' in lcls[b] or 'm' in lcls[b]) and kset[b][:2] == ('L', 'latn'):
                        raw[mn][(a, b)] = max(8.0, P.sb * 0.16)
    # a pair is kept when it matters on the default master (thresholds per pair kind);
    # every master then carries a value for exactly that pair set
    keep = set()
    for k, v in raw[dn].items():
        ka, kb = kset[k[0]][0], kset[k[1]][0]
        thr = 25.0 if ('punct' in (ka, kb) or (ka, kb) == ('L', 'U')) else 14.0
        if abs(v) >= thr:
            keep.add(k)
    for a in rcls:                         # r + n / m always carries its positive value
        if 'r' in rcls[a] and kset[a][:2] == ('L', 'latn'):
            for b in lcls:
                if ('n' in lcls[b] or 'm' in lcls[b]) and kset[b][:2] == ('L', 'latn'):
                    keep.add((a, b))
    groups = {}
    def gname(side, rep, members):
        return rep if len(members) == 1 else 'public.kern%d.%s' % (side, rep.replace('.', '_'))
    rkey = {}; lkey = {}
    for rep, members in rcls.items():
        nm = gname(1, rep, members); rkey[rep] = nm
        if len(members) > 1:
            groups[nm] = list(members)
    for rep, members in lcls.items():
        nm = gname(2, rep, members); lkey[rep] = nm
        if len(members) > 1:
            groups[nm] = list(members)
    # grade must never move text: graded masters reuse the kerning of their GRAD=0 sibling
    for mn in list(raw):
        loc = built[mn][0]
        if loc['GRAD'] != 0:
            raw[mn] = raw[master_name(dict(loc, GRAD=0))]
    out = {}
    for mn, vals in raw.items():
        loc, gl = built[mn]
        kern = {}
        for (a, b) in keep:
            kern[(rkey[a], lkey[b])] = int(round(vals.get((a, b), 0.0)))
        out[mn] = (kern, groups)
    log('  kerning: %d right classes, %d left classes, %d pairs kept' % (len(rcls), len(lcls), len(keep)))
    return out
