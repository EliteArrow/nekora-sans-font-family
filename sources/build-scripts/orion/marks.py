"""Orion — diacritical marks (combining, capital, stacked and spacing forms)."""
from __future__ import annotations
import math
from .geom import N, E, Line, G, poly, superellipse
from .parts import glyph, S, clamp, REG
from .symbols import wave, comma_shape
from .latin_lc import dot_y

MARKS = set()
MARK_BY_CP = {}
ABOVE = {0x300, 0x301, 0x302, 0x303, 0x304, 0x306, 0x307, 0x308, 0x309, 0x30A, 0x30B, 0x30C, 0x312}
UPPER_EXTRA = set()


def is_above(cp): return cp in ABOVE


def wt(P): return clamp(P.wt, 0, 1)


class Z:
    """Mark zone: lowercase marks sit over the x-height, capital marks are
    lower and flatter so that stacked Vietnamese capitals stay inside the
    line box."""
    def __init__(self, P, case):
        self.P = P; self.case = case
        self.base = P.cap if case else P.xh
        self.gap = (40 - 10 * wt(P)) if case else (64 - 18 * wt(P))
        self.mh = (P.cap * 0.128 + P.acc * 0.10) if case else (P.xh * 0.215 + P.acc * 0.10)
        self.y0 = self.base + self.gap
        self.y1 = self.y0 + self.mh
        self.t = P.acc
        self.flat = 1.28 if case else 1.0


def top_mark(name, cp=None, stack=0.55):
    """Register a mark attaching at 'top' in lowercase and .case forms."""
    def deco(fn):
        for case in (False, True):
            nm = name + ('.case' if case else '')

            def m(g, case=case):
                z = Z(g.P, case)
                top = fn(g, z)
                top = z.y1 if top is None else top
                g.w = 0.0
                g.anchor('_top', 0.0, z.base)
                g.anchor('top', 0.0, top - z.gap * stack)
            glyph(nm, None)(m)
            MARKS.add(nm)
        if cp:
            REG[name][1].append(cp)
            MARK_BY_CP[cp] = name
        return fn
    return deco


def acute_shape(g, z, x=0.0, y=None, sign=1, f=1.0, steep=1.0):
    y0 = z.y0 if y is None else y
    mh = z.mh * f
    run = mh * (0.60 if not z.case else 1.12) / steep
    tb = z.t * 0.40 * f ** 0.5; tt = z.t * (0.64 if not z.case else 0.78) * f ** 0.5
    xb = x - sign * run / 2; xt = x + sign * run / 2
    g.poly([(xb - tb, y0), (xb + tb, y0), (xt + tt, y0 + mh), (xt - tt, y0 + mh)])
    return y0 + mh


@top_mark('acutecomb', 0x301)
def acute(g, z): acute_shape(g, z)


@top_mark('gravecomb', 0x300)
def grave(g, z): acute_shape(g, z, sign=-1)


def circ_shape(g, z, x=0.0, y=None, inv=False, f=1.0):
    y0 = z.y0 if y is None else y
    mh = z.mh * f * (0.96 if not z.case else 0.92)
    w = (mh * (1.90 if not z.case else 2.55) + z.t * 0.55)
    ah = z.t * (1.10 if not z.case else 1.32)
    tk = min(z.t * (1.02 if not z.case else 0.86), mh * 0.60)
    pts = [(x - w / 2, y0), (x - w / 2 + ah, y0), (x, y0 + mh - tk), (x + w / 2 - ah, y0), (x + w / 2, y0), (x, y0 + mh)]
    if inv:
        pts = [(px, 2 * y0 + mh - py) for px, py in pts]
    g.poly(pts)
    return y0 + mh


@top_mark('circumflexcomb', 0x302)
def circumflex(g, z): circ_shape(g, z)


@top_mark('caroncomb', 0x30C)
def caron(g, z): circ_shape(g, z, inv=True)


def tilde_shape(g, z, x=0.0, y=None, f=1.0):
    y0 = z.y0 if y is None else y
    mh = z.mh * f
    w = mh * (2.05 if not z.case else 2.7) + z.t * 0.5
    amp = mh * 0.21
    t = z.t * 0.90
    yc = y0 + amp + t / 2 + mh * 0.04
    wave(g, x - w / 2, x + w / 2, yc, amp, t)
    return yc + amp + t / 2


@top_mark('tildecomb', 0x303)
def tilde(g, z): return tilde_shape(g, z)


@top_mark('macroncomb', 0x304)
def macron(g, z):
    w = z.mh * (1.70 if not z.case else 2.30) + z.t * 0.4
    t = z.t * 0.86
    y = z.y0 + z.mh * 0.16
    g.rect(-w / 2, y, w / 2, y + t)
    return y + t + z.mh * 0.12


def breve_shape(g, z, x=0.0, y=None, f=1.0):
    y0 = z.y0 if y is None else y
    mh = z.mh * f * (0.92 if not z.case else 0.86)
    w = mh * (1.80 if not z.case else 2.45) + z.t * 0.5
    t = z.t * 0.90
    te = t * 0.74
    g.stroke([N(x - w / 2 + te * 0.5, y0 + mh, 276, te), N(x, y0 + t / 2, 0, t), N(x + w / 2 - te * 0.5, y0 + mh, 84, te)], k=0.60)
    return y0 + mh


@top_mark('brevecomb', 0x306)
def breve(g, z): return breve_shape(g, z)


@top_mark('dotaccentcomb', 0x307)
def dotaccent(g, z):
    P = g.P; d = P.dotd * (1.0 if not z.case else (0.94 - 0.22 * wt(P)))
    cy = dot_y(P) if not z.case else z.y0 + d * 0.5
    g.dot(0, cy, d)
    return cy + d / 2


def dier_shape(g, z):
    P = g.P; d = P.dotd * ((0.90 - 0.06 * wt(P)) if not z.case else (0.86 - 0.22 * wt(P)))
    cy = dot_y(P) - (P.dotd - d) / 2 if not z.case else z.y0 + d * 0.5
    off = d * 0.5 + max(d * 0.34, 14.0) + (P.nw * 0.035 if not z.case else P.Hw * 0.03)
    g.dot(-off, cy, d); g.dot(off, cy, d)
    return cy + d / 2


@top_mark('dieresiscomb', 0x308)
def dieresis(g, z): return dier_shape(g, z)


@top_mark('ringcomb', 0x30A)
def ring_(g, z):
    P = g.P
    t = z.t * (0.80 - 0.22 * wt(P))
    d = z.mh * (0.94 if not z.case else 1.02) + t * 1.25
    y0 = z.y0 - z.gap * 0.22
    k = 0.56
    g.add([superellipse(0, y0 + d / 2, d / 2, d / 2, k)])
    g.add([superellipse(0, y0 + d / 2, d / 2 - t, d / 2 - t, k, cw=True)])
    return y0 + d


@top_mark('hungarumlautcomb', 0x30B)
def hungar(g, z):
    off = z.t * 0.74 + z.mh * 0.20
    acute_shape(g, z, x=-off + z.mh * 0.08); acute_shape(g, z, x=off + z.mh * 0.08)


def hook_shape(g, z, x=0.0, y=None, f=1.0):
    y0 = z.y0 if y is None else y
    mh = z.mh * f * (1.0 if not z.case else 0.98)
    t = z.t * (0.80 - 0.20 * wt(g.P))
    r = mh * (0.50 if not z.case else 0.62)
    g.stroke([N(x - r, y0 + mh - r * 0.95, 90, t * 0.86), N(x, y0 + mh - t / 2, 0, t), N(x + r, y0 + mh * 0.52, -90, t),
              N(x + r * 0.18, y0 + t * 0.41, 180, t * 0.82)], k=0.60)
    return y0 + mh


@top_mark('hookabovecomb', 0x309)
def hookabove(g, z): return hook_shape(g, z)


@top_mark('commaturnedabovecomb', 0x312)
def commaturned(g, z):
    P = g.P; d = P.dotd * (0.86 - 0.30 * wt(P))
    with g.rot180(0, z.y0 + d * 0.96):
        comma_shape(g, 0, z.y0 + 1.92 * d - d / 2, d)
    return z.y0 + d * 1.92


@top_mark('tonoscomb', None)
def tonos(g, z):
    if not z.case:
        acute_shape(g, z, steep=2.0)
    else:
        # capital tonos stands left of the letter at cap height (positioned by the assembler)
        P = g.P
        mh = P.cap * 0.26
        run = mh * 0.30
        tb = z.t * 0.40; tt = z.t * 0.66
        g.poly([(0 - tb, P.cap - mh), (0 + tb, P.cap - mh), (run + tt, P.cap), (run - tt, P.cap)])


@top_mark('dieresistonoscomb', None)
def dieresistonos(g, z):
    P = g.P; d = P.dotd * 0.82
    cy = z.y0 + d * 0.5
    off = d * 0.5 + z.mh * 0.62 + z.t * 0.75
    g.dot(-off, cy, d); g.dot(off, cy, d)
    acute_shape(g, z, steep=2.2, f=1.0)


MARK_BY_CP[0x301] = 'acutecomb'
# Greek capitals never carry dialytika-tonos: drop the unused capital form
from .parts import ORDER as _ORDER
del REG['dieresistonoscomb.case']; _ORDER.remove('dieresistonoscomb.case'); MARKS.discard('dieresistonoscomb.case')


# ------------------------------------------------------------ Vietnamese stacks
STACKS = {}


def stack(cps, lower, upper, side):
    name = 'uni%04X%04X' % cps

    @top_mark(name, None)
    def st(g, z):
        if lower == 'circ':
            top = circ_shape(g, z)
        else:
            top = breve_shape(g, z)
        gapv = z.gap * (0.30 if not z.case else 0.26) * (1.0 + 1.2 * wt(g.P))
        f = 0.86
        if upper in ('acute', 'grave'):
            sg = 1 if upper == 'acute' else -1
            if lower == 'circ':     # beside the apex: the compact Vietnamese arrangement
                return acute_shape(g, z, x=sg * (z.mh * (1.02 if not z.case else 1.42) + z.t * 0.30), y=z.y0 + z.mh * 0.50, sign=sg, f=f)
            return acute_shape(g, z, x=sg * z.mh * 0.05, y=top + gapv, sign=sg, f=f)
        if upper == 'hook':
            return hook_shape(g, z, y=top + gapv * 0.8, f=f)
        return tilde_shape(g, z, y=top + gapv, f=f)
    STACKS[cps] = name


stack((0x302, 0x301), 'circ', 'acute', 1); stack((0x302, 0x300), 'circ', 'grave', -1)
stack((0x302, 0x309), 'circ', 'hook', 0); stack((0x302, 0x303), 'circ', 'tilde', 0)
stack((0x306, 0x301), 'breve', 'acute', 0); stack((0x306, 0x300), 'breve', 'grave', 0)
stack((0x306, 0x309), 'breve', 'hook', 0); stack((0x306, 0x303), 'breve', 'tilde', 0)


# ------------------------------------------------------------ marks below / attached
def below_mark(name, cp, anchor='bottom'):
    def deco(fn):
        def m(g):
            bot = fn(g)
            g.w = 0.0
            g.anchor('_' + anchor, 0.0, 0.0)
            if anchor == 'bottom':
                g.anchor('bottom', 0.0, (bot if bot is not None else -150.0) + 14)
        glyph(name, cp)(m)
        MARKS.add(name)
        MARK_BY_CP[cp] = name
        return fn
    return deco


def gap_b(P): return 60 - 28 * wt(P)


@below_mark('dotbelowcomb', 0x323)
def dotbelow(g):
    P = g.P; d = P.dotd * (0.96 - 0.22 * wt(P))
    g.dot(0, -gap_b(P) - d / 2, d)
    return -gap_b(P) - d


@below_mark('commaaccentcomb', 0x326)
def commaaccent(g):
    P = g.P; d = P.dotd * (0.84 - 0.30 * wt(P))
    comma_shape(g, 0, -gap_b(P) - d / 2, d)
    return -gap_b(P) - d * 1.92


@below_mark('macronbelowcomb', 0x331)
def macronbelow(g):
    P = g.P
    w = P.xh * 0.36 + P.acc * 0.4; t = P.acc * 0.86
    g.rect(-w / 2, -gap_b(P) - t, w / 2, -gap_b(P))
    return -gap_b(P) - t


@below_mark('cedillacomb', 0x327)
def cedilla(g):
    P = g.P
    t = P.acc * 0.92
    D = 150.0 + P.acc * 0.22
    r = D * 0.36
    g.stroke([N(0, 10, 270, t * 0.70, line=True), N(0, -D * 0.24, 270, t * 0.70), N(r * 0.95, -D * 0.60, 270, t),
              N(-r * 0.05, -D + t * 0.42, 180, t * 0.84), N(-r * 1.05, -D * 0.74, 124, t * 0.72)], k=0.58)
    return -D


@below_mark('ogonekcomb', 0x328, 'ogonek')
def ogonek(g):
    P = g.P
    t = P.acc * 0.92
    D = 150.0 + P.acc * 0.22
    r = D * 0.50
    g.stroke([N(r * 0.12, 30, 238, t * 0.86), N(-r * 0.86, -D * 0.52, 270, t), N(-r * 0.05, -D + t * 0.45, 0, t * 0.86),
              N(r * 0.72, -D * 0.84, 22, t * 0.72)], k=0.58)


def _horn(name, case):
    def m(g):
        P = g.P
        t = (P.H if case else P.h) * 0.92
        r = (P.cap * 0.115 if case else P.xh * 0.135) + t * 0.25
        g.stroke([N(-t * 0.5, -t * 0.25, 8, t), N(r, r * 0.92, 90, t * 0.86, line=True), N(r, r * 1.22, 90, t * 0.86)], k=0.60)
        g.w = 0.0
        g.anchor('_horn', 0.0, 0.0)
    glyph(name, [0x31B] if not case else None)(m)
    MARKS.add(name)


_horn('horncomb', False); _horn('horncomb.case', True)
MARK_BY_CP[0x31B] = 'horncomb'


@glyph('caroncomb.alt')
def caron_alt(g):
    """Apostrophe-shaped caron of d, t, l, L."""
    P = g.P
    t = P.acc
    hgt = P.xh * 0.33
    g.poly([(0, P.asc - hgt), (t * 0.62, P.asc - hgt), (t * 1.55, P.asc), (t * 0.40, P.asc)])
    g.w = 0.0


MARKS.add('caroncomb.alt')


# ------------------------------------------------------------ spacing accents
def spacing(name, cp, comb, below=False):
    @glyph(name, cp)
    def sp(g):
        P = g.P
        probe = G(P); REG[comb][0](probe)
        b = probe.bounds()
        sbq = P.so * 1.25
        g.comp(comb, sbq - b[0], 0)
        g.w = (b[2] - b[0]) + 2 * sbq
    return sp


spacing('grave', 0x60, 'gravecomb'); spacing('acute', 0xB4, 'acutecomb'); spacing('circumflex', 0x2C6, 'circumflexcomb')
spacing('tilde', 0x2DC, 'tildecomb'); spacing('macron', 0xAF, 'macroncomb'); spacing('breve', 0x2D8, 'brevecomb')
spacing('dotaccent', 0x2D9, 'dotaccentcomb'); spacing('dieresis', 0xA8, 'dieresiscomb'); spacing('ring', 0x2DA, 'ringcomb')
spacing('hungarumlaut', 0x2DD, 'hungarumlautcomb'); spacing('caron', 0x2C7, 'caroncomb')
spacing('cedilla', 0xB8, 'cedillacomb'); spacing('ogonek', 0x2DB, 'ogonekcomb')
spacing('tonos', 0x384, 'tonoscomb'); spacing('dieresistonos', 0x385, 'dieresistonoscomb')
