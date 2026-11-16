"""Write Orion masters as UFO 3 sources plus a Designspace 5 document."""
from __future__ import annotations
import os, shutil, datetime
import ufoLib2
from fontTools.designspaceLib import (DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor,
                                      AxisLabelDescriptor)
from .params import Params, masters, master_name, AXES, DEFAULT, NAMED_WEIGHTS, FAMILY, UPM
from .glyphset import build_master, cmap_for
from . import marks
from .features import build_features

VERSION = (1, 0)
HHEA_ASC, HHEA_DESC = 1000, -250
COPYRIGHT = 'Copyright 2026 The Orion Project Authors'
LICENSE = ('This Font Software is licensed under the SIL Open Font License, Version 1.1. '
           'This license is available with a FAQ at: https://openfontlicense.org')


def _r(v):
    return int(round(v))


def write_master(loc, path, features_text, kerning=None, groups=None, glyphs=None, win=(1100, 300)):
    P = Params(**loc)
    glyphs = glyphs or build_master(P)
    cmap = cmap_for(glyphs)
    rev = {}
    for cp, n in cmap.items():
        rev.setdefault(n, []).append(cp)
    f = ufoLib2.Font()
    i = f.info
    i.familyName = FAMILY
    i.styleName = master_name(loc)
    i.unitsPerEm = UPM
    i.ascender = _r(P.asc); i.descender = _r(P.desc)
    i.xHeight = _r(P.xh); i.capHeight = _r(P.cap)
    i.italicAngle = 0
    i.versionMajor, i.versionMinor = VERSION
    i.copyright = COPYRIGHT
    i.openTypeNameLicense = LICENSE
    i.openTypeNameLicenseURL = 'https://openfontlicense.org'
    i.openTypeNameDesigner = 'The Orion Project Authors (parametric design generated with Claude)'
    i.openTypeNameManufacturer = 'The Orion Project'
    i.openTypeNameDescription = ('Orion is a geometric-humanist variable sans serif for streaming-television '
                                 'interfaces, with weight, width, optical size and grade axes.')
    i.openTypeOS2VendorID = 'ORIN'
    i.openTypeHheaAscender = HHEA_ASC; i.openTypeHheaDescender = HHEA_DESC; i.openTypeHheaLineGap = 0
    i.openTypeOS2TypoAscender = HHEA_ASC; i.openTypeOS2TypoDescender = HHEA_DESC; i.openTypeOS2TypoLineGap = 0
    i.openTypeOS2WinAscent = win[0]; i.openTypeOS2WinDescent = win[1]
    i.openTypeOS2Selection = [7]                      # USE_TYPO_METRICS
    i.openTypeOS2Type = []                            # installable embedding
    i.openTypeOS2WeightClass = int(loc['wght'])
    i.openTypeOS2WidthClass = {75: 3, 100: 5, 125: 7}[int(loc['wdth'])]
    i.postscriptUnderlinePosition = -100
    i.postscriptUnderlineThickness = 60        # constant: one underline weight for the whole family
    i.openTypeOS2StrikeoutPosition = _r(P.xh * 0.5 + 10)
    i.openTypeOS2StrikeoutSize = 60
    i.openTypeOS2SubscriptXSize = 600; i.openTypeOS2SubscriptYSize = 600
    i.openTypeOS2SubscriptXOffset = 0; i.openTypeOS2SubscriptYOffset = 140
    i.openTypeOS2SuperscriptXSize = 600; i.openTypeOS2SuperscriptYSize = 600
    i.openTypeOS2SuperscriptXOffset = 0; i.openTypeOS2SuperscriptYOffset = 392
    i.openTypeOS2Panose = [2, 11, 5, 3, 3, 2, 2, 2, 2, 4]
    i.openTypeHeadCreated = '2026/11/16 00:00:00'
    order = ['.notdef', 'space'] + [n for n in glyphs if n not in ('.notdef', 'space')]
    cats = {}
    for name in order:
        g = glyphs[name]
        ug = f.newGlyph(name)
        ug.width = _r(g.w)
        ug.unicodes = sorted(rev.get(name, []))
        pen = ug.getPointPen()
        for c in g.contours:
            pen.beginPath()
            for s in c:
                if s[0] == 'l':
                    pen.addPoint((_r(s[1][0]), _r(s[1][1])), 'line')
                else:
                    pen.addPoint((_r(s[1][0]), _r(s[1][1])))
                    pen.addPoint((_r(s[2][0]), _r(s[2][1])))
                    pen.addPoint((_r(s[3][0]), _r(s[3][1])), 'curve')
            pen.endPath()
        for cn, dx, dy in g.components:
            pen.addComponent(cn, (1, 0, 0, 1, _r(dx), _r(dy)))
        for an, (ax, ay) in sorted(g.anchors.items()):
            ug.appendAnchor({'name': an, 'x': _r(ax), 'y': _r(ay)})
        if name in marks.MARKS:
            cats[name] = 'mark'
        elif name not in ('.notdef',):
            cats[name] = 'base'
    f.lib['public.glyphOrder'] = order
    f.lib['public.openTypeCategories'] = cats
    f.features.text = features_text
    if kerning:
        for k, v in kerning.items():
            f.kerning[k] = v
    if groups:
        for k, v in groups.items():
            f.groups[k] = v
    if os.path.exists(path):
        shutil.rmtree(path)
    f.save(path, overwrite=True)
    return glyphs


def make_designspace(ds_path, master_dir_rel='../masters'):
    doc = DesignSpaceDocument()
    labels = {
        'wght': [(100, 'Thin'), (200, 'ExtraLight'), (300, 'Light'), (400, 'Regular'), (500, 'Medium'),
                 (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold'), (900, 'Black')],
        # STAT labels are abbreviated so that family + style never exceeds 31 characters
        'wdth': [(75, 'Cond'), (100, 'Normal'), (125, 'Ext')],
        'opsz': [(10, 'Capt'), (14, 'Text'), (72, 'Disp')],
        'GRAD': [(-50, 'G-50'), (0, 'G0'), (100, 'G100')],
    }
    for tag, name, mn, df, mx in AXES:
        a = AxisDescriptor()
        a.tag = tag; a.name = name; a.minimum = mn; a.default = df; a.maximum = mx
        a.axisLabels = []
        for v, ln in labels[tag]:
            kw = dict(name=ln, userValue=v, elidable=(v == df))
            if tag == 'wght' and v == 400:
                kw['linkedUserValue'] = 700
            if tag == 'opsz':
                rng = {10: (10, 12), 14: (12, 28), 72: (28, 72)}[v]
                kw['userMinimum'], kw['userMaximum'] = rng
            a.axisLabels.append(AxisLabelDescriptor(**kw))
        doc.addAxis(a)
    name_of = {t: n for t, n, *_ in AXES}
    for loc in masters():
        s = SourceDescriptor()
        s.filename = '%s/Orion-%s.ufo' % (master_dir_rel, master_name(loc))
        s.name = 'Orion ' + master_name(loc)
        s.familyName = FAMILY; s.styleName = master_name(loc)
        s.location = {name_of[t]: loc[t] for t in loc}
        if loc == DEFAULT:
            s.copyLib = True; s.copyInfo = True; s.copyFeatures = True; s.copyGroups = True
        doc.addSource(s)
    for wd, wname in ((100, ''), (75, 'Condensed'), (125, 'Extended')):
        for w, n in NAMED_WEIGHTS:
            ins = InstanceDescriptor()
            style = (wname + ' ' + n).strip()
            ins.familyName = FAMILY; ins.styleName = style
            ins.name = 'Orion ' + style
            ins.postScriptFontName = 'Orion-' + style.replace(' ', '')
            ins.location = {'Weight': w, 'Width': wd, 'Optical Size': 14, 'Grade': 0}
            ins.filename = '../instances/Orion-%s.ufo' % style.replace(' ', '')
            doc.addInstance(ins)
    doc.write(ds_path)
    return doc


def write_sources(root, kern_fn=None, log=print):
    """Generate all master UFOs, the feature file and the designspace under root."""
    mdir = os.path.join(root, 'masters'); ddir = os.path.join(root, 'designspace'); fdir = os.path.join(root, 'features')
    for d in (mdir, ddir, fdir):
        os.makedirs(d, exist_ok=True)
    built = {}
    for loc in masters():
        built[master_name(loc)] = (loc, build_master(Params(**loc)))
    dn = master_name(DEFAULT)
    g0 = built[dn][1]
    fea = build_features(g0, cmap_for(g0))
    open(os.path.join(fdir, 'features.fea'), 'w').write(fea)
    # vertical extremes over all masters -> OS/2 win metrics
    from .glyphset import flat_bounds
    ymax, ymin = 0, 0
    for mn, (loc, gl) in built.items():
        for n in gl:
            b = flat_bounds(gl, n)
            if b:
                ymax = max(ymax, b[3]); ymin = min(ymin, b[1])
    win = (int(-(-ymax // 1)) + 2, int(-(ymin // 1)) + 2)
    kern = kern_fn(built) if kern_fn else {}
    for mn, (loc, gl) in built.items():
        k, grp = kern.get(mn, ({}, {}))
        write_master(loc, os.path.join(mdir, 'Orion-%s.ufo' % mn), fea, k, grp, glyphs=gl, win=win)
        log('  master', mn, len(gl), 'glyphs', len(k), 'kern pairs')
    make_designspace(os.path.join(ddir, 'Orion.designspace'))
    return dict(win=win, ymax=ymax, ymin=ymin, glyphs=len(g0), built=built)
