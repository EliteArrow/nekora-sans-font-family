# -*- coding: utf-8 -*-
"""Variable-axis specimens: weight, width, optical size, grade, combined; plus type scale, kerning and multilingual."""
import json, os, sys
from common import *
sys.path.insert(0, os.path.join(ROOT, 'qa'))
from corpus import LANGUAGE_SAMPLES
T = json.load(open(os.path.join(ROOT, 'integration', 'tokens', 'orion-type-presets.json')))
WEIGHTS = [(100, 'Thin'), (200, 'ExtraLight'), (300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold'), (900, 'Black')]
HEAD = "h1 { font-size: 72px; line-height: 80px; letter-spacing: -0.015em; %s; } .sub { font-size: 22px; line-height: 32px; margin: 12px 0 30px; color: #8E95A3; max-width: 1400px; %s } .light .sub { color: #4A4F5A; }" % (fv(700, 100, 72), fv(400, 100, 22))


def weight_page():
    css = HEAD + """
    body { padding: 64px 96px 0; }
    .r { display: grid; grid-template-columns: 250px 1fr; align-items: baseline; border-top: 1px solid #262B36; padding: 9px 0 5px; }
    .r .s { font-size: 74px; line-height: 86px; white-space: nowrap; }
    """
    rows = ''.join("<div class='r'><div class='tag'>%d %s</div><div class='s' style=\"%s\">Continue Watching · Top 10 &amp; New 2024</div></div>" % (w, n, fv(w, 100, 72)) for w, n in WEIGHTS)
    body = "<h1>Weight — wght 100…900</h1><div class='sub'>Nine named instances on one continuous axis. Shown at optical size 72.</div>" + rows
    return page('Weight axis', body, css)


def width_page():
    css = HEAD + """
    body { padding: 64px 96px 0; }
    .r { display: grid; grid-template-columns: 250px 1fr; align-items: baseline; border-top: 1px solid #D9DCE1; padding: 10px 0 6px; }
    .r .s { font-size: 62px; line-height: 74px; white-space: nowrap; }
    .g { margin-bottom: 20px; }
    """
    out = []
    for w, n in ((300, 'Light'), (500, 'Medium'), (800, 'ExtraBold')):
        rows = ''.join("<div class='r'><div class='tag'>%s · wdth %d</div><div class='s' style=\"%s\">Recommended for You — Season 01</div></div>" % (n, wd, fv(w, wd, 60)) for wd in (75, 87.5, 100, 112.5, 125))
        out.append("<div class='g'>%s</div>" % rows)
    body = "<h1>Width — wdth 75…125</h1><div class='sub'>Condensed for dense rails and long localized titles, Extended for display. Counters, stems and spacing are redrawn per width, not scaled.</div>" + ''.join(out)
    return page('Width axis', body, css, 'light', 1920, 0)


def opsz_page():
    css = HEAD + """
    body { padding: 64px 96px 80px; }
    .cols { display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 36px; margin-bottom: 30px; }
    .big { font-size: 190px; line-height: 200px; white-space: nowrap; overflow: hidden; }
    .cap { border-top: 1px solid #262B36; padding-top: 10px; margin-bottom: 4px; }
    .real { display: grid; grid-template-columns: 250px 1fr 1fr; column-gap: 40px; align-items: baseline; border-top: 1px solid #262B36; padding: 14px 0 12px; }
    .real .s { white-space: nowrap; overflow: hidden; }
    """
    big = ''.join("<div><div class='cap tag'>opsz %d</div><div class='big' style=\"%s\">Rage</div></div>" % (o, fv(500, 100, o)) for o in (10, 14, 36, 72))
    real = ["<div class='real'><div class='tag'>Rendered size</div><div class='tag'>opsz fixed at 72 (display master)</div><div class='tag'>opsz = size (intended)</div></div>"]
    for px in (14, 18, 24, 36, 72):
        txt = 'Search Movies, Shows &amp; More — 2h 35m remaining'
        if px == 72: txt = 'Search &amp; More'
        real.append("<div class='real'><div class='tag'>%d px</div><div class='s' style=\"font-size:%dpx;line-height:1.3;%s\">%s</div><div class='s' style=\"font-size:%dpx;line-height:1.3;%s\">%s</div></div>"
                    % (px, px, fv(400, 100, 72), txt, px, fv(400, 100, px), txt))
    body = ("<h1>Optical size — opsz 10…72</h1><div class='sub'>Same word at the same scale: small optical sizes are wider, looser, lower in contrast and more open; "
            "display sizes tighten and sharpen. Below, the display master is misused at small sizes next to the intended setting.</div>"
            "<div class='cols'>%s</div>%s" % (big, ''.join(real)))
    return page('Optical size axis', body, css, '', 1920, 0)


def grade_page():
    css = HEAD + """
    body { padding: 64px 96px 80px; }
    .r { display: grid; grid-template-columns: 250px 1fr; align-items: baseline; border-top: 1px solid #262B36; padding: 12px 0 8px; }
    .r .s { font-size: 60px; line-height: 72px; white-space: nowrap; }
    .box { display: inline-block; outline: 1px solid #4DA3FF; outline-offset: 0; }
    .ov { position: relative; height: 150px; margin-top: 6px; }
    .ov div { position: absolute; left: 0; top: 0; font-size: 120px; line-height: 150px; white-space: nowrap; mix-blend-mode: screen; }
    .menu { display: flex; gap: 48px; margin-top: 8px; }
    .menu span { font-size: 36px; line-height: 64px; padding: 0 28px; border-radius: 10px; }
    .menu .f { background: #F2F2F2; color: #0B0D12; }
    """
    rows = ''.join("<div class='r'><div class='tag'>GRAD %d</div><div class='s'><span class='box' style=\"%s\">Play from Beginning · 00:59:48 · Łódź Đặng</span></div></div>" % (g, fv(500, 100, 60, g)) for g in (-50, 0, 50, 100))
    ov = "<div class='ov'><div style=\"%s;color:#FF4D5E\">Subtitles &amp; Audio</div><div style=\"%s;color:#35D0C0\">Subtitles &amp; Audio</div></div>" % (fv(500, 100, 72, -50), fv(500, 100, 72, 100))
    menu = ("<div class='menu' style=\"%s\"><span>Home</span><span>Series</span><span class='f' style=\"%s\">Movies</span><span>Live</span><span>My List</span></div>"
            "<div class='menu' style=\"%s\"><span>Home</span><span>Series</span><span class='f' style=\"%s\">Movies</span><span>Live</span><span>My List</span></div>"
            % (fv(500, 100, 36, 0), fv(500, 100, 36, 80), fv(500, 100, 36, 0), fv(700, 100, 36, 0)))
    body = ("<h1>Grade — GRAD −50…+100</h1><div class='sub'>Grade changes stroke weight without changing a single advance width or kerning value: the blue boxes are the text boxes and are identical in every row. "
            "Use it for focus states, for text over bright video, and to thin light-on-dark text on OLED.</div>%s"
            "<div class='tag' style='margin-top:26px'>GRAD −50 (red) over GRAD +100 (teal): same skeleton, same widths</div>%s"
            "<div class='tag' style='margin-top:18px'>Focus by grade (+80): neighbours do not move  ·  below: focus by weight (700): the row reflows</div>%s" % (rows, ov, menu))
    return page('Grade axis', body, css, '', 1920, 0)


def combined_page():
    css = HEAD + """
    body { padding: 64px 96px 80px; }
    table { border-collapse: collapse; width: 100%; }
    td, th { border-top: 1px solid #D9DCE1; padding: 8px 14px 4px 0; text-align: left; vertical-align: baseline; }
    td { font-size: 58px; line-height: 70px; white-space: nowrap; }
    .x td { font-size: 40px; line-height: 54px; }
    """
    head = "<tr><th class='tag'>wght \\ wdth</th>" + ''.join("<th class='tag'>%d</th>" % wd for wd in (75, 100, 125)) + "</tr>"
    rows = ''.join("<tr><th class='tag'>%d</th>%s</tr>" % (w, ''.join("<td style=\"%s\">Orion 4K</td>" % fv(w, wd, 58) for wd in (75, 100, 125))) for w in (100, 300, 500, 700, 900))
    ex = [('Black Condensed Display, GRAD +100 (designspace corner)', fv(900, 75, 72, 100), 'KINGDOM OF DUST — SEASON 3'),
          ('Thin Extended Display, GRAD −50 (designspace corner)', fv(100, 125, 72, -50), 'Quiet Orbit · a limited series'),
          ('Thin Condensed Caption, GRAD −50 (designspace corner)', fv(100, 75, 10, -50), 'Recommended for You · 2h 35m remaining'),
          ('Black Extended Caption, GRAD +100 (designspace corner)', fv(900, 125, 10, 100), 'NEW & POPULAR 2024'),
          ('Arbitrary interior point: wght 560, wdth 91, opsz 31, GRAD 22', fv(560, 91, 31, 22), 'Because you watched The Last Meridian'),
          ('Arbitrary interior point: wght 345, wdth 118, opsz 19, GRAD −30', fv(345, 118, 19, -30), 'Search Movies, Shows & More')]
    exr = ''.join("<tr class='x'><th class='tag' style='width:520px'>%s</th><td style=\"%s\">%s</td></tr>" % (esc(n), st, esc(s)) for n, st, s in ex)
    body = ("<h1>Combined axes</h1><div class='sub'>Weight × width at optical size 58, then corners and interior points of the four-axis designspace. "
            "All 16 corners and 75 further locations are checked for outline topology in qa/qa_interpolation.py.</div>"
            "<table>%s%s</table><table style='margin-top:36px'>%s</table>" % (head, rows, exr))
    return page('Combined axes', body, css, 'light', 1920, 0)


def scale_page(plat, cls=''):
    P = T[plat]
    css = HEAD + """
    body { padding: 64px 96px 90px; }
    .r { display: grid; grid-template-columns: 420px 1fr; column-gap: 30px; align-items: center; border-top: 1px solid %s; padding: 12px 0; }
    .r b { display: block; font-size: 22px; line-height: 28px; %s }
    .r .s { white-space: nowrap; overflow: hidden; }
    """ % ('#D9DCE1' if cls else '#262B36', fv(600, 100, 22))
    samples = {'displayXL': 'The Last Meridian', 'displayL': 'Kingdom of Dust', 'headlineL': 'New & Popular', 'headlineM': 'Continue Watching',
               'titleL': 'Harbour Lights: The Complete Series', 'titleM': 'Subtitles & Audio', 'bodyL': 'A cartographer returns to the coast she left as a child and finds the maps no longer agree.',
               'bodyM': 'Because you watched this, we think you’ll love these.', 'labelL': 'Home   Series   Movies   Live   My List', 'labelM': 'Watch Now    Play from Beginning    Skip Intro',
               'caption': 'Audio: English, Español, Français · Subtitles: 24 languages', 'metadata': '2024 • 2h 35m • TV-MA • 4K UHD • HDR • Dolby Atmos',
               'numeric': '00:59:48 / 2:35:00    ₹1,499    €19.99', 'subtitle': '— We should have left before the tide came in.'}
    rows = []
    for n, p in P.items():
        spec = "%g / %g px · wght %d · opsz %g · GRAD %d · %s em%s" % (p['fontSize'], p['lineHeight'], p['wght'], p['opsz'], p['GRAD'], ('%+g' % p['letterSpacing']) if p['letterSpacing'] else '0', ' · tnum' if p['features'] else '')
        rows.append("<div class='r'><div><b>%s</b><span class='note'>%s<br>%s · min %g px</span></div><div class='s' style=\"%s\">%s</div></div>" % (n, spec, esc(p['usage']), p['minSize'], tok(p), esc(samples[n])))
    body = "<h1>Type scale — %s</h1><div class='sub'>%s. Every row is set with the exact token values from integration/tokens/orion-type-presets.json at 1:1 pixel size.</div>%s" % (plat.upper() if plat == 'tv' else plat.capitalize(), esc(T['meta']['canvas'][plat]), ''.join(rows))
    return page('Type scale ' + plat, body, css, cls, 1920, 0)


def kerning_page():
    pairs = ['AVATAR', 'WAVE', 'Tokyo', 'Yes, To. Type', 'LT. P. F,', 'ROYALTY', 'Kyoto Wyatt', 'r. f. y, v.', '“A” ‘T’ (J)', 'rn m  rm  nn', '7.1 1,499 4K 11', 'ЮГА ТАЙНА', 'ΑΥΤΑ ΛΑΤΡΑ']
    css = HEAD + """
    body { padding: 64px 96px 90px; }
    .g { display: grid; grid-template-columns: 1fr 1fr; column-gap: 60px; }
    .col .s { font-size: 64px; line-height: 80px; border-top: 1px solid #D9DCE1; white-space: nowrap; %s }
    .hv { font-size: 96px; line-height: 110px; margin-top: 34px; white-space: nowrap; }
    """ % fv(500, 100, 64)
    off = ''.join("<div class='s' style='font-kerning:none;color:#8A8F99'>%s</div>" % esc(p) for p in pairs)
    on = ''.join("<div class='s'>%s</div>" % esc(p) for p in pairs)
    hv = ''.join("<div class='hv' style=\"%s\">AVATAR Tokyo WAVE LT. Yes</div>" % fv(w, 100, 72) for w in (100, 400, 900))
    body = ("<h1>Spacing and kerning</h1><div class='sub'>About 8,200 class-based pairs per master, generated from glyph profiles and interpolated with the outlines. Left: kerning disabled. Right: default.</div>"
            "<div class='g'><div class='col'><div class='tag'>kern off</div>%s</div><div class='col'><div class='tag'>kern on</div>%s</div></div>%s" % (off, on, hv))
    return page('Kerning', body, css, 'light', 1920, 0)


def multilingual_page():
    css = HEAD + """
    body { padding: 64px 96px 90px; }
    .g { display: grid; grid-template-columns: 1fr 1fr; column-gap: 70px; }
    .l { border-top: 1px solid #262B36; padding: 12px 0 14px; }
    .l .s { font-size: 28px; line-height: 40px; margin-top: 4px; %s }
    .l .t { font-size: 44px; line-height: 52px; %s }
    """ % (fv(400, 100, 26), fv(600, 100, 44))
    titles = {'English': 'Continue Watching', 'Spanish': 'Seguir viendo', 'French': 'Reprendre la lecture', 'German': 'Weiterschauen', 'Italian': 'Continua a guardare',
              'Portuguese': 'Continuar assistindo', 'Dutch': 'Verder kijken', 'Polish': 'Oglądaj dalej', 'Czech': 'Pokračovat ve sledování', 'Slovak': 'Pokračovať v pozeraní',
              'Hungarian': 'Megtekintés folytatása', 'Romanian': 'Continuă vizionarea', 'Turkish': 'İzlemeye devam et', 'Vietnamese': 'Tiếp tục xem', 'Greek': 'Συνέχεια παρακολούθησης',
              'Russian': 'Продолжить просмотр', 'Ukrainian': 'Продовжити перегляд', 'Bulgarian': 'Продължи гледането', 'Serbian': 'Настави гледање'}
    lang = {'Romanian': 'ro', 'Turkish': 'tr', 'Serbian': 'sr', 'Bulgarian': 'bg', 'Vietnamese': 'vi', 'Greek': 'el', 'Polish': 'pl', 'Dutch': 'nl'}
    items = []
    for name, t in titles.items():
        s = LANGUAGE_SAMPLES[name]
        s = s.split(' · ', 1)[1] if ' · ' in s else s
        items.append("<div class='l' lang='%s'><div class='tag'>%s</div><div class='t'>%s</div><div class='s'>%s</div></div>" % (lang.get(name, ''), name, esc(t), esc(s)))
    half = (len(items) + 1) // 2
    body = ("<h1>Multilingual</h1><div class='sub'>The 19 target languages, set with the TV Headline M and Body M presets. Latin, Greek (monotonic) and Cyrillic are drawn in the same system; "
            "scripts outside this set fall back to companion families (see UNICODE-COVERAGE.md).</div><div class='g'><div>%s</div><div>%s</div></div>" % (''.join(items[:half]), ''.join(items[half:])))
    return page('Multilingual', body, css, '', 1920, 0)


def spacing_page():
    css = HEAD + """
    body { padding: 64px 96px 90px; }
    .g { display: grid; grid-template-columns: 1fr 1fr; column-gap: 70px; }
    .bx { border-top: 1px solid #D9DCE1; padding-top: 14px; }
    .p { margin-top: 10px; outline: 1px dashed #B9BEC8; outline-offset: 6px; }
    .p p { margin: 0; }
    .ov { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; }
    .ov p + p { margin-top: 2em; }
    """
    txt = ("<p>Six months into a routine survey, the crew of the Halden lose contact with home and begin receiving their own transmissions.</p>"
           "<p>Đặng Thị Ánh, Ấp Ổ Ỗ Ữ Ỵ, Åse Ørsted, Çağrı Güneş, Żółć, Ξένος, Щедрик: fjord, quay, gypsy, 00:59:48.</p>")
    cols = []
    for name in ('bodyL', 'caption'):
        p = dict(T['tv'][name])
        for label, cls, scale in (('preset as specified', '', 1), ('WCAG 1.4.12 overrides: line 1.5, paragraph 2 em, letter 0.12 em, word 0.16 em', 'ov', 1),
                                  ('200 % text (WCAG 1.4.4) with the same overrides', 'ov', 2)):
            q = dict(p); q['fontSize'] *= scale; q['lineHeight'] *= scale
            cols.append("<div class='bx'><div class='tag'>%s · %s</div><div class='p %s' style=\"%s\">%s</div></div>" % (name, label, cls, tok(q), txt))
    body = ("<h1>Text-spacing overrides</h1><div class='sub'>User style overrides required by WCAG 1.4.12 and 200 %% text scaling applied to two TV presets. "
            "Nothing clips or collides, stacked Vietnamese capitals stay inside the line box, and no glyph changes form because Orion has no ligature features.</div>"
            "<div class='g'>%s</div>" % ''.join(cols))
    return page('Text-spacing overrides', body, css, 'light', 1920, 0)


PAGES = [('variable-axis/weight', weight_page, 1), ('variable-axis/width', width_page, 1), ('variable-axis/optical-size', opsz_page, 1),
         ('variable-axis/grade', grade_page, 1), ('variable-axis/combined-axes', combined_page, 1),
         ('typography-scale/type-scale-tv', lambda: scale_page('tv'), 1), ('typography-scale/type-scale-desktop', lambda: scale_page('desktop', 'light'), 1),
         ('typography-scale/type-scale-mobile', lambda: scale_page('mobile', 'light'), 2),
         ('typography-scale/kerning', kerning_page, 1), ('typography-scale/text-spacing-override', spacing_page, 1), ('typography-scale/multilingual', multilingual_page, 1)]
