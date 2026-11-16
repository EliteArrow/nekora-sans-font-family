# -*- coding: utf-8 -*-
"""OTT interface specimens (TV 1920x1080, mobile) — fictional titles, CSS-gradient artwork, real font rendering."""
import json, os
from common import *
T = json.load(open(os.path.join(ROOT, 'integration', 'tokens', 'orion-type-presets.json')))
TV = T['tv']; MB = T['mobile']

ART = [
    "radial-gradient(120% 90% at 80% 20%, #F2A65A 0%, #B5462F 34%, #3A1420 70%, #120B14 100%)",
    "radial-gradient(110% 100% at 20% 30%, #5EC8D8 0%, #1E6F8C 36%, #0F2B46 72%, #0A1220 100%)",
    "linear-gradient(135deg, #2B1B4B 0%, #6B2D7B 42%, #D9577A 78%, #F5B971 100%)",
    "radial-gradient(100% 120% at 70% 80%, #9BD67C 0%, #2F8F6B 38%, #0F3B3A 74%, #071A1C 100%)",
    "linear-gradient(160deg, #101726 0%, #223A66 45%, #6C8FD6 80%, #DCE8FF 100%)",
    "radial-gradient(90% 90% at 50% 40%, #FFD27A 0%, #E0703A 40%, #6E1F2B 76%, #1A0A12 100%)",
    "linear-gradient(200deg, #0E0E12 0%, #3B3F4A 50%, #A7AFBD 100%)",
    "radial-gradient(120% 100% at 15% 85%, #F06C8B 0%, #8B2C6B 40%, #2A1240 75%, #0C0818 100%)",
    "linear-gradient(120deg, #06281F 0%, #0F5A46 46%, #49B38A 82%, #D9F5D0 100%)",
    "radial-gradient(100% 100% at 85% 75%, #6FA8FF 0%, #2D4FB3 38%, #17205A 72%, #080A1C 100%)",
    "linear-gradient(145deg, #3A0D0D 0%, #8E1D1D 45%, #E0562F 80%, #FFC56B 100%)",
    "radial-gradient(110% 110% at 40% 20%, #C9B8FF 0%, #6C55C9 38%, #281C66 72%, #0B0820 100%)",
]
CAT = [  # title, style(wght, wdth, upper), metadata
    ('The Last Meridian', (700, 100, 0), '2024 • 2h 35m • TV-MA'), ('Quiet Orbit', (300, 125, 0), '2023 • 8 Episodes • TV-14'),
    ('KINGDOM OF DUST', (900, 75, 1), '2024 • 3 Seasons • TV-MA'), ('Harbour Lights', (600, 100, 0), '2022 • 1h 48m • PG-13'),
    ('AFTERLIGHT', (800, 112, 1), '2024 • 6 Episodes • TV-14'), ('Salt & Ember', (500, 100, 0), '2021 • 2h 04m • R'),
    ('Velvet Static', (200, 100, 0), '2023 • 10 Episodes • TV-MA'), ('NORTHBOUND', (700, 75, 1), '2020 • 1h 52m • PG'),
    ('The Glass Coast', (400, 100, 0), '2024 • 2 Seasons • TV-14'), ('Đêm Sài Gòn', (700, 100, 0), '2023 • 1h 57m • T16'),
    ('Ночной экспресс', (800, 87, 0), '2022 • 8 серий • 16+'), ('Η Θάλασσα', (300, 100, 0), '2021 • 1h 39m • K-12'),
]

NAV_CSS = fmt("""
.nav { position: absolute; top: 44px; left: 96px; right: 96px; display: flex; align-items: center; gap: 52px; z-index: 5; }
.logo { font-size: 38px; line-height: 48px; letter-spacing: 0.2em; margin-right: 28px; %s }
.nav .i { %s color: #B3B8C2; }
.nav .i.on { color: #F2F2F2; border-bottom: 4px solid #C8102E; padding-bottom: 6px; }
.light .nav .i { color: #4A4F5A; } .light .nav .i.on { color: #14161A; border-color: #B00E28; }
.nav .sp { flex: 1; }
.btn { display: inline-flex; align-items: center; gap: 14px; height: 72px; padding: 0 36px; border-radius: 10px; background: rgba(255,255,255,0.14); %s }
.btn.f { background: #F2F2F2; color: #0B0D12; box-shadow: 0 0 0 4px #0B0D12, 0 0 0 8px #4DA3FF; }
.card { position: relative; border-radius: 10px; overflow: hidden; }
.card .ti { position: absolute; left: 22px; right: 16px; bottom: 16px; color: #fff; text-shadow: 0 2px 14px rgba(0,0,0,0.55); }
""", (fv(800, 125, 38), tok(TV['labelL']), tok(TV['labelM'])))


def nav(active='Home', clock='21:47'):
    items = ''.join("<div class='i%s'>%s</div>" % (' on' if n == active else '', n) for n in ('Home', 'Series', 'Movies', 'Live', 'My List'))
    return "<div class='nav'><div class='logo'>ORION</div>%s<div class='sp'></div><div class='i'>Search</div><div class='i' style=\"font-feature-settings:'tnum' 1\">%s</div></div>" % (items, clock)


def art_title(i, size, extra=''):
    t, (w, wd, up), _ = CAT[i]
    return "<div class='ti' style=\"font-size:%dpx;line-height:1.04;letter-spacing:%s;%s;%s\">%s</div>" % (
        size, '0.04em' if up else '-0.01em', fv(w, wd, size), extra, esc(t))


def home_dark():
    css = NAV_CSS + fmt("""
    .bg { position: absolute; inset: 0; background: radial-gradient(1100px 760px at 80% 26%, #D9773F 0%, #8A2E2A 30%, #3A1420 56%, transparent 78%), radial-gradient(900px 700px at 58% 86%, #153A5E 0%, transparent 70%), #0B0D12; }
    .sc { position: absolute; inset: 0; background: linear-gradient(90deg, #0B0D12 0%, rgba(11,13,18,0.90) 26%, rgba(11,13,18,0.25) 62%, rgba(11,13,18,0) 100%), linear-gradient(0deg, #0B0D12 0%, rgba(11,13,18,0.9) 26%, rgba(11,13,18,0) 52%); }
    .hero { position: absolute; left: 96px; top: 178px; width: 900px; }
    .kick { font-size: 22px; line-height: 28px; letter-spacing: 0.16em; color: #F2B8A0; margin-bottom: 14px; %s }
    .meta { color: #B3B8C2; margin: 14px 0 16px; %s }
    .syn { color: #E4E6EA; max-width: 800px; %s }
    .btns { display: flex; gap: 22px; margin-top: 28px; }
    .row { position: absolute; left: 96px; top: 690px; right: 0; }
    .cards { display: flex; gap: 24px; margin-top: 18px; }
    .cards .card { width: 344px; height: 194px; flex: none; }
    .pr { position: absolute; left: 0; right: 0; bottom: 0; height: 6px; background: rgba(255,255,255,0.28); }
    .pr i { display: block; height: 6px; background: #C8102E; }
    .cap { margin-top: 10px; color: #B3B8C2; width: 344px; white-space: nowrap; overflow: hidden; %s }
    """, (fv(700, 100, 20), tok(TV['metadata']), tok(TV['bodyM']), tok(TV['caption'])))
    cont = [(1, 62, 'S1:E8 • 23m remaining'), (3, 35, '1h 12m remaining'), (4, 80, 'S1:E3 • 9m remaining'), (7, 18, '1h 31m remaining'), (9, 51, '58m remaining')]
    cards = ''.join("<div><div class='card' style='background:%s'>%s<div class='pr'><i style='width:%d%%'></i></div></div><div class='cap'>%s</div></div>" % (ART[i], art_title(i, 30, 'bottom:22px'), p, esc(c)) for i, p, c in cont)
    body = ("<div class='bg'></div><div class='sc'></div>%s<div class='hero'><div class='kick'>ORION ORIGINAL</div><div style=\"%s\">The Last Meridian</div>"
            "<div class='meta'>2024 • 2h 35m • TV-MA • 4K UHD • HDR • Dolby Atmos</div>"
            "<div class='syn'>A cartographer returns to the coast she left as a child and finds that the maps no longer agree with the sea.</div>"
            "<div class='btns'><div class='btn f'>▶ Watch Now</div><div class='btn'>Play from Beginning</div><div class='btn'>+ My List</div></div></div>"
            "<div class='row'><div style=\"%s\">Continue Watching</div><div class='cards'>%s</div></div>" % (nav(), tok(TV['displayXL']), tok(TV['headlineM']), cards))
    return page('TV home, dark', body, css)


def home_bright():
    css = NAV_CSS + fmt("""
    .h { position: absolute; left: 96px; top: 150px; }
    .row { position: absolute; left: 96px; right: 0; }
    .cards { display: flex; gap: 28px; margin-top: 18px; }
    .rk { display: flex; align-items: flex-end; flex: none; }
    .rk .n { font-size: 250px; line-height: 200px; color: #14161A; margin-right: -22px; %s }
    .rk .card { width: 214px; height: 306px; }
    .rk .ti { left: 16px; right: 12px; }
    .c2 .card { width: 344px; height: 194px; }
    .cap { margin-top: 10px; color: #4A4F5A; %s } .cap b { display: block; color: #14161A; %s }
    .btn { background: #E4E6EA; color: #14161A; } .btn.f { background: #14161A; color: #fff; box-shadow: 0 0 0 4px #fff, 0 0 0 8px #0A5FD1; }
    """, (fv(900, 87, 72), tok(TV['metadata']), tok(TV['titleL'])))
    rk = ''.join("<div class='rk'><div class='n'>%d</div><div class='card' style='background:%s'>%s</div></div>" % (k + 1, ART[i], art_title(i, 26)) for k, i in enumerate((2, 0, 5, 10, 8, 11)))
    c2 = ''.join("<div class='c2'><div class='card' style='background:%s'></div><div class='cap'><b>%s</b>%s</div></div>" % (ART[i], esc(CAT[i][0].title() if CAT[i][1][2] else CAT[i][0]), esc(CAT[i][2])) for i in (6, 3, 1, 4, 9))
    body = ("%s<div class='row' style='top:150px'><div style=\"%s\">Top 10 in Your Country</div><div class='cards' style='gap:40px;margin-top:26px'>%s</div></div>"
            "<div class='row' style='top:660px'><div style=\"%s\">Recommended for You</div><div class='cards'>%s</div></div>" % (nav('Movies', '09:12'), tok(TV['headlineL']), rk, tok(TV['headlineM']), c2))
    return page('TV home, bright', body, css, 'light')


def hero_titles():
    css = fmt("""
    .q { position: absolute; width: 960px; height: 540px; overflow: hidden; }
    .q .sc { position: absolute; inset: 0; background: linear-gradient(0deg, rgba(8,9,12,0.86) 0%, rgba(8,9,12,0.25) 58%, rgba(8,9,12,0) 100%); }
    .q .t { position: absolute; left: 64px; right: 48px; bottom: 96px; color: #fff; }
    .q .m { position: absolute; left: 64px; bottom: 52px; color: #E4E6EA; %s }
    .q .k { position: absolute; left: 64px; top: 48px; font-size: 18px; letter-spacing: 0.16em; color: rgba(255,255,255,0.86); %s }
    """, (tok(TV['metadata']), fv(600, 100, 18)))
    H = [(0, 'KINGDOM<br>OF DUST', 132, fv(900, 75, 72), '0.01em', '0.92', 'Black Condensed · opsz 72', '2024 • 3 Seasons • TV-MA • 4K UHD'),
         (1, 'quiet orbit', 118, fv(200, 125, 72), '-0.02em', '1', 'ExtraLight Extended · opsz 72', '2023 • 8 Episodes • TV-14 • HDR'),
         (2, 'The Glass<br>Coast', 112, fv(700, 100, 72), '-0.02em', '0.98', 'Bold · opsz 72', '2024 • 2 Seasons • TV-14 • Dolby Atmos'),
         (9, 'Đêm Sài Gòn', 104, fv(600, 100, 72, 40), '-0.015em', '1.1', 'SemiBold · GRAD +40 over bright artwork', '2023 • 1h 57m • T16 • Phụ đề'),]
    out = []
    for k, (i, t, size, st, ls, lh, note, meta) in enumerate(H):
        out.append("<div class='q' style='left:%dpx;top:%dpx;background:%s'><div class='sc'></div><div class='k'>%s</div><div class='t' style=\"font-size:%dpx;line-height:%s;letter-spacing:%s;%s\">%s</div><div class='m'>%s</div></div>"
                   % ((k % 2) * 960, (k // 2) * 540, ART[i], esc(note).upper(), size, lh, ls, st, t, esc(meta)))
    return page('Hero titles', ''.join(out), css)


def card_grid():
    css = NAV_CSS + fmt("""
    .h { position: absolute; left: 96px; top: 148px; right: 96px; display: flex; align-items: baseline; gap: 44px; }
    .tabs { display: flex; gap: 36px; color: #8E95A3; %s } .tabs .on { color: #F2F2F2; }
    .grid { position: absolute; left: 96px; top: 258px; display: grid; grid-template-columns: repeat(4, 408px); gap: 34px 32px; }
    .grid .card { width: 408px; height: 230px; }
    .t { margin-top: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; %s }
    .m { color: #8E95A3; %s }
    .foc .card { box-shadow: 0 0 0 4px #0B0D12, 0 0 0 8px #F2F2F2; transform: scale(1.04); }
    .bd { position: absolute; left: 14px; top: 14px; background: #C8102E; color: #fff; border-radius: 6px; padding: 2px 12px; font-size: 20px; line-height: 30px; letter-spacing: 0.06em; %s }
    """, (tok(TV['labelL']), tok(TV['titleL']), tok(TV['metadata']), fv(700, 100, 20)))
    cells = []
    for k in range(12):
        t, (w, wd, up), meta = CAT[k]
        name = t.title() if up else t
        badge = "<div class='bd'>NEW</div>" if k in (0, 4, 9) else ("<div class='bd' style='background:#F2F2F2;color:#0B0D12'>TOP 10</div>" if k in (2,) else '')
        cells.append("<div class='%s'><div class='card' style='background:%s'>%s%s</div><div class='t' style=\"%s\">%s</div><div class='m'>%s</div></div>"
                     % ('foc' if k == 1 else '', ART[k], badge, art_title(k, 40), 'font-variation-settings:\'wght\' 500,\'wdth\' 100,\'opsz\' 36,\'GRAD\' 80' if k == 1 else '', esc(name), esc(meta)))
    body = ("%s<div class='h'><div style=\"%s\">New &amp; Popular</div><div class='tabs'><span class='on'>All</span><span>Series</span><span>Movies</span><span>Coming Soon</span></div></div>"
            "<div class='grid'>%s</div>" % (nav('Home'), tok(TV['headlineL']), ''.join(cells)))
    return page('Card grid', body, css)


def detail_page():
    css = NAV_CSS + fmt("""
    .bg { position: absolute; inset: 0; background: radial-gradient(900px 700px at 86% 18%, #5EC8D8 0%, #1E6F8C 30%, #0F2B46 56%, transparent 80%), #0B0D12; }
    .sc { position: absolute; inset: 0; background: linear-gradient(90deg, #0B0D12 0%, rgba(11,13,18,0.92) 34%, rgba(11,13,18,0.55) 70%, rgba(11,13,18,0.35) 100%); }
    .L { position: absolute; left: 96px; top: 150px; width: 900px; }
    .meta { color: #B3B8C2; margin: 12px 0 20px; display: flex; gap: 16px; align-items: center; %s }
    .pill { border: 2px solid #8E95A3; border-radius: 6px; padding: 0 10px; line-height: 28px; }
    .syn { color: #E4E6EA; %s }
    .cr { margin-top: 20px; color: #8E95A3; %s } .cr b { color: #D5D8DE; font-weight: normal; }
    .btns { display: flex; gap: 22px; margin-top: 30px; }
    .R { position: absolute; left: 1080px; top: 150px; right: 96px; }
    .ep { display: grid; grid-template-columns: 56px 1fr auto; column-gap: 20px; align-items: baseline; padding: 15px 22px; border-radius: 10px; }
    .ep.f { background: #F2F2F2; color: #0B0D12; }
    .ep .n { color: #8E95A3; %s } .ep.f .n, .ep.f .d { color: #0B0D12; }
    .ep .t { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; %s }
    .ep .d { color: #8E95A3; %s }
    """, (tok(TV['metadata']), tok(TV['bodyL']), tok(TV['caption']), tok(TV['numeric']), tok(TV['labelL']), tok(TV['numeric'])))
    eps = [('Low Water', '52m'), ('The Survey', '48m'), ('Paper Coast', '55m'), ('Soundings', '47m'), ('A Line in Salt', '51m'), ('North by Memory', '58m'), ('Dead Reckoning', '49m'), ('Signal Fire', '1h 02m')]
    rows = ''.join("<div class='ep%s'><div class='n'>%02d</div><div class='t'%s>%s</div><div class='d'>%s</div></div>" % (' f' if k == 7 else '', k + 1, (" style=\"%s\"" % fv(500, 100, 28, 80)) if k == 7 else '', esc(t), d) for k, (t, d) in enumerate(eps))
    body = ("<div class='bg'></div><div class='sc'></div>%s<div class='L'><div style=\"%s\">Quiet Orbit</div>"
            "<div class='meta'><span>2023</span><span>•</span><span>8 Episodes</span><span>•</span><span class='pill'>TV-14</span><span class='pill'>4K UHD</span><span class='pill'>HDR</span><span class='pill'>5.1</span><span>★ 8.7/10</span></div>"
            "<div class='syn'>Six months into a routine survey, the crew of the Halden lose contact with home and begin receiving their own transmissions — dated eleven years from now. "
            "What starts as a fault report becomes a question none of them trained for: if the future has already answered, who is still asking?</div>"
            "<div class='cr'>Starring <b>Imani Okafor, Tomasz Żuławski, Linh Đặng, Søren Åkesson</b><br>Genres <b>Science fiction · Drama · Mystery</b><br>Audio <b>English, Español, Français, Deutsch, Tiếng Việt, Русский</b></div>"
            "<div class='btns'><div class='btn f'>▶ Resume S1:E8</div><div class='btn'>Play from Beginning</div><div class='btn'>Trailer</div></div></div>"
            "<div class='R'><div style=\"%s;margin:0 0 14px 22px\">Season 01 — Episode 08</div>%s</div>" % (nav('Series'), tok(TV['displayL']), tok(TV['headlineM']), rows))
    return page('Detail page and synopsis', body, css)


def playback():
    css = fmt("""
    .bg { position: absolute; inset: 0; background: radial-gradient(1200px 800px at 64% 38%, #F5C98A 0%, #C9703A 26%, #5A2430 54%, #151018 84%); }
    .top { position: absolute; left: 0; right: 0; top: 0; height: 300px; background: linear-gradient(180deg, rgba(0,0,0,0.78), rgba(0,0,0,0)); }
    .bot { position: absolute; left: 0; right: 0; bottom: 0; height: 420px; background: linear-gradient(0deg, rgba(0,0,0,0.88), rgba(0,0,0,0)); }
    .tt { position: absolute; left: 96px; top: 56px; } .tt .s { color: #D5D8DE; margin-top: 4px; %s }
    .bar { position: absolute; left: 96px; right: 96px; bottom: 190px; height: 8px; border-radius: 4px; background: rgba(255,255,255,0.3); }
    .bar i { position: absolute; left: 0; top: 0; height: 8px; width: 38.6%; border-radius: 4px; background: #C8102E; }
    .bar b { position: absolute; left: 38.6%; top: -10px; width: 28px; height: 28px; margin-left: -14px; border-radius: 14px; background: #fff; }
    .tm { position: absolute; bottom: 128px; %s }
    .ctl { position: absolute; left: 96px; right: 96px; bottom: 44px; display: flex; align-items: center; gap: 28px; }
    .ic { width: 72px; height: 72px; border-radius: 36px; display: flex; align-items: center; justify-content: center; font-size: 34px; background: rgba(255,255,255,0.14); %s }
    .ic.f { background: #F2F2F2; color: #0B0D12; box-shadow: 0 0 0 4px rgba(0,0,0,0.6), 0 0 0 8px #4DA3FF; }
    .chip { height: 72px; padding: 0 34px; border-radius: 10px; display: flex; align-items: center; background: rgba(255,255,255,0.14); %s }
    .sub { position: absolute; left: 0; right: 0; bottom: 300px; text-align: center; }
    .sub span { background: rgba(0,0,0,0.75); padding: 4px 18px; -webkit-box-decoration-break: clone; box-decoration-break: clone; %s }
    .panel { position: absolute; right: 96px; top: 150px; width: 560px; background: rgba(14,16,22,0.94); border-radius: 16px; padding: 30px 34px 26px; }
    .panel h3 { letter-spacing: 0.1em; color: #8E95A3; margin-bottom: 12px; font-weight: normal; %s }
    .op { display: flex; justify-content: space-between; padding: 9px 0; %s } .op.on { color: #fff; } .op { color: #B3B8C2; }
    """, (tok(TV['labelL']), tok(TV['numeric']), fv(500, 100, 34), tok(TV['labelM']), tok(TV['subtitle']), tok(TV['metadata']), tok(TV['labelL'])))
    langs = [('English [CC]', 1), ('Español (Latinoamérica)', 0), ('Français', 0), ('Tiếng Việt', 0), ('Türkçe', 0), ('Русский', 0), ('Українська', 0), ('Ελληνικά', 0)]
    ops = ''.join("<div class='op%s'><span>%s</span><span>%s</span></div>" % (' on' if on else '', esc(n), '✓' if on else '') for n, on in langs)
    body = ("<div class='bg'></div><div class='top'></div><div class='bot'></div>"
            "<div class='tt'><div style=\"%s\">Quiet Orbit</div><div class='s'>S1:E8 · Signal Fire</div></div>"
            "<div class='panel'><h3>SUBTITLES &amp; AUDIO</h3>%s</div>"
            "<div class='sub'><span>— We should have left before the tide came in.</span></div>"
            "<div class='bar'><i></i><b></b></div><div class='tm' style='left:96px'>00:59:48</div><div class='tm' style='right:96px'>−1:35:12</div>"
            "<div class='ctl'><div class='ic'>◀◀</div><div class='ic f'>▶</div><div class='ic'>▶▶</div><div class='chip'>↩ 10</div><div class='chip'>10 ↪</div><div style='flex:1'></div>"
            "<div class='chip'>Skip Intro</div><div class='chip'>Next Episode ▸</div><div class='chip'>Subtitles &amp; Audio</div></div>" % (tok(TV['headlineM']), ops))
    return page('Playback controls', body, css)


def subtitles():
    css = fmt("""
    .st { position: absolute; left: 0; width: 1920px; height: 270px; overflow: hidden; }
    .st .lab { position: absolute; left: 40px; top: 22px; font-size: 17px; letter-spacing: 0.12em; %s }
    .st .tx { position: absolute; left: 0; right: 0; bottom: 34px; text-align: center; %s }
    .box span { background: rgba(0,0,0,0.75); color: #fff; padding: 4px 18px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
    .out { color: #fff; text-shadow: -3px 0 0 #000, 3px 0 0 #000, 0 -3px 0 #000, 0 3px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000, 0 4px 10px rgba(0,0,0,0.7); }
    .shd { color: #fff; text-shadow: 0 2px 6px rgba(0,0,0,0.95), 0 0 2px #000; }
    .yel span { background: rgba(0,0,0,0.82); color: #FFE14D; padding: 4px 18px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
    """, (fv(700, 100, 16), tok(TV['subtitle'])))
    S = [("linear-gradient(180deg, #BFE3FF 0%, #F3F8FF 55%, #FFF3D0 100%)", '#14161A', 'BRIGHT SKY · 75% SCRIM BOX · GRAD +40', 'box', "— We should have left before the tide came in.<br>[waves crashing] Still… it’s beautiful, isn’t it?"),
         ("repeating-linear-gradient(115deg, #F2F2F2 0 26px, #1B1B1B 26px 52px, #E0562F 52px 78px, #1E6F8C 78px 104px)", '#fff', 'HIGH-FREQUENCY PATTERN · OUTLINE + SHADOW', 'out', "Chúng ta phải đi trước khi nước lên.<br>Đừng nhìn lại — hãy chạy đi, Đặng!"),
         ("radial-gradient(900px 400px at 30% 60%, #2A3550 0%, #0B0D12 70%)", '#8E95A3', 'DARK SCENE · DROP SHADOW ONLY', 'shd', "«Мы должны были уйти до прилива», — сказала она.<br>Ελληνικά: Έπρεπε να είχαμε φύγει πριν την παλίρροια."),
         ("linear-gradient(90deg, #E0562F 0%, #FFC56B 50%, #F06C8B 100%)", '#14161A', 'SATURATED VIDEO · YELLOW ON 82% BOX', 'yel', "¿Dónde está el señor Ibáñez? ¡Öffnen Sie die Tür!<br>Il était déjà là — 00:59:48 — où êtes-vous ?"),]
    out = ''.join("<div class='st' style='top:%dpx;background:%s'><div class='lab' style='color:%s'>%s</div><div class='tx %s'><span>%s</span></div></div>" % (k * 270, bg, lc, esc(lab), cls, tx)
                  for k, (bg, lc, lab, cls, tx) in enumerate(S))
    return page('Subtitles', out, css)


def mobile():
    def m(n, extra=''):
        return tok(MB[n], extra)
    css = fmt("""
    html, body { background: #E9EBEF; }
    .ph { position: absolute; top: 28px; width: 390px; height: 844px; border-radius: 44px; overflow: hidden; background: #0B0D12; color: #F2F2F2; box-shadow: 0 0 0 10px #14161A, 0 30px 60px rgba(0,0,0,0.25); }
    .ph.lt { background: #fff; color: #14161A; }
    .sb { position: absolute; top: 14px; left: 30px; right: 30px; display: flex; justify-content: space-between; font-size: 15px; z-index: 4; %s; font-feature-settings: 'tnum' 1; }
    .pad { padding: 0 20px; }
    .tabbar { position: absolute; left: 0; right: 0; bottom: 0; height: 78px; display: flex; justify-content: space-around; align-items: center; background: rgba(11,13,18,0.96); border-top: 1px solid #262B36; color: #8E95A3; %s }
    .tabbar .on { color: #F2F2F2; }
    .mb { height: 48px; border-radius: 8px; display: flex; align-items: center; justify-content: center; %s }
    .rowc { display: flex; gap: 10px; margin-top: 8px; padding-left: 20px; }
    .rowc div { width: 118px; height: 168px; border-radius: 8px; flex: none; position: relative; overflow: hidden; }
    .cap3 { position: absolute; left: 0; right: 0; top: 898px; text-align: center; color: #4A4F5A; font-size: 14px; letter-spacing: 0.08em; %s }
    """, (fv(600, 100, 14), m('caption'), m('labelM'), fv(600, 100, 13)))
    # 1 home
    h1 = ("<div class='ph' style='left:70px'><div class='sb'><span>21:47</span><span>5G ▮▮▮</span></div>"
          "<div style='height:500px;background:%s;position:relative'><div style='position:absolute;inset:0;background:linear-gradient(0deg,#0B0D12 2%%,rgba(11,13,18,0) 58%%)'></div>"
          "<div style='position:absolute;left:20px;right:20px;bottom:74px;text-align:center'><div style=\"%s\">The Last Meridian</div><div style=\"%s;color:#D5D8DE;margin-top:6px\">2024 • 2h 35m • TV-MA • 4K UHD</div></div>"
          "<div style='position:absolute;left:20px;right:20px;bottom:14px;display:flex;gap:10px'><div class='mb' style='flex:1;background:#F2F2F2;color:#0B0D12'>▶ Watch Now</div><div class='mb' style='flex:1;background:rgba(255,255,255,0.16)'>+ My List</div></div></div>"
          "<div class='pad' style=\"%s;margin-top:16px\">Continue Watching</div><div class='rowc'>%s</div>"
          "<div class='tabbar'><span class='on'>Home</span><span>Search</span><span>Downloads</span><span>Profile</span></div></div>"
          % (ART[0], m('displayL'), m('metadata'), m('headlineM'), ''.join("<div style='background:%s'></div>" % ART[i] for i in (1, 4, 7, 9))))
    # 2 detail
    eps = [('1. Low Water', '52m'), ('2. The Survey', '48m'), ('3. Paper Coast', '55m')]
    h2 = ("<div class='ph' style='left:525px'><div class='sb'><span>21:48</span><span>5G ▮▮▮</span></div><div style='height:220px;background:%s'></div><div class='pad'>"
          "<div style=\"%s;margin-top:14px\">Quiet Orbit</div><div style=\"%s;color:#B3B8C2;margin-top:4px\">2023 • 8 Episodes • TV-14 • HDR • 5.1</div>"
          "<div class='mb' style='background:#F2F2F2;color:#0B0D12;margin-top:14px'>▶ Resume S1:E8</div><div class='mb' style='background:#1E232D;margin-top:8px'>↓ Download</div>"
          "<div style=\"%s;color:#D5D8DE;margin-top:14px\">Six months into a routine survey, the crew of the Halden lose contact with home and begin receiving their own transmissions — dated eleven years from now.</div>"
          "<div style=\"%s;margin-top:18px\">Season 01</div>%s</div>"
          "<div class='tabbar'><span>Home</span><span class='on'>Search</span><span>Downloads</span><span>Profile</span></div></div>"
          % (ART[1], m('headlineL'), m('metadata'), m('bodyM'), m('titleL'),
             ''.join("<div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #262B36'><span style=\"%s\">%s</span><span style=\"%s;color:#8E95A3\">%s</span></div>" % (m('bodyL'), esc(t), m('numeric'), d) for t, d in eps)))
    # 3 light: plans / account with prices and numerals
    plans = [('Mobile', '₹149', '480p · 1 screen'), ('Standard', '₹499', '1080p · 2 screens'), ('Premium', '₹1,499', '4K UHD + HDR · 4 screens')]
    h3 = ("<div class='ph lt' style='left:980px'><div class='sb'><span>09:12</span><span>Wi‑Fi ▮▮▮</span></div><div class='pad' style='padding-top:64px'>"
          "<div style=\"%s\">Choose your plan</div><div style=\"%s;color:#4A4F5A;margin-top:8px\">Cancel anytime. Prices include taxes where applicable.</div>%s"
          "<div class='mb' style='background:#B00E28;color:#fff;margin-top:22px'>Continue</div>"
          "<div style=\"%s;color:#636A76;margin-top:16px\">Also billed as €19.99 · R$ 39,90 · £15.99 · ¥1,980 per month depending on region. Next charge on 16/12/2026.</div></div></div>"
          % (m('headlineL'), m('bodyM'),
             ''.join("<div style='border:%s;border-radius:12px;padding:14px 16px;margin-top:14px;display:flex;justify-content:space-between;align-items:center'><div><div style=\"%s\">%s</div><div style=\"%s;color:#636A76\">%s</div></div><div style=\"%s;font-feature-settings:'tnum' 1\">%s<span style=\"%s;color:#636A76\">/mo</span></div></div>"
                     % ('2px solid #14161A' if k == 2 else '1px solid #C9CDD4', m('titleL'), n, m('caption'), d, m('headlineM'), p, m('caption')) for k, (n, p, d) in enumerate(plans)), m('caption')))
    caps = "<div class='cap3'>MOBILE PRESETS (pt / sp) · RENDERED AT 2× DEVICE PIXEL RATIO · HOME · DETAIL · PLAN PICKER (LIGHT)</div>"
    return page('Mobile UI', h1 + h2 + h3 + caps, css, '', 1440, 940)


def comparison():
    D = json.load(open(os.path.join(ROOT, 'qa', 'reports', 'reference-comparison.json')))
    LAB = [('cap', 'Cap height'), ('xh', 'x-height'), ('asc', 'Ascender (l)'), ('desc', 'Descender (p)'), ('stemUC', 'Capital stem (I)'),
           ('O_w', 'O width'), ('o_w', 'o width'), ('o_overshoot', 'o overshoot'), ('adv_n', 'n advance'), ('adv_H', 'H advance'), ('avg_lc_adv', 'Mean lowercase advance'),
           ('avg_uc_adv', 'Mean capital advance'), ('space', 'Word space'), ('period_w', 'Period width'), ('hyphen_th', 'Hyphen thickness'), ('adv_0', 'Figure advance')]
    css = fmt("""
    body { padding: 64px 96px 90px; }
    h1 { font-size: 72px; line-height: 80px; letter-spacing: -0.015em; %s; }
    .sub { font-size: 22px; line-height: 32px; margin: 12px 0 26px; color: #4A4F5A; max-width: 1500px; %s }
    table { border-collapse: collapse; width: 100%; margin-bottom: 34px; }
    th, td { border-top: 1px solid #D9DCE1; padding: 8px 18px 7px 0; text-align: right; font-size: 24px; line-height: 32px; font-feature-settings: 'tnum' 1; %s }
    th:first-child, td:first-child { text-align: left; }
    thead th { font-size: 15px; letter-spacing: 0.1em; text-transform: uppercase; color: #636A76; border-top: none; %s }
    td.o { %s }
    """, (fv(700, 100, 72), fv(400, 100, 22), fv(400, 100, 24), fv(600, 100, 14), fv(700, 100, 24)))
    cols = D['columns']
    head = "<thead><tr><th>Metric (units / 1000 em)</th>%s</tr></thead>" % ''.join("<th>%s</th>" % esc(c['label']) for c in cols)
    rows = []
    for k, lab in LAB:
        rows.append("<tr><td>%s</td>%s</tr>" % (lab, ''.join("<td%s>%s</td>" % (" class='o'" if i == 0 else '', ('%g' % round(c['metrics'][k])) if c['metrics'].get(k) is not None else '—') for i, c in enumerate(cols))))
    rows.append("<tr><td>x-height / cap height</td>%s</tr>" % ''.join("<td%s>%.3f</td>" % (" class='o'" if i == 0 else '', c['metrics']['xh'] / c['metrics']['cap']) for i, c in enumerate(cols)))
    w = D['weights']
    head2 = "<thead><tr><th>Weight series vs primary reference</th>%s</tr></thead>" % ''.join("<th>Orion %s / Gotham %s</th>" % (x['style'], x['gotham_style']) for x in w)
    rows2 = []
    for k, lab in (('stemUC', 'Capital stem'), ('xh', 'x-height'), ('O_w', 'O width'), ('avg_lc_adv', 'Mean lowercase advance')):
        rows2.append("<tr><td>%s</td>%s</tr>" % (lab, ''.join("<td><span style=\"%s\">%g</span> / %g</td>" % (fv(700, 100, 24), round(x['orion'][k]), round(x['gotham'][k])) for x in w)))
    body = ("<h1>Reference comparison — metrics only</h1><div class='sub'>Orion measured with the same script as the four reference families. Only numbers are compared: no reference outline is rendered, "
            "stored or shipped. Orion sits at Gotham’s cap height with a slightly taller x-height, between Gotham’s width and Inter’s economy, and with a wider weight range than any single reference.</div>"
            "<table>%s%s</table><table>%s%s</table>" % (head, ''.join(rows), head2, ''.join(rows2)))
    return page('Reference comparison', body, css, 'light', 1920, 0)


PAGES = [('ott-tv/tv-home-dark', home_dark, 1), ('ott-tv/tv-home-bright', home_bright, 1), ('ott-tv/hero-titles', hero_titles, 1), ('ott-tv/card-grid', card_grid, 1),
         ('ott-tv/detail-synopsis', detail_page, 1), ('ott-tv/playback-controls', playback, 1), ('ott-tv/subtitles', subtitles, 1),
         ('mobile/mobile-ui', mobile, 2), ('comparison/reference-metrics', comparison, 1)]
