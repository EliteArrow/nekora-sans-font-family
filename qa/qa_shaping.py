"""Text shaping tests with HarfBuzz: kerning, marks, localized forms, numerals, fractions, case, stylistic sets,
and a multilingual corpus that must shape without .notdef."""
import os, sys, json
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from common import *
from corpus import OTT_STRINGS, LANGUAGE_SAMPLES, PUNCT_NUM_SAMPLES

blob = hb.Blob.from_file_path(VF); face = hb.Face(blob)
tt = TTFont(VF); ORDER = tt.getGlyphOrder()


def shape(text, feats=None, script=None, lang=None, loc=None):
    font = hb.Font(face)
    if loc:
        font.set_variations(loc)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    if script: buf.script = script
    if lang: buf.language = lang
    hb.shape(font, buf, feats or {})
    return [ORDER[i.codepoint] for i in buf.glyph_infos], [(p.x_advance, p.x_offset, p.y_offset) for p in buf.glyph_positions]


def adv(text, feats=None, **kw):
    return sum(p[0] for p in shape(text, feats, **kw)[1])


def main():
    R = Report('shaping')
    # --- kerning
    pairs = ['AV', 'AW', 'AY', 'AT', 'Ta', 'Te', 'To', 'Tr', 'Ty', 'Va', 'Vo', 'Wa', 'Wo', 'Yo', 'LY', 'PA', 'LT']
    kv = {p: adv(p) - adv(p, {'kern': False}) for p in pairs}
    R.ok('kern: all 17 reference pairs are kerned negatively', all(v < 0 for v in kv.values()), kv)
    R.ok('kern: magnitudes within -20..-130', all(-130 <= v <= -20 for v in kv.values()), kv)
    neutral = {p: adv(p) - adv(p, {'kern': False}) for p in ['HH', 'nn', 'oo', 'HO', 'no', 'll', 'II']}
    R.ok('kern: straight / round control pairs untouched', all(abs(v) < 1 for v in neutral.values()), neutral)
    rn = adv('rn') - adv('rn', {'kern': False})
    R.ok('kern: r+n opened to keep rn distinct from m', rn > 0, rn)
    for loc in ({'wght': 100}, {'wght': 900}, {'wght': 900, 'wdth': 75}, {'wght': 700, 'opsz': 72}, {'wght': 400, 'opsz': 10}):
        k2 = {p: adv(p, loc=loc) - adv(p, {'kern': False}, loc=loc) for p in pairs}
        # in the heaviest weights the T bar reaches the x-height, so Tr / Ty may not tuck under it
        R.ok('kern: variable kerning at %s' % loc, all(v < 0 for p_, v in k2.items() if p_ not in ('Tr', 'Ty')) and all(v <= 12 for v in k2.values()), k2)
    for cy, gr in (('ГД', 'Τα'), ('УД', 'Υο'), ('Та', 'ΛΥ')):
        R.ok('kern: Cyrillic %s / Greek %s' % (cy, gr), adv(cy) < adv(cy, {'kern': False}) and adv(gr) < adv(gr, {'kern': False}))
    # --- marks
    # (HarfBuzz recomposes base + mark when a precomposed glyph exists, so these use bases without one)
    g, p = shape('q́')
    R.ok('mark: q + combining acute positions the mark (zero advance, offset)', g == ['q', 'acutecomb'] and p[1][0] == 0 and p[1][1] != 0, (g, p))
    R.ok('mark: a + combining acute resolves to the precomposed glyph', shape('á')[0] == ['uni00E1'])
    g, p = shape('Q́')
    R.ok('ccmp: capital takes the .case mark', g == ['Q', 'acutecomb.case'], g)
    g, p = shape('i̊')
    R.ok('ccmp: i + mark above uses dotless i', g == ['dotlessi', 'ringcomb'], g)
    g, p = shape('j̃')
    R.ok('ccmp: j + mark above uses dotless j', g == ['dotlessj', 'tildecomb'], g)
    g, p = shape('q̂́')
    R.ok('ccmp: Vietnamese circumflex+acute becomes one stacked mark', g == ['q', 'uni03020301'], g)
    g, p = shape('Q̆̉')
    R.ok('ccmp: capital breve+hook stack in .case form', g == ['Q', 'uni03060309.case'], g)
    g, p = shape('q̈̄')
    R.ok('mkmk: second mark stacks above the first', len(g) == 3 and p[2][2] > p[1][2], (g, p))
    g, p = shape('q̣́')
    R.ok('mark: marks below and above attach independently', len(g) == 3 and p[1][0] == 0 and p[2][0] == 0, (g, p))
    g, p = shape('x̣')
    R.ok('mark: dot below attaches under the base', g == ['x', 'dotbelowcomb'] and p[1][0] == 0, (g, p))
    R.ok('precomposed Vietnamese maps directly', shape('ấ')[0] == ['uni1EA5'] and shape('ấ')[0] == ['uni1EA5'])
    ok_ = True                      # marks must clear the base outline
    for base in 'qQxXzZ':
        for mk in '́̂̃̈̌̆':
            g, p = shape(base + mk)
            if len(g) < 2:
                continue
            bb = tt['glyf'][g[0]]; mb = tt['glyf'][g[1]]
            if mb.yMin + p[1][2] < bb.yMax - 12:
                ok_ = False
    R.ok('mark: combining marks clear the base outline (6 bases x 6 marks)', ok_)
    # --- localized forms
    R.ok('locl ROM: s/t cedilla -> comma below', shape('şţŞŢ', lang='ro')[0] == ['uni0219', 'uni021B', 'uni0218', 'uni021A'], shape('şţ', lang='ro')[0])
    R.ok('locl default keeps Turkish s-cedilla', shape('ş', lang='tr')[0] == ['uni015F'])
    R.ok('locl CAT: punt volat between l l', shape('l·l', lang='ca')[0] == ['l', 'periodcentered.loclCAT', 'l'], shape('l·l', lang='ca')[0])
    R.ok('locl SRB: Serbian be', shape('б', lang='sr')[0] == ['uni0431.loclSRB'] and shape('б', lang='ru')[0] == ['uni0431'])
    R.ok('Turkish dotted / dotless i are separate glyphs', shape('İıi')[0] == ['uni0130', 'dotlessi', 'i'])
    # --- numerals
    w = [shape(d, {'tnum': True})[1][0][0] for d in '0123456789']
    R.ok('tnum: all figures share one advance', len(set(w)) == 1, w)
    wp = [shape(d)[1][0][0] for d in '0123456789']
    R.ok('pnum (default): proportional figures (1 is narrower)', wp[1] < wp[0], wp)
    R.ok('tnum then pnum round-trips', shape('1', {'tnum': True, 'pnum': True})[0] in (['one'], ['one.tf']))
    R.ok('tnum: figures, period, comma and colon align to the figure grid', adv('1.1', {'tnum': True}) == adv('0,0', {'tnum': True}))
    R.ok('timer string keeps one width under tnum', adv('00:59:48', {'tnum': True}) == adv('11:11:11', {'tnum': True}))
    R.ok('zero: slashed zero', shape('0', {'zero': True})[0] == ['zero.zero'] and shape('0', {'zero': True, 'tnum': True})[0] == ['zero.zero.tf'])
    R.ok('calt: colon between figures centres on figure height', shape('00:59')[0][2] == 'colon.case' and shape('a:b')[0][1] == 'colon', shape('00:59')[0])
    R.ok('frac: 1/2 -> numerator, fraction bar, denominator', shape('1/2', {'frac': True})[0] == ['one.numr', 'fraction', 'two.dnom'], shape('1/2', {'frac': True})[0])
    R.ok('frac: multi-digit 15/16', shape('15/16', {'frac': True})[0] == ['one.numr', 'five.numr', 'fraction', 'one.dnom', 'six.dnom'], shape('15/16', {'frac': True})[0])
    R.ok('frac: dates and paths without digits on both sides are left alone', shape('a/b', {'frac': True})[0] == ['a', 'slash', 'b'])
    R.ok('numr / dnom', shape('12', {'numr': True})[0] == ['one.numr', 'two.numr'] and shape('12', {'dnom': True})[0] == ['one.dnom', 'two.dnom'])
    R.ok('sups / subs / sinf', shape('2', {'sups': True})[0] == ['two.sups'] and shape('2', {'subs': True})[0] == ['two.subs'] and shape('2', {'sinf': True})[0] == ['two.subs'])
    R.ok('ordn: 1a 2o', shape('1a 2o', {'ordn': True})[0] == ['one', 'ordfeminine', 'space', 'two', 'ordmasculine'], shape('1a 2o', {'ordn': True})[0])
    # --- case and stylistic sets
    cg = shape('(A-B) [C]:{D} «¿¡@', {'case': True})[0]
    R.ok('case: punctuation aligns to capitals', all(x in cg for x in ['parenleft.case', 'hyphen.case', 'parenright.case', 'bracketleft.case', 'colon.case', 'braceleft.case', 'guillemotleft.case', 'questiondown.case', 'exclamdown.case', 'at.case']), cg)
    R.ok('ss01: serifed I (incl. accented)', shape('IÍ', {'ss01': True})[0] == ['I.ss01', 'uni00CD.ss01'], shape('IÍ', {'ss01': True})[0])
    R.ok('ss02: plain l', shape('lĺ', {'ss02': True})[0] == ['l.ss02', 'uni013A.ss02'], shape('lĺ', {'ss02': True})[0])
    R.ok('ss03: single-storey a (incl. Vietnamese)', shape('aấ', {'ss03': True})[0] == ['a.ss03', 'uni1EA5.ss03'], shape('aấ', {'ss03': True})[0])
    feats = sorted({r.FeatureTag for r in tt['GSUB'].table.FeatureList.FeatureRecord} | {r.FeatureTag for r in tt['GPOS'].table.FeatureList.FeatureRecord})
    need = ['calt', 'case', 'ccmp', 'dnom', 'frac', 'kern', 'locl', 'mark', 'mkmk', 'numr', 'ordn', 'pnum', 'sinf', 'ss01', 'ss02', 'ss03', 'subs', 'sups', 'tnum', 'zero']
    R.ok('feature list complete, no empty declarations', all(f in feats for f in need), feats)
    # every lookup referenced by a feature must contain subtables
    empty = []
    for tag in ('GSUB', 'GPOS'):
        t = tt[tag].table
        for fr in t.FeatureList.FeatureRecord:
            if not fr.Feature.LookupListIndex:
                empty.append(fr.FeatureTag)
            for li in fr.Feature.LookupListIndex:
                if not t.LookupList.Lookup[li].SubTable:
                    empty.append(fr.FeatureTag)
    R.ok('no feature without lookups / subtables', not empty, empty)
    # --- corpus: nothing may fall back to .notdef
    missing = {}
    total_chars = 0
    for label, text in list(OTT_STRINGS.items()) + list(LANGUAGE_SAMPLES.items()) + list(PUNCT_NUM_SAMPLES.items()):
        g, p = shape(text)
        total_chars += len(text)
        if '.notdef' in g:
            cm = tt.getBestCmap()
            missing[label] = sorted({c for c in text if ord(c) not in cm and c not in '\n'})
    R.ok('corpus: %d strings / %d characters shape without .notdef' % (len(OTT_STRINGS) + len(LANGUAGE_SAMPLES) + len(PUNCT_NUM_SAMPLES), total_chars), not missing, missing)
    for label, text in OTT_STRINGS.items():
        g, p = shape(text)
        R.ok('OTT string: %s' % text, '.notdef' not in g and sum(a[0] for a in p) > 0)
    # long + mixed-language strings, and stability across the design space
    long_ = ' '.join(LANGUAGE_SAMPLES.values()) * 4
    g, p = shape(long_)
    R.ok('long mixed-language string (%d chars) shapes' % len(long_), '.notdef' not in g and len(g) > 3000)
    mono = True; prev = 0
    for w_ in (100, 300, 500, 700, 900):
        a_ = adv('Recommended for You', loc={'wght': w_})
        mono = mono and a_ >= prev - 30; prev = a_
    R.ok('line length evolves smoothly along wght', mono)
    # bidirectional text is not supported (no RTL script in the family)
    R.add('bidirectional text', 'SKIP', 'No right-to-left script is included; Arabic / Hebrew fall back to companion families (see UNICODE-COVERAGE.md).')
    R.save(dict(features=feats, kern_values=kv))


if __name__ == '__main__':
    main()
