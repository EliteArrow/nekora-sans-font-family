"""Metric comparison of Orion against the reference families (numbers only — no reference outline is read into the
project, exported or shipped).  Reference numbers come from qa/reference_audit.py run on the user's licensed copies:

    python3 -I qa/reference_audit.py "<Reference dir>" qa/reports/reference-metrics.json

This script measures Orion with the same function and writes qa/reports/reference-comparison.json."""
import os, sys, json
from fontTools.ttLib import TTFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from reference_audit import measure
ROOT = os.path.dirname(HERE)
REF = json.load(open(os.path.join(ROOT, 'qa', 'reports', 'reference-metrics.json')))
KEYS = ['cap', 'xh', 'asc', 'desc', 'stemUC', 'stemLC', 'O_w', 'o_w', 'o_overshoot', 'adv_n', 'adv_H', 'adv_o', 'avg_lc_adv', 'avg_uc_adv', 'space', 'period_w', 'hyphen_th', 'fig', 'adv_0']
COLS = [('Orion Regular', None, 400), ('Gotham Book', 'Gotham-Book.otf', 'm'), ('Inter (wght 400)', 'Inter-VariableFont_opsz,wght.ttf', 'm_wght400'),
        ('Roboto Flex (wght 400)', 'RobotoFlex-VariableFont_GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,opsz,slnt,wdth,wght.ttf', 'm_wght400'),
        ('Netflix Sans Regular', 'NetflixSans-Regular.otf', 'm')]
WEIGHTS = [('Thin', 100, 'Gotham-Thin.otf'), ('Light', 300, 'Gotham-Light.otf'), ('Regular', 400, 'Gotham-Book.otf'), ('Medium', 500, 'Gotham-Medium.otf'),
           ('Bold', 700, 'Gotham-Bold.otf'), ('Black', 900, 'Gotham-Black.otf')]
out = {'note': 'Units per 1000 em. Reference values measured from the licensed reference fonts; only these numbers are stored.', 'columns': [], 'weights': []}
vf = TTFont(os.path.join(ROOT, 'fonts', 'variable', 'Orion-VF.ttf'))
for label, fn, key in COLS:
    m = measure(vf, {'wght': key}) if fn is None else REF[fn][key]
    out['columns'].append({'label': label, 'metrics': {k: m.get(k) for k in KEYS}})
for name, w, gf in WEIGHTS:
    o = measure(vf, {'wght': w}); g = REF[gf]['m']
    out['weights'].append({'style': name, 'wght': w, 'orion': {k: o.get(k) for k in ('xh', 'stemUC', 'stemLC', 'O_w', 'adv_n', 'avg_lc_adv')},
                           'gotham': {k: g.get(k) for k in ('xh', 'stemUC', 'stemLC', 'O_w', 'adv_n', 'avg_lc_adv')}, 'gotham_style': gf.split('-')[1].split('.')[0]})
json.dump(out, open(os.path.join(ROOT, 'qa', 'reports', 'reference-comparison.json'), 'w'), indent=1)
print('reference-comparison.json written:', [c['label'] for c in out['columns']])
