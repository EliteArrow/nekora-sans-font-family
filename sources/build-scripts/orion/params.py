"""Orion design space and parametric design rules.

All measurable rules of the family live here (units: 1000 per em).
A Params object is evaluated at a design-space location; glyph functions read
only from it, so every master is drawn from the same rules.
"""
from __future__ import annotations

UPM = 1000
FAMILY = 'Orion'

AXES = [  # tag, name, min, default, max
    ('wght', 'Weight', 100, 400, 900),
    ('wdth', 'Width', 75, 100, 125),
    ('opsz', 'Optical Size', 10, 14, 72),
    ('GRAD', 'Grade', -50, 0, 100),
]
DEFAULT = dict(wght=400, wdth=100, opsz=14, GRAD=0)

W_ANCH = (100, 400, 900)
O_ANCH = (10, 14, 72)
D_ANCH = (75, 100, 125)


def _i1(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    for i in range(1, len(xs)):
        if x <= xs[i]:
            t = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            return ys[i - 1] + (ys[i] - ys[i - 1]) * t
    return ys[-1]


# name -> {opsz: (wght100, wght400, wght900)}   (wdth = 100, GRAD = 0)
T = {
    # --- stems
    'V':   {10: (36, 92, 186), 14: (27, 88, 196), 72: (19, 85, 206)},      # capital vertical stem
    'vr':  {10: (.95, .955, .965), 14: (.95, .955, .965), 72: (.95, .95, .96)},  # lowercase / capital stem
    'cU':  {10: (.97, .92, .82), 14: (.96, .89, .78), 72: (.95, .86, .74)},  # capital horizontal / vertical
    'cL':  {10: (.97, .91, .79), 14: (.96, .88, .75), 72: (.95, .85, .71)},  # lowercase horizontal / vertical
    # --- vertical metrics
    'xh':  {10: (526, 530, 540), 14: (518, 522, 534), 72: (504, 510, 524)},
    'os':  {10: (12, 12, 14), 14: (11, 11, 13), 72: (10, 10, 12)},
    # --- body widths
    'nw':  {10: (432, 452, 528), 14: (420, 440, 520), 72: (412, 432, 520)},  # n, outer stem to outer stem
    'ow':  {10: (512, 528, 590), 14: (500, 516, 584), 72: (494, 510, 584)},  # o outer width
    'Hw':  {10: (552, 572, 648), 14: (540, 560, 640), 72: (532, 552, 640)},  # H outer width
    'Ow':  {10: (690, 702, 752), 14: (680, 692, 748), 72: (676, 688, 748)},  # O outer width
    # --- sidebearings
    'sb':  {10: (88, 84, 52), 14: (78, 72, 44), 72: (62, 56, 34)},          # lowercase straight side
    'so':  {10: (60, 52, 32), 14: (53, 44, 26), 72: (40, 33, 19)},          # lowercase round side
    'SB':  {10: (102, 98, 62), 14: (92, 86, 54), 72: (74, 68, 42)},        # capital straight side
    'SO':  {10: (68, 60, 38), 14: (61, 52, 32), 72: (48, 40, 24)},          # capital round side
    # --- shape character
    'k':   {10: (.600, .604, .612), 14: (.590, .594, .604), 72: (.574, .578, .590)},  # round tension
    'jf':  {10: (1.0, .80, .54), 14: (1.0, .84, .60), 72: (1.0, .88, .64)},  # branch (join) thickness / stem
    'bury': {10: (.06, .20, .30), 14: (.05, .18, .28), 72: (.04, .14, .24)},  # counter overlap into stem
    'ap':  {10: (1.16, 1.14, 1.10), 14: (1.0, 1.0, 1.0), 72: (.80, .80, .84)},  # aperture openness
    'dot': {10: (2.05, 1.30, 1.04), 14: (1.90, 1.25, 1.02), 72: (1.70, 1.19, 1.0)},  # dot size / lc stem
    'acc': {10: (1.0, .86, .56), 14: (1.0, .82, .52), 72: (1.0, .78, .48)},  # accent stroke / lc stem
    'punct': {10: (1.08, 1.08, 1.06), 14: (1.0, 1.0, 1.0), 72: (.95, .95, .96)},
}

# width-axis multipliers: {wdth: (wght100, wght400, wght900)}
WIDTH = {
    'body': {75: (.790, .790, .800), 100: (1, 1, 1), 125: (1.200, 1.195, 1.170)},
    'stem': {75: (.98, .935, .80), 100: (1, 1, 1), 125: (1.0, 1.045, 1.09)},
    'side': {75: (.80, .80, .78), 100: (1, 1, 1), 125: (1.10, 1.10, 1.12)},
    'kadd': {75: (.034, .034, .034), 100: (0, 0, 0), 125: (-.012, -.012, -.012)},
    'contr': {75: (1.0, 1.02, 1.10), 100: (1, 1, 1), 125: (1.0, .99, .96)},
}

# grade: stem delta per master weight for GRAD = -50 and +100
GRADE = {-50: (-5.0, -8.0, -10.0), 0: (0, 0, 0), 100: (10.0, 15.0, 13.0)}


class Params:
    def __init__(self, wght=400, wdth=100, opsz=14, GRAD=0):
        self.wght, self.wdth, self.opsz, self.GRAD = wght, wdth, opsz, GRAD
        self.loc = dict(wght=wght, wdth=wdth, opsz=opsz, GRAD=GRAD)

        def t(name):
            ys = [_i1(wght, W_ANCH, T[name][o]) for o in O_ANCH]
            return _i1(opsz, O_ANCH, ys)

        def wm(name):
            ys = [_i1(wght, W_ANCH, WIDTH[name][d]) for d in D_ANCH]
            return _i1(wdth, D_ANCH, ys)

        self.wf = wf = wm('body')
        sf = wm('stem')
        self.sidef = side = wm('side')
        # --- vertical metrics
        self.cap = 700.0
        self.asc = 742.0
        self.desc = -204.0
        self.figh = 700.0
        self.xh = t('xh')
        self.os = t('os')
        # --- stems (ungraded = layout skeleton; graded = ink)
        self.V0 = t('V') * sf
        self.v0 = self.V0 * t('vr')
        cU = min(1.0, t('cU') * wm('contr')); cL = min(1.0, t('cL') * wm('contr'))
        self.H0 = self.V0 * cU
        self.h0 = self.v0 * cL
        g = _i1(GRAD, (-50, 0, 100), [_i1(wght, W_ANCH, GRADE[x]) for x in (-50, 0, 100)])
        self.gd = g
        self.V = self.V0 + g
        self.v = self.v0 + g * 0.97
        self.H = self.H0 + g * cU
        self.h = self.h0 + g * cL
        self.cU, self.cL = cU, cL
        # round strokes run slightly heavier than straight stems (optical)
        self.Vo = self.V * 1.035
        self.vo = self.v * 1.03
        self.Vo0 = self.V0 * 1.035
        self.vo0 = self.v0 * 1.03
        # diagonals
        self.Dg = self.V * 0.985
        self.dg = self.v * 0.985
        # --- widths
        self.nw = t('nw') * wf
        self.ow = t('ow') * wf
        self.Hw = t('Hw') * wf
        self.Ow = t('Ow') * wf
        # --- spacing
        self.sb = t('sb') * side
        self.so = t('so') * side
        self.SB = t('SB') * side
        self.SO = t('SO') * side
        self.sd = self.so * 0.36          # diagonal sides
        self.SD = self.SO * 0.34
        # --- character
        self.k = t('k') + wm('kadd')
        self.kdot = 0.74
        self.jf = t('jf')
        self.bury = t('bury')
        self.ap = t('ap')
        self.dotd = self.v0 * t('dot') + g * 0.9
        self.acc = self.v0 * t('acc') + g * 0.8
        self.punct = t('punct')
        # weight position 0..1 (0 thin, 1 black) for rules that key on colour
        self.wt = (self.V0 - 20.0) / 180.0

    def ki(self, rxi, ryi, c=0.42, upper=None):
        """Counter tension.  When the stroke is heavy the counter is much
        narrower in proportion than the outer shape; its short ends are then
        flattened (squarer) so the counter stays open instead of becoming a
        pointed lens.  Thin strokes leave the counter parallel to the outside."""
        rxi = max(rxi, 1.0); ryi = max(ryi, 1.0)
        if upper is None:
            upper = ryi * 2 > self.xh * 0.9
        tv, th = (self.Vo, self.H) if upper else (self.vo, self.h)
        ao = (rxi + tv) / (ryi + th); ai = rxi / ryi
        kh = self.k + c * max(0.0, min(ao, 1.6) - ai)
        kv = self.k + c * max(0.0, min(1.0 / ao, 1.6) - 1.0 / ai)
        return (min(kh, 0.80), min(kv, 0.80))

    def th(self, upper, ang):
        """Stroke thickness for a travel direction: vertical travel = stem,
        horizontal travel = thinner horizontal stroke."""
        import math
        s = abs(math.sin(math.radians(ang)))
        v, h = (self.Vo, self.H) if upper else (self.vo, self.h)
        return h + (v - h) * s * s

    def scaled(self, s, weight_comp=1.0):
        """Parameter set for small forms (superiors, fractions, ordinals).
        Geometry shrinks by s, strokes shrink less so colour matches the text."""
        import copy
        q = copy.copy(self)
        geo = ('cap', 'asc', 'desc', 'figh', 'xh', 'nw', 'ow', 'Hw', 'Ow')
        for a in geo:
            setattr(q, a, getattr(self, a) * s)
        st = s * weight_comp
        for a in ('V0', 'v0', 'H0', 'h0', 'V', 'v', 'H', 'h', 'Vo', 'vo', 'Vo0', 'vo0', 'Dg', 'dg', 'dotd', 'acc'):
            setattr(q, a, getattr(self, a) * st)
        for a in ('sb', 'so', 'SB', 'SO', 'sd', 'SD'):
            setattr(q, a, getattr(self, a) * s * 0.9)
        q.os = self.os * s
        return q


def masters():
    """Master locations.  wght x wdth at the default optical size, optical-size
    extremes at three weights, and grade extremes at three weights."""
    out = []
    for w in W_ANCH:
        for d in D_ANCH:
            out.append(dict(wght=w, wdth=d, opsz=14, GRAD=0))
    for o in (10, 72):
        for w in W_ANCH:
            out.append(dict(wght=w, wdth=100, opsz=o, GRAD=0))
    for g in (-50, 100):
        for w in W_ANCH:
            out.append(dict(wght=w, wdth=100, opsz=14, GRAD=g))
    return out


def master_name(loc):
    return 'w%d_d%d_o%d_g%s' % (loc['wght'], loc['wdth'], loc['opsz'],
                                ('m%d' % -loc['GRAD']) if loc['GRAD'] < 0 else str(loc['GRAD']))


NAMED_WEIGHTS = [(100, 'Thin'), (200, 'ExtraLight'), (300, 'Light'), (400, 'Regular'), (500, 'Medium'),
                 (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold'), (900, 'Black')]
