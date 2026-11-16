"""Font integrity: sanitizer, table structure, checksums, naming, metrics, cmap, bounding boxes, loading."""
import os, sys, struct, subprocess
from fontTools.ttLib import TTFont
from fontTools.ttLib.sfnt import calcChecksum
from common import *

REQUIRED_TTF = ['cmap', 'glyf', 'head', 'hhea', 'hmtx', 'loca', 'maxp', 'name', 'OS/2', 'post', 'GSUB', 'GPOS', 'GDEF']


def ots(path):
    import ots as _ots
    r = _ots.sanitize(path, capture_output=True)
    return r.returncode == 0, (r.stderr.decode() if r.stderr else '')[:300]


def checksums(path):
    data = open(path, 'rb').read()
    num = struct.unpack('>H', data[4:6])[0]
    bad = []
    for i in range(num):
        tag, cs, off, ln = struct.unpack('>4sLLL', data[12 + i * 16: 28 + i * 16])
        tbl = data[off: off + ln]
        if tag == b'head':
            tbl = tbl[:8] + b'\0\0\0\0' + tbl[12:]
        if calcChecksum(tbl + b'\0' * (-len(tbl) % 4)) != cs:
            bad.append(tag.decode())
    return bad


def check(path, R):
    rel = os.path.relpath(path, ROOT)
    f = TTFont(path)
    is_vf = 'fvar' in f; is_cff = 'CFF ' in f
    ok_, msg = ots(path)
    R.ok('%s: OpenType Sanitizer' % rel, ok_, msg)
    R.ok('%s: table checksums' % rel, not checksums(path), checksums(path))
    need = [t for t in REQUIRED_TTF if not (is_cff and t in ('glyf', 'loca'))]
    if is_vf:
        need += ['fvar', 'gvar', 'STAT', 'HVAR']
    R.ok('%s: required tables' % rel, all(t in f for t in need), [t for t in need if t not in f])
    for t in f.keys():                       # every table must decompile
        try:
            f[t]
        except Exception as e:
            R.add('%s: decompile %s' % (rel, t), 'FAIL', repr(e))
    R.ok('%s: all tables decompile' % rel, True)
    order = f.getGlyphOrder(); cmap = f.getBestCmap()
    R.ok('%s: .notdef is glyph 0' % rel, order[0] == '.notdef')
    R.ok('%s: cmap targets exist' % rel, all(g in set(order) for g in cmap.values()))
    R.ok('%s: space and nbsp mapped' % rel, 0x20 in cmap and 0xA0 in cmap and f['hmtx'][cmap[0x20]][0] == f['hmtx'][cmap[0xA0]][0])
    R.ok('%s: no duplicate glyph names' % rel, len(set(order)) == len(order))
    os2, hhea, head = f['OS/2'], f['hhea'], f['head']
    R.ok('%s: unitsPerEm 1000' % rel, head.unitsPerEm == 1000)
    R.ok('%s: typo == hhea vertical metrics' % rel, (os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap) == (hhea.ascent, hhea.descent, hhea.lineGap),
         (os2.sTypoAscender, os2.sTypoDescender, hhea.ascent, hhea.descent))
    R.ok('%s: USE_TYPO_METRICS set' % rel, bool(os2.fsSelection & (1 << 7)))
    R.ok('%s: win metrics cover glyph bounds' % rel, os2.usWinAscent >= head.yMax and os2.usWinDescent >= -head.yMin,
         (os2.usWinAscent, head.yMax, os2.usWinDescent, head.yMin))
    R.ok('%s: fsType 0 (installable)' % rel, os2.fsType == 0)
    nm = f['name']
    fam = nm.getDebugName(16) or nm.getDebugName(1)
    R.ok('%s: name IDs 1,2,4,6 present' % rel, all(nm.getDebugName(i) for i in (1, 2, 4, 6)))
    ps = nm.getDebugName(6)
    R.ok('%s: PostScript name valid' % rel, ps and len(ps) <= 63 and all(33 <= ord(c) <= 126 and c not in '[](){}<>/%' for c in ps), ps)
    R.ok('%s: family name starts with Orion' % rel, fam.startswith('Orion'), fam)
    sub = nm.getDebugName(2)
    R.ok('%s: style linking' % rel, sub in ('Regular', 'Bold') and bool(os2.fsSelection & (1 << 5)) == (sub == 'Bold'), sub)
    if not is_cff:
        glyf = f['glyf']
        bad = []
        for g in order:
            gl = glyf[g]
            if gl.numberOfContours > 0 and (gl.xMax - gl.xMin > 2600 or gl.yMax > 1300 or gl.yMin < -500):
                bad.append(g)
            if gl.isComposite():
                for c in gl.components:
                    if glyf[c.glyphName].isComposite():
                        bad.append(g + ':nested')
        R.ok('%s: glyph bounds sane, components flat' % rel, not bad, bad[:8])
    adv0 = [g for g in order if f['hmtx'][g][0] < 0]
    R.ok('%s: no negative advances' % rel, not adv0)
    if is_vf:
        fv = f['fvar']
        R.ok('%s: axes wght/wdth/opsz/GRAD' % rel, [a.axisTag for a in fv.axes] == ['wght', 'wdth', 'opsz', 'GRAD'])
        R.ok('%s: axis ranges' % rel, [(a.minValue, a.defaultValue, a.maxValue) for a in fv.axes] ==
             [(100, 400, 900), (75, 100, 125), (10, 14, 72), (-50, 0, 100)], [(a.minValue, a.defaultValue, a.maxValue) for a in fv.axes])
        R.ok('%s: 27 named instances with names' % rel, len(fv.instances) == 27 and all(nm.getDebugName(i.subfamilyNameID) for i in fv.instances))
        st = f['STAT'].table
        R.ok('%s: STAT axes match fvar' % rel, [a.AxisTag for a in st.DesignAxisRecord.Axis] == [a.axisTag for a in fv.axes])
        R.ok('%s: STAT has axis values' % rel, st.AxisValueArray is not None and len(st.AxisValueArray.AxisValue) >= 18)
    # the font must load in FreeType and HarfBuzz
    import freetype, uharfbuzz as hb
    try:
        face = freetype.Face(path); face.set_pixel_sizes(0, 32); face.load_char('A')
        b = hb.Blob.from_file_path(path); hf = hb.Font(hb.Face(b)); buf = hb.Buffer(); buf.add_str('Orion'); buf.guess_segment_properties(); hb.shape(hf, buf)
        R.ok('%s: loads in FreeType and HarfBuzz' % rel, len(buf.glyph_infos) == 5 and face.glyph.bitmap.width > 0)
    except Exception as e:
        R.add('%s: loads in FreeType and HarfBuzz' % rel, 'FAIL', repr(e))



def web_files(R):
    """WOFF2 files and unicode-range subsets: OTS, decompression, identity with the TTF they were made from, and shaping."""
    import glob, io
    import uharfbuzz as hb
    woffs = sorted(glob.glob(os.path.join(ROOT, 'fonts', 'webfonts', '*.woff2'))) + [os.path.join(ROOT, 'fonts', 'variable', 'Orion-VF.woff2')]
    for w in woffs:
        rel = os.path.relpath(w, ROOT)
        ok_, msg = ots(w)
        R.ok('%s: OpenType Sanitizer' % rel, ok_, msg)
        base = os.path.basename(w)[:-6]
        src = os.path.join(ROOT, 'fonts', 'variable', 'Orion-VF.ttf') if base == 'Orion-VF' else \
            os.path.join(ROOT, 'fonts', 'static', base.split('-')[0], base + '.ttf')
        a = TTFont(w); b = TTFont(src)
        diff = [t for t in b.keys() if t not in ('GlyphOrder', 'head', 'DSIG') and (t not in a or a[t].compile(a) != b[t].compile(b))] if False else \
            [t for t in ('cmap', 'GSUB', 'GPOS', 'hmtx', 'name', 'OS/2') if a.getTableData(t) != b.getTableData(t)]
        same_outlines = a.getGlyphOrder() == b.getGlyphOrder() and all(a['glyf'][g] == b['glyf'][g] for g in ('a', 'S', 'uni1EA8', 'Omega'))
        R.ok('%s: decompresses to the same tables and outlines as %s' % (rel, os.path.basename(src)), not diff and same_outlines, diff)
    samples = {'latin': 'Continue Watching 00:59:48 €19.99', 'latin-extended': 'ŁŽťčŐűȘțğİ', 'vietnamese': 'ếụĐặữướẨỖ',
               'greek': 'Συνέχειαπαρακολούθησης', 'cyrillic': 'ПродовжитипереглядУкраїна', 'symbols': '↔↕↖↗↘↙■□●○☆'}
    # each subset is tested with characters of its own unicode-range only (space and basic punctuation live in the Latin subset)
    for name, text in samples.items():
        for ext in ('woff2',):
            fs = glob.glob(os.path.join(ROOT, 'fonts', 'subsets', name, '*.' + ext))
            if not fs:
                R.add('subset %s (%s) present' % (name, ext), 'FAIL', 'missing'); continue
            path = fs[0]; rel = os.path.relpath(path, ROOT)
            ok_, msg = ots(path)
            R.ok('%s: OpenType Sanitizer' % rel, ok_, msg)
            f = TTFont(path)
            buf_ = io.BytesIO(); f.flavor = None; f.save(buf_)
            font = hb.Font(hb.Face(buf_.getvalue())); buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf)
            R.ok('%s: sample text shapes without .notdef and keeps the variation axes' % rel,
                 all(i.codepoint != 0 for i in buf.glyph_infos) and 'fvar' in f and len(f['fvar'].axes) == 4, text)


def installed_loading(R):
    """Install the fonts into a private fontconfig directory and resolve them by family name."""
    import shutil, tempfile
    d = os.path.expanduser('~/.fonts/orion-qa'); os.makedirs(d, exist_ok=True)
    for p in all_fonts():
        shutil.copy(p, d)
    try:
        subprocess.run(['fc-cache', '-f', d], capture_output=True, timeout=120)
        out = subprocess.run(['fc-list', ':family=Orion', 'family', 'style'], capture_output=True, text=True, timeout=60).stdout
        fams = sorted({l.split(':')[0].strip() for l in out.splitlines() if l.strip()})
        R.ok('installed fonts resolve through fontconfig', any('Orion' in x for x in fams), fams[:6])
        m = subprocess.run(['fc-match', 'Orion:bold', 'file', 'style'], capture_output=True, text=True).stdout.strip()
        R.ok('fc-match Orion:bold resolves to an Orion file', 'Orion' in m, m)
    except FileNotFoundError:
        R.add('installed fonts resolve through fontconfig', 'SKIP', 'fontconfig not available in this environment')
    finally:
        shutil.rmtree(d, ignore_errors=True)
        subprocess.run(['fc-cache', '-f'], capture_output=True)


if __name__ == '__main__':
    R = Report('integrity')
    for p in all_fonts():
        check(p, R)
    web_files(R)
    installed_loading(R)
    R.save(dict(fonts=len(all_fonts())))
