# -*- coding: utf-8 -*-
"""Glyph sheets: complete character set, numerals / symbols / punctuation, OpenType features."""
import os, unicodedata
from fontTools.ttLib import TTFont
from common import *

BLOCKS = [
    ('Basic Latin', 0x20, 0x7E), ('Latin-1 Supplement', 0xA0, 0xFF), ('Latin Extended-A', 0x100, 0x17F),
    ('Latin Extended-B (selected)', 0x180, 0x24F), ('IPA / Modifier letters / Spacing accents', 0x250, 0x2FF),
    ('Combining diacritical marks', 0x300, 0x36F), ('Greek (monotonic)', 0x370, 0x3FF), ('Cyrillic', 0x400, 0x4FF),
    ('Latin Extended Additional (Welsh, Vietnamese …)', 0x1E00, 0x1EFF), ('General punctuation', 0x2000, 0x206F),
    ('Superscripts and subscripts', 0x2070, 0x209F), ('Currency symbols', 0x20A0, 0x20CF), ('Letterlike symbols', 0x2100, 0x214F),
    ('Number forms', 0x2150, 0x218F), ('Arrows', 0x2190, 0x21FF), ('Mathematical operators', 0x2200, 0x22FF),
    ('Technical, control pictures', 0x2300, 0x243F), ('Geometric shapes, symbols, dingbats', 0x25A0, 0x27BF),
]


def charset_page():
    tt = TTFont(os.path.join(ROOT, 'fonts', 'variable', 'Orion-VF.ttf'))
    cps = sorted(tt.getBestCmap())
    n_glyphs = tt['maxp'].numGlyphs
    secs = []
    used = set()
    for name, lo, hi in BLOCKS:
        cs = [c for c in cps if lo <= c <= hi and unicodedata.category(chr(c)) not in ('Zs', 'Cf', 'Cc')]
        used.update(c for c in cps if lo <= c <= hi)
        if not cs:
            continue
        cells = ''.join("<div class='c'><span>%s</span></div>" % (('&#x25CC;&#x%X;' % c) if unicodedata.category(chr(c)) == 'Mn' else '&#x%X;' % c) for c in cs)
        secs.append("<section><div class='tag'>%s <b>%d</b></div><div class='grid'>%s</div></section>" % (esc(name), len(cs), cells))
    rest = [c for c in cps if c not in used and unicodedata.category(chr(c)) not in ('Zs', 'Cf', 'Cc')]
    if rest:
        cells = ''.join("<div class='c'><span>&#x%X;</span></div>" % c for c in rest)
        secs.append("<section><div class='tag'>Other <b>%d</b></div><div class='grid'>%s</div></section>" % (len(rest), cells))
    css = """
    body { padding: 80px 96px 110px; }
    h1 { font-size: 88px; line-height: 96px; letter-spacing: -0.02em; %s; }
    .sub { font-size: 24px; line-height: 34px; margin: 14px 0 46px; color: #4A4F5A; %s; max-width: 1300px; }
    section { margin-bottom: 34px; }
    .tag b { color: #14161A; margin-left: 10px; font-weight: normal; }
    .grid { display: grid; grid-template-columns: repeat(32, 54px); margin-top: 12px; border-top: 1px solid #D9DCE1; border-left: 1px solid #D9DCE1; width: max-content; }
    .c { width: 54px; height: 62px; border-right: 1px solid #D9DCE1; border-bottom: 1px solid #D9DCE1; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .c span { font-size: 30px; line-height: 1; %s; }
    """ % (fv(700, 100, 72), fv(400, 100, 22), fv(400, 100, 28))
    body = ("<h1>Orion — character set</h1><div class='sub'>%d encoded characters, %d glyphs. Regular, optical size 28. "
            "Rendered from fonts/variable/Orion-VF.woff2 by Chromium.</div>%s" % (len(cps), n_glyphs, ''.join(secs)))
    return page('Character set', body, css, 'light', 1920, 0)


def numerals_page():
    rows = [
        ('Proportional figures (default)', "0123456789", ''),
        ('Tabular figures — tnum', "0123456789", "font-feature-settings:'tnum' 1"),
        ('Slashed zero — zero', "0O 100 2000 B80", "font-feature-settings:'zero' 1"),
        ('Tabular clock, colon centred on figures — tnum + calt', "00:59:48  23:11:07  1:41:11", "font-feature-settings:'tnum' 1"),
        ('Fractions — precomposed and frac', "½ ⅓ ⅔ ¼ ¾ ⅛ ⅜ ⅝ ⅞  <span style=\"font-feature-settings:'frac' 1\">1/2 3/4 5/8 15/16 2 1/3</span>", ''),
        ('Superiors, inferiors, ordinals — sups, subs, ordn', "x<span style=\"font-feature-settings:'sups' 1\">2</span> H<span style=\"font-feature-settings:'subs' 1\">2</span>O CO<span style=\"font-feature-settings:'subs' 1\">2</span> ¹²³⁴⁵⁶⁷⁸⁹⁰ ₀₁₂₃₄₅₆₇₈₉ 1ª 2º <span style=\"font-feature-settings:'ordn' 1\">1a 2o</span> №5", ''),
        ('Currency', "$ ¢ £ ¥ € ₹ ₽ ₩ ₺ ₴ ₦ ₫ ₪ ₱ ₸ ₿ ƒ ¤ ₼   ₹1,499  €19.99  R$ 39,90  £7.99  ¥980", ''),
        ('Mathematical', "+ − × ÷ = ≠ &lt; &gt; ≤ ≥ ± ≈ ~ ^ ¬ ∞ √ ∑ ∏ ∫ ∂ ∆ ◊ µ π Ω %  ‰ ° ′ ″", ''),
        ('Punctuation', "“Quote” ‘single’ „low“ «guillemets» ‹single› — – - _ … · • ¡¿ !? ( ) [ ] { } / \\ | ¦ * † ‡ § ¶ @ &amp; #", ''),
        ('Case-sensitive punctuation — case', "(H-O) [A–Z] {X} «Ñ» ¿QUÉ? ¡YA! A·B @ORION  →  <span style=\"font-feature-settings:'case' 1\">(H-O) [A–Z] {X} «Ñ» ¿QUÉ? ¡YA! A·B @ORION</span>", ''),
        ('Arrows and navigation', "← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↵ ↩ ↪ ⇤ ⇥ ⇧ ⌫ ␣", ''),
        ('Interface symbols', "▲ ▼ ◀ ▶ ▴ ▾ ◂ ▸ ● ○ ■ □ ◆ ★ ☆ ✓ ✕ © ® ™ ℗", ''),
        ('Confusable pairs', "Il1|  O0o  S5  B8  69  rn m  cl d  vv w  c e  <span style=\"font-feature-settings:'ss01' 1,'ss02' 1\">Il1 (ss01 + ss02)</span>", ''),
    ]
    css = """
    body { padding: 72px 96px 90px; }
    h1 { font-size: 72px; line-height: 80px; letter-spacing: -0.015em; %s; margin-bottom: 36px; }
    .r { display: grid; grid-template-columns: 420px 1fr; align-items: baseline; border-top: 1px solid #262B36; padding: 17px 0 15px; }
    .r .tag { font-size: 14px; line-height: 20px; padding-right: 24px; }
    .r .s { font-size: 46px; line-height: 58px; %s; white-space: pre-wrap; }
    """ % (fv(700, 100, 72), fv(500, 100, 44))
    body = "<h1>Numerals, symbols, punctuation</h1>" + ''.join(
        "<div class='r'><div class='tag'>%s</div><div class='s' style=\"%s\">%s</div></div>" % (esc(t), st, s) for t, s, st in rows)
    return page('Numerals, symbols and punctuation', body, css, '', 1920, 0)


def features_page():
    F = [
        ('kern', 'Kerning', 'AVATAR Tokyo LT. Wave', "font-kerning:none", "font-kerning:normal"),
        ('tnum', 'Tabular figures', '1:11:11 / 2:08:40', '', "font-feature-settings:'tnum' 1"),
        ('zero', 'Slashed zero', 'B0O8 · ID 4O07-0Q', '', "font-feature-settings:'zero' 1"),
        ('case', 'Capital forms', '¿SEASON 2—EPISODE (8)?', '', "font-feature-settings:'case' 1"),
        ('frac', 'Fractions', '1/2 3/4 7/8 15/16', '', "font-feature-settings:'frac' 1"),
        ('sups / subs', 'Superiors and inferiors', 'Dolby1 H2O m2', '', "font-feature-settings:'sups' 1"),
        ('ordn', 'Ordinals', '1a 2o temporada', '', "font-feature-settings:'ordn' 1"),
        ('ss01', 'Serifed capital I', 'Illinois IMAX II', '', "font-feature-settings:'ss01' 1"),
        ('ss02', 'Plain l without tail', 'All hello million', '', "font-feature-settings:'ss02' 1"),
        ('ss03', 'Single-storey a', 'Saga drama anthology', '', "font-feature-settings:'ss03' 1"),
        ('locl', 'Romanian, Catalan, Serbian', "<span lang='ro'>Ştiinţă</span> <span lang='ca'>col·lecció</span> <span lang='sr'>бб</span>", 'LANGNONE', ''),
        ('ccmp / mark / mkmk', 'Combining marks', 'é ấ ớ Ǻ ǖ x̂', "font-feature-settings:'mark' 0,'mkmk' 0,'ccmp' 0", ''),
    ]
    css = """
    body { padding: 72px 96px 90px; }
    h1 { font-size: 72px; line-height: 80px; letter-spacing: -0.015em; %s; margin-bottom: 14px; }
    .sub { font-size: 22px; line-height: 32px; color: #4A4F5A; margin-bottom: 34px; %s }
    .h, .r { display: grid; grid-template-columns: 330px 1fr 1fr; column-gap: 40px; align-items: baseline; }
    .h { padding-bottom: 10px; }
    .r { border-top: 1px solid #D9DCE1; padding: 16px 0 14px; }
    .r b { font-size: 26px; %s; display: block; }
    .r .s { font-size: 44px; line-height: 56px; %s; white-space: nowrap; }
    .r .off { color: #8A8F99; }
    """ % (fv(700, 100, 72), fv(400, 100, 22), fv(600, 100, 26), fv(500, 100, 44))
    rows = ["<div class='h'><div class='tag'>Feature</div><div class='tag'>Off</div><div class='tag'>On</div></div>"]
    for tag, name, s, off, on in F:
        s_off = s
        if off == 'LANGNONE':
            import re
            s_off = re.sub(r" lang='[a-z]+'", '', s); off = ''
        if tag.startswith('sups'):
            s_off = 'Dolby1 H2O m2'
            s = "Dolby<span style=\"font-feature-settings:'sups' 1\">1</span> H<span style=\"font-feature-settings:'subs' 1\">2</span>O m<span style=\"font-feature-settings:'sups' 1\">2</span>"; on = ''
        rows.append("<div class='r'><div><b>%s</b><span class='note'>%s</span></div><div class='s off' style=\"%s\">%s</div><div class='s' style=\"%s\">%s</div></div>"
                    % (tag, esc(name), off, s_off, on, s))
    body = "<h1>OpenType features</h1><div class='sub'>Every feature below is compiled into the font and exercised by qa/qa_shaping.py. There are no empty features.</div>" + ''.join(rows)
    return page('OpenType features', body, css, 'light', 1920, 0)


PAGES = [('glyph-sheets/character-set', charset_page, 1), ('glyph-sheets/numerals-symbols-punctuation', numerals_page, 1),
         ('glyph-sheets/opentype-features', features_page, 1)]
