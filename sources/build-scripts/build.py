#!/usr/bin/env python3
"""Orion build pipeline.

    python3 build.py all            # sources -> variable font -> statics -> webfonts -> subsets
    python3 build.py sources vf     # individual stages

Stages
  sources  parametric generator -> UFO masters, features.fea, Orion.designspace
  vf       fontmake (ufo2ft / varLib) -> variable TTF, then post-processing
  statics  varLib.instancer -> static TTF families (overlaps removed, autohinted when ttfautohint is present)
  otf      fontmake -> static CFF OTFs for the text family
  web      WOFF2 for the variable font and statics
  subsets  unicode-range subsets of the variable font + CSS
"""
from __future__ import annotations
import os, sys, subprocess, shutil, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.environ.get('ORION_ROOT') or os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(ROOT, 'sources')
FONTS = os.path.join(ROOT, 'fonts')
TMP = os.path.join(ROOT, '.build')

from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import ttProgram
from fontTools.varLib import instancer
from fontTools import subset as ftsubset
from orion.params import NAMED_WEIGHTS, FAMILY

VERSION = '1.000'
VF_NAME = 'Orion-VF'

STATIC_FAMILIES = [   # family name, file prefix, fixed axis values
    ('Orion', 'Orion', dict(wdth=100, opsz=14, GRAD=0)),
    ('Orion Display', 'OrionDisplay', dict(wdth=100, opsz=72, GRAD=0)),
    ('Orion Condensed', 'OrionCondensed', dict(wdth=75, opsz=14, GRAD=0)),
]

SUBSETS = {
    'latin': 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,'
             'U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD,U+2190,U+2192,U+2713,U+2715,U+25B6,U+25C0,U+2605,U+20B9',
    'latin-extended': 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,'
                      'U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF',
    'vietnamese': 'U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,'
                  'U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB',
    'greek': 'U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF',
    'cyrillic': 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116',
    'symbols': 'U+2190-21FF,U+2200-22FF,U+2300-23FF,U+2423,U+25A0-25FF,U+2605-2606,U+2713-2717',
}


def log(*a):
    print('[build]', *a, flush=True)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.stderr.write(r.stdout[-3000:] + r.stderr[-6000:])
        raise SystemExit('command failed: ' + ' '.join(cmd))
    return r


# ------------------------------------------------------------------ stages
def stage_sources():
    from orion.ufo import write_sources
    from orion.kerning import build_kerning
    t = time.time()
    r = write_sources(SRC, kern_fn=build_kerning, log=lambda *a: None)
    json.dump(dict(win=r['win'], ymax=r['ymax'], ymin=r['ymin'], glyphs=r['glyphs']),
              open(os.path.join(SRC, 'build-info.json'), 'w'), indent=1)
    log('sources: %d glyphs x 21 masters, yMax %.0f yMin %.0f (%.0fs)' % (r['glyphs'], r['ymax'], r['ymin'], time.time() - t))


def set_overlap_flags(font):
    glyf = font['glyf']
    for name in font.getGlyphOrder():
        g = glyf[name]
        if g.isComposite():
            g.components[0].flags |= 0x0400          # OVERLAP_COMPOUND
        elif g.numberOfContours > 0:
            g.flags[0] |= 0x40                       # OVERLAP_SIMPLE


def fix_unhinted(font):
    """Unhinted TrueType: smooth rendering at all sizes, dropout control on."""
    gasp = newTable('gasp'); gasp.version = 1; gasp.gaspRange = {0xFFFF: 0x000F}
    font['gasp'] = gasp
    prep = newTable('prep'); prep.program = ttProgram.Program()
    prep.program.fromAssembly(['PUSHW[]', '511', 'SCANCTRL[]', 'PUSHB[]', '4', 'SCANTYPE[]'])
    font['prep'] = prep
    font['head'].flags |= 1 << 3


def common_fixes(font):
    from fontTools.ttLib.tables.O_S_2f_2 import Panose
    os2 = font['OS/2']
    os2.recalcUnicodeRanges(font)
    os2.ulCodePageRange1 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 7) | (1 << 8)   # 1252 1250 1251 1253 1254 1257 1258
    os2.ulCodePageRange2 = 0
    os2.fsType = 0
    os2.achVendID = 'ORIN'
    font['head'].fontRevision = float(VERSION)
    font['post'].isFixedPitch = 0
    meta = newTable('meta'); meta.data = {'dlng': 'Latn, Grek, Cyrl', 'slng': 'Latn, Grek, Cyrl'}
    font['meta'] = meta


def set_names(font, family, style, vf=False):
    name = font['name']
    ribbi = style in ('Regular', 'Bold')
    full = (family + ' ' + style).strip()
    ps = (family.replace(' ', '') + '-' + style.replace(' ', ''))
    for nid in (1, 2, 3, 4, 5, 6, 16, 17, 21, 22, 25):
        name.removeNames(nameID=nid)
    def put(nid, s):
        name.setName(s, nid, 3, 1, 0x409)
    if ribbi:
        put(1, family); put(2, style)
    else:
        put(1, full); put(2, 'Regular'); put(16, family); put(17, style)
    put(3, '%s;ORIN;%s' % (VERSION, ps)); put(4, full); put(5, 'Version ' + VERSION); put(6, ps)
    if vf:
        put(25, family.replace(' ', ''))
    os2 = font['OS/2']
    os2.fsSelection &= ~((1 << 0) | (1 << 5) | (1 << 6))
    if style == 'Bold':
        os2.fsSelection |= 1 << 5; font['head'].macStyle = 1
    else:
        font['head'].macStyle = 0
        os2.fsSelection |= 1 << 6            # REGULAR for every upright, non-bold style
    os2.fsSelection |= 1 << 7


def stage_vf():
    os.makedirs(TMP, exist_ok=True)
    raw = os.path.join(TMP, 'Orion-VF-raw.ttf')
    t = time.time()
    run(['fontmake', '-m', os.path.join(SRC, 'designspace', 'Orion.designspace'), '-o', 'variable',
         '--output-path', raw, '--flatten-components'])
    f = TTFont(raw)
    set_overlap_flags(f)
    fix_unhinted(f)
    common_fixes(f)
    set_names(f, FAMILY, 'Regular', vf=True)
    out = os.path.join(FONTS, 'variable'); os.makedirs(out, exist_ok=True)
    p = os.path.join(out, VF_NAME + '.ttf')
    f.save(p)
    log('variable font: %s  %.0f KB  (%.0fs)' % (os.path.relpath(p, ROOT), os.path.getsize(p) / 1024, time.time() - t))


def drop_slivers(font, min_area=150.0):
    """Overlap removal can leave contours a few units across; remove them."""
    from fontTools.pens.areaPen import AreaPen
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    glyf = font['glyf']; gs = font.getGlyphSet(); n = 0
    for name in font.getGlyphOrder():
        g = glyf[name]
        if g.numberOfContours <= 1:
            continue
        rec = RecordingPen(); gs[name].draw(rec)
        contours = []; cur = []
        for op in rec.value:
            cur.append(op)
            if op[0] in ('closePath', 'endPath'):
                contours.append(cur); cur = []
        keep = []
        for c in contours:
            ap = AreaPen(gs)
            for op, args in c:
                getattr(ap, op)(*args)
            if abs(ap.value) >= min_area:
                keep.append(c)
        if len(keep) != len(contours) and keep:
            pen = TTGlyphPen(gs)
            for c in keep:
                for op, args in c:
                    getattr(pen, op)(*args)
            ng = pen.glyph()
            glyf[name] = ng; n += 1
    return n


def autohint(path):
    try:
        import ttfautohint
    except Exception:
        return False
    tmp = path + '.hinted'
    ttfautohint.ttfautohint(in_file=path, out_file=tmp, hinting_range_min=8, hinting_range_max=50,
                            no_info=True, increase_x_height=0, windows_compatibility=False,
                            default_script='latn', fallback_script='latn')
    os.replace(tmp, path)
    f = TTFont(path)
    gasp = newTable('gasp'); gasp.version = 1; gasp.gaspRange = {0xFFFF: 0x000F}
    f['gasp'] = gasp
    f.save(path)
    return True


def stage_statics(hint=True):
    vf = os.path.join(FONTS, 'variable', VF_NAME + '.ttf')
    out = os.path.join(FONTS, 'static'); os.makedirs(out, exist_ok=True)
    t = time.time(); n = 0; hinted = False
    for family, prefix, fixed in STATIC_FAMILIES:
        fdir = os.path.join(out, prefix); os.makedirs(fdir, exist_ok=True)
        for w, style in NAMED_WEIGHTS:
            f = TTFont(vf)
            loc = dict(fixed, wght=w)
            inst = instancer.instantiateVariableFont(f, loc, overlap=instancer.OverlapMode.REMOVE)
            for tag in ('STAT', 'MVAR', 'avar', 'HVAR', 'fvar', 'gvar', 'cvar'):
                if tag in inst:
                    del inst[tag]
            set_names(inst, family, style)
            inst['OS/2'].usWeightClass = w
            inst['OS/2'].usWidthClass = 3 if fixed['wdth'] == 75 else 5
            drop_slivers(inst)
            p = os.path.join(fdir, '%s-%s.ttf' % (prefix, style))
            inst.save(p)
            if hint:
                hinted = autohint(p) or hinted
            n += 1
    log('statics: %d TTF in %d families%s (%.0fs)' % (n, len(STATIC_FAMILIES), ', autohinted (ttfautohint)' if hinted else ', unhinted', time.time() - t))


def stage_otf():
    """CFF-flavoured static OTFs of the text family, interpolated from the UFO sources."""
    t = time.time()
    out = os.path.join(FONTS, 'static-otf'); os.makedirs(out, exist_ok=True)
    work = os.path.join(TMP, 'otf'); shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
    names = '|'.join('Orion %s' % s for w, s in NAMED_WEIGHTS)
    run(['fontmake', '-m', os.path.join(SRC, 'designspace', 'Orion.designspace'), '-o', 'otf', '-i', '^(%s)$' % names,
         '--output-dir', work, '--flatten-components', '--optimize-cff', '1'])
    n = 0
    for fn in sorted(os.listdir(work)):
        if fn.endswith('.otf'):
            f = TTFont(os.path.join(work, fn))
            style = fn[:-4].split('-')[-1]
            common_fixes(f); set_names(f, FAMILY, style)
            f.save(os.path.join(out, 'Orion-%s.otf' % style)); n += 1
    shutil.rmtree(os.path.join(SRC, 'instances'), ignore_errors=True)
    log('otf: %d static CFF fonts (%.0fs)' % (n, time.time() - t))


def to_woff2(src, dst):
    f = TTFont(src); f.flavor = 'woff2'; f.save(dst)


def stage_web():
    out = os.path.join(FONTS, 'webfonts'); os.makedirs(out, exist_ok=True)
    vf = os.path.join(FONTS, 'variable', VF_NAME + '.ttf')
    to_woff2(vf, os.path.join(FONTS, 'variable', VF_NAME + '.woff2'))
    n = 1
    sdir = os.path.join(FONTS, 'static')
    for fam in sorted(os.listdir(sdir)):
        for fn in sorted(os.listdir(os.path.join(sdir, fam))):
            if fn.endswith('.ttf'):
                to_woff2(os.path.join(sdir, fam, fn), os.path.join(out, fn[:-4] + '.woff2')); n += 1
    log('web: %d WOFF2 files; variable %.0f KB' % (n, os.path.getsize(os.path.join(FONTS, 'variable', VF_NAME + '.woff2')) / 1024))


def stage_subsets():
    vf = os.path.join(FONTS, 'variable', VF_NAME + '.ttf')
    base = os.path.join(FONTS, 'subsets')
    css = ['/* Orion variable font, split by script with unicode-range (generated by build.py) */']
    report = {}
    for nm, ur in SUBSETS.items():
        d = os.path.join(base, nm); os.makedirs(d, exist_ok=True)
        opts = ftsubset.Options()
        opts.layout_features = ['*']; opts.flavor = 'woff2'; opts.name_IDs = ['*']; opts.notdef_outline = True
        opts.glyph_names = False; opts.drop_tables += ['meta']
        f = TTFont(vf)
        cps = ftsubset.parse_unicodes(ur.replace('U+', ''))
        have = set(f.getBestCmap())
        cps = [c for c in cps if c in have]
        s = ftsubset.Subsetter(opts); s.populate(unicodes=cps); s.subset(f)
        p = os.path.join(d, 'Orion-VF.%s.woff2' % nm)
        f.flavor = 'woff2'; f.save(p)
        report[nm] = dict(codepoints=len(cps), bytes=os.path.getsize(p))
        css.append("@font-face {\n  font-family: 'Orion';\n  src: url('%s/Orion-VF.%s.woff2') format('woff2');\n"
                   "  font-weight: 100 900;\n  font-stretch: 75%% 125%%;\n  font-style: normal;\n  font-display: swap;\n"
                   "  unicode-range: %s;\n}" % (nm, nm, ur))
    open(os.path.join(base, 'orion-subsets.css'), 'w').write('\n'.join(css) + '\n')
    json.dump(report, open(os.path.join(base, 'subsets.json'), 'w'), indent=1)
    log('subsets: ' + ', '.join('%s %d cp / %.0f KB' % (k, v['codepoints'], v['bytes'] / 1024) for k, v in report.items()))


STAGES = dict(sources=stage_sources, vf=stage_vf, statics=stage_statics, otf=stage_otf, web=stage_web, subsets=stage_subsets)

if __name__ == '__main__':
    args = sys.argv[1:] or ['all']
    todo = ['sources', 'vf', 'statics', 'otf', 'web', 'subsets'] if 'all' in args else args
    for st in todo:
        STAGES[st]()
