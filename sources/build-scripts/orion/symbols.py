"""Orion — punctuation, currency, mathematical operators, arrows and UI symbols."""
from __future__ import annotations
import math
from .geom import N, E, Line, G, poly, poly_raw, superellipse, round_rect, reverse_contour
from .parts import glyph, S, round_nodes, term, ring, arch, bowl, sline, edges, diag, vee, hook, clamp
from . import latin_lc as lc, latin_uc as uc
from .latin_uc import U, ctop, cbot, wtc, fig_w, fig_sb, fig_adv, d_bowl


def pd(P): return P.dotd * 1.08 * P.punct
def psb(P): return P.so * 1.20 + 6
def axis(P): return P.cap * 0.5
def hair(P): return P.H * 0.97


# ------------------------------------------------------------ spaces
def _space(name, uni, f):
    @glyph(name, uni)
    def sp(g):
        g.w = f(g.P)
    return sp


_space('space', [0x20], lambda P: P.nw * 0.50 + P.sb * 0.5)
_space('uni00A0', [0xA0], lambda P: P.nw * 0.50 + P.sb * 0.5)
_space('uni2002', [0x2002], lambda P: 500.0)
_space('uni2003', [0x2003], lambda P: 1000.0)
_space('uni2007', [0x2007], lambda P: fig_adv(P))
_space('uni2008', [0x2008], lambda P: pd(P) + 2 * psb(P))
_space('uni2009', [0x2009], lambda P: 180.0 * P.wf ** 0.5)
_space('uni200A', [0x200A], lambda P: 90.0 * P.wf ** 0.5)
_space('uni202F', [0x202F], lambda P: 180.0 * P.wf ** 0.5)
_space('uni200B', [0x200B], lambda P: 0.0)


# ------------------------------------------------------------ dots and commas
def comma_shape(g, cx, cy, d):
    g.dot(cx, cy, d)
    g.poly([(cx + d / 2, cy - d * 0.04), (cx + d / 2, cy - d * 0.44), (cx - d * 0.06, cy - d * 1.40),
            (cx - d * 0.42, cy - d * 1.40), (cx + d * 0.04, cy - d * 0.42)])


@glyph('period', 0x2E)
def period(g):
    P = g.P; d = pd(P)
    g.dot(psb(P) + d / 2, d / 2, d)
    g.w = d + 2 * psb(P)


@glyph('comma', 0x2C)
def comma(g):
    P = g.P; d = pd(P)
    comma_shape(g, psb(P) + d / 2, d / 2, d)
    g.w = d + 2 * psb(P)


@glyph('colon', 0x3A)
def colon(g):
    P = g.P; d = pd(P)
    g.dot(psb(P) + d / 2, d / 2, d); g.dot(psb(P) + d / 2, P.xh - d / 2, d)
    g.w = d + 2 * psb(P)


@glyph('colon.case')
def colon_case(g):
    """Colon centred on figure height: used by `case` and between digits (timers)."""
    P = g.P; d = pd(P)
    gap = P.cap * 0.36
    g.dot(psb(P) + d / 2, axis(P) - gap / 2 - d * 0.0, d); g.dot(psb(P) + d / 2, axis(P) + gap / 2, d)
    g.w = d + 2 * psb(P)


@glyph('semicolon', 0x3B)
def semicolon(g):
    P = g.P; d = pd(P)
    comma_shape(g, psb(P) + d / 2, d / 2, d); g.dot(psb(P) + d / 2, P.xh - d / 2, d)
    g.w = d + 2 * psb(P)


@glyph('ellipsis', 0x2026)
def ellipsis(g):
    P = g.P; d = pd(P)
    step = d + 2 * psb(P) * 0.86
    for i in range(3):
        g.dot(psb(P) + d / 2 + i * step, d / 2, d)
    g.w = 2 * step + d + 2 * psb(P)


@glyph('periodcentered', 0xB7)
def periodcentered(g):
    P = g.P; d = pd(P)
    g.dot(psb(P) + d / 2, P.xh * 0.5, d)
    g.w = d + 2 * psb(P)


@glyph('bullet', 0x2022)
def bullet(g):
    P = g.P
    d = P.xh * 0.33 + P.v0 * 0.55
    g.dot(psb(P) + d / 2, P.xh * 0.5, d, k=0.62)
    g.w = d + 2 * psb(P)


@glyph('exclam', 0x21)
def exclam(g):
    P = g.P; s = U(P); d = pd(P)
    cx = psb(P) * 1.1 + max(d, s.v * 1.08) / 2
    wt_, wb = s.v * 1.08, s.v * 0.80
    yb = d + P.cap * 0.115
    g.poly([(cx - wb / 2, yb), (cx + wb / 2, yb), (cx + wt_ / 2, P.cap), (cx - wt_ / 2, P.cap)])
    g.dot(cx, d / 2, d)
    g.w = 2 * cx


@glyph('exclamdown', 0xA1)
def exclamdown(g):
    P = g.P
    probe = G(P); exclam(probe)
    with g.rot180(probe.w / 2, P.xh / 2):
        exclam(g)
    g.w = probe.w


def question_shape(g):
    P = g.P; s = U(P); d = pd(P)
    w = fig_w(P) * 0.86
    x0 = psb(P) * 0.8; x1 = x0 + w
    cx = (x0 + x1) / 2 - w * 0.03
    yuc = P.cap * 0.735
    ru = dict(cx=(x0 + x1) / 2, cy=yuc, rx=(x1 - x0) / 2 - s.o0 * 0.92, ry=ctop(P) - yuc - s.h)
    th = 180 - (30.0 + 10.0 * (P.ap - 1.0))
    yend = d + P.cap * 0.115
    g.stroke([N(x0 + s.o0 * 0.46, yuc, 90, s.o * 0.92), N((x0 + x1) / 2, ctop(P) - s.h / 2, 0, s.h),
              N(x1 - s.o0 / 2, yuc, -90, s.o), N(cx, yend + P.cap * 0.12, -90, s.v * 0.92, line=True, k=0.50),
              N(cx, yend, -90, s.v * 0.92)],
             cut0=term(ru, th, P), kR=P.ki(ru['rx'], ru['ry']))
    g.dot(cx, d / 2, d)
    g.w = x1 + psb(P) * 0.8


@glyph('question', 0x3F)
def question(g): question_shape(g)


@glyph('questiondown', 0xBF)
def questiondown(g):
    P = g.P
    probe = G(P); question_shape(probe)
    with g.rot180(probe.w / 2, P.xh / 2):
        question_shape(g)
    g.w = probe.w


# ------------------------------------------------------------ quotes
def qd(P): return pd(P) * 0.96


@glyph('quotesingle', 0x27)
def quotesingle(g):
    P = g.P; s = U(P)
    wt_, wb = s.v * 1.0, s.v * 0.70
    cx = psb(P) * 0.9 + wt_ / 2
    g.poly([(cx - wb / 2, P.cap * 0.62), (cx + wb / 2, P.cap * 0.62), (cx + wt_ / 2, P.asc), (cx - wt_ / 2, P.asc)])
    g.w = 2 * cx


@glyph('quotedbl', 0x22)
def quotedbl(g):
    P = g.P; s = U(P)
    wt_, wb = s.v * 1.0, s.v * 0.70
    cx = psb(P) * 0.9 + wt_ / 2
    step = wt_ + max(P.so * 1.5, wt_ * 0.55)
    for i in range(2):
        g.poly([(cx + i * step - wb / 2, P.cap * 0.62), (cx + i * step + wb / 2, P.cap * 0.62),
                (cx + i * step + wt_ / 2, P.asc), (cx + i * step - wt_ / 2, P.asc)])
    g.w = 2 * cx + step


def _quote(name, uni, n, flip, base):
    @glyph(name, uni)
    def q(g):
        P = g.P; d = qd(P)
        sbq = psb(P) * 0.85
        step = d + sbq * 1.1
        ytop = d if base else P.asc
        w = (n - 1) * step + d + 2 * sbq
        if flip:
            g.rot180(w / 2, ytop - d * 0.95)
        for i in range(n):
            comma_shape(g, sbq + d / 2 + i * step, ytop - d / 2, d)
        if flip:
            g.pop()
        g.w = w
    return q


_quote('quoteright', 0x2019, 1, False, False)
_quote('quoteleft', 0x2018, 1, True, False)
_quote('quotesinglbase', 0x201A, 1, False, True)
_quote('quotedblright', 0x201D, 2, False, False)
_quote('quotedblleft', 0x201C, 2, True, False)
_quote('quotedblbase', 0x201E, 2, False, True)


def _prime(name, uni, n):
    @glyph(name, uni)
    def pr(g):
        P = g.P; s = U(P)
        t = s.v * 0.86
        sbq = psb(P) * 0.8
        step = t * 1.9
        for i in range(n):
            x = sbq + i * step
            g.poly([(x, P.cap * 0.64), (x + t * 0.72, P.cap * 0.64), (x + t * 1.9, P.asc), (x + t * 0.85, P.asc)])
        g.w = sbq * 2 + (n - 1) * step + t * 1.9
    return pr


_prime('minute', 0x2032, 1)
_prime('second', 0x2033, 2)


def chevron(g, xv, yc, dx, dy, t):
    """Open chevron with its vertex at (xv, yc), arms running to xv + dx."""
    sg = 1 if dx > 0 else -1
    x1_ = xv + dx
    ext = (t / 2) / (abs(dy) / math.hypot(dx, dy))        # keep the outer tip on xv
    xv = xv + sg * min(ext, abs(dx) * 0.5)
    dx = x1_ - xv
    up = Line((xv, yc), (xv + dx, yc + dy)); lo = Line((xv, yc), (xv + dx, yc - dy))
    uo = up.offset(sg * t / 2); ui = up.offset(-sg * t / 2)
    lo_o = lo.offset(-sg * t / 2); li = lo.offset(sg * t / 2)
    x1 = xv + dx
    iv = ui & li
    lim = x1 - sg * abs(dx) * 0.12                     # the inner vertex never passes the arm ends
    if (iv[0] - lim) * sg > 0:
        iv = (lim, iv[1])
    g.poly([uo.at_x(x1), uo & lo_o, lo_o.at_x(x1), li.at_x(x1), iv, ui.at_x(x1)])


def _guil(name, uni, n, right):
    @glyph(name, uni)
    def gl(g):
        P = g.P; s = S(P, False)
        t = s.d * (0.90 - 0.22 * clamp(P.wt, 0, 1))
        dx = P.xh * 0.30 * P.wf ** 0.6 + t * 0.55; dy = P.xh * 0.31 + t * 0.10
        sbq = P.so * 1.3
        step = dx * 0.92 + t * 0.9
        w = sbq * 2 + dx + t * 0.7 + (n - 1) * step
        for i in range(n):
            if right:
                chevron(g, sbq + dx + t * 0.6 + i * step, P.xh * 0.5, -dx, dy, t)
            else:
                chevron(g, sbq + t * 0.1 + i * step, P.xh * 0.5, dx, dy, t)
        g.w = w
    return gl


_guil('guilsinglleft', 0x2039, 1, False)
_guil('guilsinglright', 0x203A, 1, True)
_guil('guillemotleft', 0xAB, 2, False)
_guil('guillemotright', 0xBB, 2, True)


# ------------------------------------------------------------ dashes
def _dash(name, uni, wfn, case=False):
    @glyph(name, uni)
    def dsh(g):
        P = g.P
        t = P.h * 0.98
        w = wfn(P)
        sbq = P.so * 1.15 if w < 420 else P.so * 0.3
        y = axis(P) if case else P.xh * 0.5 + P.cap * 0.012
        g.rect(sbq, y - t / 2, sbq + w, y + t / 2)
        g.w = w + 2 * sbq
    return dsh


_dash('hyphen', [0x2D, 0x2010, 0x2011], lambda P: P.nw * 0.60)
_dash('endash', [0x2013, 0x2012], lambda P: 500.0 * P.wf ** 0.7)
_dash('emdash', [0x2014, 0x2015], lambda P: 900.0 * P.wf ** 0.7)
_dash('hyphen.case', None, lambda P: P.nw * 0.60, True)
_dash('endash.case', None, lambda P: 500.0 * P.wf ** 0.7, True)
_dash('emdash.case', None, lambda P: 900.0 * P.wf ** 0.7, True)


@glyph('underscore', 0x5F)
def underscore(g):
    P = g.P
    g.rect(0, -150 - P.h * 0.9 / 2, 520 * P.wf ** 0.7, -150 + P.h * 0.9 / 2)
    g.w = 520 * P.wf ** 0.7


# ------------------------------------------------------------ brackets
def paren_shape(g, case=False):
    P = g.P; s = U(P)
    ytop = P.cap + 42 if case else P.asc + 26
    ybot = -42 if case else P.desc * 0.80
    depth = P.Hw * 0.20
    t = s.v * 0.90
    x0 = P.so * 1.45
    phi = 27.0
    g.stroke([N(x0 + depth + t * 0.36, ytop, 270 - phi, t * 0.74), N(x0 + t / 2, (ytop + ybot) / 2, 270, t),
              N(x0 + depth + t * 0.36, ybot, 270 + phi, t * 0.74)], k=0.60)
    g.w = x0 + depth + t * 0.72 + P.so * 0.7


def _mirror(name, uni, fn, *a):
    @glyph(name, uni)
    def m(g):
        probe = G(g.P); fn(probe, *a)
        with g.flip_x(probe.w / 2):
            fn(g, *a)
        g.w = probe.w
    return m


glyph('parenleft', 0x28)(lambda g: paren_shape(g))
_mirror('parenright', 0x29, paren_shape)
glyph('parenleft.case')(lambda g: paren_shape(g, True))
_mirror('parenright.case', None, paren_shape, True)


def bracket_shape(g, case=False):
    P = g.P; s = U(P)
    ytop = P.cap + 42 if case else P.asc + 26
    ybot = -42 if case else P.desc * 0.80
    t = s.v * 0.88; th = s.h * 0.88
    x0 = P.SB * 0.92; arm = P.Hw * 0.20 + t * 0.4
    g.rect(x0, ybot, x0 + t, ytop)
    g.rect(x0, ytop - th, x0 + t + arm, ytop)
    g.rect(x0, ybot, x0 + t + arm, ybot + th)
    g.w = x0 + t + arm + P.so * 0.8


glyph('bracketleft', 0x5B)(lambda g: bracket_shape(g))
_mirror('bracketright', 0x5D, bracket_shape)
glyph('bracketleft.case')(lambda g: bracket_shape(g, True))
_mirror('bracketright.case', None, bracket_shape, True)


def brace_shape(g, case=False):
    P = g.P; s = U(P)
    ytop = P.cap + 42 if case else P.asc + 26
    ybot = -42 if case else P.desc * 0.80
    ym = (ytop + ybot) / 2
    t = s.v * 0.86; th = s.h * 0.84
    arm = P.Hw * 0.17 + t * 0.2
    x0 = P.so * 1.1
    xm = x0 + arm + t / 2
    x1 = xm + t / 2 + arm
    ry = min((ytop - ym) * 0.30, arm * 1.5 + t * 0.5)
    for sgn in (1, -1):
        ye = ytop if sgn > 0 else ybot
        nodes = [N(x1, ye - sgn * th / 2, 180, th), N(xm, ye - sgn * ry, 270 if sgn > 0 else 90, t, line=True),
                 N(xm, ym + sgn * ry, 270 if sgn > 0 else 90, t), N(x0, ym + sgn * th * 0.0, 180, th)]
        g.stroke(nodes, k=0.62)
    g.w = x1 + P.so * 0.9


glyph('braceleft', 0x7B)(lambda g: brace_shape(g))
_mirror('braceright', 0x7D, brace_shape)
glyph('braceleft.case')(lambda g: brace_shape(g, True))
_mirror('braceright.case', None, brace_shape, True)


def slash_shape(g, y0=None, y1=None, dx=None, f=0.90):
    P = g.P; s = U(P)
    y0 = P.desc * 0.62 if y0 is None else y0
    y1 = P.asc + 20 if y1 is None else y1
    dx = P.Hw * 0.50 if dx is None else dx
    x0 = P.sd * 1.0
    ln = diag(g, (x0, y0), (x0 + dx, y1), s.d * f, -1, -1, t0=s.d0 * f)
    g.w = g.bounds()[2] + P.sd * 1.0


glyph('slash', [0x2F, 0x2215])(lambda g: slash_shape(g))
_mirror('backslash', 0x5C, slash_shape)


@glyph('fraction', 0x2044)
def fraction(g):
    """Fraction bar: narrow advance with overhang so numerators and denominators tuck in."""
    P = g.P; s = U(P)
    dx = P.Hw * 0.62; over = P.Hw * 0.26
    diag(g, (-over, -P.cap * 0.04), (-over + dx, P.cap * 1.04), s.d * 0.72, -1, -1, t0=s.d0 * 0.72)
    g.w = dx - 2 * over + s.d0 * (0.75 + 0.5 * wtc(P))


@glyph('bar', 0x7C)
def bar(g):
    P = g.P; s = U(P)
    t = s.v * 0.88
    g.rect(P.SB * 0.95, P.desc * 0.92, P.SB * 0.95 + t, P.asc + 26)
    g.w = t + 2 * P.SB * 0.95


@glyph('brokenbar', 0xA6)
def brokenbar(g):
    P = g.P; s = U(P)
    t = s.v * 0.88
    ym = (P.asc + 26 + P.desc * 0.92) / 2
    g.rect(P.SB * 0.95, P.desc * 0.92, P.SB * 0.95 + t, ym - 55)
    g.rect(P.SB * 0.95, ym + 55, P.SB * 0.95 + t, P.asc + 26)
    g.w = t + 2 * P.SB * 0.95


@glyph('asterisk', 0x2A)
def asterisk(g):
    P = g.P; s = U(P)
    r = P.cap * 0.215 + s.v * 0.2
    t = s.v * (0.80 - 0.14 * wtc(P))
    cx = P.so * 1.2 + r; cy = P.cap - r * 0.92
    for a in (0, 60, 120):
        with g.rot(a, cx, cy):
            g.rect(cx - t / 2, cy - r, cx + t / 2, cy + r)
    g.w = 2 * cx


@glyph('numbersign', 0x23)
def numbersign(g):
    P = g.P; s = U(P)
    w = fig_w(P) * 1.06
    x0 = fig_sb(P) * 0.9
    t = s.v * (0.86 - 0.12 * wtc(P)); th = s.h * (0.90 - 0.10 * wtc(P))
    lean = P.cap * 0.14
    for f in (0.30, 0.70):
        xb = x0 + w * f - lean / 2
        diag(g, (xb, 0), (xb + lean, P.cap), t, 0, 0)
    for yy in (0.335, 0.665):
        g.rect(x0, P.cap * yy - th / 2, x0 + w, P.cap * yy + th / 2)
    g.w = w + 2 * x0


# ------------------------------------------------------------ operators
def op_w(P): return fig_w(P) * 0.90
def op_x0(P): return (fig_adv(P) - op_w(P)) / 2


@glyph('plus', 0x2B)
def plus(g):
    P = g.P; t = hair(P); w = op_w(P); x0 = op_x0(P); a = axis(P)
    g.rect(x0, a - t / 2, x0 + w, a + t / 2)
    g.rect(x0 + w / 2 - t / 2, a - w / 2, x0 + w / 2 + t / 2, a + w / 2)
    g.w = fig_adv(P)


@glyph('minus', 0x2212)
def minus(g):
    P = g.P; t = hair(P); w = op_w(P); x0 = op_x0(P); a = axis(P)
    g.rect(x0, a - t / 2, x0 + w, a + t / 2)
    g.w = fig_adv(P)


@glyph('equal', 0x3D)
def equal(g):
    P = g.P; t = hair(P); w = op_w(P); x0 = op_x0(P); a = axis(P)
    gp = P.cap * 0.115 + t * 0.5
    g.rect(x0, a + gp - t / 2, x0 + w, a + gp + t / 2); g.rect(x0, a - gp - t / 2, x0 + w, a - gp + t / 2)
    g.w = fig_adv(P)


@glyph('notequal', 0x2260)
def notequal(g):
    P = g.P; s = U(P)
    equal(g)
    cx = fig_adv(P) / 2; a = axis(P)
    diag(g, (cx - P.cap * 0.10, a - P.cap * 0.27), (cx + P.cap * 0.10, a + P.cap * 0.27), hair(P) * 0.92, 0, 0)


@glyph('multiply', 0xD7)
def multiply(g):
    P = g.P; t = hair(P); w = op_w(P) * 0.84; a = axis(P); cx = fig_adv(P) / 2
    for ang in (45, -45):
        with g.rot(ang, cx, a):
            g.rect(cx - w * 0.66, a - t / 2, cx + w * 0.66, a + t / 2)
    g.w = fig_adv(P)


@glyph('divide', 0xF7)
def divide(g):
    P = g.P; t = hair(P); w = op_w(P); x0 = op_x0(P); a = axis(P); d = pd(P) * 0.96
    g.rect(x0, a - t / 2, x0 + w, a + t / 2)
    off = P.cap * 0.135 + t / 2 + d / 2
    g.dot(x0 + w / 2, a + off, d); g.dot(x0 + w / 2, a - off, d)
    g.w = fig_adv(P)


@glyph('plusminus', 0xB1)
def plusminus(g):
    P = g.P; t = hair(P); w = op_w(P); x0 = op_x0(P)
    a = axis(P) + P.cap * 0.10
    g.rect(x0, a - t / 2, x0 + w, a + t / 2)
    g.rect(x0 + w / 2 - t / 2, a - w * 0.42, x0 + w / 2 + t / 2, a + w * 0.42)
    g.rect(x0, 0, x0 + w, t)
    g.w = fig_adv(P)


def _ineq(name, uni, right, eq):
    @glyph(name, uni)
    def iq(g):
        P = g.P; t = hair(P) * 0.98; w = op_w(P); x0 = op_x0(P)
        dy = w * (0.40 if not eq else 0.33)
        a = axis(P) + (P.cap * 0.12 + t * 0.2 if eq else 0)
        if right:
            chevron(g, x0 + w, a, -w, dy, t)
        else:
            chevron(g, x0, a, w, dy, t)
        if eq:
            g.rect(x0, 0, x0 + w, t)
        g.w = fig_adv(P)
    return iq


_ineq('less', 0x3C, False, False); _ineq('greater', 0x3E, True, False)
_ineq('lessequal', 0x2264, False, True); _ineq('greaterequal', 0x2265, True, True)


def wave(g, x0, x1, yc, amp, t):
    w = x1 - x0
    g.stroke([N(x0, yc - amp * 0.55, 58, t * 0.80), N(x0 + w * 0.27, yc + amp, 0, t), N((x0 + x1) / 2, yc, -30, t * 1.02),
              N(x1 - w * 0.27, yc - amp, 0, t), N(x1, yc + amp * 0.55, 58, t * 0.80)], k=0.56)


@glyph('asciitilde', 0x7E)
def asciitilde(g):
    P = g.P
    wave(g, op_x0(P), op_x0(P) + op_w(P), axis(P), P.cap * 0.058 + hair(P) * 0.18, hair(P))
    g.w = fig_adv(P)


@glyph('approxequal', 0x2248)
def approxequal(g):
    P = g.P
    gp = P.cap * 0.115 + hair(P) * 0.5
    for sgn in (1, -1):
        wave(g, op_x0(P), op_x0(P) + op_w(P), axis(P) + sgn * gp, P.cap * 0.050 + hair(P) * 0.12, hair(P) * 0.96)
    g.w = fig_adv(P)


@glyph('asciicircum', 0x5E)
def asciicircum(g):
    P = g.P; s = U(P)
    w = op_w(P) * 0.92; x0 = (fig_adv(P) - w) / 2
    t = hair(P)
    up = Line((x0 + w / 2, P.cap), (x0, P.cap * 0.56)); dn = Line((x0 + w / 2, P.cap), (x0 + w, P.cap * 0.56))
    lo, li = up.offset(-t / 2), up.offset(t / 2)
    ro, ri = dn.offset(t / 2), dn.offset(-t / 2)
    yb = P.cap * 0.56
    g.poly([lo.at_y(yb), li.at_y(yb), li & ri, ri.at_y(yb), ro.at_y(yb), lo & ro])
    g.w = fig_adv(P)


@glyph('logicalnot', 0xAC)
def logicalnot(g):
    P = g.P; t = hair(P); w = op_w(P); x0 = op_x0(P); a = axis(P)
    g.rect(x0, a - t / 2, x0 + w, a + t / 2)
    g.rect(x0 + w - t * 1.02, a - P.cap * 0.25, x0 + w, a + t / 2)
    g.w = fig_adv(P)


@glyph('infinity', 0x221E)
def infinity(g):
    P = g.P; s = S(P, False)
    w = fig_w(P) * (0.74 + 0.10 * clamp(P.wt, 0, 1)); hgt = P.cap * (0.50 + 0.06 * clamp(P.wt, 0, 1))
    x0 = P.so * 1.2; y0 = axis(P) - hgt / 2
    f = 0.92 - 0.30 * clamp(P.wt, 0, 1)
    for i in (0, 1):
        xa = x0 + i * (w - s.o0 * f)
        rn = round_nodes(P, xa, xa + w, y0, y0 + hgt, False, fl=f, fr=f, ft=1.0, fb=1.0)
        g.stroke([rn['r'], rn['t'], rn['l'], rn['b']], closed=True, kL=rn['ki'])
    g.w = x0 * 2 + 2 * w - s.o0 * f


@glyph('radical', 0x221A)
def radical(g):
    P = g.P; s = U(P)
    t = hair(P) * 0.96; td = min(t * 1.22, s.v)
    x0 = fig_sb(P) * 0.8; w = fig_w(P) * 1.05
    yt = P.cap * 0.44; top_ = P.cap + 60
    xv = x0 + w * 0.40
    dn = Line((x0 + w * 0.17, yt), (xv, 0)); up = Line((xv, 0), (x0 + w, top_))
    dn_in, dn_out = dn.offset(td / 2), dn.offset(-td / 2)
    up_in, up_out = up.offset(t / 2), up.offset(-t / 2)
    g.poly([dn_out.at_y(yt), dn_in.at_y(yt), dn_in & up_in, up_in.at_y(top_), up_out.at_y(top_),
            up_out.at_y(0), dn_out.at_y(0)])
    g.rect(x0, yt - t, dn_in.at_y(yt)[0], yt)
    g.w = g.bounds()[2] + fig_sb(P) * 0.5


@glyph('summation', 0x2211)
def summation(g):
    P = g.P; s = U(P)
    t = s.h * 0.94; td = s.d * 0.86
    x0 = P.SO; w = P.Hw * 0.94; x1 = x0 + w
    y1 = P.cap; y0 = P.desc * 0.5
    ym = (y0 + y1) / 2; xm = x0 + w * 0.56
    a = sline((x0, y1 - t), -1, (xm, ym), +1, td); b = sline((x0, y0 + t), -1, (xm, ym), +1, td)
    al, ar = edges(a, td); bl, br = edges(b, td)
    g.poly([(x0, y0), (x1, y0), (x1, y0 + t), br.at_y(y0 + t), br & ar, ar.at_y(y1 - t), (x1, y1 - t), (x1, y1),
            (x0, y1), (x0, y1 - t), al & bl, (x0, y0 + t)])
    g.w = x1 + P.SO


@glyph('product', 0x220F)
def product(g):
    P = g.P; s = U(P)
    x0 = P.SO * 0.8; w = P.Hw * 1.08
    y0 = P.desc * 0.5
    t = s.v * 0.92
    g.rect(x0, P.cap - s.h * 0.94, x0 + w, P.cap)
    g.vstem(x0 + w * 0.10 + t / 2, y0, P.cap, t); g.vstem(x0 + w * 0.90 - t / 2, y0, P.cap, t)
    g.w = w + 2 * x0


@glyph('integral', 0x222B)
def integral(g):
    P = g.P; s = U(P)
    t = s.v * 0.86
    x0 = P.so; w = P.Hw * 0.52
    g.stroke([N(x0 + w, P.asc + 10, 180, s.h * 0.86), N(x0 + w / 2, (P.asc + P.desc) / 2, 264, t),
              N(x0, P.desc * 0.92, 180, s.h * 0.86)], k=0.66)
    g.w = w + 2 * x0


@glyph('partialdiff', 0x2202)
def partialdiff(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P); x1 = x0 + fig_w(P) * 0.96
    ybt = P.cap * 0.60
    rn = ring(g, x0, x1, cbot(P), ybt, upper=True, ft=0.92)
    cxt = (x0 + x1) / 2 - (x1 - x0) * 0.10
    xlv = x0 + (x1 - x0) * 0.14
    yuc = P.cap * 0.74
    ru = dict(cx=cxt, cy=yuc, rx=cxt - xlv - s.o0 * 0.9, ry=ctop(P) - yuc - s.h)
    g.stroke([N(x1 - s.o0 / 2, rn['cy'], 90, s.o), N(cxt, ctop(P) - s.h / 2, 180, s.h),
              N(xlv + s.o0 * 0.45, yuc, 270, s.o * 0.9)], cut1=term(ru, 180 - 34, P))
    g.w = x1 + fig_sb(P)


def outline_poly(g, outer, inner):
    g.add([poly(outer)])
    g.add([reverse_contour(poly(inner))])


@glyph('uni2206', [0x2206])
def increment(g):
    P = g.P; s = U(P)
    w = P.Ow * 0.96; x0 = P.SD * 1.2; x1 = x0 + w; cx = (x0 + x1) / 2
    t = s.d * 0.94; hb = s.h * 0.94
    lo = Line((x0, 0), (cx, P.cap + hb * 0.15)); ro = Line((x1, 0), (cx, P.cap + hb * 0.15))
    li = lo.offset(-t); ri = ro.offset(t)
    apex_o = (cx, P.cap)
    g.add([poly([(x0, 0), (x1, 0), ro.at_y(P.cap), lo.at_y(P.cap)])])
    g.add([reverse_contour(poly([li.at_y(hb), ri.at_y(hb), li & ri]))])
    g.w = w + 2 * x0


@glyph('lozenge', 0x25CA)
def lozenge(g):
    P = g.P; s = U(P)
    w = fig_w(P) * 0.92; x0 = (fig_adv(P) - w) / 2; cx = fig_adv(P) / 2
    y0 = -P.cap * 0.04; y1 = P.cap * 1.04; cy = (y0 + y1) / 2
    t = s.d * 0.80
    k = t / math.sin(math.atan2((y1 - y0) / 2, w / 2))
    g.add([poly([(cx, y0), (x0 + w, cy), (cx, y1), (x0, cy)])])
    kx = k * 1.0; ky = k * ((y1 - y0) / w)
    g.add([reverse_contour(poly([(cx, y0 + ky), (x0 + w - kx, cy), (cx, y1 - ky), (x0 + kx, cy)]))])
    g.w = fig_adv(P)


# ------------------------------------------------------------ percent and small forms
def small_P(P, s=0.60, comp=1.42):
    return P.scaled(s, min(comp, 1.0 / s) * (1.0 - 0.36 * clamp(P.wt, 0, 1) ** 1.2))


def small_zero(g, x, y, Ps):
    sub = G(Ps, g.name)
    ring(sub, 0, fig_w(Ps) * 0.96, -Ps.os, Ps.cap + Ps.os, upper=True)
    with g.shift(x, y):
        g.add(sub.contours)
    return fig_w(Ps) * 0.96


@glyph('percent', 0x25)
def percent(g):
    P = g.P; s = U(P)
    Ps = small_P(P, 0.56, 1.50)
    zw = fig_w(Ps) * 0.96
    x0 = P.SO * 0.9
    gapw = P.Hw * 0.30
    small_zero(g, x0, P.cap - Ps.cap, Ps)
    small_zero(g, x0 + zw + gapw, 0, Ps)
    cx = x0 + zw + gapw / 2
    diag(g, (cx - P.Hw * 0.30, 0), (cx + P.Hw * 0.30, P.cap), s.d * 0.80, 0, 0)
    g.w = x0 * 2 + 2 * zw + gapw


@glyph('perthousand', 0x2030)
def perthousand(g):
    P = g.P; s = U(P)
    Ps = small_P(P, 0.56, 1.50)
    zw = fig_w(Ps) * 0.96
    x0 = P.SO * 0.9
    gapw = P.Hw * 0.30; g2 = P.SO * 0.9
    small_zero(g, x0, P.cap - Ps.cap, Ps)
    small_zero(g, x0 + zw + gapw, 0, Ps)
    small_zero(g, x0 + 2 * zw + gapw + g2, 0, Ps)
    cx = x0 + zw + gapw / 2
    diag(g, (cx - P.Hw * 0.30, 0), (cx + P.Hw * 0.30, P.cap), s.d * 0.80, 0, 0)
    g.w = x0 * 2 + 3 * zw + gapw + g2


@glyph('degree', 0xB0)
def degree(g):
    P = g.P
    d = P.cap * 0.40 + P.V0 * 0.35
    x0 = P.so * 1.3
    f = 0.70 - 0.22 * clamp(P.wt, 0, 1)
    with g.shift(x0, P.cap + P.os - d):
        rn = round_nodes(P, 0, d, 0, d, True, fl=f, fr=f, ft=f / P.cU, fb=f / P.cU)
        g.stroke([rn['r'], rn['t'], rn['l'], rn['b']], closed=True, kL=P.k)
    g.w = d + 2 * x0


def _small_fig(base, i):
    """Denominator figure (drawn), with numerator / superior / inferior as shifted components."""
    @glyph(base + '.dnom')
    def dn(g):
        P = g.P
        Ps = small_P(P)
        sub = g.embed(uc.__dict__[base] if base in uc.__dict__ else None, Ps, 0, 0)
        g.w = sub.w
    for suf, dyf, uni in (('.numr', lambda P: P.cap * 0.40, None), ('.sups', lambda P: P.cap * 0.56, SUPS.get(i)),
                          ('.subs', lambda P: -P.cap * 0.20, SUBS.get(i))):
        def mk(dyf=dyf):
            def fn(g):
                g.comp(base + '.dnom', 0, dyf(g.P))
                g.w = None
            return fn
        glyph(base + suf, uni)(mk())


SUPS = {0: 0x2070, 1: 0xB9, 2: 0xB2, 3: 0xB3, 4: 0x2074, 5: 0x2075, 6: 0x2076, 7: 0x2077, 8: 0x2078, 9: 0x2079}
SUBS = {i: 0x2080 + i for i in range(10)}
FIGS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
for _i, _n in enumerate(FIGS):
    _small_fig(_n, _i)


def _tab(base, wf=1.0):
    @glyph(base + '.tf')
    def tf(g):
        g.tf = (base, wf); g.w = None
    return tf


for _n in FIGS + ['zero.zero']:
    _tab(_n)
for _n in ('period', 'comma', 'colon', 'colon.case'):
    _tab(_n, 0.5)


def _raised(name, base, dyf):
    @glyph(name)
    def r(g):
        g.comp(base, 0, dyf(g.P)); g.w = None
    return r


for _n in ('guilsinglleft', 'guilsinglright', 'guillemotleft', 'guillemotright', 'periodcentered', 'bullet'):
    _raised(_n + '.case', _n, lambda P: (P.cap - P.xh) / 2)
for _n in ('exclamdown', 'questiondown'):
    _raised(_n + '.case', _n, lambda P: P.cap - P.xh)
_raised('at.case', 'at', lambda P: (P.cap * 0.5) - ((P.desc * 0.80 + P.cap + P.os + 8) / 2))


@glyph('uni20AB', [0x20AB])
def dong(g):
    P = g.P; s = S(P, False)
    g.comp('dcroat', 0, P.cap - P.asc)
    g.under = s.h * 0.84
    g.w = None


def _frac(name, uni, num, den):
    @glyph(name, uni)
    def fr(g):
        g.frac = (num, den)      # resolved to components by the glyph-set assembler
        g.w = None
    return fr


_frac('onequarter', 0xBC, 'one', 'four'); _frac('onehalf', 0xBD, 'one', 'two'); _frac('threequarters', 0xBE, 'three', 'four')
_frac('onethird', 0x2153, 'one', 'three'); _frac('twothirds', 0x2154, 'two', 'three')
_frac('oneeighth', 0x215B, 'one', 'eight'); _frac('threeeighths', 0x215C, 'three', 'eight')
_frac('fiveeighths', 0x215D, 'five', 'eight'); _frac('seveneighths', 0x215E, 'seven', 'eight')


@glyph('ordfeminine', 0xAA)
def ordfeminine(g):
    P = g.P; Ps = small_P(P, 0.62, 1.36)
    sub = g.embed(lc.a, Ps, 0, P.cap - Ps.xh)
    g.w = sub.w


@glyph('ordmasculine', 0xBA)
def ordmasculine(g):
    P = g.P; Ps = small_P(P, 0.62, 1.36)
    sub = g.embed(lc.o, Ps, 0, P.cap - Ps.xh)
    g.w = sub.w


# ------------------------------------------------------------ at, ampersand
@glyph('at', 0x40)
def at(g):
    P = g.P; s = S(P, False)
    f = 0.80 - 0.24 * clamp(P.wt, 0, 1)
    to = s.o * f; to0 = s.o0 * f; th = s.h * f
    W = P.Ow * 1.18 + s.o0 * 0.6
    x0 = P.SO; x1 = x0 + W
    y0 = P.desc * 0.80; y1 = P.cap + P.os + 8
    cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    # inner a
    aw = W * 0.40 + to0 * 0.5; ah = (y1 - y0) * 0.44 + th
    ax0 = cx - aw * 0.56; ay0 = cy - ah * 0.50
    xs = ax0 + aw
    rna = round_nodes(P, ax0, xs + to0 * 0.2, ay0, ay0 + ah, False, fl=f, fr=f * 0.8, ft=f, fb=f)
    g.stroke([rna['r'], rna['t'], rna['l'], rna['b']], closed=True, kL=rna['ki'])
    # stem, tail and the outer round as one stroke
    rxo = (x1 - x0) / 2; ryo = (y1 - y0) / 2
    xre = x1 - to0 / 2
    ytail = ay0 + th * 0.5
    rn = dict(cx=cx, cy=cy, rx=rxo - to0 / 2, ry=ryo - th / 2, rxi=rxo - to0, ryi=ryo - th)
    xt = xs + (xre - xs) * 0.52
    g.stroke([N(xs, ay0 + ah - th * 0.2, -90, to, line=True), N(xs, ytail + (xt - xs) * 0.9, -90, to),
              N(xt, ytail, 0, th), N(xre, cy, 90, to), N(cx, y1 - th / 2, 180, th), N(x0 + to0 / 2, cy, 270, to),
              N(cx, y0 + th / 2, 0, th), N(xre, cy, 90, to)], cut1=term(rn, -52, P), k=P.k)
    g.w = x1 + P.SO


@glyph('ampersand', 0x26)
def ampersand(g):
    P = g.P; s = U(P)
    w = P.Hw * 1.06
    x0 = P.SO * 1.05
    wt = wtc(P)
    tv = s.o * (0.98 - 0.16 * wt); th = s.h * (0.98 - 0.16 * wt); td = s.d * (0.98 - 0.12 * wt)
    cap = P.cap
    def X(f): return x0 + w * f
    xl = X(0.0) + s.o0 / 2
    g.stroke([N(X(0.905), cap * 0.455, 258, td * 0.92),
              N(X(0.415), cbot(P) + th / 2, 180, th),
              N(xl, cap * 0.245, 90, tv),
              N(X(0.66 + 0.09 * wt) - s.o0 / 2, cap * (0.775 - 0.03 * wt), 90, tv * (0.94 - 0.10 * wt), k=0.50),
              N(X(0.44), ctop(P) - th * 0.45, 180, th * 0.90),
              N(X(0.19 - 0.07 * wt) + s.o0 / 2, cap * (0.775 - 0.03 * wt), 270, tv * (0.94 - 0.10 * wt)),
              N(X(1.0) - td * 0.30, -cap * 0.05 - td * 0.55, -49, td)],
             cut1=('y', 0.0), k=P.k)
    g.w = X(1.0) + P.SD * 1.2
    g.anchor('top', X(0.44), cap)


# ------------------------------------------------------------ currency
def bars(g, x0, x1, ys, t):
    for y in ys:
        g.rect(x0, y - t / 2, x1, y + t / 2)


@glyph('dollar', 0x24)
def dollar(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.02; w = fig_w(P) * 0.96
    lc.s_shape(g, x0, w, cbot(P), ctop(P), s, P.cap, upper=True)
    t = s.v * (0.78 - 0.16 * wtc(P))
    cx = x0 + w / 2
    ext = P.cap * 0.115
    g.rect(cx - t / 2, P.cap - s.h * 0.5, cx + t / 2, P.cap + ext)
    g.rect(cx - t / 2, -ext, cx + t / 2, s.h * 0.5)
    g.anchors.clear()
    g.w = fig_adv(P)


@glyph('cent', 0xA2)
def cent(g):
    P = g.P; s = S(P, False)
    probe = G(P); lc.c(probe)
    dx = (fig_adv(P) - probe.w) / 2
    with g.shift(dx, 0):
        lc.c(g)
    cx = dx + P.so + P.ow * 0.985 / 2
    t = s.v * (0.78 - 0.16 * clamp(P.wt, 0, 1))
    ext = P.cap * 0.115
    g.rect(cx - t / 2, P.xh - s.h * 0.5, cx + t / 2, P.xh + ext)
    g.rect(cx - t / 2, -ext, cx + t / 2, s.h * 0.5)
    g.anchors.clear()
    g.w = fig_adv(P)


@glyph('sterling', 0xA3)
def sterling(g):
    """Pound: stem with an f-like hook, foot and crossbar (the hook is a tested primitive in every weight)."""
    P = g.P; s = U(P)
    x0 = fig_sb(P); w = fig_w(P); x1 = x0 + w
    xs = x0 + w * 0.31
    x_end = x1 - w * 0.03
    reach = x_end - (xs + s.v0 / 2)
    y_turn = ctop(P) - min(reach * 0.95, P.cap * 0.30) - s.h / 2
    hook(g, xs, s.h * 0.5, y_turn, x_end, ctop(P), upper=True)
    g.rect(x0, 0, x1, s.h)
    hb = s.h * 0.92
    g.rect(x0 + w * 0.02, P.cap * 0.40 - hb / 2, x0 + w * 0.74, P.cap * 0.40 + hb / 2)
    g.w = fig_adv(P)


@glyph('yen', 0xA5)
def yen(g):
    P = g.P; s = U(P)
    w = fig_w(P) * 1.10; x0 = (fig_adv(P) - w) / 2; x1 = x0 + w; cx = (x0 + x1) / 2
    yj = P.cap * 0.44
    t = s.d * 0.96; t0 = s.d0 * 0.96
    cl = sline((x0, P.cap), -1, (cx, yj), 0, t0); cr = sline((x1, P.cap), +1, (cx, yj), 0, t0)
    ll, lr_ = edges(cl, t); rl, rr = edges(cr, t)
    g.poly([ll.at_y(P.cap), lr_.at_y(P.cap), lr_ & rl, rl.at_y(P.cap), rr.at_y(P.cap), rr.at_x(cx + s.v / 2),
            (cx + s.v / 2, 0), (cx - s.v / 2, 0), ll.at_x(cx - s.v / 2)])
    hb = s.h * (0.88 - 0.14 * wtc(P))
    bars(g, x0 + w * 0.12, x1 - w * 0.12, (P.cap * 0.40, P.cap * 0.40 - hb - max(P.cap * 0.07, hb * 0.5)), hb)
    g.w = fig_adv(P)


@glyph('Euro', 0x20AC)
def euro(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.10; x1 = fig_sb(P) + fig_w(P) * 1.10
    rn = round_nodes(P, x0, x1, cbot(P), ctop(P), upper=True)
    th = 46.0 + 12.0 * (P.ap - 1.0)
    g.stroke([rn['r'], rn['t'], rn['l'], rn['b'], rn['r']], cut0=term(rn, th, P), cut1=term(rn, -th, P), kL=rn['ki'])
    hb = s.h * (0.86 - 0.14 * wtc(P))
    gp = max(P.cap * 0.075, hb * 0.55)
    xb0 = fig_sb(P) - fig_w(P) * 0.06
    bars(g, xb0, rn['cx'] + (x1 - x0) * 0.10, (axis(P) + gp / 2 + hb / 2, axis(P) - gp / 2 - hb / 2), hb)
    g.w = fig_adv(P)


@glyph('uni20B9', [0x20B9])
def rupee(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P); w = fig_w(P) * 0.98; x1 = x0 + w
    hb = s.h * (0.94 - 0.10 * wtc(P))
    y2 = P.cap * 0.50
    g.rect(x0, P.cap - hb, x1, P.cap)
    xc = x0 + w * 0.30
    yb1 = P.cap - hb / 2
    g.stroke([N(x0, yb1, 0, hb, line=True), N(xc, yb1, 0, hb), N(x1 - w * 0.12 - s.o0 / 2, (yb1 + y2) / 2, -90, s.o * 0.96),
              N(xc, y2, 180, hb, line=True), N(x0, y2, 180, hb)], kR=P.ki(w * 0.5, (yb1 - y2) / 2 - hb / 2))
    ymid = (yb1 + y2) / 2
    g.rect(x0, ymid - hb / 2, x1, ymid + hb / 2)
    t = s.d * 0.96
    diag(g, (x0 + w * 0.06, y2), (x1 - w * 0.08, 0), t, -1, +1, t0=s.d0 * 0.96)
    g.w = fig_adv(P)


def letter_with_bars(name, uni, fn, ys, x_ext=(0.0, 0.0), on_fig=True, tf=0.84):
    @glyph(name, uni)
    def lb(g):
        P = g.P; s = U(P)
        probe = G(P); fn(probe)
        b = probe.bounds()
        dx = (fig_adv(P) - probe.w) / 2 if on_fig else 0
        with g.shift(dx, 0):
            fn(g)
        hb = s.h * (tf - 0.14 * wtc(P))
        bw = b[2] - b[0]
        bars(g, dx + b[0] + bw * x_ext[0], dx + b[2] + bw * x_ext[1], [P.cap * y for y in ys], hb)
        g.anchors.clear()
        g.w = fig_adv(P) if on_fig else probe.w
    return lb


letter_with_bars('uni20A9', [0x20A9], uc.W, (0.40,), (-0.03, 0.03), on_fig=False)        # won
letter_with_bars('uni20A6', [0x20A6], uc.N_, (0.57, 0.36), (-0.10, 0.10), on_fig=False)   # naira
letter_with_bars('uni20B1', [0x20B1], uc.P_, (0.80, 0.62), (-0.12, 0.10), on_fig=False)   # peso


@glyph('uni20BD', [0x20BD])
def ruble(g):
    P = g.P; s = U(P)
    probe = G(P); uc.P_(probe)
    off = P.Hw * 0.10
    with g.shift(off, 0):
        uc.P_(g)
    hb = s.h * (0.86 - 0.12 * wtc(P))
    xs = off + P.SB
    g.rect(xs - P.Hw * 0.16, P.cap * 0.20 - hb / 2, xs + P.Hw * 0.52, P.cap * 0.20 + hb / 2)
    g.anchors.clear()
    g.w = probe.w + off


@glyph('uni20B8', [0x20B8])
def tenge(g):
    P = g.P; s = U(P)
    w = fig_w(P) * 1.06; x0 = (fig_adv(P) - w) / 2
    hb = s.h * (0.90 - 0.10 * wtc(P))
    g.rect(x0, P.cap - hb, x0 + w, P.cap)
    y2 = P.cap - hb - max(P.cap * 0.075, hb * 0.5)
    g.rect(x0, y2 - hb, x0 + w, y2)
    g.vstem(x0 + w / 2, 0, y2, s.v)
    g.w = fig_adv(P)


@glyph('uni20BF', [0x20BF])
def bitcoin(g):
    P = g.P; s = U(P)
    uc.B(g)
    t = s.v * (0.64 - 0.12 * wtc(P))
    ext = P.cap * 0.115
    xa = P.SB + P.Hw * 0.30
    for xx in (xa, xa + t * 2.3):
        g.rect(xx - t / 2, P.cap - s.h * 0.5, xx + t / 2, P.cap + ext)
        g.rect(xx - t / 2, -ext, xx + t / 2, s.h * 0.5)
    g.anchors.clear()


@glyph('uni20BA', [0x20BA])
def lira(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.02; w = fig_w(P) * 0.98; x1 = x0 + w
    xs = x0 + w * 0.24
    ry = P.cap * 0.44
    yt = cbot(P) + ry
    cx = (xs + x1) / 2
    rn = dict(cx=cx, cy=yt, rx=x1 - cx - s.o0 * 0.96, ry=ry - s.h)
    g.stroke([N(xs, P.cap, -90, s.v, line=True), N(xs, yt, -90, s.v), N(cx, cbot(P) + s.h / 2, 0, s.h),
              N(x1 - s.o0 * 0.48, yt, 90, s.o * 0.96)], kL=P.ki(rn['rx'], rn['ry']))
    hb = s.h * (0.86 - 0.14 * wtc(P))
    for yy in (0.66, 0.66 - 0.19):
        yc = P.cap * yy
        rise = P.cap * 0.13
        g.poly([(x0 - w * 0.02, yc - rise / 2 - hb / 2), (x0 + w * 0.62, yc + rise / 2 - hb / 2),
                (x0 + w * 0.62, yc + rise / 2 + hb / 2), (x0 - w * 0.02, yc - rise / 2 + hb / 2)])
    g.w = fig_adv(P)


@glyph('uni20B4', [0x20B4])
def hryvnia(g):
    P = g.P; s = U(P)
    x0 = fig_sb(P) + fig_w(P) * 0.02; w = fig_w(P) * 0.96
    with g.flip_x(x0 + w / 2):
        lc.s_shape(g, x0, w, cbot(P), ctop(P), s, P.cap, upper=True)
    hb = s.h * (0.80 - 0.16 * wtc(P))
    gp = max(P.cap * 0.07, hb * 0.5)
    bars(g, x0 - w * 0.06, x0 + w * 1.06, (axis(P) + gp / 2 + hb / 2, axis(P) - gp / 2 - hb / 2), hb)
    g.anchors.clear()
    g.w = fig_adv(P)


@glyph('uni20AA', [0x20AA])
def sheqel(g):
    P = g.P; s = U(P)
    t = s.v * 0.92; th = s.h * 0.94
    x0 = P.SB * 0.9; w = P.Hw * 1.22
    step = w * 0.31
    xa = x0 + t / 2
    r = step * 0.9
    # left form: stem, arch over the top, down to the middle
    g.stroke([N(xa, 0, 90, t, line=True), N(xa, P.cap - r, 90, t), N(xa + r, P.cap - th / 2, 0, th, line=True),
              N(xa + 2 * step - r, P.cap - th / 2, 0, th), N(xa + 2 * step, P.cap - r, -90, t, line=True),
              N(xa + 2 * step, P.cap * 0.26, -90, t)], k=0.62)
    xb = xa + step
    g.stroke([N(xb, P.cap * 0.74, -90, t, line=True), N(xb, r, -90, t), N(xb + r, th / 2, 0, th, line=True),
              N(xb + 2 * step - r, th / 2, 0, th), N(xb + 2 * step, r, 90, t, line=True), N(xb + 2 * step, P.cap, 90, t)], k=0.62)
    g.w = xb + 2 * step + t / 2 + x0


@glyph('uni20BC', [0x20BC])
def manat(g):
    P = g.P; s = U(P)
    w = fig_w(P) * 1.10; x0 = (fig_adv(P) - w) / 2; x1 = x0 + w
    top = P.cap * 0.80 + P.os
    ry = top * 0.72
    cx = (x0 + x1) / 2
    g.stroke([N(x0 + s.v0 / 2, 0, 90, s.v, line=True), N(x0 + s.v0 / 2, top - ry, 90, s.v), N(cx, top - s.h / 2, 0, s.h),
              N(x1 - s.v0 / 2, top - ry, -90, s.v, line=True), N(x1 - s.v0 / 2, 0, -90, s.v)],
             kR=P.ki(w / 2 - s.v0, ry - s.h))
    g.vstem(cx, 0, P.cap, s.v * 0.9)
    g.w = fig_adv(P)


@glyph('florin', 0x192)
def florin(g):
    P = g.P; s = S(P, False)
    left = (P.nw - s.v0) * 0.30; reach = (P.nw - s.v0) * 0.44
    xs = P.so * 0.9 + left + s.v0 / 2 + reach * 0.3
    with g.skew(9, 0):
        hook(g, xs, P.xh * 0.3, P.asc - (P.nw - s.v0) * 0.40 - s.h / 2, xs + s.v0 / 2 + reach, P.asc + P.os * 0.4)
        hook(g, xs, P.xh * 0.4, P.desc + (P.nw - s.v0) * 0.40 + s.h / 2, xs - s.v0 / 2 - reach, P.desc)
        g.rect(xs - s.v0 / 2 - left, P.xh - s.h, xs + s.v0 / 2 + reach * 0.86, P.xh)
    g.w = g.bounds()[2] + P.so * 0.1


@glyph('currency', 0xA4)
def currency(g):
    P = g.P; s = U(P)
    d = fig_w(P) * 0.72; cx = fig_adv(P) / 2; cy = axis(P)
    f = 0.82
    rn = round_nodes(P, cx - d / 2, cx + d / 2, cy - d / 2, cy + d / 2, True, fl=f, fr=f, ft=f, fb=f)
    g.stroke([rn['r'], rn['t'], rn['l'], rn['b']], closed=True, kL=rn['ki'])
    t = s.h * 0.82
    for a in (45, 135, 225, 315):
        with g.rot(a, cx, cy):
            g.rect(cx + d * 0.42, cy - t / 2, cx + d * 0.72, cy + t / 2)
    g.w = fig_adv(P)


# ------------------------------------------------------------ publishing marks
def circled(name, uni, fn, scale=0.50):
    @glyph(name, uni)
    def c_(g):
        P = g.P; s = U(P)
        f = 0.60 - 0.10 * wtc(P)
        d = P.cap + 2 * P.os + 26
        x0 = P.SO; cy = P.cap / 2
        rn = round_nodes(P, x0, x0 + d, cy - d / 2, cy + d / 2, True, fl=f, fr=f, ft=f, fb=f)
        g.stroke([rn['r'], rn['t'], rn['l'], rn['b']], closed=True, kL=P.k)
        Ps = P.scaled(scale, min(1.0 / scale, 1.42) * (0.92 - 0.14 * wtc(P)))
        probe = G(Ps); fn(probe)
        b = probe.bounds()
        g.embed(fn, Ps, x0 + d / 2 - (b[0] + b[2]) / 2, cy - Ps.cap / 2)
        g.anchors.clear()
        g.w = d + 2 * x0
    return c_


circled('copyright', 0xA9, uc.C)
circled('registered', 0xAE, uc.R)
circled('uni2117', [0x2117], uc.P_)


@glyph('trademark', 0x2122)
def trademark(g):
    P = g.P
    Ps = small_P(P, 0.46, 1.6)
    y = P.cap - Ps.cap
    a = g.embed(uc.T, Ps, P.so * 0.6, y)
    b = g.embed(uc.M, Ps, P.so * 0.6 + a.w * 0.96, y)
    g.anchors.clear()
    g.w = P.so * 1.2 + a.w * 0.96 + b.w


@glyph('section', 0xA7)
def section(g):
    """Two S forms sharing one central ring."""
    P = g.P; s = U(P)
    x0 = fig_sb(P) * 0.9; w = fig_w(P) * 0.84
    wt = wtc(P)
    Ps = P.scaled(1.0, 0.94 - 0.10 * wt)
    ss = S(Ps, True)
    ht = ss.h * (0.98 - 0.10 * wt); sp = ss.o * (1.02 - 0.12 * wt)
    ytop = P.asc + P.os * 0.5; ybot = P.desc * 0.62 - P.os * 0.5
    hh = ((ytop - ybot) + ht - 0.56 * sp) / 1.5
    delta = (hh - 2 * ht + 1.12 * sp) / 2
    sub = G(Ps, g.name)
    lc.s_shape(sub, x0, w, ytop - hh, ytop, ss, P.cap, upper=True, sym=True)
    g.add(sub.contours)
    with g.shift(0, -delta):
        g.add(sub.contours)
    g.w = w + 2 * x0


@glyph('paragraph', 0xB6)
def paragraph(g):
    P = g.P; s = U(P)
    t = s.v * 0.84
    x0 = P.SO * 0.9; w = P.Hw * 0.92
    xs1 = x0 + w * 0.58; xs2 = x0 + w - t / 2
    yb = P.cap * 0.42; y1 = P.cap; y0 = P.desc * 0.60
    cy = (yb + y1) / 2; ry = (y1 - yb) / 2; k = P.k
    rx = xs1 - x0
    g.add([[('l', (xs1, y1)), ('c', (xs1 - rx * k, y1), (x0, cy + ry * k), (x0, cy)),
            ('c', (x0, cy - ry * k), (xs1 - rx * k, yb), (xs1, yb))]])
    g.vstem(xs1, y0, y1, t); g.vstem(xs2, y0, y1, t)
    g.rect(xs1, y1 - s.h * 0.9, xs2, y1)
    g.w = x0 + w + P.SB * 0.8


def _dagger(name, uni, dbl):
    @glyph(name, uni)
    def dg(g):
        P = g.P; s = U(P)
        t = s.v * 0.90; th = s.h * 0.92
        w = fig_w(P) * 0.78; x0 = P.so * 1.5; cx = x0 + w / 2
        y0 = P.desc * 0.70
        g.vstem(cx, y0, P.asc, t)
        g.rect(x0, P.xh * 0.94 - th / 2, x0 + w, P.xh * 0.94 + th / 2)
        if dbl:
            yy = y0 + (P.asc - P.xh * 0.94)
            g.rect(x0, yy - th / 2, x0 + w, yy + th / 2)
        g.w = w + 2 * x0
    return dg


_dagger('dagger', 0x2020, False); _dagger('daggerdbl', 0x2021, True)


@glyph('uni2116', [0x2116])
def numero(g):
    P = g.P; s = U(P)
    uc.N_(g)
    base = G(P); uc.N_(base)
    Ps = small_P(P, 0.60, 1.40)
    o_ = g.embed(lc.o, Ps, base.w - P.SB * 0.45, P.cap - Ps.xh - Ps.os)
    hb = s.h * 0.80
    xo = base.w - P.SB * 0.45
    g.rect(xo + Ps.so, P.cap * 0.26 - hb / 2, xo + o_.w - Ps.so, P.cap * 0.26 + hb / 2)
    g.anchors.clear()
    g.w = xo + o_.w + P.so * 0.3


# ------------------------------------------------------------ arrows and UI symbols
def arr_t(P): return hair(P) * 0.98
def arr_len(P): return 760.0 * (0.72 + 0.28 * P.wf)
def arr_sb(P): return 60.0


def arrow_right(g, x0, x1, cy, P, head=True, tail_head=False):
    t = arr_t(P)
    hd = P.cap * 0.27 + t * 0.6
    g.rect(x0 + (t * 0.5 if tail_head else 0), cy - t / 2, x1 - t * 0.5, cy + t / 2)
    if head:
        chevron(g, x1, cy, -hd, hd, t)
    if tail_head:
        chevron(g, x0, cy, hd, hd, t)


def _arrow(name, uni, ang, double=False):
    @glyph(name, uni)
    def ar(g):
        P = g.P
        L = arr_len(P); sbq = arr_sb(P)
        diagl = ang % 90 != 0
        vert = ang % 180 == 90
        a = axis(P)
        if vert:
            Lv = P.cap + 130
            w = 2 * (P.cap * 0.27 + arr_t(P) * 1.6) + 2 * sbq
            cx = w / 2; cy = (P.cap) / 2
            with g.rot(ang, cx, cy):
                arrow_right(g, cx - Lv / 2, cx + Lv / 2, cy, P, tail_head=double)
            g.w = w
        else:
            Ld = L * (0.94 if diagl else 1.0)
            w = (Ld * 0.74 if diagl else L) + 2 * sbq
            cx = w / 2
            with g.rot(ang, cx, a):
                arrow_right(g, cx - Ld / 2, cx + Ld / 2, a, P, tail_head=double)
            g.w = w
    return ar


_arrow('arrowright', 0x2192, 0); _arrow('arrowleft', 0x2190, 180)
_arrow('arrowup', 0x2191, 90); _arrow('arrowdown', 0x2193, 270)
_arrow('arrowboth', 0x2194, 0, True); _arrow('arrowupdn', 0x2195, 90, True)
_arrow('uni2197', [0x2197], 45); _arrow('uni2196', [0x2196], 135)
_arrow('uni2199', [0x2199], 225); _arrow('uni2198', [0x2198], 315)


def _tabarrow(name, uni, right):
    @glyph(name, uni)
    def ta(g):
        P = g.P
        L = arr_len(P); sbq = arr_sb(P); a = axis(P); t = arr_t(P)
        w = L + 2 * sbq
        hd = P.cap * 0.27 + t * 0.6
        if not right:
            g.flip_x(w / 2)
        arrow_right(g, sbq, sbq + L - t * 1.6, a, P)
        g.rect(sbq + L - t, a - hd, sbq + L, a + hd)
        if not right:
            g.pop()
        g.w = w
    return ta


_tabarrow('uni21E5', [0x21E5], True); _tabarrow('uni21E4', [0x21E4], False)


@glyph('uni21B5', [0x21B5])
def return_arrow(g):
    """Return / Enter."""
    P = g.P
    L = arr_len(P); sbq = arr_sb(P); a = P.cap * 0.30; t = arr_t(P)
    w = L + 2 * sbq
    with g.rot(180, w / 2, a):
        arrow_right(g, sbq, sbq + L, a, P)
    g.rect(sbq + L - t, a - t / 2, sbq + L, P.cap * 0.86)
    g.w = w


def _hookarrow(name, uni, right):
    @glyph(name, uni)
    def ha(g):
        P = g.P
        L = arr_len(P); sbq = arr_sb(P); t = arr_t(P)
        w = L + 2 * sbq
        yb = P.cap * 0.26; r = P.cap * 0.215 + t * 0.45
        if right:
            g.flip_x(w / 2)
        with g.rot(180, w / 2, yb):
            arrow_right(g, sbq + r * 0.6, sbq + L, yb, P)
        xr = sbq + L - r - t / 2
        g.stroke([N(xr - r * 0.2, yb, 0, t, line=True), N(xr, yb, 0, t), N(xr + r, yb + r, 90, t), N(xr, yb + 2 * r, 180, t, line=True),
                  N(xr - r * 0.75, yb + 2 * r, 180, t)], k=0.56)
        if right:
            g.pop()
        g.w = w
    return ha


_hookarrow('uni21A9', [0x21A9], False); _hookarrow('uni21AA', [0x21AA], True)


@glyph('uni21E7', [0x21E7])
def shift_arrow(g):
    P = g.P
    t = arr_t(P) * 0.92
    w = P.cap * 0.92; x0 = arr_sb(P); cx = x0 + w / 2
    y0 = -P.cap * 0.02; y1 = P.cap * 1.02
    ym = y1 - w * 0.52
    sw = w * 0.25
    outer = [(cx, y1), (x0 + w, ym), (cx + sw, ym), (cx + sw, y0), (cx - sw, y0), (cx - sw, ym), (x0, ym)]
    dx = t * 2.41
    inner = [(cx, y1 - t * 1.41), (x0 + w - dx, ym + t), (cx + sw - t, ym + t), (cx + sw - t, y0 + t),
             (cx - sw + t, y0 + t), (cx - sw + t, ym + t), (x0 + dx, ym + t)]
    outline_poly(g, outer, inner)
    g.w = w + 2 * x0


@glyph('uni232B', [0x232B])
def erase_left(g):
    P = g.P
    t = arr_t(P) * 0.92
    h = P.cap * 0.72; w = h * 1.62
    x0 = arr_sb(P); a = axis(P)
    y0 = a - h / 2; y1 = a + h / 2
    nose = h * 0.46
    outer = [(x0, a), (x0 + nose, y1), (x0 + w, y1), (x0 + w, y0), (x0 + nose, y0)]
    ix = t * 1.36
    inner = [(x0 + ix, a), (x0 + nose + t * 0.42, y1 - t), (x0 + w - t, y1 - t), (x0 + w - t, y0 + t), (x0 + nose + t * 0.42, y0 + t)]
    outline_poly(g, outer, inner)
    cx = x0 + nose + (w - nose) * 0.46
    r = h * (0.19 - 0.07 * wtc(P))
    tx = t * (0.46 - 0.16 * wtc(P))
    for ang in (45, -45):
        with g.rot(ang, cx, a):
            g.rect(cx - r * 1.41, a - tx, cx + r * 1.41, a + tx)
    g.w = w + 2 * x0


@glyph('uni2423', [0x2423])
def open_box(g):
    P = g.P
    t = arr_t(P)
    w = 520.0 * P.wf ** 0.6; x0 = arr_sb(P)
    g.rect(x0, -P.cap * 0.10, x0 + w, -P.cap * 0.10 + t)
    g.rect(x0, -P.cap * 0.10, x0 + t, P.cap * 0.13); g.rect(x0 + w - t, -P.cap * 0.10, x0 + w, P.cap * 0.13)
    g.w = w + 2 * x0


def _tri(name, uni, ang, scale):
    @glyph(name, uni)
    def tr(g):
        P = g.P
        s_ = P.cap * 0.80 * scale
        x0 = arr_sb(P) * (0.9 if scale > 0.8 else 0.7)
        cx = x0 + s_ / 2; cy = axis(P)
        hgt = s_ * 0.88
        with g.rot(ang, cx, cy):
            g.poly([(cx - s_ / 2, cy - hgt / 2), (cx + s_ / 2, cy - hgt / 2), (cx, cy + hgt / 2)])
        g.w = s_ + 2 * x0
    return tr


_tri('uni25B2', [0x25B2], 0, 1.0); _tri('uni25BC', [0x25BC], 180, 1.0)
_tri('uni25B6', [0x25B6], -90, 1.0); _tri('uni25C0', [0x25C0], 90, 1.0)
_tri('uni25B4', [0x25B4], 0, 0.56); _tri('uni25BE', [0x25BE], 180, 0.56)
_tri('uni25B8', [0x25B8], -90, 0.56); _tri('uni25C2', [0x25C2], 90, 0.56)


def _shape(name, uni, kind, filled):
    @glyph(name, uni)
    def sh(g):
        P = g.P
        d = P.cap * 0.80; x0 = arr_sb(P); cx = x0 + d / 2; cy = axis(P)
        t = arr_t(P) * 0.92
        if kind == 'circle':
            g.add([superellipse(cx, cy, d / 2, d / 2, 0.5523)])
            if not filled:
                g.add([superellipse(cx, cy, d / 2 - t, d / 2 - t, 0.5523, cw=True)])
        elif kind == 'square':
            q = d * 0.90
            g.add([poly([(cx - q / 2, cy - q / 2), (cx + q / 2, cy - q / 2), (cx + q / 2, cy + q / 2), (cx - q / 2, cy + q / 2)])])
            if not filled:
                q2 = q - 2 * t
                g.add([reverse_contour(poly([(cx - q2 / 2, cy - q2 / 2), (cx + q2 / 2, cy - q2 / 2), (cx + q2 / 2, cy + q2 / 2), (cx - q2 / 2, cy + q2 / 2)]))])
        elif kind == 'diamond':
            q = d * 0.56
            g.add([poly([(cx, cy - q), (cx + q, cy), (cx, cy + q), (cx - q, cy)])])
        g.w = d + 2 * x0
    return sh


_shape('uni25CF', [0x25CF], 'circle', True); _shape('uni25CB', [0x25CB], 'circle', False)
_shape('uni25A0', [0x25A0], 'square', True); _shape('uni25A1', [0x25A1], 'square', False)
_shape('uni25C6', [0x25C6], 'diamond', True)


def star_pts(cx, cy, R, r):
    pts = []
    for i in range(10):
        a = math.radians(90 + i * 36)
        rr = R if i % 2 == 0 else r
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


@glyph('uni2605', [0x2605])
def star(g):
    P = g.P
    R = P.cap * 0.50; x0 = arr_sb(P) * 0.8; cx = x0 + R * 0.951; cy = axis(P) - R * 0.05
    g.add([poly(star_pts(cx, cy, R, R * 0.40))])
    g.w = 2 * cx


@glyph('uni2606', [0x2606])
def star_open(g):
    P = g.P
    R = P.cap * 0.50; x0 = arr_sb(P) * 0.8; cx = x0 + R * 0.951; cy = axis(P) - R * 0.05
    t = arr_t(P) * 0.90
    g.add([poly(star_pts(cx, cy, R, R * 0.40))])
    g.add([reverse_contour(poly(star_pts(cx, cy, R - t * 2.2, R * 0.40 - t * 0.9)))])
    g.w = 2 * cx


@glyph('uni2713', [0x2713])
def check(g):
    P = g.P; s = U(P)
    t = s.d * 0.96
    x0 = arr_sb(P); w = P.cap * 0.94
    xa = x0 + w * 0.36
    dn = Line((x0 + t * 0.2, P.cap * 0.36), (xa, 0)); up = Line((xa, 0), (x0 + w, P.cap * 0.94))
    dl, dr = dn.offset(t / 2), dn.offset(-t / 2)
    ul, ur = up.offset(t / 2), up.offset(-t / 2)
    y_s = P.cap * 0.36
    p_top_l = dn.offset(-t / 2).at_y(y_s); p_top_r = dn.offset(t / 2).at_y(y_s + t * 0.9)
    g.poly([p_top_l, dn.offset(-t / 2) & up.offset(-t / 2), up.offset(-t / 2).at_y(P.cap * 0.94 - t * 0.3),
            up.offset(t / 2).at_y(P.cap * 0.94 + t * 0.3), dn.offset(t / 2) & up.offset(t / 2), p_top_r])
    g.w = w + 2 * x0 + t * 0.3


@glyph('uni2715', [0x2715])
def cross_mark(g):
    P = g.P; s = U(P)
    t = s.d * 0.96
    d = P.cap * 0.76; x0 = arr_sb(P); cx = x0 + d / 2; cy = axis(P)
    for ang in (45, -45):
        with g.rot(ang, cx, cy):
            g.rect(cx - d * 0.66, cy - t / 2, cx + d * 0.66, cy + t / 2)
    g.w = d + 2 * x0


@glyph('.notdef')
def notdef(g):
    P = g.P
    w = 520.0; t = 44.0
    g.add([poly([(60, 0), (60 + w - 120, 0), (60 + w - 120, P.cap), (60, P.cap)])])
    g.add([reverse_contour(poly([(60 + t, t), (60 + w - 120 - t, t), (60 + w - 120 - t, P.cap - t), (60 + t, P.cap - t)]))])
    g.w = w
