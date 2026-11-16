"""Orion — Cyrillic (Russian, Ukrainian, Belarusian, Bulgarian, Serbian, Macedonian)."""
from __future__ import annotations
from .geom import N, E, Line, G
from .parts import glyph, S, round_nodes, term, ring, arch, bowl, sline, edges, diag, vee, hook, clamp
from . import latin_lc as lc, latin_uc as uc
from .latin_lc import top, bot
from .latin_uc import U, ctop, cbot, wtc, d_bowl
from .greek import alias, eps_shape, six_like


class Cx:
    """Case context: Cyrillic lowercase is largely built as small capitals,
    drawn with lowercase strokes on the x-height."""
    def __init__(self, P, up):
        self.P = P; self.up = up; self.s = S(P, up)
        self.ht = P.cap if up else P.xh
        self.sb = P.SB if up else P.sb
        self.so = P.SO if up else P.so
        self.sd = P.SD if up else P.sd
        self.w = P.Hw if up else P.nw * 1.04
        self.ow = P.Ow if up else P.ow
        self.top = self.ht + P.os; self.bot = -P.os
        self.tick = (P.cap * 0.20) if up else (P.xh * 0.24)


def both(cap_cp, name_fn=None):
    """Register an upper and lower form from one construction."""
    def deco(fn):
        glyph('uni%04X' % cap_cp, [cap_cp])(lambda g: fn(g, Cx(g.P, True)))
        lo = cap_cp + 1 if cap_cp >= 0x460 else (cap_cp + 0x20 if cap_cp >= 0x410 else cap_cp + 0x50)
        glyph('uni%04X' % lo, [lo])(lambda g: fn(g, Cx(g.P, False)))
        return fn
    return deco


def lower(cp):
    def deco(fn):
        glyph('uni%04X' % cp, [cp])(lambda g: fn(g, Cx(g.P, False)))
        return fn
    return deco


# capitals identical to Latin / Greek
for _cp, _b in ((0x410, 'A'), (0x412, 'B'), (0x415, 'E'), (0x41A, 'K'), (0x41C, 'M'), (0x41D, 'H'), (0x41E, 'O'),
                (0x420, 'P'), (0x421, 'C'), (0x422, 'T'), (0x425, 'X'), (0x405, 'S'), (0x406, 'I'), (0x408, 'J'),
                (0x413, 'Gamma'), (0x41F, 'Pi')):
    alias('uni%04X' % _cp, [_cp], _b)
# lowercase identical to Latin
for _cp, _b in ((0x430, 'a'), (0x435, 'e'), (0x43E, 'o'), (0x440, 'p'), (0x441, 'c'), (0x443, 'y'), (0x445, 'x'),
                (0x455, 's'), (0x456, 'i'), (0x458, 'j')):
    alias('uni%04X' % _cp, [_cp], _b)


def stems(g, c, xs_list, y0=0.0, y1=None):
    for x in xs_list:
        g.vstem(x, y0, c.ht if y1 is None else y1, c.s.v)


def soft_bowl(g, c, xs, x1, ytop):
    """Lower bowl of the soft-sign family."""
    fm = 0.94 - 0.08 * clamp(c.P.wt, 0, 1)
    d_bowl(g, xs, x1, 0, ytop, c.s, ft=fm, straight=0.30)


# ------------------------------------------------------------ small capitals for lowercase
@lower(0x432)
def ve(g, c):                                   # в
    P = g.P; s = c.s
    xs = c.sb + s.v0 / 2
    w = c.w * (0.92 + 0.06 * clamp(P.wt, 0, 1))
    x1 = c.sb + w; x1u = c.sb + w * 0.945
    ym = c.ht * 0.528
    fm = 0.93 - 0.10 * clamp(P.wt, 0, 1); hm = s.h * fm
    g.vstem(xs, 0, c.ht, s.v)
    d_bowl(g, xs, x1u, ym - hm / 2, c.ht, s, fb=fm, fr=0.96, straight=0.30)
    d_bowl(g, xs, x1, 0, ym + hm / 2, s, ft=fm, straight=0.26)
    g.w = x1 + c.so * 0.95


@lower(0x433)
def ghe(g, c):                                  # г
    s = c.s
    xs = c.sb + s.v0 / 2; w = c.w * 0.78
    g.vstem(xs, 0, c.ht, s.v)
    g.rect(xs, c.ht - s.h, c.sb + w, c.ht)
    g.w = c.sb + w + c.so * 0.40
    g.anchor('top', c.sb + w * 0.45, c.ht)


@both(0x490)
def ghe_upturn(g, c):                           # Ґ ґ
    s = c.s
    xs = c.sb + s.v0 / 2; w = c.w * (0.80 if c.up else 0.78)
    g.vstem(xs, 0, c.ht, s.v)
    g.rect(xs, c.ht - s.h, c.sb + w, c.ht)
    tv = s.v * 0.80
    g.rect(c.sb + w - tv, c.ht - s.h, c.sb + w, c.ht + c.tick * 0.72)
    g.w = c.sb + w + c.so * 0.50


@both(0x414)
def de(g, c):                                   # Д д
    P = g.P; s = c.s
    w = c.w * (1.10 if c.up else 1.06)
    x0 = c.so * 0.55
    ext = w * 0.075
    xr = x0 + w - ext - s.v0 / 2
    hb = s.h
    g.rect(x0, 0, x0 + w, hb)
    tv = s.v * 0.86
    for xx in (x0, x0 + w - tv):
        g.rect(xx, -c.tick, xx + tv, hb)
    g.vstem(xr, 0, c.ht, s.v)
    f = 0.92 - 0.10 * wtc(P)
    xtl = x0 + ext + w * 0.22
    ln = sline((x0 + ext, hb), -1, (xtl, c.ht), -1, s.d0 * f)
    l, r = edges(ln, s.d * f)
    g.poly([l.at_y(hb * 0.5), r.at_y(hb * 0.5), r.at_y(c.ht), l.at_y(c.ht)])
    g.rect(l.at_y(c.ht)[0], c.ht - s.h, xr, c.ht)
    g.w = x0 * 2 + w
    g.anchor('top', (xtl + xr) / 2, c.ht)


@both(0x416)
def zhe(g, c):                                  # Ж ж
    P = g.P; s = c.s
    reach = (c.w - s.v0) * (0.74 if c.up else 0.78)
    probe = G(P)
    lc.k_arms(probe, 0, s, c.ht, reach)
    half = probe.bounds()[2]
    cx = c.sd * 1.2 + half
    g.vstem(cx, 0, c.ht, s.v * 0.96)
    with g.shift(cx, 0):
        lc.k_arms(g, 0, s, c.ht, reach)
    with g.flip_x(cx):
        with g.shift(cx, 0):
            lc.k_arms(g, 0, s, c.ht, reach)
    g.w = 2 * cx


@both(0x417)
def ze(g, c):                                   # З з
    w = c.ow * (0.74 if c.up else 0.78)
    x0 = c.so * 1.05
    eps_shape(g, x0, x0 + w, c.bot, c.top, c.up)
    g.w = w + c.so * 2.0


@both(0x418)
def i_cyr(g, c):                                # И и
    P = g.P; s = c.s
    w = c.w * (1.035 if c.up else 1.0)
    xl = c.sb + s.v0 / 2; xr = c.sb + w - s.v0 / 2
    f = 0.95 - 0.15 * wtc(P)
    stems(g, c, (xl, xr))
    diag(g, (c.sb, 0), (c.sb + w, c.ht), s.d * f, -1, +1, t0=s.d0 * f)
    g.w = w + 2 * c.sb


@lower(0x43A)
def ka(g, c):                                   # к
    g.comp('kgreenlandic', 0, 0); g.w = None


@both(0x41B)
def el(g, c):                                   # Л л
    P = g.P; s = c.s
    w = c.w * (1.02 if c.up else 1.0)
    x0 = c.sd * 1.6
    xr = x0 + w - s.v0 / 2
    f = 0.95 - 0.10 * wtc(P)
    xtl = x0 + w * 0.26
    ln = sline((x0, 0), -1, (xtl, c.ht), -1, s.d0 * f)
    l, r = edges(ln, s.d * f)
    g.poly([l.at_y(0), r.at_y(0), r.at_y(c.ht), l.at_y(c.ht)])
    g.rect(l.at_y(c.ht)[0], c.ht - s.h, xr, c.ht)
    g.vstem(xr, 0, c.ht, s.v)
    g.w = xr + s.v0 / 2 + c.sb
    g.anchor('top', (xtl + xr) / 2, c.ht)


@lower(0x43C)
def em(g, c):                                   # м
    P = g.P; s = c.s
    w = c.w * 1.20
    xl = c.sb + s.v0 / 2; xr = c.sb + w - s.v0 / 2
    f = 0.90 - 0.16 * wtc(P)
    stems(g, c, (xl, xr))
    vee(g, c.sb, c.sb + w, c.ht, 0, s.d * f, s.d0 * f, s.d0 * (0.84 - 0.34 * wtc(P)))
    g.w = w + 2 * c.sb


@lower(0x43D)
def en(g, c):                                   # н
    s = c.s
    xl = c.sb + s.v0 / 2; xr = c.sb + c.w - s.v0 / 2
    stems(g, c, (xl, xr))
    hb = s.h * 0.97
    g.rect(xl, c.ht * 0.53 - hb / 2, xr, c.ht * 0.53 + hb / 2)
    g.w = c.w + 2 * c.sb


@lower(0x43F)
def pe(g, c):                                   # п
    s = c.s
    xl = c.sb + s.v0 / 2; xr = c.sb + c.w - s.v0 / 2
    stems(g, c, (xl, xr))
    g.rect(xl, c.ht - s.h, xr, c.ht)
    g.w = c.w + 2 * c.sb


@lower(0x442)
def te(g, c):                                   # т
    s = c.s
    w = c.w * 0.98; lsb = c.so * 0.62
    g.rect(lsb, c.ht - s.h, lsb + w, c.ht)
    g.vstem(lsb + w / 2, 0, c.ht, s.v)
    g.w = w + 2 * lsb


@glyph('uni0423', [0x423])
def U_cyr(g):                                   # У
    P = g.P; s = U(P)
    w = P.Hw * 1.10; x0 = P.SD; x1 = x0 + w
    ap = s.d0 * (0.90 - 0.28 * wtc(P))
    yv = P.cap * 0.26
    cl, cr, crotch = vee(g, x0, x1, P.cap, yv, s.d, s.d0, ap, draw=False, cx=(x0 + x1) / 2 + w * 0.04)
    ll, lr = edges(cl, s.d); rl, rr = edges(cr, s.d)
    g.poly([rr.at_y(P.cap), rl.at_y(P.cap), crotch, lr.at_y(P.cap), ll.at_y(P.cap), ll & rl, rl.at_y(0), rr.at_y(0)])
    g.w = w + 2 * P.SD
    g.anchor('top', (x0 + x1) / 2, P.cap)


@both(0x424)
def ef(g, c):                                   # Ф ф
    P = g.P; s = c.s
    if c.up:
        w = P.Ow * (1.04 + 0.10 * wtc(P)); x0 = P.SO
        ring(g, x0, x0 + w, P.cap * 0.12, P.cap * 0.88, upper=True, ft=0.94, fb=0.94)
        g.vstem(x0 + w / 2, 0, P.cap, s.v * (1.0 - 0.10 * wtc(P)))
    else:
        w = P.ow * (1.16 + 0.20 * wtc(P)); x0 = P.so
        ring(g, x0, x0 + w, bot(P), top(P))
        g.vstem(x0 + w / 2, P.desc, P.asc, s.v * (0.96 - 0.14 * wtc(P)))
        g.anchor('top', x0 + w / 2, P.asc)
    g.w = w + 2 * x0


def sha_body(g, c, n, tick):
    s = c.s
    pitch = (c.w - s.v0) * (0.80 if n == 3 else 1.0)
    xl = c.sb + s.v0 / 2
    xs = [xl + i * pitch for i in range(n)]
    stems(g, c, xs)
    xe = xs[-1] + s.v0 / 2 + (c.w * 0.085 if tick else 0)
    g.rect(c.sb, 0, xe, s.h)
    if tick:
        tv = s.v * 0.86
        g.rect(xe - tv, -c.tick, xe, s.h)
    g.w = xe + (c.so * 0.9 if tick else c.sb)


both(0x426)(lambda g, c: sha_body(g, c, 2, True))      # Ц ц
both(0x428)(lambda g, c: sha_body(g, c, 3, False))     # Ш ш
both(0x429)(lambda g, c: sha_body(g, c, 3, True))      # Щ щ


@both(0x427)
def che(g, c):                                  # Ч ч
    P = g.P; s = c.s
    w = c.w * 0.94
    xl = c.sb * 0.92 + s.v0 / 2; xr = c.sb * 0.92 + w - s.v0 / 2
    ym = c.ht * 0.40
    r = min((w - s.v0) * 0.52, c.ht * 0.34)
    hm = s.h * 0.97
    g.vstem(xr, 0, c.ht, s.v)
    g.stroke([N(xl, c.ht, -90, s.v, line=True), N(xl, ym + r, -90, s.v), N(xl + r, ym, 0, hm, line=True), N(xr, ym, 0, hm)],
             kL=P.ki(r - s.v0 / 2, r - hm / 2))
    g.w = w + c.sb * 1.92


@both(0x42C)
def soft(g, c):                                 # Ь ь
    s = c.s
    xs = c.sb + s.v0 / 2; w = c.w * (0.90 if c.up else 0.92)
    g.vstem(xs, 0, c.ht, s.v)
    soft_bowl(g, c, xs, c.sb + w, c.ht * 0.585)
    g.w = c.sb + w + c.so * 0.95


@both(0x42A)
def hard(g, c):                                 # Ъ ъ
    s = c.s
    flag = c.w * 0.24
    xs = c.so * 0.6 + flag + s.v0 / 2; w = c.w * (0.90 if c.up else 0.92)
    g.vstem(xs, 0, c.ht, s.v)
    g.rect(xs - s.v0 / 2 - flag, c.ht - s.h, xs, c.ht)
    soft_bowl(g, c, xs, xs - s.v0 / 2 + w, c.ht * 0.585)
    g.w = xs - s.v0 / 2 + w + c.so * 0.95


@both(0x42B)
def yeru(g, c):                                 # Ы ы
    s = c.s
    xs = c.sb + s.v0 / 2; w = c.w * (0.86 if c.up else 0.88)
    g.vstem(xs, 0, c.ht, s.v)
    soft_bowl(g, c, xs, c.sb + w, c.ht * 0.585)
    x2 = c.sb + w + c.so + c.sb * 0.9 + s.v0 / 2
    g.vstem(x2, 0, c.ht, s.v)
    g.w = x2 + s.v0 / 2 + c.sb


@both(0x42D)
def e_rev(g, c):                                # Э э
    P = g.P; s = c.s
    w = c.ow * (0.90 if c.up else 0.93)
    x0 = c.so * 0.9
    wtot = w + x0 + c.so
    with g.flip_x(wtot / 2):
        rn = round_nodes(P, c.so, c.so + w * 1.04, c.bot, c.top, upper=c.up)
        th = (43.0 if c.up else 44.0) + 14.0 * (P.ap - 1.0)
        g.stroke([rn['r'], rn['t'], rn['l'], rn['b'], rn['r']], cut0=term(rn, th, P), cut1=term(rn, -th, P), kL=rn['ki'])
        hb = s.h * 0.94
        g.rect(c.so + s.o0 * 0.5, rn['cy'] - hb / 2, rn['cx'] + w * 0.14, rn['cy'] + hb / 2)
    g.w = wtot


@both(0x404)
def ye_ukr(g, c):                               # Є є
    P = g.P; s = c.s
    w = c.ow * (0.93 if c.up else 0.95)
    rn = round_nodes(P, c.so, c.so + w * 1.04, c.bot, c.top, upper=c.up)
    th = (43.0 if c.up else 44.0) + 14.0 * (P.ap - 1.0)
    g.stroke([rn['r'], rn['t'], rn['l'], rn['b'], rn['r']], cut0=term(rn, th, P), cut1=term(rn, -th, P), kL=rn['ki'])
    hb = s.h * 0.94
    g.rect(c.so + s.o0 * 0.5, rn['cy'] - hb / 2, rn['cx'] + w * 0.20, rn['cy'] + hb / 2)
    g.w = g.bounds()[2] + c.so * 0.56


@both(0x42E)
def yu(g, c):                                   # Ю ю
    P = g.P; s = c.s
    xs = c.sb + s.v0 / 2
    ow = c.ow * (0.90 if c.up else 0.94)
    x0 = c.sb + s.v0 + c.w * 0.22
    g.vstem(xs, 0, c.ht, s.v)
    rn = ring(g, x0, x0 + ow, c.bot, c.top, upper=c.up)
    hb = s.h * 0.95
    g.rect(xs, c.ht * 0.52 - hb / 2, x0 + s.o0 * 0.5, c.ht * 0.52 + hb / 2)
    g.w = x0 + ow + c.so


@both(0x42F)
def ya(g, c):                                   # Я я
    P = g.P; s = c.s
    w = c.w * (0.915 if c.up else 0.93)
    wtot = c.sb + w * 1.02 + c.sd * 1.4
    with g.flip_x(wtot / 2):
        xs = c.sb + s.v0 / 2
        x1 = c.sb + w * 0.965
        yb = c.ht * 0.44 - s.h * 0.45
        g.vstem(xs, 0, c.ht, s.v)
        d_bowl(g, xs, x1, yb, c.ht, s, fb=0.95, straight=0.30)
        t = s.d * (1.0 - 0.05 * wtc(P)); t0 = s.d0 * (1.0 - 0.05 * wtc(P))
        xj = xs + s.v0 / 2 + (x1 - xs) * (0.30 + 0.04 * wtc(P))
        diag(g, (xj, yb + s.h * 0.5), (c.sb + w * 1.02, 0), t, -1, +1, t0=t0)
    g.w = wtot


@glyph('uni0411', [0x411])
def Be(g):                                      # Б
    P = g.P; s = U(P); c = Cx(P, True)
    xs = c.sb + s.v0 / 2; w = c.w * 0.90
    g.vstem(xs, 0, c.ht, s.v)
    g.rect(xs, c.ht - s.h, c.sb + w * 0.92, c.ht)
    soft_bowl(g, c, xs, c.sb + w, c.ht * 0.585)
    g.w = c.sb + w + c.so * 0.95


@glyph('uni0431', [0x431])
def be(g):                                      # б
    P = g.P; s = S(P, False)
    x0 = P.so; x1 = x0 + P.ow
    ybt = P.xh * 0.96 + P.os
    rn = ring(g, x0, x1, bot(P), ybt)
    xe = x1 - P.ow * 0.04
    cxt = (x0 + xe) / 2 + P.ow * 0.08
    g.stroke([N(x0 + s.o0 / 2, rn['cy'], 90, s.o), N(cxt, P.asc - s.h / 2, 0, s.h * 0.98, line=True), N(xe, P.asc - s.h / 2, 0, s.h * 0.98)],
             kR=P.ki(cxt - x0 - s.o0, P.asc - rn['cy'] - s.h))
    g.w = P.ow + 2 * P.so
    g.anchor('top', x0 + P.ow * 0.5, P.asc)


@glyph('uni0431.loclSRB')
def be_srb(g):
    """Serbian / Macedonian be: the flag rises as a curl instead of a bar."""
    P = g.P; s = S(P, False)
    x0 = P.so; x1 = x0 + P.ow
    ybt = P.xh * 0.94 + P.os
    rn = ring(g, x0, x1, bot(P), ybt)
    g.stroke([N(x0 + s.o0 / 2, rn['cy'], 90, s.o), N(x0 + P.ow * 0.40, P.xh + (P.asc - P.xh) * 0.56, 40, s.o * 0.90),
              N(x1 - P.ow * 0.10, P.asc - s.h * 0.45, 14, s.h * 0.92)], k=P.k)
    g.w = P.ow + 2 * P.so


@both(0x409)
def lje(g, c):                                  # Љ љ
    P = g.P; s = c.s
    w = c.w * (0.96 if c.up else 0.96)
    x0 = c.sd * 1.6
    xr = x0 + w - s.v0 / 2
    f = 0.95 - 0.10 * wtc(P)
    xtl = x0 + w * 0.26
    ln = sline((x0, 0), -1, (xtl, c.ht), -1, s.d0 * f)
    l, r = edges(ln, s.d * f)
    g.poly([l.at_y(0), r.at_y(0), r.at_y(c.ht), l.at_y(c.ht)])
    g.rect(l.at_y(c.ht)[0], c.ht - s.h, xr, c.ht)
    g.vstem(xr, 0, c.ht, s.v)
    x1 = xr + s.v0 / 2 + c.w * 0.62
    soft_bowl(g, c, xr, x1, c.ht * 0.585)
    g.w = x1 + c.so * 0.95


@both(0x40A)
def nje(g, c):                                  # Њ њ
    s = c.s
    xl = c.sb + s.v0 / 2; xr = c.sb + c.w * 0.96 - s.v0 / 2
    stems(g, c, (xl, xr))
    hb = s.h * 0.95
    ytop = c.ht * 0.585
    g.rect(xl, ytop - hb, xr, ytop)
    x1 = xr + s.v0 / 2 + c.w * 0.62
    soft_bowl(g, c, xr, x1, ytop)
    g.w = x1 + c.so * 0.95


@both(0x40F)
def dzhe(g, c):                                 # Џ џ
    s = c.s
    xl = c.sb + s.v0 / 2; xr = c.sb + c.w - s.v0 / 2
    stems(g, c, (xl, xr))
    g.rect(xl, 0, xr, s.h)
    tv = s.v * 0.86
    cx = (xl + xr) / 2
    g.rect(cx - tv / 2, -c.tick, cx + tv / 2, s.h)
    g.w = c.w + 2 * c.sb


@glyph('uni0402', [0x402])
def Dje(g):                                     # Ђ
    P = g.P; s = U(P)
    w = P.Hw * 1.10; lsb = P.SO * 0.62
    xs = lsb + w * 0.30
    g.rect(lsb, P.cap - s.h, lsb + w * 0.80, P.cap)
    g.vstem(xs, 0, P.cap, s.v)
    xr = lsb + w - s.v0 / 2
    arch(g, xs, xr, P.cap * 0.60 + P.os, upper=True, href=P.cap * 0.6, stem_to=P.cap * 0.10, lo=0.30, hi=0.50)
    yt = s.h / 2 + max((w - s.v0) * 0.20, s.v * 0.62)
    hook(g, xr, max(P.cap * 0.24, yt + 6), yt, xr - max((w - s.v0) * 0.30, s.v * 1.0), 0, upper=True)
    g.w = lsb + w + P.SB * 0.9


@glyph('uni040B', [0x40B])
def Tshe(g):                                    # Ћ
    P = g.P; s = U(P)
    w = P.Hw * 1.10; lsb = P.SO * 0.62
    xs = lsb + w * 0.30
    g.rect(lsb, P.cap - s.h, lsb + w * 0.80, P.cap)
    g.vstem(xs, 0, P.cap, s.v)
    arch(g, xs, lsb + w - s.v0 / 2, P.cap * 0.60 + P.os, upper=True, href=P.cap * 0.6, lo=0.30, hi=0.50)
    g.w = lsb + w + P.SB * 0.95


@glyph('uni0452', [0x452])
def dje(g):                                     # ђ
    P = g.P; s = S(P, False)
    xl, xr = lc.n_body(g, True)
    hb = s.h * 0.86; yb = P.xh + (P.asc - P.xh) * 0.52
    g.rect(xl - s.v0 / 2 - P.nw * 0.13, yb - hb / 2, xl + s.v0 / 2 + P.nw * 0.26, yb + hb / 2)
    hook(g, xr, P.xh * 0.30, P.desc + (P.nw - s.v0) * 0.36 + s.h / 2, xr - (P.nw - s.v0) * 0.48, P.desc)
    g.anchor('top', xl, P.asc)


@glyph('uni045B', [0x45B])
def tshe(g):                                    # ћ
    g.comp('hbar', 0, 0); g.w = None

