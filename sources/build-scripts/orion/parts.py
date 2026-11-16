"""Shared construction parts for Orion glyphs (stems, arches, bowls, terminals)."""
from __future__ import annotations
import math
from .geom import N, E, Line, add, sub, mul, unit, G

REG = {}      # glyph name -> (fn, [unicodes])
ORDER = []
UPPER = set() # glyph names that take capital (.case) marks and capital metrics


def glyph(name, uni=None, upper=None):
    import unicodedata
    def deco(fn):
        u = [] if uni is None else ([uni] if isinstance(uni, int) else list(uni))
        REG[name] = (fn, u)
        if name not in ORDER:
            ORDER.append(name)
        up = upper
        if up is None:
            up = any(unicodedata.category(chr(c)) == 'Lu' for c in u)
        if up or name in ('I.ss01',):
            UPPER.add(name)
        return fn
    return deco


def clamp(x, a, b): return max(a, min(b, x))


class S:
    """Stroke set for a case: U (capitals / figures) or L (lowercase)."""
    def __init__(self, P, upper):
        self.upper = upper
        if upper:
            self.v0, self.v, self.h0, self.h, self.o0, self.o = P.V0, P.V, P.H0, P.H, P.Vo0, P.Vo
            self.d = P.Dg; self.d0 = P.V0 * 0.985
        else:
            self.v0, self.v, self.h0, self.h, self.o0, self.o = P.v0, P.v, P.h0, P.h, P.vo0, P.vo
            self.d = P.dg; self.d0 = P.v0 * 0.985
        self.j0 = P.jf * self.v0 * 0.94; self.j = P.jf * self.v * 0.94


def round_nodes(P, x0, x1, y0, y1, upper=False, fl=1.0, fr=1.0, ft=1.0, fb=1.0, cx=None, tl=None, tr=None):
    """Four extreme nodes of a round (counter-clockwise travel).
    x0/x1 are the ungraded outer extremes; y0/y1 the outer vertical extremes.
    Horizontal walls keep their centre line under grade, vertical extremes keep
    their outer edge, so GRAD never moves metrics."""
    s = S(P, upper)
    tl0 = s.o0 * fl; tr0 = s.o0 * fr
    tlg = s.o * fl if tl is None else tl
    trg = s.o * fr if tr is None else tr
    tt = s.h * ft; tb = s.h * fb
    cx = (x0 + x1) / 2.0 if cx is None else cx
    cy = ((y0 + tb) + (y1 - tt)) / 2.0          # extremes sit at the counter's centre
    return dict(
        r=N(x1 - tr0 / 2, cy, 90, trg), t=N(cx, y1 - tt / 2, 180, tt),
        l=N(x0 + tl0 / 2, cy, 270, tlg), b=N(cx, y0 + tb / 2, 0, tb),
        cx=cx, cy=cy, rx=(x1 - x0) / 2 - (tl0 + tr0) / 4, ry=(y1 - y0) / 2 - (tt + tb) / 4,
        rxi=(x1 - x0) / 2 - (tl0 + tr0) / 2, ryi=(y1 - y0) / 2 - (tt + tb) / 2,
        ki=P.ki((x1 - x0) / 2 - (tl0 + tr0) / 2, (y1 - y0) / 2 - (tt + tb) / 2))


def term(rn, theta, P):
    """Terminal cut: a straight face starting at the inner (counter) edge at
    polar angle theta about the round's centre.  Anchoring on the counter edge
    makes the aperture explicit in every weight.  The face leans 18 degrees
    off vertical in light and regular weights and rotates toward the stroke
    normal as weight shrinks the counters (so heavy terminals stay blunt)."""
    th = theta % 360.0
    if th < 90: al, quad = th, 1
    elif th < 180: al, quad = 180 - th, 2
    elif th < 270: al, quad = th - 180, 3
    else: al, quad = 360 - th, 4
    u = clamp(P.wt, 0, 1) ** 1.3
    F = 72.0 * (1 - u) + min(72.0, al + 8.0) * u
    fa = {1: F, 2: 180 - F, 3: F, 4: -F}[quad]
    r = math.radians(theta)
    c, s_ = math.cos(r), math.sin(r)
    n = 2.35
    rad = (abs(c) ** n + abs(s_) ** n) ** (-1.0 / n)
    p = (rn['cx'] + max(6.0, rn.get('rxi', rn['rx'])) * c * rad, rn['cy'] + max(6.0, rn.get('ryi', rn['ry'])) * s_ * rad)
    return ('line', p, fa)


def ring(g, x0, x1, y0, y1, upper=False, **kw):
    rn = round_nodes(g.P, x0, x1, y0, y1, upper, **kw)
    g.stroke([rn['r'], rn['t'], rn['l'], rn['b']], closed=True, kL=rn['ki'])
    return rn


def arch(g, xs, xr, top, upper=False, stem_to=0.0, cut=None, shift=0.03, href=None, ft=1.0, fr=1.0,
         r_line=True, deep=0.14, lo=0.30, hi=0.43, end=None):
    """Arch springing from the stem centred at xs and descending the stem at xr.
    The branch is thinned and buried in the stem (see Params.jf, Params.bury)."""
    P = g.P; s = S(P, upper)
    href = P.xh if href is None else href
    xin = xs + s.v0 / 2 - P.bury * s.v0            # counter's left extreme
    x0 = xin - s.j0 / 2
    outer_r = ((xr + s.v0 / 2) - (xin - s.j0)) / 2
    ry = clamp(outer_r, lo * href, hi * href)
    ys = top - ry
    cx = (xin + xr - s.v0 / 2) / 2 + shift * (xr - xs)
    h = s.h * ft
    ki = P.ki((xr - s.v0 / 2 - xin) / 2, ry - h)
    nodes = [N(x0, ys - deep * ry, 90, s.j), N(cx, top - h / 2, 0, h)]
    if cut is not None:
        nodes.append(N(xr, ys, -90, s.v * fr))
        g.stroke(nodes, cut1=cut, kR=ki)
    else:
        nodes.append(N(xr, ys, -90, s.v * fr, line=True))
        nodes.append(N(xr, stem_to, -90, s.v * fr))
        if end is not None:
            nodes[-1] = end
        g.stroke(nodes, kR=ki)
    return dict(cx=cx, ys=ys, ry=ry, xin=xin)


def bowl(g, xs, y0, y1, cw, upper=False, ft=1.0, fb=1.0):
    """Round bowl on the right of a stem centred at xs; cw = counter width."""
    P = g.P; s = S(P, upper)
    xin = xs + s.v0 / 2 - P.bury * s.v0
    x0 = xin - s.j0
    x1 = xin + cw + s.o0
    rn = round_nodes(P, x0, x1, y0, y1, upper, fl=P.jf, ft=ft, fb=fb, cx=xin + cw / 2)
    g.stroke([rn['r'], rn['t'], rn['l'], rn['b']], closed=True, kL=rn['ki'])
    return x1


def sline(pa, sa, pb, sb_, t0):
    """Centre line of a straight stroke of thickness t0 whose edge on side sa
    (-1 left edge, 0 centre, +1 right edge; measured horizontally) passes
    through pa, and whose edge on side sb_ passes through pb."""
    a, b = pa, pb
    for _ in range(4):
        ln = Line(a, b)
        hw = ln.hw(t0) / 2
        a = (pa[0] - sa * hw, pa[1]); b = (pb[0] - sb_ * hw, pb[1])
    return Line(a, b)


def edges(ln, t):
    """Left and right edges (shifted horizontally) of a stroke along ln."""
    hw = ln.hw(t) / 2
    return Line((ln.p[0] - hw, ln.p[1]), d=ln.d), Line((ln.p[0] + hw, ln.p[1]), d=ln.d)


def diag(g, pa, pb, t, sa=0, sb_=0, t0=None):
    """Straight stroke with horizontal cuts at both ends."""
    ln = sline(pa, sa, pb, sb_, t if t0 is None else t0)
    l, r = edges(ln, t)
    g.poly([l.at_y(pa[1]), r.at_y(pa[1]), r.at_y(pb[1]), l.at_y(pb[1])])
    return ln


def vee(g, x0, x1, y_open, y_apex, t, t0, apex, cx=None, bar=None, draw=True):
    """V construction (or inverted when y_open < y_apex): two straight strokes
    meeting in a flat apex of width `apex`. Returns the centre lines."""
    cx = (x0 + x1) / 2 if cx is None else cx
    cl = sline((x0, y_open), -1, (cx - apex / 2, y_apex), -1, t0)
    cr = sline((x1, y_open), +1, (cx + apex / 2, y_apex), +1, t0)
    ll, lr = edges(cl, t); rl, rr = edges(cr, t)
    crotch = lr & rl
    # keep the crotch on the open side of the apex line for every master
    lim = y_apex + (y_open - y_apex) * 0.04
    if (y_open > y_apex and crotch[1] < lim) or (y_open < y_apex and crotch[1] > lim):
        crotch = (crotch[0], lim)
    if draw:
        g.poly([ll.at_y(y_open), lr.at_y(y_open), crotch, rl.at_y(y_open), rr.at_y(y_open),
                rr.at_y(y_apex), ll.at_y(y_apex)])
    return cl, cr, crotch


def hook(g, xs, y_from, y_turn, x_end, y_edge, upper=False, cutface=None, fend=1.0, k=None, th_end=None):
    """Stem that turns into a horizontal run (tails of l, t, j, f, J ...).
    Travels from (xs, y_from) to y_turn, turns, and reaches x_end with its outer
    edge resting on y_edge.  The turn radius adapts to stroke weight."""
    P = g.P; s = S(P, upper)
    up = y_edge > y_from if abs(y_from - y_turn) < 40 else y_from < y_turn
    right = x_end > xs
    h = (s.h if th_end is None else th_end) * fend
    yc = y_edge + h / 2 if y_edge <= min(y_from, y_turn) else y_edge - h / 2
    a0 = 90 if up else -90
    a1 = 0 if right else 180
    # the straight run must keep its direction even when a heavy turn needs more room
    if up and y_from > y_turn - 2: y_from = y_turn - 2
    if not up and y_from < y_turn + 2: y_from = y_turn + 2
    nodes = [N(xs, y_from, a0, s.v, line=True), N(xs, y_turn, a0, s.v), N(x_end, yc, a1, h)]
    g.stroke(nodes, k=P.k if k is None else k)
