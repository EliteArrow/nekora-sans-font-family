"""Orion — Latin capitals and figures."""
from __future__ import annotations
from .geom import N, E, Line, G
from .parts import (glyph, S, round_nodes, term, ring, arch, bowl, sline, edges, diag, vee, hook, clamp)
from .latin_lc import s_shape, w_shape, x_shape, z_shape, k_arms


def U(P): return S(P, True)
def ctop(P): return P.cap + P.os
def cbot(P): return -P.os
def wtc(P): return clamp(P.wt, 0, 1)


# ------------------------------------------------------------ straight caps
@glyph('H', 0x48)
def H(g):
    P = g.P; s = U(P)
    xl = P.SB + s.v0 / 2; xr = P.SB + P.Hw - s.v0 / 2
    g.vstem(xl, 0, P.cap, s.v); g.vstem(xr, 0, P.cap, s.v)
    hb = s.h * 0.97
    g.rect(xl, P.cap * 0.525 - hb / 2, xr, P.cap * 0.525 + hb / 2)
    g.w = P.Hw + 2 * P.SB


@glyph('I', 0x49)
def I(g):
    P = g.P; s = U(P)
    g.vstem(P.SB + s.v0 / 2, 0, P.cap, s.v)
    g.w = s.v0 + 2 * P.SB


@glyph('I.ss01')
def I_serif(g):
    """Serifed I for the disambiguation set."""
    P = g.P; s = U(P)
    half = s.v0 * 0.5 + P.Hw * 0.17
    lsb = P.SB * 0.72
    xs = lsb + half
    hs = s.h * 0.92
    g.vstem(xs, 0, P.cap, s.v)
    g.rect(xs - half, 0, xs + half, hs)
    g.rect(xs - half, P.cap - hs, xs + half, P.cap)
    g.w = 2 * xs


def e_arms(g, xs, s, w, arms, mid=0.525):
    P = g.P
    x_in = xs - s.v0 / 2
    for kind in arms:
        if kind == 't':
            g.rect(xs, P.cap - s.h, x_in + w, P.cap)
        elif kind == 'b':
            g.rect(xs, 0, x_in + w * 1.02, s.h)
        elif kind == 'm':
            hm = s.h * 0.96
            g.rect(xs, P.cap * mid - hm / 2, x_in + w * 0.925, P.cap * mid + hm / 2)


@glyph('E', 0x45)
def E_(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2; w = P.Hw * 0.815
    g.vstem(xs, 0, P.cap, s.v)
    e_arms(g, xs, s, w, 'tmb')
    g.w = P.SB + w * 1.02 + P.SO * 0.82


@glyph('F', 0x46)
def F(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2; w = P.Hw * 0.79
    g.vstem(xs, 0, P.cap, s.v)
    e_arms(g, xs, s, w, 'tm', mid=0.50)
    g.w = P.SB + w + P.SO * 0.62
    g.anchor('bottom', xs, 0)


@glyph('L', 0x4C)
def L(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2; w = P.Hw * 0.765
    g.vstem(xs, 0, P.cap, s.v)
    g.rect(xs, 0, P.SB + w, s.h)
    g.w = P.SB + w + P.SO * 0.55
    g.anchor('top', xs, P.cap)


@glyph('T', 0x54)
def T(g):
    P = g.P; s = U(P)
    w = P.Hw * 1.02; lsb = P.SO * 0.62
    g.rect(lsb, P.cap - s.h, lsb + w, P.cap)
    g.vstem(lsb + w / 2, 0, P.cap, s.v)
    g.w = w + 2 * lsb


# ------------------------------------------------------------ round caps
@glyph('O', 0x4F)
def O(g):
    P = g.P
    ring(g, P.SO, P.SO + P.Ow, cbot(P), ctop(P), upper=True)
    g.w = P.Ow + 2 * P.SO


@glyph('Q', 0x51)
def Q(g):
    P = g.P; s = U(P)
    O(g)
    x1 = P.SO + P.Ow
    t = s.d * (0.96 - 0.10 * wtc(P))
    diag(g, (x1 - P.Ow * 0.40, P.cap * 0.235), (x1 + P.Ow * 0.015, -P.cap * 0.115), t, 0, +1, t0=s.d0 * (0.96 - 0.10 * wtc(P)))
    g.anchor('bottom', P.SO + P.Ow / 2, 0)


def tc(P): return 43.0 + 14.0 * (P.ap - 1.0)


@glyph('C', 0x43)
def C(g):
    P = g.P
    rn = round_nodes(P, P.SO, P.SO + P.Ow * 0.972, cbot(P), ctop(P), upper=True)
    th = tc(P)
    g.stroke([rn['r'], rn['t'], rn['l'], rn['b'], rn['r']], cut0=term(rn, th, P),
             cut1=term(rn, -th, P), kL=rn['ki'])
    g.w = g.bounds()[2] + P.SO * 0.56
    g.anchor('top', rn['cx'] + P.Ow * 0.02, P.cap); g.anchor('bottom', rn['cx'] + P.Ow * 0.02, 0)


@glyph('G', 0x47)
def G_(g):
    P = g.P; s = U(P)
    x0 = P.SO; x1 = P.SO + P.Ow * 0.985
    rn = round_nodes(P, x0, x1, cbot(P), ctop(P), upper=True)
    ybt = P.cap * 0.475
    hb = s.h * 0.97
    end = N(x1 - s.o0 / 2 - s.o0 * 0.02, ybt, 90, s.v)
    g.stroke([rn['r'], rn['t'], rn['l'], rn['b'], end], cut0=term(rn, tc(P) + 2, P), kL=rn['ki'])
    g.rect(rn['cx'] + P.Ow * 0.055, ybt - hb, x1 - s.o0 / 2, ybt)
    g.w = x1 + P.SO * 0.86
    g.anchor('top', rn['cx'] + P.Ow * 0.02, P.cap); g.anchor('bottom', rn['cx'] + P.Ow * 0.02, 0)


def d_bowl(g, xs, x1, y0, y1, s, ft=1.0, fb=1.0, fr=1.0, straight=0.16):
    """Bowl of D / B / P / R: bars leave the stem straight, then turn."""
    P = g.P
    ht = s.h * ft; hb = s.h * fb
    xin = xs + s.v0 / 2
    xc = xin + (x1 - s.o0 * fr - xin) * straight
    ryi = (y1 - y0) / 2 - (ht + hb) / 2
    ki = P.ki(x1 - s.o0 * fr - xc, ryi)
    g.stroke([N(xs, y1 - ht / 2, 0, ht, line=True), N(xc, y1 - ht / 2, 0, ht),
              N(x1 - s.o0 * fr / 2, ((y0 + hb) + (y1 - ht)) / 2, -90, s.o * fr),
              N(xc, y0 + hb / 2, 180, hb, line=True), N(xs, y0 + hb / 2, 180, hb)], kR=ki)


@glyph('D', 0x44)
def D(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2
    x1 = P.SB + P.Ow * 0.925
    g.vstem(xs, 0, P.cap, s.v)
    d_bowl(g, xs, x1, 0, P.cap, s, straight=0.10)
    g.w = x1 + P.SO
    g.anchor('top', (P.SB + x1) / 2 - P.Ow * 0.03, P.cap); g.anchor('bottom', (P.SB + x1) / 2 - P.Ow * 0.03, 0)


@glyph('B', 0x42)
def B(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2
    w = P.Hw * (0.90 + 0.02 * wtc(P))
    x1 = P.SB + w; x1u = P.SB + w * 0.945
    ym = P.cap * 0.528
    fm = 0.93 - 0.08 * wtc(P)
    hm = s.h * fm
    g.vstem(xs, 0, P.cap, s.v)
    d_bowl(g, xs, x1u, ym - hm / 2, P.cap, s, fb=fm, fr=0.96, straight=0.34)
    d_bowl(g, xs, x1, 0, ym + hm / 2, s, ft=fm, straight=0.30)
    g.w = x1 + P.SO * 0.92
    g.anchor('top', P.SB + w * 0.46, P.cap); g.anchor('bottom', P.SB + w * 0.46, 0)


@glyph('P', 0x50)
def P_(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2
    w = P.Hw * 0.885
    x1 = P.SB + w
    g.vstem(xs, 0, P.cap, s.v)
    d_bowl(g, xs, x1, P.cap * 0.415 - s.h * 0.45, P.cap, s, fb=0.95, straight=0.30)
    g.w = x1 + P.SO * 0.62
    g.anchor('top', P.SB + w * 0.46, P.cap); g.anchor('bottom', xs, 0)


@glyph('R', 0x52)
def R(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2
    w = P.Hw * 0.915
    x1 = P.SB + w * 0.965
    yb = P.cap * 0.44 - s.h * 0.45
    g.vstem(xs, 0, P.cap, s.v)
    d_bowl(g, xs, x1, yb, P.cap, s, fb=0.95, straight=0.30)
    t = s.d * (1.0 - 0.05 * wtc(P)); t0 = s.d0 * (1.0 - 0.05 * wtc(P))
    xj = xs + s.v0 / 2 + (x1 - xs) * (0.30 + 0.04 * wtc(P))
    diag(g, (xj, yb + s.h * 0.5), (P.SB + w * 1.02, 0), t, -1, +1, t0=t0)
    g.w = P.SB + w * 1.02 + P.SD * 1.4
    g.anchor('top', P.SB + w * 0.46, P.cap); g.anchor('bottom', P.SB + w * 0.5, 0)


@glyph('S', 0x53)
def S_(g):
    P = g.P; s = U(P)
    s_shape(g, P.SO * 1.0, P.Ow * (0.665 + 0.035 * wtc(P)), cbot(P), ctop(P), s, P.cap, upper=True)
    g.w = g.bounds()[2] + P.SO * 0.95


@glyph('U', 0x55)
def U_(g):
    P = g.P; s = U(P)
    w = P.Hw * 0.985
    xl = P.SB * 0.94 + s.v0 / 2; xr = P.SB * 0.94 + w - s.v0 / 2
    ry = clamp(w / 2, 0.30 * P.cap, 0.46 * P.cap)
    yr = cbot(P) + ry
    ki = P.ki((w - 2 * s.v0) / 2, ry - s.h)
    g.stroke([N(xl, P.cap, -90, s.v, line=True), N(xl, yr, -90, s.v), N((xl + xr) / 2, cbot(P) + s.h / 2, 0, s.h),
              N(xr, yr, 90, s.v, line=True), N(xr, P.cap, 90, s.v)], kL=ki)
    g.w = w + 2 * P.SB * 0.94


@glyph('J', 0x4A)
def J(g):
    P = g.P; s = U(P)
    w = P.Hw * 0.70
    lsb = P.SO * 0.55
    xs = lsb + w - s.v0 / 2
    xlv = lsb
    cx = (xlv + xs) / 2
    ry = clamp((xs + s.v0 / 2 - xlv) / 2, 0.24 * P.cap, 0.40 * P.cap)
    yt = cbot(P) + ry
    rn = dict(cx=cx, cy=yt, rx=cx - (xlv + s.o0 * 0.92), ry=ry - s.h)
    th = 180 + 24.0 + 10.0 * (P.ap - 1.0)
    g.stroke([N(xs, P.cap, -90, s.v, line=True), N(xs, yt, -90, s.v), N(cx, cbot(P) + s.h / 2, 180, s.h),
              N(xlv + s.o0 * 0.46, yt, 90, s.o * 0.92)], cut1=term(rn, th, P), kR=P.ki(rn['rx'], rn['ry']))
    g.w = xs + s.v0 / 2 + P.SB * 0.96
    g.anchor('top', xs, P.cap); g.anchor('bottom', cx, 0)


# ------------------------------------------------------------ diagonal caps
@glyph('A', 0x41)
def A(g):
    P = g.P; s = U(P)
    w = P.Ow * (0.965 + 0.03 * wtc(P))
    x0 = P.SD; x1 = x0 + w
    ap = s.d0 * (0.92 - 0.30 * wtc(P))
    cl, cr, crotch = vee(g, x0, x1, 0, P.cap, s.d, s.d0, ap)
    hb = s.h * 0.95
    yb = P.cap * 0.262
    g.poly([cl.at_y(yb - hb / 2), cr.at_y(yb - hb / 2), cr.at_y(yb + hb / 2), cl.at_y(yb + hb / 2)])
    g.w = w + 2 * P.SD
    g.anchor('ogonek', x1 - s.d0 * 0.3, 0)


@glyph('V', 0x56)
def V(g):
    P = g.P; s = U(P)
    w = P.Ow * (0.945 + 0.03 * wtc(P))
    vee(g, P.SD, P.SD + w, P.cap, 0, s.d, s.d0, s.d0 * (0.90 - 0.30 * wtc(P)))
    g.w = w + 2 * P.SD


@glyph('W', 0x57)
def W(g):
    P = g.P; s = U(P)
    w = P.Ow * (1.43 + 0.05 * wtc(P))
    w_shape(g, P.SD, w, P.cap, s)
    g.w = w + 2 * P.SD


@glyph('X', 0x58)
def X(g):
    P = g.P; s = U(P)
    w = P.Hw * 1.12
    x_shape(g, P.SD * 1.1, w, P.cap, s, top_in=0.03)
    g.w = w + 2.2 * P.SD


@glyph('Y', 0x59)
def Y(g):
    P = g.P; s = U(P)
    w = P.Hw * 1.14
    x0 = P.SD * 0.8; x1 = x0 + w; cx = (x0 + x1) / 2
    yj = P.cap * (0.40 - 0.03 * wtc(P))
    t = s.d * (0.98 - 0.04 * wtc(P)); t0 = s.d0 * (0.98 - 0.04 * wtc(P))
    cl = sline((x0, P.cap), -1, (cx, yj), 0, t0); cr = sline((x1, P.cap), +1, (cx, yj), 0, t0)
    ll, lr = edges(cl, t); rl, rr = edges(cr, t)
    g.poly([ll.at_y(P.cap), lr.at_y(P.cap), lr & rl, rl.at_y(P.cap), rr.at_y(P.cap), rr.at_x(cx + s.v / 2),
            (cx + s.v / 2, 0), (cx - s.v / 2, 0), ll.at_x(cx - s.v / 2)])
    g.w = w + 1.6 * P.SD


@glyph('Z', 0x5A)
def Z(g):
    P = g.P; s = U(P)
    w = P.Hw * 1.02
    z_shape(g, P.SO * 0.86, w, P.cap, s, top_in=0.035)
    g.w = w + P.SO * 1.72


@glyph('K', 0x4B)
def K(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2
    g.vstem(xs, 0, P.cap, s.v)
    k_arms(g, xs, s, P.cap, (P.Hw - s.v0) * 1.03)
    g.w = g.bounds()[2] + P.SD * 0.7
    g.anchor('top', P.SB + P.Hw * 0.5, P.cap); g.anchor('bottom', P.SB + P.Hw * 0.5, 0)


@glyph('M', 0x4D)
def M(g):
    P = g.P; s = U(P)
    w = P.Hw * (1.235 + 0.03 * wtc(P))
    xl = P.SB + s.v0 / 2; xr = P.SB + w - s.v0 / 2
    f = 0.90 - 0.16 * wtc(P)
    g.vstem(xl, 0, P.cap, s.v); g.vstem(xr, 0, P.cap, s.v)
    vee(g, P.SB, P.SB + w, P.cap, 0, s.d * f, s.d0 * f, s.d0 * (0.84 - 0.34 * wtc(P)))
    g.w = w + 2 * P.SB


@glyph('N', 0x4E)
def N_(g):
    P = g.P; s = U(P)
    w = P.Hw * 1.035
    xl = P.SB + s.v0 / 2; xr = P.SB + w - s.v0 / 2
    f = 0.95 - 0.15 * wtc(P)
    g.vstem(xl, 0, P.cap, s.v); g.vstem(xr, 0, P.cap, s.v)
    diag(g, (P.SB, P.cap), (P.SB + w, 0), s.d * f, -1, +1, t0=s.d0 * f)
    g.w = w + 2 * P.SB


# ------------------------------------------------------------ figures
def fig_w(P): return P.Hw * 0.862          # figure body width
def fig_sb(P): return P.SO * 1.06
def fig_adv(P): return fig_w(P) + 2 * fig_sb(P)


def center_fig(g, P, lf=1.0, rf=1.0):
    """Figures are drawn on the tabular grid, then given proportional
    sidebearings.  The tabular set (.tf) re-centres the same outlines on the
    fixed advance, so timers never jitter and both sets share one design."""
    b = g.bounds()
    sbp = fig_sb(P)
    g.dx = sbp * lf - b[0]
    g.translate(g.dx)
    g.w = (b[2] - b[0]) + sbp * (lf + rf)


@glyph('zero', 0x30)
def zero(g):
    P = g.P
    ring(g, fig_sb(P), fig_sb(P) + fig_w(P), cbot(P), ctop(P), upper=True)
    center_fig(g, P)


@glyph('zero.zero')
def zero_slash(g):
    P = g.P; s = U(P)
    zero(g)
    b = g.bounds(); x0 = b[0]; x1 = b[2]
    t = s.h * (0.74 - 0.12 * wtc(P))
    diag(g, (x0 + s.o0 * 0.80, P.cap * 0.22), (x1 - s.o0 * 0.80, P.cap * 0.78), t, 0, 0)


@glyph('one', 0x31)
def one(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P); w = fig_w(P)
    xs = x0 + w * 0.60
    g.vstem(xs, 0, P.cap, s.v)
    t = s.d * (0.86 - 0.08 * wtc(P))
    xfl = x0 + w * 0.10
    up = Line((xs, P.cap), (xfl, P.cap - P.cap * 0.215))
    lo = up.offset(t) if up.offset(t).at_x(xs)[1] < P.cap else up.offset(-t)
    g.poly([up.at_x(xs), up.at_x(xfl), lo.at_x(xfl), lo.at_x(xs)])
    center_fig(g, P, 0.80, 1.45)


@glyph('two', 0x32)
def two(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.03; x1 = fig_sb(P) + fig_w(P) * 0.975
    w = x1 - x0
    yuc = P.cap * 0.705
    xl = x0 + w * 0.02
    cxu = (xl + x1) / 2
    ru = dict(cx=cxu, cy=yuc, rx=cxu - xl - s.o0 * 0.92, ry=ctop(P) - yuc - s.h)
    th = 180 - (27.0 + 10.0 * (P.ap - 1.0))
    td = s.d * (1.0 - 0.06 * wtc(P))
    ang = 222.0 + 5.0 * wtc(P)
    hw = td / abs(__import__('math').sin(__import__('math').radians(ang))) / 2
    g.stroke([N(xl + s.o0 * 0.46, yuc, 90, s.o * 0.92), N(cxu, ctop(P) - s.h / 2, 0, s.h),
              N(x1 - s.o0 / 2, yuc, -90, s.o), N(x0 + hw * 0.96, s.h * 0.5, ang, td)],
             cut0=term(ru, th, P), kR=P.ki(ru['rx'], ru['ry']))
    g.rect(x0, 0, x1 + w * 0.02, s.h)
    center_fig(g, P)


@glyph('three', 0x33)
def three(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.02; x1 = fig_sb(P) + fig_w(P) * 0.985
    w = x1 - x0
    ym = P.cap * 0.535
    fm = 0.90 - 0.10 * wtc(P); hm = s.h * fm
    x1u = x1 - w * 0.05
    xlu = x0 + w * 0.05
    yuc = ((ym + hm / 2) + (ctop(P) - s.h)) / 2; ylc = ((ym - hm / 2) + (cbot(P) + s.h)) / 2
    cxu = (xlu + x1u) / 2; cxl = (x0 + x1) / 2
    xm0 = cxl - w * 0.14 * (1.0 - 0.8 * wtc(P))
    ru = dict(cx=cxu, cy=yuc, rx=max(cxu - xlu - s.o0 * 0.92, 0.40 * (cxu - xlu)), ry=max(ctop(P) - yuc - s.h, 0.40 * (ctop(P) - yuc)))
    rl = dict(cx=cxl, cy=ylc, rx=max(cxl - x0 - s.o0 * 0.92, 0.40 * (cxl - x0)), ry=max(ylc - cbot(P) - s.h, 0.40 * (ylc - cbot(P))))
    thu = 180 - (33.0 + 10.0 * (P.ap - 1.0)); thl = 180 + (30.0 + 10.0 * (P.ap - 1.0))
    g.stroke([N(xlu + s.o0 * 0.46, yuc, 90, s.o * 0.92), N(cxu, ctop(P) - s.h / 2, 0, s.h),
              N(x1u - s.o0 * 0.48, yuc, -90, s.o * 0.96), N(cxl + w * 0.02, ym, 180, hm, line=True), N(xm0, ym, 180, hm)],
             cut0=term(ru, thu, P), kR=P.ki(ru['rx'], ru['ry']))
    g.stroke([N(xm0, ym, 0, hm, line=True), N(cxl + w * 0.02, ym, 0, hm), N(x1 - s.o0 / 2, ylc, -90, s.o),
              N(cxl, cbot(P) + s.h / 2, 180, s.h), N(x0 + s.o0 * 0.46, ylc, 90, s.o * 0.92)],
             cut1=term(rl, thl, P), kR=P.ki(rl['rx'], rl['ry']))
    center_fig(g, P)


@glyph('four', 0x34)
def four(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) - fig_w(P) * 0.02; w = fig_w(P) * 1.04
    xs = x0 + w * 0.735
    yb = P.cap * 0.205
    g.vstem(xs, 0, P.cap, s.v)
    g.rect(x0, yb, x0 + w, yb + s.h)
    f = 0.94 - 0.10 * wtc(P)
    diag(g, (x0, yb + s.h * 0.5), (xs + s.v0 / 2, P.cap), s.d * f, -1, +1, t0=s.d0 * f)
    center_fig(g, P, 0.70, 0.80)


@glyph('five', 0x35)
def five(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.03; x1 = fig_sb(P) + fig_w(P) * 0.985
    w = x1 - x0
    xn = x0 + w * 0.115 + s.v0 / 2
    ybt = P.cap * (0.635 + 0.015 * wtc(P))
    ybc = (ybt + cbot(P)) / 2
    cxb = (x0 + x1) / 2 + w * 0.02
    g.rect(xn - s.v / 2, P.cap - s.h, x1 - w * 0.06, P.cap)
    ystart = ybc + (ybt - ybc) * 0.06
    lean = w * 0.035
    g.poly([(xn - s.v / 2, P.cap), (xn + s.v / 2, P.cap), (xn + s.v / 2 - lean, ystart), (xn - s.v / 2 - lean, ystart)])
    rl = dict(cx=cxb, cy=ybc, rx=max(cxb - x0 - s.o0 * 0.92, 0.40 * (cxb - x0)), ry=max(ybc - cbot(P) - s.h, 0.40 * (ybc - cbot(P))))
    thl = 180 + (30.0 + 10.0 * (P.ap - 1.0))
    xin = xn + s.v0 / 2 - lean - min(P.bury, 0.05) * s.v0
    g.stroke([N(xin - s.j0 / 2, ystart, 90, s.j), N(cxb, ybt - s.h / 2, 0, s.h), N(x1 - s.o0 / 2, ybc, -90, s.o),
              N(cxb - w * 0.02, cbot(P) + s.h / 2, 180, s.h), N(x0 + s.o0 * 0.46, ybc, 90, s.o * 0.92)],
             cut1=term(rl, thl, P), kR=P.ki(rl['rx'], rl['ry']))
    center_fig(g, P)


def six_shape(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.01; x1 = fig_sb(P) + fig_w(P) * 0.99
    w = x1 - x0
    ybt = P.cap * (0.625 + 0.02 * wtc(P))
    rn = ring(g, x0, x1, cbot(P), ybt, upper=True, ft=0.94)
    cxt = (x0 + x1) / 2 + w * 0.06
    x1v = x1 - w * 0.03
    yuc = P.cap * 0.67
    ru = dict(cx=cxt, cy=yuc, rx=x1v - cxt - s.o0 * 0.92, ry=ctop(P) - yuc - s.h)
    th = 30.0 + 10.0 * (P.ap - 1.0)
    g.stroke([N(x0 + s.o0 / 2, rn['cy'], 90, s.o), N(cxt, ctop(P) - s.h / 2, 0, s.h),
              N(x1v - s.o0 * 0.46, yuc, -90, s.o * 0.92)], cut1=term(ru, th, P),
             kR=P.ki(cxt - x0 - s.o0, ctop(P) - rn['cy'] - s.h))


@glyph('six', 0x36)
def six(g):
    six_shape(g); center_fig(g, g.P)


@glyph('nine', 0x39)
def nine(g):
    P = g.P
    with g.rot180(fig_adv(P) / 2, P.cap / 2):
        six_shape(g)
    center_fig(g, P)


@glyph('seven', 0x37)
def seven(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.02; x1 = fig_sb(P) + fig_w(P) * 0.99
    w = x1 - x0
    t = s.d * (1.0 - 0.03 * wtc(P)); t0 = s.d0 * (1.0 - 0.03 * wtc(P))
    c = sline((x1, P.cap), +1, (x0 + w * 0.20, 0), -1, t0)
    l, r = edges(c, t)
    g.poly([(x0, P.cap), r.at_y(P.cap), r.at_y(0), l.at_y(0), l.at_y(P.cap - s.h), (x0, P.cap - s.h)])
    center_fig(g, P, 0.85, 0.70)


@glyph('eight', 0x38)
def eight(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P); x1 = x0 + fig_w(P)
    w = x1 - x0
    ym = P.cap * 0.532
    fm = 0.86 - 0.10 * wtc(P); hm = s.h * fm
    ring(g, x0 + w * 0.048, x1 - w * 0.048, ym - hm / 2, ctop(P), upper=True, fb=fm, fl=0.96, fr=0.96)
    ring(g, x0, x1, cbot(P), ym + hm / 2, upper=True, ft=fm)
    center_fig(g, P)
