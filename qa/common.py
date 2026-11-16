"""Shared helpers for the Orion QA suite."""
import os, sys, json, glob, itertools
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
VF = os.path.join(ROOT, 'fonts', 'variable', 'Orion-VF.ttf')
STATIC = os.path.join(ROOT, 'fonts', 'static')
REPORTS = os.path.join(ROOT, 'qa', 'reports')
os.makedirs(REPORTS, exist_ok=True)
AXES = dict(wght=(100, 400, 900), wdth=(75, 100, 125), opsz=(10, 14, 72), GRAD=(-50, 0, 100))
DEFAULT = dict(wght=400, wdth=100, opsz=14, GRAD=0)


def all_fonts():
    out = [VF]
    out += sorted(glob.glob(os.path.join(STATIC, '*', '*.ttf')))
    out += sorted(glob.glob(os.path.join(ROOT, 'fonts', 'static-otf', '*.otf')))
    return out


def corners():
    keys = list(AXES)
    return [dict(zip(keys, c)) for c in itertools.product(*[(AXES[k][0], AXES[k][2]) for k in keys])]


def grid_locations(seed=7, n_random=40):
    import random
    rnd = random.Random(seed)
    locs = [dict(DEFAULT)]
    for k, (mn, df, mx) in AXES.items():                       # each axis independently
        for v in (mn, (mn + df) / 2, (df + mx) / 2, mx):
            locs.append(dict(DEFAULT, **{k: v}))
    locs += corners()                                           # all 16 corners
    for w in (200, 300, 500, 600, 700, 800):                    # named weights at three widths
        for d in (75, 100, 125):
            locs.append(dict(DEFAULT, wght=w, wdth=d))
    for _ in range(n_random):                                   # arbitrary intermediates
        locs.append({k: round(rnd.uniform(mn, mx), 1) for k, (mn, df, mx) in AXES.items()})
    seen = []; out = []
    for l in locs:
        t = tuple(sorted(l.items()))
        if t not in seen:
            seen.append(t); out.append(l)
    return out


class Report:
    def __init__(self, name):
        self.name = name; self.rows = []
    def add(self, check, status, detail=''):
        self.rows.append(dict(check=check, status=status, detail=detail))
        if status != 'PASS':
            print('  [%s] %s  %s' % (status, check, str(detail)[:200]))
    def ok(self, check, cond, detail='', warn=False):
        self.add(check, 'PASS' if cond else ('WARN' if warn else 'FAIL'), detail if not cond else (detail if isinstance(detail, str) and len(detail) < 120 else ''))
        return cond
    def summary(self):
        c = {}
        for r in self.rows:
            c[r['status']] = c.get(r['status'], 0) + 1
        return c
    def save(self, extra=None):
        d = dict(suite=self.name, summary=self.summary(), results=self.rows)
        if extra:
            d.update(extra)
        json.dump(d, open(os.path.join(REPORTS, self.name + '.json'), 'w'), indent=1, ensure_ascii=False)
        print('%-16s %s' % (self.name, self.summary()))
        return d
