"""Orion — Greek (monotonic)."""
from __future__ import annotations
from .geom import N, E, Line, G, poly, reverse_contour
from .parts import glyph, S, round_nodes, term, ring, arch, bowl, sline, edges, diag, vee, hook, clamp
from . import latin_lc as lc, latin_uc as uc, symbols as sy
from .latin_lc import top, bot, cwl
from .latin_uc import U, ctop, cbot, wtc, d_bowl


def alias(name, uni, base):
    @glyph(name, uni)
    def a(g):
        g.comp(base, 0, 0); g.w = None
    return a


# ------------------------------------------------------------ capitals
for _n, _u, _b in (('Alpha', 0x391, 'A'), ('Beta', 0x392, 'B'), ('Epsilon', 0x395, 'E'), ('Zeta', 0x396, 'Z'),
                   ('Eta', 0x397, 'H'), ('Iota', 0x399, 'I'), ('Kappa', 0x39A, 'K'), ('Mu', 0x39C, 'M'), ('Nu', 0x39D, 'N'),
                   ('Omicron', 0x39F, 'O'), ('Rho', 0x3A1, 'P'), ('Tau', 0x3A4, 'T'), ('Upsilon', 0x3A5, 'Y'), ('Chi', 0x3A7, 'X')):
    alias(_n, _u, _b)


@glyph('Gamma', 0x393)
def Gamma(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2; w = P.Hw * 0.80
    g.vstem(xs, 0, P.cap, s.v)
    g.rect(xs, P.cap - s.h, P.SB + w, P.cap)
    g.w = P.SB + w + P.SO * 0.42
    g.anchor('top', P.SB + w * 0.42, P.cap); g.anchor('bottom', xs, 0)


@glyph('Delta', 0x394)
def Delta(g):
    P = g.P; s = U(P)
    w = P.Ow * (0.965 + 0.03 * wtc(P)); x0 = P.SD * 1.1; x1 = x0 + w; cx = (x0 + x1) / 2
    t = s.d; hb = s.h
    ap = s.d0 * (0.92 - 0.30 * wtc(P))
    cl = sline((x0, 0), -1, (cx - ap / 2, P.cap), -1, s.d0); cr = sline((x1, 0), +1, (cx + ap / 2, P.cap), +1, s.d0)
    ll, lr = edges(cl, t); rl, rr = edges(cr, t)
    g.add([poly([ll.at_y(0), rr.at_y(0), rr.at_y(P.cap), ll.at_y(P.cap)])])
    g.add([reverse_contour(poly([lr.at_y(hb), rl.at_y(hb), lr & rl]))])
    g.w = w + 2 * x0


@glyph('Theta', 0x398)
def Theta(g):
    P = g.P; s = U(P)
    uc.O(g)
    hb = s.h * 0.95
    ins = s.o0 + (P.Ow - 2 * s.o0) * 0.14
    g.rect(P.SO + ins, P.cap * 0.5 - hb / 2, P.SO + P.Ow - ins, P.cap * 0.5 + hb / 2)


@glyph('Lambda', 0x39B)
def Lambda(g):
    P = g.P; s = U(P)
    w = P.Ow * (0.945 + 0.03 * wtc(P))
    vee(g, P.SD, P.SD + w, 0, P.cap, s.d, s.d0, s.d0 * (0.92 - 0.30 * wtc(P)))
    g.w = w + 2 * P.SD


@glyph('Xi', 0x39E)
def Xi(g):
    P = g.P; s = U(P)
    w = P.Hw * 0.98; x0 = P.SO * 1.0
    g.rect(x0, P.cap - s.h, x0 + w, P.cap); g.rect(x0, 0, x0 + w, s.h)
    hm = s.h * 0.96
    g.rect(x0 + w * 0.10, P.cap * 0.52 - hm / 2, x0 + w * 0.90, P.cap * 0.52 + hm / 2)
    g.w = w + 2 * x0


@glyph('Pi', 0x3A0)
def Pi(g):
    P = g.P; s = U(P)
    xl = P.SB + s.v0 / 2; xr = P.SB + P.Hw - s.v0 / 2
    g.vstem(xl, 0, P.cap, s.v); g.vstem(xr, 0, P.cap, s.v)
    g.rect(xl, P.cap - s.h, xr, P.cap)
    g.w = P.Hw + 2 * P.SB


@glyph('Sigma', 0x3A3)
def Sigma(g):
    P = g.P; s = U(P)
    t = s.h; td = s.d * (0.96 - 0.06 * wtc(P))
    x0 = P.SO * 0.9; w = P.Hw * 0.98; x1 = x0 + w
    ym = P.cap * 0.51; xm = x0 + w * 0.56
    a = sline((x0, P.cap - t), -1, (xm, ym), +1, td); b = sline((x0, t), -1, (xm, ym), +1, td)
    al, ar = edges(a, td); bl, br = edges(b, td)
    g.poly([(x0, 0), (x1, 0), (x1, t), br.at_y(t), br & ar, ar.at_y(P.cap - t), (x1 - w * 0.03, P.cap - t), (x1 - w * 0.03, P.cap),
            (x0, P.cap), (x0, P.cap - t), al & bl, (x0, t)])
    g.w = x1 + P.SO * 0.8


@glyph('Phi', 0x3A6)
def Phi(g):
    P = g.P; s = U(P)
    w = P.Ow * (1.02 + 0.10 * wtc(P)); x0 = P.SO
    ring(g, x0, x0 + w, P.cap * 0.14, P.cap * 0.86, upper=True, ft=0.94, fb=0.94)
    g.vstem(x0 + w / 2, 0, P.cap, s.v * (1.0 - 0.10 * wtc(P)))
    g.w = w + 2 * x0


@glyph('Psi', 0x3A8)
def Psi(g):
    P = g.P; s = U(P)
    w = P.Hw * 1.16; x0 = P.SB * 0.8
    xl = x0 + s.v0 / 2; xr = x0 + w - s.v0 / 2
    ybot = P.cap * 0.28
    ry = clamp(w / 2, 0.20 * P.cap, 0.40 * P.cap)
    g.stroke([N(xl, P.cap, -90, s.v, line=True), N(xl, ybot + ry, -90, s.v), N((xl + xr) / 2, ybot + s.h / 2, 0, s.h),
              N(xr, ybot + ry, 90, s.v, line=True), N(xr, P.cap, 90, s.v)], kL=P.ki(w / 2 - s.v0, ry - s.h))
    g.vstem((xl + xr) / 2, 0, P.cap, s.v)
    g.w = w + 2 * x0


@glyph('Omega', [0x3A9, 0x2126])
def Omega(g):
    P = g.P; s = U(P)
    w = P.Ow * 1.0; x0 = P.SO * 0.9; x1 = x0 + w; cx = (x0 + x1) / 2
    foot = w * 0.345
    ycy = P.cap * 0.56
    xa = x0 + foot - s.o0 * 0.42; xb = x1 - foot + s.o0 * 0.42
    g.stroke([N(xa, s.h * 0.5, 118, s.o * 0.94), N(x0 + s.o0 / 2, ycy, 90, s.o), N(cx, ctop(P) - s.h / 2, 0, s.h),
              N(x1 - s.o0 / 2, ycy, -90, s.o), N(xb, s.h * 0.5, 242, s.o * 0.94)],
             kR=P.ki(w / 2 - s.o0, (ctop(P) - ycy) - s.h))
    g.rect(x0, 0, x0 + foot, s.h); g.rect(x1 - foot, 0, x1, s.h)
    g.w = w + 2 * x0


# ------------------------------------------------------------ lowercase
@glyph('alpha', 0x3B1)
def alpha(g):
    P = g.P; s = S(P, False)
    lsb = P.so
    xr = lsb + s.o0 + cwl(P) - P.bury * s.v0 + s.v0 / 2
    with g.flip_x(xr):
        bowl(g, xr, bot(P), top(P), cwl(P))
    tail = (P.nw - s.v0) * 0.20
    hook(g, xr, P.xh, P.xh * 0.30 + s.h / 2, xr + s.v0 / 2 + tail, 0)
    g.w = xr + s.v0 / 2 + tail + P.so * 0.8
    g.anchor('top', lsb + (xr - lsb) * 0.52, P.xh)


@glyph('beta', 0x3B2)
def beta(g):
    P = g.P; s = S(P, False)
    w = P.nw * 1.04
    xl = P.sb + s.v0 / 2; x1 = P.sb + w
    xr_up = x1 - w * 0.10 - s.v0 / 2
    htop = P.asc + P.os
    ym = P.xh * 0.60
    fm = 0.92 - 0.10 * clamp(P.wt, 0, 1); hm = s.h * fm
    a = arch(g, xl, xr_up, htop, stem_to=ym + hm, href=P.asc, lo=0.20, hi=0.30)
    g.vstem(xl, P.desc, a['ys'], s.v)
    # upper bowl closes back to the waist
    g.stroke([N(xr_up, ym + hm * 1.4 + P.xh * 0.05, -90, s.v * 0.98), N(xr_up - (xr_up - xl) * 0.42, ym, 180, hm, line=True),
              N(xl, ym, 180, hm)], k=P.k)
    d_bowl(g, xl, x1, 0, ym + hm / 2, s, ft=fm, straight=0.26)
    g.w = x1 + P.so
    g.anchor('top', (xl + x1) / 2, P.asc)


@glyph('gamma', 0x3B3)
def gamma(g):
    P = g.P; s = S(P, False)
    w_ = P.nw * 1.06; x0 = P.sd; x1 = x0 + w_; cx = (x0 + x1) / 2
    yj = P.xh * 0.02
    cl = sline((x0, P.xh), -1, (cx, yj), 0, s.d0); cr = sline((x1, P.xh), +1, (cx, yj), 0, s.d0)
    ll, lr = edges(cl, s.d); rl, rr = edges(cr, s.d)
    g.poly([ll.at_y(P.xh), lr.at_y(P.xh), lr & rl, rl.at_y(P.xh), rr.at_y(P.xh), rr.at_x(cx + s.v / 2),
            (cx + s.v / 2, P.desc), (cx - s.v / 2, P.desc), ll.at_x(cx - s.v / 2)])
    g.w = w_ + 2 * P.sd


def six_like(g, x0, x1, ybt, ytop, upper, mirror=False):
    P = g.P; s = S(P, upper)
    w = x1 - x0
    rn = ring(g, x0, x1, -P.os, ybt, upper=upper, ft=0.94)
    cxt = (x0 + x1) / 2 + w * 0.05
    x1v = x1 - w * 0.04
    yuc = ytop - (ytop - ybt) * 0.62 - s.h
    yuc = max(yuc, rn['cy'] + 20)
    ru = dict(cx=cxt, cy=yuc, rx=x1v - cxt - s.o0 * 0.92, ry=ytop - yuc - s.h)
    g.stroke([N(x0 + s.o0 / 2, rn['cy'], 90, s.o), N(cxt, ytop - s.h / 2, 0, s.h), N(x1v - s.o0 * 0.46, yuc, -90, s.o * 0.92)],
             cut1=term(ru, 32.0, P), kR=P.ki(cxt - x0 - s.o0, ytop - rn['cy'] - s.h))


@glyph('delta', 0x3B4)
def delta(g):
    P = g.P
    six_like(g, P.so, P.so + P.ow, P.xh * 0.90 + P.os, P.asc + P.os, False)
    g.w = P.ow + 2 * P.so
    g.anchor('top', P.so + P.ow * 0.55, P.asc)


def eps_shape(g, x0, x1, y0, y1, upper, mid=0.535):
    """Open form with two bowls (epsilon, Cyrillic ze when mirrored)."""
    P = g.P; s = S(P, upper)
    w = x1 - x0
    ym = y0 + (y1 - y0) * mid
    wt = clamp(P.wt, 0, 1)
    fm = 0.90 - 0.10 * wt; hm = s.h * fm
    x1u = x1 - w * 0.05; xlu = x0 + w * 0.05
    yuc = ((ym + hm / 2) + (y1 - s.h)) / 2; ylc = ((ym - hm / 2) + (y0 + s.h)) / 2
    cxu = (xlu + x1u) / 2; cxl = (x0 + x1) / 2
    xm0 = cxl - w * 0.14 * (1.0 - 0.8 * wt)
    ru = dict(cx=cxu, cy=yuc, rx=cxu - xlu - s.o0 * 0.92, ry=y1 - yuc - s.h)
    rl = dict(cx=cxl, cy=ylc, rx=cxl - x0 - s.o0 * 0.92, ry=ylc - y0 - s.h)
    thu = 180 - (33.0 + 10.0 * (P.ap - 1.0)); thl = 180 + (30.0 + 10.0 * (P.ap - 1.0))
    g.stroke([N(xlu + s.o0 * 0.46, yuc, 90, s.o * 0.92), N(cxu, y1 - s.h / 2, 0, s.h),
              N(x1u - s.o0 * 0.48, yuc, -90, s.o * 0.96), N(cxl + w * 0.02, ym, 180, hm, line=True), N(xm0, ym, 180, hm)],
             cut0=term(ru, thu, P), kR=P.ki(ru['rx'], ru['ry']))
    g.stroke([N(xm0, ym, 0, hm, line=True), N(cxl + w * 0.02, ym, 0, hm), N(x1 - s.o0 / 2, ylc, -90, s.o),
              N(cxl, y0 + s.h / 2, 180, s.h), N(x0 + s.o0 * 0.46, ylc, 90, s.o * 0.92)],
             cut1=term(rl, thl, P), kR=P.ki(rl['rx'], rl['ry']))


@glyph('epsilon', 0x3B5)
def epsilon(g):
    P = g.P
    w = P.ow * 0.80; x0 = P.so * 1.1
    with g.flip_x(x0 + w / 2):
        eps_shape(g, x0, x0 + w, bot(P), top(P), False)
    g.w = w + P.so * 1.9


@glyph('zeta', 0x3B6)
def zeta(g):
    P = g.P; s = S(P, False)
    w = P.ow * 0.82; x0 = P.so * 1.1; x1 = x0 + w
    g.rect(x0 + w * 0.06, P.asc - s.h, x1, P.asc)
    cx = (x0 + x1) / 2
    yb = s.h * 0.5 + P.xh * 0.02
    g.stroke([N(x1 - s.o0 * 0.62, P.asc - s.h * 0.5, 214, s.o * 0.92), N(x0 + s.o0 / 2, P.xh * 0.40, 270, s.o),
              N(cx + w * 0.04, yb, 0, s.h), N(x1 - s.o0 * 0.48, P.desc * 0.42, -90, s.o * 0.92),
              N(cx + w * 0.10, P.desc * 0.90 + s.h * 0.45, 180, s.h * 0.90)], k=P.k)
    g.w = x1 + P.so * 0.9
    g.anchor('top', cx, P.asc)


@glyph('eta', 0x3B7)
def eta(g):
    P = g.P; s = S(P, False)
    xl = P.sb + s.v0 / 2; xr = P.sb + P.nw - s.v0 / 2
    g.vstem(xl, 0, P.xh, s.v)
    arch(g, xl, xr, top(P), stem_to=P.desc)
    g.w = P.nw + P.sb * 1.93
    g.anchor('top', P.sb + P.nw * 0.52, P.xh); g.anchor('bottom', xl, 0)


@glyph('theta', 0x3B8)
def theta(g):
    P = g.P; s = S(P, False)
    w = P.ow * 0.90; x0 = P.so
    ring(g, x0, x0 + w, bot(P), P.asc + P.os)
    hb = s.h * 0.92
    yb = (P.asc) * 0.5
    g.rect(x0 + s.o0 * 0.5, yb - hb / 2, x0 + w - s.o0 * 0.5, yb + hb / 2)
    g.w = w + 2 * x0
    g.anchor('top', x0 + w / 2, P.asc)


@glyph('iota', 0x3B9)
def iota(g):
    P = g.P; s = S(P, False)
    xs = P.sb + s.v0 / 2
    tail = (P.nw - s.v0) * 0.24
    hook(g, xs, P.xh, P.xh * 0.32 + s.h / 2, xs + s.v0 / 2 + tail, 0)
    g.w = xs + s.v0 / 2 + tail + P.so * 0.9
    g.anchor('top', xs, P.xh); g.anchor('bottom', xs + tail * 0.3, 0)


alias('kappa', 0x3BA, 'kgreenlandic')


@glyph('lambda', 0x3BB)
def lambda_(g):
    P = g.P; s = S(P, False)
    w_ = P.nw * 1.06; x0 = P.sd; x1 = x0 + w_
    t = s.d; t0 = s.d0
    main = sline((x0 + w_ * 0.12, P.asc), -1, (x1, 0), +1, t0)
    ml, mr = edges(main, t)
    g.poly([ml.at_y(0), mr.at_y(0), mr.at_y(P.asc), ml.at_y(P.asc)])
    jy = P.xh * 0.60
    jp = main.at_y(jy)
    leg = sline((x0, 0), -1, (jp[0], jy), 0, t0 * 0.96)
    l2, r2 = edges(leg, t * 0.96)
    g.poly([l2.at_y(0), r2.at_y(0), r2.at_y(jy), l2.at_y(jy)])
    g.w = w_ + 2 * P.sd
    g.anchor('top', x0 + w_ * 0.25, P.asc)


@glyph('mu', [0x3BC, 0xB5])
def mu(g):
    P = g.P; s = S(P, False)
    lc.u(g)
    w = P.nw + P.sb * 1.93
    xl = w - (P.sb + P.nw - s.v0 / 2)
    g.vstem(xl, P.desc, P.xh * 0.4, s.v)


alias('nu', 0x3BD, 'v')


@glyph('xi', 0x3BE)
def xi(g):
    P = g.P; s = S(P, False)
    w = P.ow * 0.82; x0 = P.so * 1.1; x1 = x0 + w
    cx = (x0 + x1) / 2
    wt = clamp(P.wt, 0, 1)
    hm = s.h * (0.90 - 0.10 * wt)
    ym = P.asc * 0.56
    g.stroke([N(x1 - w * 0.04, P.asc - s.h / 2, 180, s.h, line=True), N(cx + w * 0.04, P.asc - s.h / 2, 180, s.h),
              N(x0 + w * 0.10 + s.o0 / 2, (P.asc + ym) / 2, 270, s.o * 0.94), N(cx + w * 0.02, ym, 0, hm, line=True),
              N(x1 - w * 0.16, ym, 0, hm)], k=P.k)
    yb = s.h * 0.5 + P.xh * 0.02
    g.stroke([N(x1 - w * 0.16, ym, 180, hm, line=True), N(cx + w * 0.02, ym, 180, hm), N(x0 + s.o0 / 2, (ym + yb) / 2, 270, s.o),
              N(cx + w * 0.04, yb, 0, s.h), N(x1 - s.o0 * 0.48, P.desc * 0.42, -90, s.o * 0.92),
              N(cx + w * 0.10, P.desc * 0.90 + s.h * 0.45, 180, s.h * 0.90)], k=P.k)
    g.w = x1 + P.so * 0.9
    g.anchor('top', cx, P.asc)


alias('omicron', 0x3BF, 'o')


@glyph('pi', 0x3C0)
def pi(g):
    P = g.P; s = S(P, False)
    w = P.nw * 1.08; x0 = P.so * 0.9
    g.rect(x0, P.xh - s.h, x0 + w, P.xh)
    g.vstem(x0 + w * 0.20 + s.v0 * 0.2, 0, P.xh, s.v)
    xr = x0 + w * 0.80 - s.v0 * 0.2
    tail = (P.nw - s.v0) * 0.12
    hook(g, xr, P.xh, P.xh * 0.22 + s.h / 2, xr + s.v0 / 2 + tail, 0)
    g.w = max(x0 + w, xr + s.v0 / 2 + tail) + P.so * 0.9


@glyph('rho', 0x3C1)
def rho(g):
    P = g.P; s = S(P, False)
    x0 = P.so * 1.15; x1 = x0 + P.ow * 0.97
    rn = ring(g, x0, x1, bot(P), top(P))
    g.vstem(x0 + s.o0 / 2, P.desc, rn['cy'], s.o)
    g.w = x1 + P.so


@glyph('uni03C2', [0x3C2])
def sigmafinal(g):
    P = g.P; s = S(P, False)
    x0 = P.so; x1 = x0 + P.ow * 0.94
    rn = round_nodes(P, x0, x1, P.xh * 0.02, top(P))
    cx = rn['cx']
    g.stroke([rn['r'], rn['t'], rn['l'], N(cx + P.ow * 0.02, P.xh * 0.02 + s.h / 2, 0, s.h),
              N(x1 - P.ow * 0.08 - s.o0 * 0.48, P.desc * 0.42, -90, s.o * 0.92),
              N(cx + P.ow * 0.06, P.desc * 0.90 + s.h * 0.45, 180, s.h * 0.90)], cut0=term(rn, lc.theta_c(P), P), kL=rn['ki'])
    g.w = g.bounds()[2] + P.so * 0.5


@glyph('sigma', 0x3C3)
def sigma(g):
    P = g.P; s = S(P, False)
    x0 = P.so; x1 = x0 + P.ow * 0.98
    ring(g, x0, x1, bot(P), P.xh)
    ext = P.ow * 0.14
    g.rect((x0 + x1) / 2, P.xh - s.h, x1 + ext, P.xh)
    g.w = x1 + ext + P.so * 0.55
    g.anchor('top', (x0 + x1) / 2, P.xh)


@glyph('tau', 0x3C4)
def tau(g):
    P = g.P; s = S(P, False)
    w = P.nw * 0.92; x0 = P.so * 0.8
    g.rect(x0, P.xh - s.h, x0 + w, P.xh)
    xs = x0 + w * 0.46
    tail = (P.nw - s.v0) * 0.24
    hook(g, xs, P.xh, P.xh * 0.30 + s.h / 2, xs + s.v0 / 2 + tail, 0)
    g.w = x0 + w + P.so * 0.8


def cup(g, xl, xr, ytop, ybot, s, P):
    w = xr - xl + s.v0
    ry = clamp(w / 2, 0.30 * P.xh, 0.46 * P.xh)
    g.stroke([N(xl, ytop, -90, s.v, line=True), N(xl, ybot + ry, -90, s.v), N((xl + xr) / 2, ybot + s.h / 2, 0, s.h),
              N(xr, ybot + ry, 90, s.v, line=True), N(xr, ytop, 90, s.v)], kL=P.ki(w / 2 - s.v0, ry - s.h))


@glyph('upsilon', 0x3C5)
def upsilon(g):
    P = g.P; s = S(P, False)
    w = P.nw * 0.98; x0 = P.sb * 0.92
    cup(g, x0 + s.v0 / 2, x0 + w - s.v0 / 2, P.xh, bot(P), s, P)
    g.w = w + 2 * x0


@glyph('phi', 0x3C6)
def phi(g):
    P = g.P; s = S(P, False)
    wt = clamp(P.wt, 0, 1)
    w = P.ow * (1.10 + 0.22 * wt); x0 = P.so
    ring(g, x0, x0 + w, bot(P), top(P))
    g.vstem(x0 + w / 2, P.desc, P.asc, s.v * (0.96 - 0.14 * wt))
    g.w = w + 2 * x0
    g.anchor('top', x0 + w / 2, P.asc)


@glyph('chi', 0x3C7)
def chi(g):
    P = g.P; s = S(P, False)
    w_ = P.nw * 1.08
    with g.shift(0, P.desc):
        lc.x_shape(g, P.sd * 1.1, w_, P.xh - P.desc, s)
    g.w = w_ + 2.2 * P.sd


@glyph('psi', 0x3C8)
def psi(g):
    P = g.P; s = S(P, False)
    w = P.nw * 1.22; x0 = P.sb * 0.9
    cup(g, x0 + s.v0 / 2, x0 + w - s.v0 / 2, P.xh, bot(P), s, P)
    g.vstem(x0 + w / 2, P.desc, P.asc, s.v * 0.96)
    g.w = w + 2 * x0
    g.anchor('top', x0 + w / 2, P.asc)


@glyph('omega', 0x3C9)
def omega(g):
    P = g.P; s = S(P, False)
    w = P.ow * 1.42; x0 = P.so; x1 = x0 + w; cx = (x0 + x1) / 2
    vm = s.v * 0.92
    ymid = P.xh * 0.60
    for sg in (1, -1):
        xo = x0 if sg > 0 else x1
        xe = xo + sg * s.o0 / 2
        cxc = (xe + cx) / 2
        nodes = [N(xo + sg * w * 0.13, P.xh, 270 - sg * 34, s.o * 0.86), N(xe, P.xh * 0.44, 270, s.o),
                 N(cxc, bot(P) + s.h / 2, 0 if sg > 0 else 180, s.h), N(cx, ymid - (w * 0.10), 90, vm, line=True), N(cx, ymid, 90, vm)]
        if sg < 0:
            g.stroke(nodes, kR=P.ki(w / 4 - s.o0 * 0.7, P.xh * 0.44))
        else:
            g.stroke(nodes, kL=P.ki(w / 4 - s.o0 * 0.7, P.xh * 0.44))
    g.w = w + 2 * x0


@glyph('anoteleia', 0x387)
def anoteleia(g):
    g.comp('periodcentered', 0, g.P.xh * 0.42); g.w = None


alias('uni037E', [0x37E], 'semicolon')
