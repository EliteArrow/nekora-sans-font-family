"""Orion — Latin lowercase."""
from __future__ import annotations
from .geom import N, E, Line, G
from .parts import glyph, S, round_nodes, term, ring, arch, bowl, sline, edges, diag, vee, hook, clamp



def top(P): return P.xh + P.os
def bot(P): return -P.os
def cwl(P): return (P.ow - 2 * P.vo0) * 0.985      # bowl counter width (b d p q g)


def dot_y(P, base=None):
    base = P.xh if base is None else base
    gap = 88 - 46 * clamp(P.wt, 0, 1)
    return base + gap + P.dotd / 2


@glyph('o', 0x6F)
def o(g):
    P = g.P
    ring(g, P.so, P.so + P.ow, bot(P), top(P))
    g.w = P.ow + 2 * P.so


def n_body(g, tall=False):
    P = g.P; s = S(P, False)
    xl = P.sb + s.v0 / 2; xr = P.sb + P.nw - s.v0 / 2
    g.vstem(xl, 0, P.asc if tall else P.xh, s.v)
    arch(g, xl, xr, top(P))
    g.w = P.nw + P.sb * 1.93
    return xl, xr


@glyph('n', 0x6E)
def n(g): n_body(g)


@glyph('h', 0x68)
def h(g):
    n_body(g, True)
    g.anchor('top', g.P.sb + g.P.v0 / 2, g.P.asc)


@glyph('m', 0x6D)
def m(g):
    P = g.P; s = S(P, False)
    pitch = (P.nw - s.v0) * (0.925 - 0.03 * P.wt)
    xl = P.sb + s.v0 / 2; xm = xl + pitch; xr = xm + pitch
    g.vstem(xl, 0, P.xh, s.v)
    arch(g, xl, xm, top(P), lo=0.27)
    arch(g, xm, xr, top(P), lo=0.27)
    g.w = xr + s.v0 / 2 + P.sb * 0.93


@glyph('u', 0x75)
def u(g):
    P = g.P
    w = P.nw + P.sb * 1.93
    with g.rot180(w / 2, P.xh / 2):
        n_body(g)
    g.w = w


@glyph('r', 0x72)
def r(g):
    P = g.P; s = S(P, False)
    xl = P.sb + s.v0 / 2
    span = (P.nw - s.v0) * (0.86 + 0.06 * P.wt)
    xr = xl + span
    g.vstem(xl, 0, P.xh, s.v)
    # arm: arch trimmed by a vertical face
    xin = xl + s.v0 / 2 - P.bury * s.v0
    cx = (xin + xr - s.v0 / 2) / 2
    xcut = cx + (xr - s.v0 / 2 - cx) * (0.60 + 0.10 * P.wt)
    arch(g, xl, xr, top(P), cut=('x', xcut), shift=0.0, fr=0.92)
    g.w = xcut + P.so * 0.58
    g.anchor('top', (xl + xcut) / 2 + s.v0 * 0.1, P.xh)
    g.anchor('bottom', xl, 0)


@glyph('dotlessi', 0x131)
def dotlessi(g):
    P = g.P
    g.vstem(P.sb + P.v0 / 2, 0, P.xh, P.v)
    g.w = P.v0 + 2 * P.sb


@glyph('i', 0x69)
def i(g):
    P = g.P
    dotlessi(g)
    g.dot(P.sb + P.v0 / 2, dot_y(P), P.dotd)


def j_body(g):
    P = g.P; s = S(P, False)
    reach = (P.nw - s.v0) * 0.36 + s.v0 * 0.25
    xs = P.sb * 0.9 + reach * 0.42 + s.v0 / 2
    hook(g, xs, P.xh, P.desc + (P.nw - s.v0) * 0.42 + s.h / 2, xs - reach, P.desc)
    g.w = xs + s.v0 / 2 + P.sb
    return xs


@glyph('dotlessj', 0x237)
def dotlessj(g): j_body(g)


@glyph('j', 0x6A)
def j(g):
    P = g.P
    xs = j_body(g)
    g.dot(xs, dot_y(P), P.dotd)


@glyph('l', 0x6C)
def l(g):
    """Default l carries a tail so that I, l and 1 never share a silhouette."""
    P = g.P; s = S(P, False)
    xs = P.sb + s.v0 / 2
    tail = (P.nw - s.v0) * 0.27
    hook(g, xs, P.asc, P.xh * 0.34 + s.h / 2, xs + s.v0 / 2 + tail, 0)
    g.w = xs + s.v0 / 2 + tail + P.so * 0.9
    g.anchor('top', xs, P.asc); g.anchor('bottom', xs + tail * 0.4, 0)


@glyph('l.ss02')
def l_plain(g):
    P = g.P
    g.vstem(P.sb + P.v0 / 2, 0, P.asc, P.v)
    g.w = P.v0 + 2 * P.sb


@glyph('t', 0x74)
def t(g):
    P = g.P; s = S(P, False)
    left = (P.nw - s.v0) * 0.27
    tail = (P.nw - s.v0) * 0.36
    xs = P.so * 0.7 + left + s.v0 / 2
    ytop = P.xh + (P.asc - P.xh) * 0.62
    x_end = xs + s.v0 / 2 + tail
    slant = s.v * 0.30
    nodes = [E((xs + s.v / 2, ytop), (xs - s.v / 2, ytop - slant), -90, line=True),
             N(xs, P.xh * 0.33 + s.h / 2, -90, s.v), N(x_end, s.h / 2, 0, s.h)]
    g.stroke(nodes)
    g.rect(xs - s.v0 / 2 - left, P.xh - s.h, x_end - s.v0 * 0.04, P.xh)
    g.w = x_end + P.so * 0.75
    g.anchor('top', xs, ytop); g.anchor('bottom', xs + tail * 0.45, 0)


@glyph('f', 0x66)
def f(g):
    P = g.P; s = S(P, False)
    left = (P.nw - s.v0) * 0.24
    reach = (P.nw - s.v0) * 0.40
    xs = P.so * 0.7 + left + s.v0 / 2
    x_end = xs + s.v0 / 2 + reach
    hook(g, xs, 0, P.asc - (P.nw - s.v0) * 0.40 - s.h / 2, x_end, P.asc + P.os * 0.4)
    g.rect(xs - s.v0 / 2 - left, P.xh - s.h, x_end - s.v0 * 0.10, P.xh)
    g.w = x_end + P.so * 0.2
    g.anchor('top', xs + reach * 0.3, P.asc); g.anchor('bottom', xs, 0)


def theta_c(P): return 44.0 + 14.0 * (P.ap - 1.0)
def theta_e(P): return 33.0 + 14.0 * (P.ap - 1.0)


@glyph('c', 0x63)
def c(g):
    P = g.P
    rn = round_nodes(P, P.so, P.so + P.ow * 0.985, bot(P), top(P))
    th = theta_c(P)
    g.stroke([rn['r'], rn['t'], rn['l'], rn['b'], rn['r']], cut0=term(rn, th, P), cut1=term(rn, -th, P), kL=rn['ki'])
    g.w = g.bounds()[2] + P.so * 0.50
    g.anchor('top', rn['cx'] + P.ow * 0.02, P.xh); g.anchor('bottom', rn['cx'] + P.ow * 0.02, 0)


@glyph('e', 0x65)
def e(g):
    P = g.P; s = S(P, False)
    x0 = P.so; x1 = P.so + P.ow * 0.975
    wt = clamp(P.wt, 0, 1)
    rn = round_nodes(P, x0, x1, bot(P), top(P), ft=1.0 - 0.12 * wt, fb=1.0 - 0.04 * wt)
    hb = s.h * (0.96 - 0.26 * wt)
    ybb = rn['cy'] - hb * 0.42
    start = N(x1 - s.o0 / 2, ybb, 90, s.o, line=True)
    g.stroke([start, rn['r'], rn['t'], rn['l'], rn['b'], rn['r']], cut1=term(rn, -theta_e(P), P), kL=rn['ki'])
    g.rect(x0 + s.o0 * 0.5, ybb, x1 - s.o0 * 0.5, ybb + hb)
    g.w = x1 + P.so * 0.92
    g.anchor('top', rn['cx'], P.xh); g.anchor('bottom', rn['cx'], 0)


@glyph('a', 0x61)
def a(g):
    P = g.P; s = S(P, False)
    aw = P.nw * 0.95
    lsb = P.so * 1.12
    xr = lsb + aw - s.v0 / 2
    xlv = lsb + aw * 0.045
    outer_r = (xr + s.v0 / 2 - xlv) / 2
    ry = clamp(outer_r * 0.92, 0.27 * P.xh, 0.40 * P.xh)
    ysh = top(P) - ry
    cxt = (xlv + xr) / 2 + s.v0 * 0.10
    tv = s.o * 0.90
    rn = dict(cx=cxt, cy=ysh, rx=cxt - (xlv + s.o0 * 0.9), ry=ry - s.h)
    th = 180 - (30.0 + 12.0 * (P.ap - 1.0))
    wt = clamp(P.wt, 0, 1)
    ha = s.h * (1.0 - 0.10 * wt)
    g.stroke([N(xr, 0, 90, s.v, line=True), N(xr, ysh, 90, s.v), N(cxt, top(P) - ha / 2, 180, ha),
              N(xlv + s.o0 * 0.45, ysh, 270, tv)], cut1=term(rn, th, P))
    # bowl: asymmetric — flat into the stem, round on the left
    ybt = P.xh * (0.585 + 0.035 * wt)
    hbt = s.h * (0.92 - 0.28 * wt)
    xin = xr - s.v0 / 2 + P.bury * s.v0
    cyb = (ybt + bot(P)) / 2
    cwid = xin - (lsb + s.o0)
    nodes = [N(xin + s.j0 / 2, cyb, 90, s.j), N(xin - cwid * 0.20, ybt - hbt / 2, 180, hbt),
             N(lsb + s.o0 / 2, cyb - (ybt - bot(P)) * 0.03, 270, s.o * (1.0 - 0.06 * wt)),
             N(lsb + s.o0 + cwid * 0.52, bot(P) + s.h * (1.0 - 0.10 * wt) / 2, 0, s.h * (1.0 - 0.10 * wt))]
    g.stroke(nodes, closed=True)
    g.w = xr + s.v0 / 2 + P.sb * 0.90
    g.anchor('top', cxt - s.v0 * 0.1, P.xh); g.anchor('bottom', (lsb + xr) / 2, 0)
    g.anchor('ogonek', xr + s.v0 / 2, 0)


@glyph('a.ss03')
def a_single(g):
    P = g.P; s = S(P, False)
    lsb = P.so
    xin_to_right = cwl(P)
    # bowl on the left of the stem
    xr = lsb + s.o0 + xin_to_right - P.bury * s.v0 + s.v0 / 2
    with g.flip_x(xr):
        bowl(g, xr, bot(P), top(P), cwl(P))
    g.vstem(xr, 0, P.xh, s.v)
    g.w = xr + s.v0 / 2 + P.sb


@glyph('s', 0x73)
def s_(g):
    P = g.P; s = S(P, False)
    s_shape(g, P.so * 1.05, P.ow * (0.745 + 0.03 * clamp(P.wt, 0, 1)), bot(P), top(P), s, P.xh)
    g.w = g.bounds()[2] + P.so * 0.98


def s_shape(g, x0, w, y0, y1, s, href, upper=False, sym=False):
    """S construction shared by s, S and the dollar sign: two rounds joined
    by a spine that runs fairly flat through the centre."""
    P = g.P
    wt = clamp(P.wt, 0, 1)
    H = y1 - y0
    ht = s.h * (0.98 - 0.20 * wt)                       # top / bottom arcs
    sp = s.o * (1.02 - 0.22 * wt)                       # spine
    cy = y0 + H * (0.5 if sym else 0.512)
    x1 = x0 + w
    xul = x0 + w * 0.035; xur = x1 - w * 0.055          # upper round is narrower
    if sym:
        xul, xur = x0, x1
    xll = x0; xlr = x1
    tv = s.o * (0.97 - 0.11 * wt)
    te = tv * 0.95
    # round extremes sit at the centre of each counter
    yuc = ((y1 - ht) + (cy + sp * 0.56)) / 2
    ylc = ((y0 + ht) + (cy - sp * 0.56)) / 2
    cx = (x0 + x1) / 2
    ang = -(21.0 - 5.0 * wt + (5.0 if not upper else 0.0))
    # terminal anchors: on the counter edge, but never closer to the centre than 40 % of the outer radius,
    # so that heavy weights (tiny counters) keep full-length arms instead of stubs
    ru = dict(cx=(xul + xur) / 2, cy=yuc, rx=max((xur - xul) / 2 - s.o0, 0.36 * (xur - xul) / 2), ry=max((y1 - yuc) - ht, 0.36 * (y1 - yuc)))
    rl = dict(cx=(xll + xlr) / 2, cy=ylc, rx=max((xlr - xll) / 2 - s.o0, 0.36 * (xlr - xll) / 2), ry=max((ylc - y0) - ht, 0.36 * (ylc - y0)))
    thu = 47.0 + 10.0 * (P.ap - 1.0) 
    thl = 180 + 44.0 + 10.0 * (P.ap - 1.0) 
    nodes = [N(xur - s.o0 / 2, yuc, 90, te),
             N(ru['cx'] + w * 0.015, y1 - ht / 2, 180, ht),
             N(xul + s.o0 / 2, yuc, 270, tv),
             N(cx, cy, ang, sp),
             N(xlr - s.o0 / 2, ylc, 270, tv),
             N(rl['cx'] - w * 0.015, y0 + ht / 2, 180, ht),
             N(xll + s.o0 / 2, ylc, 90, te)]
    g.stroke(nodes, cut0=term(ru, thu, P), cut1=term(rl, thl, P))
    g.anchor('top', cx, href); g.anchor('bottom', cx, 0)


def bd_body(g, tall, down):
    """b-type glyph: stem at left, bowl at right. d, p, q are reflections."""
    P = g.P; s = S(P, False)
    xs = P.sb + s.v0 / 2
    g.vstem(xs, P.desc if down else 0, P.asc if tall else P.xh, s.v)
    x1 = bowl(g, xs, bot(P), top(P), cwl(P))
    g.w = x1 + P.so
    return xs, x1


@glyph('b', 0x62)
def b(g):
    xs, x1 = bd_body(g, True, False)
    g.anchor('top', xs, g.P.asc)


@glyph('p', 0x70)
def p(g): bd_body(g, False, True)


@glyph('d', 0x64)
def d(g):
    P = g.P
    probe = G(P); xs, x1 = bd_body(probe, True, False)
    w = probe.w
    with g.flip_x(w / 2):
        bd_body(g, True, False)
    g.w = w
    g.anchor('top', w - xs, P.asc)


@glyph('q', 0x71)
def q(g):
    P = g.P
    probe = G(P); bd_body(probe, False, True)
    w = probe.w
    with g.flip_x(w / 2):
        bd_body(g, False, True)
    g.w = w


@glyph('g', 0x67)
def g_(g):
    P = g.P; s = S(P, False)
    lsb = P.so
    xr = lsb + s.o0 + cwl(P) - P.bury * s.v0 + s.v0 / 2
    with g.flip_x(xr):
        bowl(g, xr, bot(P), top(P), cwl(P))
    # stem and descending hook
    xlv = lsb + (xr - lsb) * 0.07
    cxh = (xlv + xr) / 2
    ry = clamp((xr - xlv) / 2 * 0.95, 0.22 * P.xh, 0.36 * P.xh)
    y_turn = P.desc + ry
    rn = dict(cx=cxh, cy=y_turn, rx=cxh - (xlv + s.o0 * 0.9), ry=ry - s.h)
    th = 180 + 36.0 + 12.0 * (P.ap - 1.0)
    g.stroke([N(xr, P.xh, -90, s.v, line=True), N(xr, y_turn, -90, s.v), N(cxh, P.desc + s.h / 2, 180, s.h),
              N(xlv + s.o0 * 0.45, y_turn, 90, s.o * 0.9)], cut1=term(rn, th, P))
    g.w = xr + s.v0 / 2 + P.sb
    g.anchor('top', lsb + (xr - lsb) * 0.5, P.xh)


@glyph('k', 0x6B)
def k(g):
    P = g.P; s = S(P, False)
    xs = P.sb + s.v0 / 2
    g.vstem(xs, 0, P.asc, s.v)
    k_arms(g, xs, s, P.xh, (P.nw - s.v0) * 1.04 + s.v0 * 0.3)
    g.w = g.bounds()[2] + P.sd * 0.6
    g.anchor('top', xs, P.asc)


def k_arms(g, xs, s, height, reach):
    P = g.P
    wt = clamp(P.wt, 0, 1)
    xe = xs + s.v0 / 2
    ta = s.d * (0.94 - 0.08 * wt); tl = s.d * (1.0 - 0.04 * wt)
    ta0 = s.d0 * (0.94 - 0.08 * wt); tl0 = s.d0 * (1.0 - 0.04 * wt)
    # arm: lower edge leaves the stem at 31% of the height
    arm = sline((xe - s.v0 * 0.5, height * 0.31), +1, (xe + reach * 0.93, height), +1, ta0)
    al, ar = edges(arm, ta)
    g.poly([al.at_x(xs), ar.at_x(xs), ar.at_y(height), al.at_y(height)])
    # leg: springs from the arm, ends on the baseline
    jx = xe + reach * (0.22 + 0.05 * wt)
    jy = arm.at_x(jx)[1]
    leg = sline((jx, jy + s.d0 * 0.4), 0, (xe + reach, 0), +1, tl0)
    ll, lr = edges(leg, tl)
    g.poly([ll.at_y(0), lr.at_y(0), lr & ar, ll & al])


@glyph('v', 0x76)
def v(g):
    P = g.P; s = S(P, False)
    w = P.nw * 1.07
    vee(g, P.sd, P.sd + w, P.xh, 0, s.d, s.d0, s.d0 * (0.86 - 0.26 * clamp(P.wt, 0, 1)))
    g.w = w + 2 * P.sd


def w_shape(g, x0, w, y1, s, mid_drop=0.0):
    """W: four straight strokes, flat apexes; inner strokes thinned in heavy weights."""
    P = g.P
    wt = clamp(P.wt, 0, 1)
    t_o, t_i = s.d * (1.0 - 0.06 * wt), s.d * (0.94 - 0.12 * wt)
    t_o0, t_i0 = s.d0 * (1.0 - 0.06 * wt), s.d0 * (0.94 - 0.12 * wt)
    ap = s.d0 * (0.80 - 0.30 * wt)
    apm = s.d0 * (0.74 - 0.30 * wt)
    x1 = x0 + w; xm = (x0 + x1) / 2
    xa1 = x0 + w * 0.272; xa2 = x1 - w * 0.272
    ym = y1 - mid_drop
    c1 = sline((x0, y1), -1, (xa1 - ap / 2, 0), -1, t_o0)
    c2 = sline((xa1 + ap / 2, 0), +1, (xm - apm / 2, ym), -1, t_i0)
    c3 = sline((xm + apm / 2, ym), +1, (xa2 - ap / 2, 0), -1, t_i0)
    c4 = sline((xa2 + ap / 2, 0), +1, (x1, y1), +1, t_o0)
    l1, r1 = edges(c1, t_o); l2, r2 = edges(c2, t_i); l3, r3 = edges(c3, t_i); l4, r4 = edges(c4, t_o)
    def lim_lo(p): return (p[0], max(p[1], y1 * 0.05))
    def lim_hi(p): return (p[0], min(p[1], ym - y1 * 0.05))
    g.poly([l1.at_y(y1), r1.at_y(y1), lim_lo(r1 & l2), l2.at_y(ym), r3.at_y(ym), lim_lo(r3 & l4),
            l4.at_y(y1), r4.at_y(y1), r4.at_y(0), l3.at_y(0), lim_hi(l3 & r2), r2.at_y(0), l1.at_y(0)])


@glyph('w', 0x77)
def w(g):
    P = g.P; s = S(P, False)
    w_ = P.nw * (1.66 + 0.06 * clamp(P.wt, 0, 1))
    w_shape(g, P.sd, w_, P.xh, s)
    g.w = w_ + 2 * P.sd


def x_shape(g, x0, w, y1, s, top_in=0.035):
    P = g.P
    wt = clamp(P.wt, 0, 1)
    t = s.d * (0.98 - 0.06 * wt); t0 = s.d0 * (0.98 - 0.06 * wt)
    x1 = x0 + w
    ti = w * top_in
    a = sline((x0, 0), -1, (x1 - ti, y1), +1, t0)      # rising stroke
    b = sline((x0 + ti, y1), -1, (x1, 0), +1, t0)      # falling stroke
    al, ar = edges(a, t); bl, br = edges(b, t)
    g.poly([al.at_y(0), ar.at_y(0), ar.at_y(y1), al.at_y(y1)])
    g.poly([bl.at_y(0), br.at_y(0), br.at_y(y1), bl.at_y(y1)])


@glyph('x', 0x78)
def x(g):
    P = g.P; s = S(P, False)
    w_ = P.nw * 1.04
    x_shape(g, P.sd * 1.1, w_, P.xh, s)
    g.w = w_ + 2.2 * P.sd


@glyph('y', 0x79)
def y(g):
    P = g.P; s = S(P, False)
    w_ = P.nw * 1.07
    x0 = P.sd; x1 = x0 + w_
    ap = s.d0 * (0.86 - 0.26 * clamp(P.wt, 0, 1))
    cl, cr, crotch = vee(g, x0, x1, P.xh, 0, s.d, s.d0, ap, draw=False)
    ll, lr = edges(cl, s.d); rl, rr = edges(cr, s.d)
    g.poly([rr.at_y(P.xh), rl.at_y(P.xh), crotch, lr.at_y(P.xh), ll.at_y(P.xh), ll & rl,
            rl.at_y(P.desc), rr.at_y(P.desc)])
    g.w = w_ + 2 * P.sd
    g.anchor('top', (x0 + x1) / 2, P.xh); g.anchor('bottom', (x0 + x1) / 2 + w_ * 0.30, 0)


def z_shape(g, x0, w, y1, s, top_in=0.03):
    P = g.P
    wt = clamp(P.wt, 0, 1)
    h = s.h; t0 = s.d0 * (1.0 - 0.04 * wt); t = s.d * (1.0 - 0.04 * wt)
    x1 = x0 + w; xt0 = x0 + w * top_in
    c = sline((x0, h), -1, (x1, y1 - h), +1, t0)
    l, r = edges(c, t)
    ur = r.at_y(y1 - h); ur = (min(ur[0], x1), ur[1])
    ll_ = l.at_y(h); ll_ = (max(ll_[0], x0), ll_[1])
    g.poly([(x0, 0), (x1, 0), (x1, h), r.at_y(h), ur, (x1, y1), (xt0, y1), (xt0, y1 - h), l.at_y(y1 - h), ll_])


@glyph('z', 0x7A)
def z(g):
    P = g.P; s = S(P, False)
    w_ = P.nw * 0.96
    z_shape(g, P.so * 0.9, w_, P.xh, s)
    g.w = w_ + P.so * 1.8
