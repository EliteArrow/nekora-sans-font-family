"""Orion geometry kernel.

Every glyph in Orion is produced by this kernel from design parameters.
Outlines are original constructions: superelliptic stroke bands, explicit
polygons for diagonals, and trimmed arcs for terminals.  Because each glyph
function emits the same point structure for any parameter set, all masters are
interpolation-compatible by construction.

Contour format (closed, PostScript orientation: outer = CCW, counter = CW):
    [('l', (x, y)) | ('c', (c1x, c1y), (c2x, c2y), (x, y)), ...]
The start point of a contour is the end point of its last segment.
"""
from __future__ import annotations
import math

CIRCLE_K = 0.5522847498


# ----------------------------------------------------------------- vectors
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def mul(a, s): return (a[0] * s, a[1] * s)
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def cross(a, b): return a[0] * b[1] - a[1] * b[0]
def length(a): return math.hypot(a[0], a[1])
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
def unit(deg):
    r = math.radians(deg)
    return (math.cos(r), math.sin(r))
def norm(a):
    l = length(a) or 1.0
    return (a[0] / l, a[1] / l)
def ang_of(a): return math.degrees(math.atan2(a[1], a[0]))


class Line:
    """Infinite line helper for diagonal construction."""
    __slots__ = ('p', 'd')

    def __init__(self, p, q=None, d=None, ang=None):
        self.p = p
        if q is not None:
            self.d = norm(sub(q, p))
        elif d is not None:
            self.d = norm(d)
        else:
            self.d = unit(ang)

    def at_y(self, y):
        t = (y - self.p[1]) / self.d[1]
        return (self.p[0] + self.d[0] * t, y)

    def at_x(self, x):
        t = (x - self.p[0]) / self.d[0]
        return (x, self.p[1] + self.d[1] * t)

    def offset(self, dist):
        """Parallel line shifted to the LEFT of direction by dist (negative = right)."""
        n = (-self.d[1], self.d[0])
        return Line(add(self.p, mul(n, dist)), d=self.d)

    def __and__(self, other):
        c = cross(self.d, other.d)
        if abs(c) < 1e-9:
            return self.p
        t = cross(sub(other.p, self.p), other.d) / c
        return add(self.p, mul(self.d, t))

    def hw(self, th):
        """Horizontal width of a stroke of perpendicular thickness th along this line."""
        return th / max(abs(self.d[1]), 1e-6)

    def vh(self, th):
        return th / max(abs(self.d[0]), 1e-6)


# ----------------------------------------------------------------- cubics
def cubic_pt(p0, p1, p2, p3, t):
    mt = 1 - t
    a = mt * mt * mt; b = 3 * mt * mt * t; c = 3 * mt * t * t; d = t * t * t
    return (a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
            a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1])


def cubic_split(p0, p1, p2, p3, t):
    p01 = lerp(p0, p1, t); p12 = lerp(p1, p2, t); p23 = lerp(p2, p3, t)
    p012 = lerp(p01, p12, t); p123 = lerp(p12, p23, t)
    m = lerp(p012, p123, t)
    return (p0, p01, p012, m), (m, p123, p23, p3)


def curve_handles(A, dA, B, dB, k):
    """Handles for a cubic from A (tangent dA) to B (tangent dB).

    Handles lie on the tangent lines, scaled so that a 90-degree turn with
    k = CIRCLE_K is a circular arc; larger k gives the squarer, superelliptic
    arcs that define Orion's rounds."""
    c = cross(dA, dB)
    chord = length(sub(B, A))
    if abs(c) > 0.02:
        s = cross(sub(B, A), dB) / c
        u = cross(sub(B, A), dA) / c
        if s > 1e-6 and u < -1e-6:
            theta = math.acos(max(-1.0, min(1.0, dot(dA, dB))))
            base = (4.0 / 3.0) * math.tan(theta / 4) / math.tan(theta / 2) / CIRCLE_K
            if isinstance(k, tuple):
                fa = k[0] * dA[0] * dA[0] + k[1] * dA[1] * dA[1]
                fb = k[0] * dB[0] * dB[0] + k[1] * dB[1] * dB[1]
            else:
                fa = fb = k
            fa = min(base * fa, 0.94); fb = min(base * fb, 0.94)
            return add(A, mul(dA, s * fa)), add(B, mul(dB, u * fb))
    d = chord / 3.0
    return add(A, mul(dA, d)), sub(B, mul(dB, d))


class Node:
    __slots__ = ('L', 'R', 'dL', 'dR', 'line', 'k')

    def __init__(self, L, R, dL, dR, line=False, k=None):
        self.L = L; self.R = R; self.dL = dL; self.dR = dR; self.line = line; self.k = k


def N(x, y, a, t, line=False, k=None, tl=None, tr=None, aL=None, aR=None):
    """Stroke node: centre (x, y), travel direction a (degrees), thickness t.
    L is the edge to the left of travel, R to the right."""
    d = unit(a)
    n = (-d[1], d[0])
    tl = t / 2.0 if tl is None else tl
    tr = t / 2.0 if tr is None else tr
    return Node((x + n[0] * tl, y + n[1] * tl), (x - n[0] * tr, y - n[1] * tr),
                unit(a if aL is None else aL), unit(a if aR is None else aR), line, k)


def E(L, R, a, line=False, k=None, aL=None, aR=None):
    """Stroke node given by explicit edge points."""
    return Node(L, R, unit(a if aL is None else aL), unit(a if aR is None else aR), line, k)


def _side_segments(pts, dirs, nodes, closed, k, use_node_k=True):
    n = len(nodes)
    segs = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        j = (i + 1) % n
        A, B = pts[i], pts[j]
        if nodes[i].line:
            segs.append(['l', A, B])
        else:
            kk = nodes[i].k if (nodes[i].k is not None and use_node_k) else k
            c1, c2 = curve_handles(A, dirs[i], B, dirs[j], kk)
            segs.append(['c', A, c1, c2, B])
    return segs


def _cut_fn(cut):
    kind = cut[0]
    if kind == 'x':
        return lambda p: p[0] - cut[1]
    if kind == 'y':
        return lambda p: p[1] - cut[1]
    p0 = cut[1]; n = unit(cut[2] + 90.0)          # ('line', point, angle)
    return lambda p: (p[0] - p0[0]) * n[0] + (p[1] - p0[1]) * n[1]


def _seg_pt(seg, t):
    if seg[0] == 'l':
        return lerp(seg[1], seg[2], t)
    return cubic_pt(seg[1], seg[2], seg[3], seg[4], t)


def _find_t(seg, f):
    a, b = 0.0, 1.0
    fa, fb = f(_seg_pt(seg, a)), f(_seg_pt(seg, b))
    if fa == 0: return 0.0
    if fb == 0: return 1.0
    if fa * fb > 0:
        return None
    for _ in range(40):
        m = (a + b) / 2
        fm = f(_seg_pt(seg, m))
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a + b) / 2


def _trim(seg, t, keep_tail):
    if seg[0] == 'l':
        m = lerp(seg[1], seg[2], t)
        return ['l', m, seg[2]] if keep_tail else ['l', seg[1], m]
    a, b = cubic_split(seg[1], seg[2], seg[3], seg[4], t)
    return ['c', *b] if keep_tail else ['c', *a]


WARN = []


def stroke(nodes, closed=False, cut0=None, cut1=None, k=0.58, kL=None, kR=None, tag=''):
    """Expand a list of stroke nodes into closed contour(s).

    open  -> one CCW band: right edge forward, cap, left edge back, cap.
    closed-> two contours (ring); the node sequence must run counter-clockwise.
    cut0 / cut1 trim the first / last segment of both edges by a straight line,
    producing a planar terminal on a curve taken from the full round."""
    Ls = _side_segments([n.L for n in nodes], [n.dL for n in nodes], nodes, closed, k if kL is None else kL, kL is None)
    Rs = _side_segments([n.R for n in nodes], [n.dR for n in nodes], nodes, closed, k if kR is None else kR, kR is None)
    if closed:
        outer = [(s[0], *s[2:]) for s in Rs]
        inner = [(s[0], *s[2:]) for s in reverse_segs(Ls)]
        return [outer, inner]
    for cut, idx, tail in ((cut0, 0, True), (cut1, -1, False)):
        if cut is None:
            continue
        f = _cut_fn(cut)
        for side in (Ls, Rs):
            t = _find_t(side[idx], f)
            if t is None:
                WARN.append('cut miss %s %s' % (tag, cut[0]))
                t = 0.0 if tail else 1.0
            side[idx] = _trim(side[idx], t, tail)
    out = [(s[0], *s[2:]) for s in Rs]
    out.append(('l', Ls[-1][-1]))
    for s in reverse_segs(Ls):
        out.append((s[0], *s[2:]))
    out.append(('l', Rs[0][1]))
    return [out]


def reverse_segs(segs):
    out = []
    for s in reversed(segs):
        if s[0] == 'l':
            out.append(['l', s[2], s[1]])
        else:
            out.append(['c', s[4], s[3], s[2], s[1]])
    return out


def reverse_contour(c):
    """Reverse direction of a contour in our segment format."""
    n = len(c)
    pts_end = [s[-1] for s in c]
    out = []
    # start point of segment i is end point of segment i-1
    for i in range(n - 1, -1, -1):
        start = pts_end[i - 1]
        s = c[i]
        if s[0] == 'l':
            out.append(('l', start))
        else:
            out.append(('c', s[2], s[1], start))
    return out


POLY_LOG = []     # orientation decisions, compared across masters by the build


def poly(pts):
    """Closed polygon; orientation normalised to CCW."""
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        a += x0 * y1 - x1 * y0
    POLY_LOG.append(a < 0)
    if a < 0:
        pts = list(reversed(pts))
    return [('l', p) for p in pts[1:]] + [('l', pts[0])]


def poly_raw(pts):
    return [('l', p) for p in pts[1:]] + [('l', pts[0])]


def superellipse(cx, cy, rx, ry, k=0.58, cw=False, kx=None):
    """Closed superelliptic contour with on-curve points at the four extremes."""
    hx = rx * (kx if kx is not None else k); hy = ry * k
    r = (cx + rx, cy); t = (cx, cy + ry); l = (cx - rx, cy); b = (cx, cy - ry)
    c = [('c', (cx + rx, cy + hy), (cx + hx, cy + ry), t),
         ('c', (cx - hx, cy + ry), (cx - rx, cy + hy), l),
         ('c', (cx - rx, cy - hy), (cx - hx, cy - ry), b),
         ('c', (cx + hx, cy - ry), (cx + rx, cy - hy), r)]
    return reverse_contour(c) if cw else c


def round_rect(x0, y0, x1, y1, r, k=0.6):
    """Rounded rectangle (squircle-like when r is half the short side)."""
    r = max(0.0, min(r, (x1 - x0) / 2.0, (y1 - y0) / 2.0))
    h = r * (1 - k)
    return [('l', (x1 - r, y0)), ('c', (x1 - h, y0), (x1, y0 + h), (x1, y0 + r)),
            ('l', (x1, y1 - r)), ('c', (x1, y1 - h), (x1 - h, y1), (x1 - r, y1)),
            ('l', (x0 + r, y1)), ('c', (x0 + h, y1), (x0, y1 - h), (x0, y1 - r)),
            ('l', (x0, y0 + r)), ('c', (x0, y0 + h), (x0 + h, y0), (x0 + r, y0))]


def xform_contour(c, m):
    """Apply affine m = (a, b, c, d, e, f): x' = a x + c y + e, y' = b x + d y + f."""
    a, b, cc, d, e, f = m
    def T(p): return (a * p[0] + cc * p[1] + e, b * p[0] + d * p[1] + f)
    out = [(s[0], *[T(p) for p in s[1:]]) for s in c]
    if a * d - b * cc < 0:
        out = reverse_contour(out)
    return out


def mat_mul(m, n):
    """Compose: apply n first, then m."""
    a, b, c, d, e, f = m
    a2, b2, c2, d2, e2, f2 = n
    return (a * a2 + c * b2, b * a2 + d * b2, a * c2 + c * d2, b * c2 + d * d2,
            a * e2 + c * f2 + e, b * e2 + d * f2 + f)


IDENT = (1, 0, 0, 1, 0, 0)


def flatten(c, steps=6):
    """Polyline approximation of a contour (for metrics / kerning analysis)."""
    pts = []
    prev = c[-1][-1]
    for s in c:
        if s[0] == 'l':
            pts.append(s[1])
        else:
            for i in range(1, steps + 1):
                pts.append(cubic_pt(prev, s[1], s[2], s[3], i / steps))
        prev = s[-1]
    return pts


def contour_bounds(c):
    pts = flatten(c, 8)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def signed_area(c):
    pts = flatten(c, 6)
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        a += x0 * y1 - x1 * y0
    return a / 2.0


class G:
    """Glyph builder."""

    def __init__(self, P, name=''):
        self.P = P; self.name = name
        self.contours = []; self.components = []; self.anchors = {}
        self.w = 0.0
        self._m = IDENT; self._stack = []

    # -- transforms (same in every master, so compatibility is preserved)
    def push(self, m):
        self._stack.append(self._m); self._m = mat_mul(self._m, m); return self
    def pop(self):
        self._m = self._stack.pop()
    def __enter__(self): return self
    def __exit__(self, *a): self.pop()
    def flip_x(self, cx): return self.push((-1, 0, 0, 1, 2 * cx, 0))
    def flip_y(self, cy): return self.push((1, 0, 0, -1, 0, 2 * cy))
    def rot180(self, cx, cy): return self.push((-1, 0, 0, -1, 2 * cx, 2 * cy))
    def shift(self, dx, dy=0): return self.push((1, 0, 0, 1, dx, dy))
    def scale(self, sx, sy=None, ox=0, oy=0):
        sy = sx if sy is None else sy
        return self.push((sx, 0, 0, sy, ox - sx * ox, oy - sy * oy))
    def rot(self, deg, ox=0, oy=0):
        c = math.cos(math.radians(deg)); s_ = math.sin(math.radians(deg))
        return self.push((c, s_, -s_, c, ox - c * ox + s_ * oy, oy - s_ * ox - c * oy))
    def embed(self, fn, P, dx=0, dy=0):
        """Draw another glyph function with its own parameter set at an offset."""
        sub = G(P, self.name)
        fn(sub)
        with self.shift(dx, dy):
            self.add(sub.contours)
        return sub
    def skew(self, deg, oy=0):
        t = math.tan(math.radians(deg))
        return self.push((1, 0, t, 1, -t * oy, 0))

    def add(self, cs):
        for c in cs:
            self.contours.append(c if self._m == IDENT else xform_contour(c, self._m))
        return self

    # -- primitives
    def poly(self, pts): return self.add([poly(pts)])
    def rect(self, x0, y0, x1, y1): return self.add([poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])])
    def vstem(self, cx, y0, y1, t): return self.rect(cx - t / 2, y0, cx + t / 2, y1)
    def hbar(self, x0, x1, cy, t): return self.rect(x0, cy - t / 2, x1, cy + t / 2)
    def stroke(self, nodes, **kw):
        kw.setdefault('k', self.P.k); kw.setdefault('tag', self.name)
        return self.add(stroke(nodes, **kw))
    def ring(self, cx, cy, rx, ry, tl, tr, tt, tb, k=None, ki=None):
        """Bowl: outer radii rx/ry about (cx, cy); wall thickness left/right/top/bottom."""
        k = self.P.k if k is None else k
        ki = k if ki is None else ki
        outer = superellipse(cx, cy, rx, ry, k)
        ix0 = cx - rx + tl; ix1 = cx + rx - tr; iy0 = cy - ry + tb; iy1 = cy + ry - tt
        inner = superellipse((ix0 + ix1) / 2, (iy0 + iy1) / 2, (ix1 - ix0) / 2, (iy1 - iy0) / 2, ki, cw=True)
        return self.add([outer, inner])
    def dot(self, cx, cy, d, k=None):
        """Orion's squircle dot: a superellipse that is squarer than the bowls."""
        k = self.P.kdot if k is None else k
        return self.add([superellipse(cx, cy, d / 2, d / 2, k)])
    def oval(self, cx, cy, rx, ry, k=None, cw=False):
        return self.add([superellipse(cx, cy, rx, ry, self.P.k if k is None else k, cw=cw)])

    def translate(self, dx, dy=0.0):
        self.contours = [[(s[0], *[(p[0] + dx, p[1] + dy) for p in s[1:]]) for s in c] for c in self.contours]
        self.anchors = {k: (x + dx, y + dy) for k, (x, y) in self.anchors.items()}

    def comp(self, name, dx=0, dy=0):
        self.components.append((name, dx, dy)); return self
    def anchor(self, name, x, y):
        self.anchors[name] = (x, y); return self

    def bounds(self):
        bs = [contour_bounds(c) for c in self.contours]
        if not bs:
            return None
        return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))
