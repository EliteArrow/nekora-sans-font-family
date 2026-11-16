"""Orion — extended Latin letters that are not plain base + mark composites."""
from __future__ import annotations
from .geom import N, E, Line, G
from .parts import glyph, S, round_nodes, term, ring, arch, bowl, sline, edges, diag, vee, hook, clamp
from . import latin_lc as lc, latin_uc as uc
from .latin_lc import top, bot, cwl, dot_y
from .latin_uc import U, ctop, cbot, wtc, d_bowl
from .symbols import pd


def slash_through(g, x0, x1, y0, y1, t):
    diag(g, (x0, y0), (x1, y1), t, 0, 0)


@glyph('Oslash', 0xD8)
def Oslash(g):
    P = g.P; s = U(P)
    uc.O(g)
    slash_through(g, P.SO + P.Ow * 0.10, P.SO + P.Ow * 0.90, -P.cap * 0.07, P.cap * 1.07, s.h * (0.78 - 0.14 * wtc(P)))


@glyph('oslash', 0xF8)
def oslash(g):
    P = g.P; s = S(P, False)
    lc.o(g)
    slash_through(g, P.so + P.ow * 0.08, P.so + P.ow * 0.92, -P.xh * 0.09, P.xh * 1.09, s.h * (0.78 - 0.14 * clamp(P.wt, 0, 1)))


@glyph('AE', 0xC6)
def AE(g):
    P = g.P; s = U(P)
    w_e = P.Hw * 0.80
    x0 = P.SD
    xs = x0 + P.Ow * 0.52 + s.v0 / 2
    g.vstem(xs, 0, P.cap, s.v)
    uc.e_arms(g, xs, s, w_e, 'tmb')
    t = s.d * (0.96 - 0.06 * wtc(P)); t0 = s.d0 * (0.96 - 0.06 * wtc(P))
    cl = sline((x0, 0), -1, (xs, P.cap), +1, t0)
    l, r = edges(cl, t)
    g.poly([l.at_y(0), r.at_y(0), r.at_y(P.cap), l.at_y(P.cap)])
    hb = s.h * 0.95; yb = P.cap * 0.262
    g.poly([cl.at_y(yb - hb / 2), (xs, yb - hb / 2), (xs, yb + hb / 2), cl.at_y(yb + hb / 2)])
    g.rect(l.at_y(P.cap)[0], P.cap - s.h, xs, P.cap)
    g.w = xs - s.v0 / 2 + w_e * 1.02 + P.SO * 0.82
    g.anchor('top', xs + w_e * 0.2, P.cap); g.anchor('bottom', xs, 0)


@glyph('ae', 0xE6)
def ae(g):
    P = g.P; s = S(P, False)
    wt = clamp(P.wt, 0, 1)
    lsb = P.so * 1.12
    aw = P.nw * 0.90
    xe0 = lsb + aw - s.o0                      # e's left extreme doubles as the stem of a
    xe1 = xe0 + P.ow * 0.975
    rn = round_nodes(P, xe0, xe1, bot(P), top(P))
    hb = s.h * (0.96 - 0.12 * wt)
    ybb = rn['cy'] - hb * 0.42
    start = N(xe1 - s.o0 / 2, ybb, 90, s.o, line=True)
    g.stroke([start, rn['r'], rn['t'], rn['l'], rn['b'], rn['r']], cut1=term(rn, -lc.theta_e(P), P), kL=rn['ki'])
    g.rect(xe0 + s.o0 * 0.5, ybb, xe1 - s.o0 * 0.5, ybb + hb)
    # arch of a, springing from the shared wall
    xr = xe0 + s.o0 / 2
    xlv = lsb + aw * 0.045
    outer_r = (xr + s.v0 / 2 - xlv) / 2
    ry = clamp(outer_r * 0.92, 0.27 * P.xh, 0.40 * P.xh)
    ysh = top(P) - ry
    cxt = (xlv + xr) / 2 + s.v0 * 0.10
    ra = dict(cx=cxt, cy=ysh, rx=cxt - (xlv + s.o0 * 0.9), ry=ry - s.h)
    th = 180 - (30.0 + 12.0 * (P.ap - 1.0))
    g.stroke([N(xr, rn['cy'], 90, s.o, line=True), N(xr, ysh, 90, s.o), N(cxt, top(P) - s.h / 2, 180, s.h),
              N(xlv + s.o0 * 0.45, ysh, 270, s.o * 0.90)], cut1=term(ra, th, P))
    ybt = P.xh * (0.585 + 0.02 * wt)
    hbt = s.h * (0.92 - 0.14 * wt)
    xin = xr - s.v0 / 2 + P.bury * s.v0
    cyb = (ybt + bot(P)) / 2
    cwid = xin - (lsb + s.o0)
    g.stroke([N(xin + s.j0 / 2, cyb, 90, s.j), N(xin - cwid * 0.20, ybt - hbt / 2, 180, hbt),
              N(lsb + s.o0 / 2, cyb - (ybt - bot(P)) * 0.03, 270, s.o), N(lsb + s.o0 + cwid * 0.52, bot(P) + s.h / 2, 0, s.h)],
             closed=True)
    g.w = xe1 + P.so * 0.92
    g.anchor('top', xr, P.xh); g.anchor('bottom', xr, 0)


@glyph('OE', 0x152)
def OE(g):
    P = g.P; s = U(P)
    w_e = P.Hw * 0.80
    x0 = P.SO
    xs = x0 + P.Ow * 0.56 + s.v0 / 2
    with g.flip_x(xs):
        d_bowl(g, xs, 2 * xs - x0, 0, P.cap, s, straight=0.10)
    g.vstem(xs, 0, P.cap, s.v)
    uc.e_arms(g, xs, s, w_e, 'tmb')
    g.w = xs - s.v0 / 2 + w_e * 1.02 + P.SO * 0.82
    g.anchor('top', xs, P.cap); g.anchor('bottom', xs, 0)


@glyph('oe', 0x153)
def oe(g):
    P = g.P; s = S(P, False)
    wt = clamp(P.wt, 0, 1)
    ring(g, P.so, P.so + P.ow, bot(P), top(P))
    xe0 = P.so + P.ow - s.o0
    xe1 = xe0 + P.ow * 0.975
    rn = round_nodes(P, xe0, xe1, bot(P), top(P))
    hb = s.h * (0.96 - 0.12 * wt)
    ybb = rn['cy'] - hb * 0.42
    g.stroke([N(xe1 - s.o0 / 2, ybb, 90, s.o, line=True), rn['r'], rn['t'], rn['l'], rn['b'], rn['r']],
             cut1=term(rn, -lc.theta_e(P), P), kL=rn['ki'])
    g.rect(xe0 + s.o0 * 0.5, ybb, xe1 - s.o0 * 0.5, ybb + hb)
    g.w = xe1 + P.so * 0.92
    g.anchor('top', xe0 + s.o0 / 2, P.xh); g.anchor('bottom', xe0 + s.o0 / 2, 0)


def eszett(g, upper):
    P = g.P; s = S(P, upper)
    wt = clamp(P.wt, 0, 1)
    sb = P.SB if upper else P.sb
    w = (P.Hw * (0.98 + 0.12 * wt)) if upper else (P.nw * (1.06 + 0.16 * wt))
    htop = (P.cap + P.os) if upper else (P.asc + P.os)
    xl = sb + s.v0 / 2
    x1 = sb + w
    xr_up = x1 - w * ((0.17 if upper else 0.19) + 0.03 * wt) - s.v0 / 2
    ym = (P.cap * 0.50) if upper else (P.xh * 0.60)
    fm = 0.92 - 0.14 * wt; hm = s.h * fm
    a = arch(g, xl, xr_up, htop, upper=upper, stem_to=ym - hm / 2, href=(P.cap if upper else P.asc), lo=0.20, hi=0.34,
             fr=1.0 - 0.10 * wt)
    g.vstem(xl, 0, a['ys'], s.v)
    hb = s.h * (1.0 - 0.10 * wt); tv = s.o * (1.0 - 0.12 * wt)
    ylc = ((ym - hm / 2) + (-P.os + hb)) / 2
    xlv = xl + s.v0 / 2 + w * (0.13 - 0.06 * wt)
    cxl = (xlv + x1) / 2
    xm0 = xr_up - s.v0 / 2
    rl = dict(cx=cxl, cy=ylc, rx=cxl - xlv - tv * 0.92, ry=ylc + P.os - hb)
    g.stroke([N(xm0, ym, 0, hm, line=True), N(max(cxl + w * 0.04, xm0 + 4), ym, 0, hm), N(x1 - tv / 2, ylc, -90, tv),
              N(cxl, -P.os + hb / 2, 180, hb), N(xlv + tv * 0.46, ylc, 90, tv * 0.92)],
             cut1=term(rl, 180 + 34, P), kR=P.ki(rl['rx'], rl['ry']))
    g.w = x1 + (P.SO if upper else P.so)
    g.anchor('top', (xl + x1) / 2, P.cap if upper else P.asc); g.anchor('bottom', (xl + x1) / 2, 0)


glyph('germandbls', 0xDF)(lambda g: eszett(g, False))
glyph('uni1E9E', [0x1E9E])(lambda g: eszett(g, True))


@glyph('Eth', [0xD0, 0x110])
def Eth(g):
    P = g.P; s = U(P)
    off = P.Hw * 0.07
    with g.shift(off, 0):
        uc.D(g)
    probe = G(P); uc.D(probe)
    xs = off + P.SB + s.v0 / 2
    hb = s.h * 0.92
    g.rect(xs - s.v0 / 2 - P.Hw * 0.13, P.cap * 0.525 - hb / 2, xs + s.v0 / 2 + P.Hw * 0.22, P.cap * 0.525 + hb / 2)
    g.w = probe.w + off
    g.anchors = {k: (x + off, y) for k, (x, y) in probe.anchors.items()}


@glyph('eth', 0xF0)
def eth(g):
    P = g.P; s = S(P, False)
    x0 = P.so; x1 = x0 + P.ow
    ybt = P.xh * 0.94 + P.os
    rn = ring(g, x0, x1, bot(P), ybt)
    xt = x0 + P.ow * 0.26
    g.stroke([N(x1 - s.o0 / 2, rn['cy'], 90, s.o), N(xt, P.asc - s.h * 0.2, 150, s.o * 0.86)],
             kL=None)
    t = s.h * (0.84 - 0.12 * clamp(P.wt, 0, 1))
    cxb = x0 + P.ow * 0.60; cyb = P.xh + (P.asc - P.xh) * 0.52
    with g.rot(28, cxb, cyb):
        g.rect(cxb - P.ow * 0.26, cyb - t / 2, cxb + P.ow * 0.26, cyb + t / 2)
    g.w = P.ow + 2 * P.so
    g.anchor('top', x0 + P.ow / 2, P.asc)


@glyph('Thorn', 0xDE)
def Thorn(g):
    P = g.P; s = U(P)
    xs = P.SB + s.v0 / 2
    w = P.Hw * 0.87
    g.vstem(xs, 0, P.cap, s.v)
    d_bowl(g, xs, P.SB + w, P.cap * 0.185, P.cap * 0.815, s, straight=0.30)
    g.w = P.SB + w + P.SO * 0.8


@glyph('thorn', 0xFE)
def thorn(g):
    lc.bd_body(g, True, True)


@glyph('dcroat', 0x111)
def dcroat(g):
    P = g.P; s = S(P, False)
    lc.d(g)
    xs = g.anchors['top'][0]
    hb = s.h * 0.86
    yb = P.xh + (P.asc - P.xh) * 0.52
    g.rect(xs - s.v0 / 2 - P.nw * 0.30, yb - hb / 2, xs + s.v0 / 2 + P.nw * 0.12, yb + hb / 2)
    g.w = max(g.w, xs + s.v0 / 2 + P.nw * 0.12 + P.so * 0.6)


@glyph('Hbar', 0x126)
def Hbar(g):
    P = g.P; s = U(P)
    uc.H(g)
    hb = s.h * 0.84
    g.rect(P.SB - P.Hw * 0.07, P.cap * 0.80 - hb / 2, P.SB + P.Hw * 1.07, P.cap * 0.80 + hb / 2)


@glyph('hbar', 0x127)
def hbar(g):
    P = g.P; s = S(P, False)
    lc.h(g)
    hb = s.h * 0.86; yb = P.xh + (P.asc - P.xh) * 0.52
    xs = P.sb + s.v0 / 2
    g.rect(xs - s.v0 / 2 - P.nw * 0.13, yb - hb / 2, xs + s.v0 / 2 + P.nw * 0.26, yb + hb / 2)


@glyph('Lslash', 0x141)
def Lslash(g):
    P = g.P; s = U(P)
    off = P.Hw * 0.07
    with g.shift(off, 0):
        uc.L(g)
    probe = G(P); uc.L(probe)
    xs = off + P.SB + s.v0 / 2
    t = s.h * 0.92
    diag(g, (xs - P.Hw * 0.20, P.cap * 0.40), (xs + P.Hw * 0.24, P.cap * 0.62), t * 0.95, 0, 0)
    g.w = probe.w + off
    g.anchors = {k: (x + off, y) for k, (x, y) in probe.anchors.items()}
    b = g.bounds()
    if b[0] < P.SD:
        g.w += P.SD - b[0]; g.translate(P.SD - b[0])


@glyph('lslash', 0x142)
def lslash(g):
    P = g.P; s = S(P, False)
    off = P.nw * 0.10
    with g.shift(off, 0):
        lc.l(g)
    probe = G(P); lc.l(probe)
    xs = off + P.sb + s.v0 / 2
    t = s.h * 0.90
    diag(g, (xs - P.nw * 0.24, P.asc * 0.44), (xs + P.nw * 0.24, P.asc * 0.62), t * 0.95, 0, 0)
    g.w = probe.w + off
    g.anchors = {k: (x + off, y) for k, (x, y) in probe.anchors.items()}
    b = g.bounds()
    if b[0] < P.sd:
        g.w += P.sd - b[0]; g.translate(P.sd - b[0])
    g.w = max(g.w, g.bounds()[2] + P.sd)


@glyph('Tbar', 0x166)
def Tbar(g):
    P = g.P; s = U(P)
    uc.T(g)
    probe = G(P); uc.T(probe)
    cx = probe.w / 2; hb = s.h * 0.86
    g.rect(cx - P.Hw * 0.24, P.cap * 0.46 - hb / 2, cx + P.Hw * 0.24, P.cap * 0.46 + hb / 2)


@glyph('tbar', 0x167)
def tbar(g):
    P = g.P; s = S(P, False)
    lc.t(g)
    xs = g.anchors['top'][0]; hb = s.h * 0.82
    g.rect(xs - s.v0 / 2 - P.nw * 0.16, P.xh * 0.50 - hb / 2, xs + s.v0 / 2 + P.nw * 0.22, P.xh * 0.50 + hb / 2)


@glyph('Eng', 0x14A)
def Eng(g):
    P = g.P; s = U(P)
    w = P.Hw * 1.0
    xl = P.SB + s.v0 / 2; xr = P.SB + w - s.v0 / 2
    g.vstem(xl, 0, P.cap, s.v)
    arch(g, xl, xr, ctop(P), upper=True, href=P.cap, stem_to=P.cap * 0.10, lo=0.30, hi=0.42)
    hook(g, xr, P.cap * 0.30, P.desc * 0.90 + (w - s.v0) * 0.30 + s.h / 2, xr - (w - s.v0) * 0.46, P.desc * 0.90, upper=True)
    g.w = w + 2 * P.SB * 0.97
    g.anchor('top', P.SB + w / 2, P.cap); g.anchor('bottom', P.SB + w / 2, 0)


@glyph('eng', 0x14B)
def eng(g):
    P = g.P; s = S(P, False)
    xl, xr = lc.n_body(g)
    hook(g, xr, P.xh * 0.30, P.desc + (P.nw - s.v0) * 0.36 + s.h / 2, xr - (P.nw - s.v0) * 0.48, P.desc)
    g.anchor('top', P.sb + P.nw / 2, P.xh); g.anchor('bottom', P.sb + P.nw / 2, 0)


@glyph('kgreenlandic', 0x138)
def kgreenlandic(g):
    P = g.P; s = S(P, False)
    xs = P.sb + s.v0 / 2
    g.vstem(xs, 0, P.xh, s.v)
    lc.k_arms(g, xs, s, P.xh, (P.nw - s.v0) * 1.04 + s.v0 * 0.3)
    g.w = g.bounds()[2] + P.sd * 0.6


@glyph('longs', 0x17F)
def longs(g):
    P = g.P; s = S(P, False)
    left = (P.nw - s.v0) * 0.16; reach = (P.nw - s.v0) * 0.40
    xs = P.so * 0.9 + left + s.v0 / 2
    x_end = xs + s.v0 / 2 + reach
    hook(g, xs, 0, P.asc - (P.nw - s.v0) * 0.40 - s.h / 2, x_end, P.asc + P.os * 0.4)
    g.rect(xs - s.v0 / 2 - left, P.xh - s.h, xs, P.xh)
    g.w = x_end + P.so * 0.2


def e_turned(g, upper):
    P = g.P; s = S(P, upper)
    if upper:
        x0 = P.SO; x1 = x0 + P.Ow * 0.94; y0 = cbot(P); y1 = ctop(P)
    else:
        x0 = P.so; x1 = x0 + P.ow * 0.975; y0 = bot(P); y1 = top(P)
    w = x1 + x0 * 0.92
    wt = clamp(P.wt, 0, 1)
    with g.rot180(w / 2, (y0 + y1) / 2):
        rn = round_nodes(P, x0, x1, y0, y1, upper)
        hb = s.h * (0.96 - 0.12 * wt)
        ybb = rn['cy'] - hb * 0.42
        g.stroke([N(x1 - s.o0 / 2, ybb, 90, s.o, line=True), rn['r'], rn['t'], rn['l'], rn['b'], rn['r']],
                 cut1=term(rn, -lc.theta_e(P), P), kL=rn['ki'])
        g.rect(x0 + s.o0 * 0.5, ybb, x1 - s.o0 * 0.5, ybb + hb)
    g.w = w


glyph('schwa', 0x259)(lambda g: e_turned(g, False))
glyph('Schwa', 0x18F)(lambda g: e_turned(g, True))


@glyph('IJ', 0x132)
def IJ(g):
    g.seq = ['I', 'J']; g.w = None


@glyph('ij', 0x133)
def ij(g):
    g.seq = ['i', 'j']; g.w = None


@glyph('napostrophe', 0x149)
def napostrophe(g):
    g.seq = ['quoteright', ('n', -g.P.sb * 0.5)]; g.w = None


@glyph('Ldot', 0x13F)
def Ldot(g):
    P = g.P; d = pd(P)
    uc.L(g)
    g.dot(P.SB + P.Hw * (0.50 + 0.07 * wtc(P)), P.cap * 0.56, d * (1.0 - 0.15 * wtc(P)))


@glyph('ldot', 0x140)
def ldot(g):
    P = g.P; d = pd(P)
    lc.l(g)
    probe = G(P); lc.l(probe)
    g.dot(probe.w + d * 0.30, P.xh * 0.5, d)
    g.w = probe.w + d * 0.80 + P.so * 0.7


@glyph('periodcentered.loclCAT')
def punt_volat(g):
    """Catalan punt volat, tucked between two l (l·l)."""
    P = g.P; d = pd(P)
    g.dot(d * 0.5 - P.so * 0.15, P.xh * 0.5, d)
    g.w = d * 0.72


@glyph('periodcentered.loclCAT.case')
def punt_volat_case(g):
    P = g.P; d = pd(P)
    g.dot(-P.Hw * 0.20, P.cap * 0.5, d)
    g.w = P.SO * 0.4
