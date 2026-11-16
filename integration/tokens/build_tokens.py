#!/usr/bin/env python3
"""Generate platform integration files from orion-type-presets.json (single source of truth for type tokens)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); INT = os.path.dirname(HERE)
T = json.load(open(os.path.join(HERE, 'orion-type-presets.json')))
PLATFORMS = ['tv', 'desktop', 'tablet', 'mobile']
NAMES = list(T['tv'])


def kebab(n):
    return ''.join('-' + c.lower() if c.isupper() else c for c in n).replace('-x-l', '-xl')


def w(path, text):
    p = os.path.join(INT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)


# ------------------------------------------------------------------ CSS
css = ['/* Orion — web integration. Generated from tokens/orion-type-presets.json by tokens/build_tokens.py. */', '',
       '/* 1. Variable font (Chromium >= 62, Safari >= 11, Firefox >= 62; Tizen >= 6.5, webOS >= 5). */',
       "@font-face {\n  font-family: 'Orion';\n  src: url('../../fonts/variable/Orion-VF.woff2') format('woff2-variations'),\n       url('../../fonts/variable/Orion-VF.woff2') format('woff2'),\n       url('../../fonts/variable/Orion-VF.ttf') format('truetype');\n"
       "  font-weight: 100 900;\n  font-stretch: 75% 125%;\n  font-style: normal;\n  font-display: swap;\n}", '',
       '/* 2. Static fallback family for engines without variable-font support (webOS 3-4, Tizen <= 6.0, old Android WebView). */']
for wgt, st in ((300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold'), (900, 'Black')):
    css.append("@font-face {\n  font-family: 'Orion Static';\n  src: url('../../fonts/webfonts/Orion-%s.woff2') format('woff2'),\n       url('../../fonts/static/Orion/Orion-%s.ttf') format('truetype');\n  font-weight: %d;\n  font-style: normal;\n  font-display: swap;\n}" % (st, st, wgt))
for wgt, st in ((600, 'SemiBold'), (700, 'Bold')):
    css.append("@font-face {\n  font-family: 'Orion Display Static';\n  src: url('../../fonts/webfonts/OrionDisplay-%s.woff2') format('woff2');\n  font-weight: %d;\n  font-style: normal;\n  font-display: swap;\n}" % (st, wgt))
css += ['', ':root {', "  --orion-font: 'Orion Static', system-ui, -apple-system, 'Segoe UI', Roboto, 'Noto Sans', sans-serif;",
        "  --orion-font-display: 'Orion Display Static', 'Orion Static', system-ui, sans-serif;",
        '  --orion-grade: 0;            /* -50..100: raise on bright video, lower on OLED dark UI */', '}',
        "@supports (font-variation-settings: 'wght' 400) {", "  :root {", "    --orion-font: 'Orion', system-ui, -apple-system, 'Segoe UI', Roboto, 'Noto Sans', sans-serif;",
        "    --orion-font-display: 'Orion', system-ui, sans-serif;", '  }', '}', '',
        '.orion { font-family: var(--orion-font); font-optical-sizing: auto; font-kerning: normal; text-rendering: optimizeLegibility; -webkit-font-smoothing: antialiased; }',
        '.orion-tnum { font-variant-numeric: tabular-nums; }', '.orion-zero { font-feature-settings: "zero" 1; }', '.orion-case { font-feature-settings: "case" 1; }',
        '.orion-frac { font-variant-numeric: diagonal-fractions; }', '.orion-ss01 { font-feature-settings: "ss01" 1; }   /* serifed I */',
        '.orion-ss02 { font-feature-settings: "ss02" 1; }   /* plain l */', '.orion-ss03 { font-feature-settings: "ss03" 1; }   /* single-storey a */',
        '.orion-condensed { font-stretch: 75%; }', '.orion-extended { font-stretch: 125%; }', '']


def css_rule(sel, p, display):
    feat = "\n  font-variant-numeric: tabular-nums;" if 'tnum' in p['features'] else ''
    fam = 'var(--orion-font-display)' if display else 'var(--orion-font)'
    return ("%s {\n  font-family: %s;\n  font-size: %gpx;\n  line-height: %gpx;\n  font-weight: %d;\n  font-stretch: %d%%;\n  letter-spacing: %gem;\n"
            "  font-variation-settings: 'opsz' %g, 'GRAD' calc(var(--orion-grade) + %d);%s\n}" %
            (sel, fam, p['fontSize'], p['lineHeight'], p['wght'], p['wdth'], p['letterSpacing'], min(72, max(10, p['opsz'])), p['GRAD'], feat))


for plat in PLATFORMS:
    css.append('/* ---- %s presets (%s) ---- */' % (plat, T['meta']['canvas'][plat]))
    for n in NAMES:
        css.append(css_rule('.orion-%s-%s' % (plat, kebab(n)), T[plat][n], n.startswith(('display', 'headline'))))
    css.append('')
css += ['/* Responsive aliases: .orion-<token> picks the platform preset from the viewport (TV apps should use .orion-tv-* directly). */']
for n in NAMES:
    css.append(css_rule('.orion-%s' % kebab(n), T['mobile'][n], n.startswith(('display', 'headline'))))
css.append('@media (min-width: 600px) {')
for n in NAMES:
    css.append('  ' + css_rule('.orion-%s' % kebab(n), T['tablet'][n], n.startswith(('display', 'headline'))).replace('\n', '\n  '))
css.append('}\n@media (min-width: 1024px) {')
for n in NAMES:
    css.append('  ' + css_rule('.orion-%s' % kebab(n), T['desktop'][n], n.startswith(('display', 'headline'))).replace('\n', '\n  '))
css.append('}')
css += ['', '/* Subtitles: never rely on the font alone — always add a scrim or outline (see ACCESSIBILITY.md). */',
        '.orion-subtitle-box { display: inline; padding: 0.08em 0.4em; background: rgba(0, 0, 0, 0.75); color: #fff; box-decoration-break: clone; -webkit-box-decoration-break: clone; }', '']
w('css/orion.css', '\n'.join(css))

# ------------------------------------------------------------------ React / TypeScript
ts = ['// Orion type presets for React (web, React Native Web, TV web apps). Generated — edit tokens/orion-type-presets.json.',
      "import type { CSSProperties } from 'react';", '',
      "export type OrionPlatform = 'tv' | 'desktop' | 'tablet' | 'mobile';",
      'export type OrionToken = ' + ' | '.join("'%s'" % n for n in NAMES) + ';', '',
      'export interface OrionPreset { fontSize: number; lineHeight: number; letterSpacing: number; wght: number; wdth: number; opsz: number; GRAD: number; features: string; usage: string; minSize: number; }', '',
      'export const orionPresets: Record<OrionPlatform, Record<OrionToken, OrionPreset>> = ' + json.dumps({p: T[p] for p in PLATFORMS}, indent=2) + ';', '',
      '/** Inline style for a preset. `grade` (-50..100) shifts GRAD without changing layout. */',
      'export function orionStyle(platform: OrionPlatform, token: OrionToken, grade = 0): CSSProperties {',
      '  const p = orionPresets[platform][token];',
      '  return {',
      "    fontFamily: \"'Orion', 'Orion Static', system-ui, sans-serif\",",
      '    fontSize: p.fontSize, lineHeight: `${p.lineHeight}px`, fontWeight: p.wght, fontStretch: `${p.wdth}%`,',
      '    letterSpacing: `${p.letterSpacing}em`,',
      "    fontVariationSettings: `'opsz' ${Math.min(72, Math.max(10, p.opsz))}, 'GRAD' ${p.GRAD + grade}`,",
      "    fontVariantNumeric: p.features.includes('tnum') ? 'tabular-nums' : undefined,",
      '  };', '}', '']
w('react/orionTypography.ts', '\n'.join(ts))
w('react/OrionText.tsx', '''// Minimal text component using the Orion presets.
import React from 'react';
import { orionStyle, OrionPlatform, OrionToken } from './orionTypography';

export interface OrionTextProps extends React.HTMLAttributes<HTMLSpanElement> {
  token: OrionToken;
  platform?: OrionPlatform;
  /** -50..100. Raise over bright video or for focused items instead of changing weight: layout does not move. */
  grade?: number;
  as?: keyof JSX.IntrinsicElements;
}

export function OrionText({ token, platform = 'tv', grade = 0, as: Tag = 'span', style, ...rest }: OrionTextProps) {
  const Any = Tag as any;
  return <Any style={{ ...orionStyle(platform, token, grade), ...style }} {...rest} />;
}

// Focus without reflow: the focused card keeps its width because only GRAD changes.
export function RowTitle({ focused, children }: { focused: boolean; children: React.ReactNode }) {
  return <OrionText token="titleL" grade={focused ? 80 : 0}>{children}</OrionText>;
}

// Playback clock: tabular figures, and the colon centres on the digits through the font's calt feature.
export function Clock({ value }: { value: string }) {
  return <OrionText token="numeric">{value}</OrionText>;
}
''')

# ------------------------------------------------------------------ Android (phone / tablet / Android TV / Fire TV)
def kt_style(n, p, sp=True):
    unit = '.sp'
    return ('    val %s = TextStyle(fontFamily = OrionFont.variable(weight = %d, width = %df, opticalSize = %gf, grade = %d),\n'
            '        fontSize = %g%s, lineHeight = %g%s, letterSpacing = %g.em%s)' %
            (n, p['wght'], p['wdth'], min(72, max(10, p['opsz'])), p['GRAD'], p['fontSize'], unit, p['lineHeight'], unit, p['letterSpacing'],
             ', fontFeatureSettings = "tnum"' if 'tnum' in p['features'] else ''))


kt = ['// Orion for Jetpack Compose (phone, tablet, Android TV, Fire TV). Generated — edit tokens/orion-type-presets.json.',
      '// Variable axes need API 26+. On API < 26 Compose falls back to the static files listed in res/font/orion.xml.',
      'package com.example.orion', '',
      'import android.os.Build', 'import androidx.compose.ui.text.ExperimentalTextApi', 'import androidx.compose.ui.text.TextStyle',
      'import androidx.compose.ui.text.font.Font', 'import androidx.compose.ui.text.font.FontFamily', 'import androidx.compose.ui.text.font.FontVariation',
      'import androidx.compose.ui.text.font.FontWeight', 'import androidx.compose.ui.unit.em', 'import androidx.compose.ui.unit.sp', '',
      'object OrionFont {',
      '    private val static = FontFamily(',
      '        Font(R.font.orion_light, FontWeight.Light), Font(R.font.orion_regular, FontWeight.Normal), Font(R.font.orion_medium, FontWeight.Medium),',
      '        Font(R.font.orion_semibold, FontWeight.SemiBold), Font(R.font.orion_bold, FontWeight.Bold), Font(R.font.orion_black, FontWeight.Black))', '',
      '    @OptIn(ExperimentalTextApi::class)',
      '    fun variable(weight: Int, width: Float = 100f, opticalSize: Float = 14f, grade: Int = 0): FontFamily =',
      '        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) FontFamily(',
      '            Font(R.font.orion_vf, weight = FontWeight(weight), variationSettings = FontVariation.Settings(',
      '                FontVariation.weight(weight), FontVariation.width(width),',
      '                FontVariation.Setting("opsz", opticalSize), FontVariation.grade(grade))))',
      '        else static', '}', '']
for plat, note in (('Tv', 'Android TV / Fire TV: values are sp on a 960x540 dp canvas (= px / 2 at 1080p)'), ('Mobile', 'phones'), ('Tablet', 'tablets')):
    src = T[plat.lower()]
    kt.append('/** %s */' % note)
    kt.append('object Orion%sType {' % plat)
    for n in NAMES:
        p = dict(src[n])
        if plat == 'Tv':
            p['fontSize'] = p['fontSize'] / 2; p['lineHeight'] = p['lineHeight'] / 2
        kt.append(kt_style(n, p))
    kt.append('}\n')
w('android/OrionTypography.kt', '\n'.join(kt))
w('android/res/font/orion.xml', '''<?xml version="1.0" encoding="utf-8"?>
<!-- Static family for View-based UI and for API < 26. Copy fonts/static/Orion/*.ttf to res/font/ with lowercase names. -->
<font-family xmlns:app="http://schemas.android.com/apk/res-auto">
    <font app:fontStyle="normal" app:fontWeight="300" app:font="@font/orion_light" />
    <font app:fontStyle="normal" app:fontWeight="400" app:font="@font/orion_regular" />
    <font app:fontStyle="normal" app:fontWeight="500" app:font="@font/orion_medium" />
    <font app:fontStyle="normal" app:fontWeight="600" app:font="@font/orion_semibold" />
    <font app:fontStyle="normal" app:fontWeight="700" app:font="@font/orion_bold" />
    <font app:fontStyle="normal" app:fontWeight="900" app:font="@font/orion_black" />
</font-family>
''')
w('android/res/font/orion_variable.xml', '''<?xml version="1.0" encoding="utf-8"?>
<!-- API 26+: one variable file (res/font/orion_vf.ttf = fonts/variable/Orion-VF.ttf) addressed per weight. -->
<font-family xmlns:android="http://schemas.android.com/apk/res/android">
    <font android:fontStyle="normal" android:fontWeight="300" android:font="@font/orion_vf" android:fontVariationSettings="'wght' 300, 'opsz' 14" />
    <font android:fontStyle="normal" android:fontWeight="400" android:font="@font/orion_vf" android:fontVariationSettings="'wght' 400, 'opsz' 14" />
    <font android:fontStyle="normal" android:fontWeight="500" android:font="@font/orion_vf" android:fontVariationSettings="'wght' 500, 'opsz' 14" />
    <font android:fontStyle="normal" android:fontWeight="600" android:font="@font/orion_vf" android:fontVariationSettings="'wght' 600, 'opsz' 14" />
    <font android:fontStyle="normal" android:fontWeight="700" android:font="@font/orion_vf" android:fontVariationSettings="'wght' 700, 'opsz' 14" />
    <font android:fontStyle="normal" android:fontWeight="900" android:font="@font/orion_vf" android:fontVariationSettings="'wght' 900, 'opsz' 14" />
</font-family>
''')
w('android/README.md', '''# Orion on Android, Android TV / Google TV and Fire TV

| Target | Files | API |
|---|---|---|
| Compose, API 26+ | `fonts/variable/Orion-VF.ttf` as `res/font/orion_vf.ttf` + `OrionTypography.kt` | `FontVariation.Settings` (wght, wdth, opsz, GRAD) |
| Views, API 26+ | `res/font/orion_variable.xml`, or `TextView.setFontVariationSettings("'wght' 600, 'GRAD' 40")` | `fontVariationSettings` |
| API 21-25, Fire OS 5 | `fonts/static/Orion/*.ttf` + `res/font/orion.xml` | static files only |

Notes
- `android:includeFontPadding="false"` (Views) or `PlatformTextStyle(includeFontPadding = false)` (Compose) gives predictable
  boxes; Orion's ascent / descent (1000 / -250) already contain stacked Vietnamese capitals.
- Tabular figures: `fontFeatureSettings = "tnum"`. Slashed zero: `"zero"`. Features combine: `"tnum, zero"`.
- TV: author on the 960 x 540 dp canvas. `OrionTvType` holds the TV presets in sp (TV density makes 1 sp = 2 px at 1080p).
- Fire TV runs Fire OS (Android based); Fire OS 6+ (API 25/28) behaves like the table above. Not verified on hardware — see QA-REPORT.md.
''')

# ------------------------------------------------------------------ Apple (iOS, iPadOS, tvOS)
sw = ['// Orion for UIKit / SwiftUI on iOS, iPadOS and tvOS. Generated — edit tokens/orion-type-presets.json.',
      '// Add fonts/variable/Orion-VF.ttf to the target and list it under UIAppFonts ("Fonts provided by application").',
      '// Reference code written against the platform documentation; it has not been compiled. Feature keys need iOS / tvOS 15.',
      'import UIKit', 'import SwiftUI', 'import CoreText', '',
      'public enum OrionAxis { static let wght = 0x77676874, wdth = 0x77647468, opsz = 0x6F70737A, grad = 0x47524144 }   // four-char tags as integers', '',
      'public struct OrionPreset { public let size: CGFloat, lineHeight: CGFloat, tracking: CGFloat, wght: CGFloat, wdth: CGFloat, opsz: CGFloat, grad: CGFloat, tabular: Bool }', '',
      'public enum Orion {',
      '    /// Variable instance. `grade` is added to the preset grade and never changes advance widths.',
      '    public static func font(size: CGFloat, wght: CGFloat = 400, wdth: CGFloat = 100, opsz: CGFloat? = nil, grad: CGFloat = 0, tabular: Bool = false) -> UIFont {',
      '        let variation: [Int: CGFloat] = [OrionAxis.wght: wght, OrionAxis.wdth: wdth, OrionAxis.opsz: min(72, max(10, opsz ?? size)), OrionAxis.grad: grad]',
      '        var attrs: [UIFontDescriptor.AttributeName: Any] = [.name: "Orion-Regular", UIFontDescriptor.AttributeName(rawValue: kCTFontVariationAttribute as String): variation]',
      '        if tabular {',
      '            attrs[.featureSettings] = [[UIFontDescriptor.FeatureKey.type: kNumberSpacingType, UIFontDescriptor.FeatureKey.selector: kMonospacedNumbersSelector]]',
      '        }',
      '        return UIFont(descriptor: UIFontDescriptor(fontAttributes: attrs), size: size)',
      '    }', '',
      '    /// Dynamic Type: scales the preset with the user setting (iOS / iPadOS). tvOS has no Dynamic Type; use the tv presets as they are.',
      '    public static func scaled(_ p: OrionPreset, style: UIFont.TextStyle = .body, grade: CGFloat = 0) -> UIFont {',
      '        let base = font(size: p.size, wght: p.wght, wdth: p.wdth, opsz: p.opsz, grad: p.grad + grade, tabular: p.tabular)',
      '        #if os(tvOS)', '        return base', '        #else', '        return UIFontMetrics(forTextStyle: style).scaledFont(for: base)', '        #endif',
      '    }', '}', '']
for plat in ('tv', 'tablet', 'mobile'):
    sw.append('public enum Orion%s {' % plat.capitalize())
    for n in NAMES:
        p = T[plat][n]
        sw.append('    public static let %s = OrionPreset(size: %g, lineHeight: %g, tracking: %g, wght: %d, wdth: %d, opsz: %g, grad: %d, tabular: %s)' %
                  (n, p['fontSize'], p['lineHeight'], p['letterSpacing'] * p['fontSize'], p['wght'], p['wdth'], min(72, max(10, p['opsz'])), p['GRAD'], 'true' if 'tnum' in p['features'] else 'false'))
    sw.append('}\n')
sw += ['public extension Text {', '    /// SwiftUI: `Text("Continue Watching").orion(OrionTv.headlineM)`',
       '    func orion(_ p: OrionPreset, grade: CGFloat = 0) -> some View {',
       '        self.font(Font(Orion.scaled(p, grade: grade))).tracking(p.tracking).lineSpacing(p.lineHeight - p.size * 1.25)', '    }', '}', '']
w('ios/OrionFont.swift', '\n'.join(sw))
w('ios/README.md', '''# Orion on iOS, iPadOS and tvOS

1. Add `fonts/variable/Orion-VF.ttf` to the app target; add it to `UIAppFonts` in Info.plist.
2. Use `OrionFont.swift`: `Orion.font(size:wght:wdth:opsz:grad:)` builds a Core Text variation instance;
   `OrionMobile`, `OrionTablet` and `OrionTv` hold the presets.
3. Optical size is not applied automatically for custom fonts: the helper sets `opsz` from the point size.
4. tvOS: values are points on the 1920 x 1080 canvas. Focus: raise `grade` by 60-80 on the focused item instead of
   switching weight, so focus engine animations do not reflow titles.
5. If you must support a system that refuses the variable file, bundle `fonts/static/Orion/*.ttf` and
   `fonts/static/OrionDisplay/*.ttf` and select by PostScript name (`Orion-SemiBold`, `OrionDisplay-Bold`, ...).

Not verified on Apple hardware in this build — see QA-REPORT.md.
''')

# ------------------------------------------------------------------ TV platforms
rk = T['tv']
brs = ["' Orion on Roku (SceneGraph). Roku loads packaged TrueType / OpenType files through the Font node.",
       "' It exposes no variable-axis or OpenType-feature controls, so ship static files:",
       "'   pkg:/fonts/Orion-Regular.ttf, Orion-Medium.ttf, Orion-SemiBold.ttf, Orion-Bold.ttf   (fonts/static/Orion)",
       "'   pkg:/fonts/OrionDisplay-Bold.ttf, OrionDisplay-SemiBold.ttf                          (fonts/static/OrionDisplay)",
       "' Sizes below are for an FHD (1920x1080) manifest: ui_resolutions=fhd. For HD manifests multiply by 0.667.", '',
       'function OrionFont(token as string) as object', '    presets = {']
wmap = {300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold', 900: 'Black'}
for n in NAMES:
    p = rk[n]
    fam = 'OrionDisplay' if p['opsz'] >= 44 else 'Orion'
    brs.append('        %s: { uri: "pkg:/fonts/%s-%s.ttf", size: %d, lineHeight: %d }' % (n, fam, wmap[p['wght']], p['fontSize'], p['lineHeight']))
brs += ['    }', '    p = presets[token]', '    font = CreateObject("roSGNode", "Font")', '    font.uri = p.uri', '    font.size = p.size', '    return font', 'end function', '',
        "' usage:  m.title.font = OrionFont(\"headlineM\")", "' Timers: Roku cannot switch on tnum, so the proportional figures are used; reserve the box width for the widest value",
        "' (all Orion figures except 1 share one advance) or draw timers with a tabular build made by `pyftfeatfreeze`-style baking.", '']
w('tv-platforms/roku/OrionFonts.brs', '\n'.join(brs))
w('tv-platforms/roku/Label-example.xml', '''<?xml version="1.0" encoding="utf-8"?>
<component name="OrionRowTitle" extends="Group">
  <children>
    <Label id="title" text="Continue Watching" color="0xF2F2F2FF" translation="[96, 120]">
      <Font role="font" uri="pkg:/fonts/Orion-SemiBold.ttf" size="44" />
    </Label>
    <Label id="meta" text="2024 • 2h 35m • TV-MA" color="0xB3B8C2FF" translation="[96, 184]">
      <Font role="font" uri="pkg:/fonts/Orion-Medium.ttf" size="24" />
    </Label>
  </children>
</component>
''')
w('tv-platforms/web-tv/orion-tv.css', '''/* Orion for Samsung Tizen and LG webOS web apps (1920 x 1080 CSS px).
   Variable fonts: Tizen 6.5+ (2022), webOS 5+ (2020, Chromium 68). Older sets get the static family through
   the @supports switch in integration/css/orion.css — include that file first. */
@import url('../../css/orion.css');

html { font-size: 28px; }                      /* body M on the TV canvas */
body { margin: 0; background: #0B0D12; color: #F2F2F2; font-family: var(--orion-font); }

/* Old engines (webOS 3-4 = Chromium 38 / 53) do not know woff2-variations or font-display: keep TTF last in src. */

.row-title   { }                               /* use class="orion-tv-headline-m" */
.card-title  { }                               /* use class="orion-tv-title-l" */
.meta        { color: #B3B8C2; }               /* use class="orion-tv-metadata" */

/* Focus: change grade and colour, not weight — width stays identical, so rows never reflow under D-pad navigation. */
.focusable { transition: color 120ms linear; }
.focusable:focus, .focusable.is-focused { --orion-grade: 80; color: #0B0D12; background: #F2F2F2; outline: 4px solid #4DA3FF; outline-offset: 4px; }

/* 720p panels and 4K UI planes: scale the whole canvas, not individual tokens. */
@media (max-height: 720px) { html { zoom: 0.6667; } }
@media (min-height: 2160px) { html { zoom: 2; } }
''')
w('tv-platforms/README.md', '''# Orion on television platforms

| Platform | Font delivery | Variable axes | OpenType features | What to ship |
|---|---|---|---|---|
| Android TV / Google TV | app resource (`res/font`) | API 26+ (`fontVariationSettings`) | `fontFeatureSettings` | `Orion-VF.ttf`; statics for API < 26 |
| Fire TV (Fire OS 6+) | app resource | as Android of the same API level | as Android | `Orion-VF.ttf` + statics |
| Apple TV (tvOS 11+) | app bundle, `UIAppFonts` | Core Text variation attribute | Core Text feature settings | `Orion-VF.ttf` |
| Samsung Tizen web apps | `@font-face` (packaged or CDN) | Tizen 6.5+ (2022 sets) | `font-feature-settings` | WOFF2 variable + static fallback |
| LG webOS web apps | `@font-face` | webOS 5+ (Chromium 68); not on webOS 3-4 | `font-feature-settings` | WOFF2 variable + static TTF/WOFF2 fallback |
| Roku (SceneGraph) | `Font` node, packaged TTF/OTF | no | no control exposed | static TTF only |

Sources for the support columns are listed in `docs/OVERVIEW.md`; the evidence per platform is in `docs/QA-REPORT.md`, section D. None of these rows was verified
on physical hardware in this build; they describe documented platform behaviour plus software-renderer tests.

Files
- `web-tv/orion-tv.css` — Tizen / webOS (and any HTML5 TV app).
- `roku/OrionFonts.brs`, `roku/Label-example.xml` — Roku.
- Android TV / Fire TV: `../android/OrionTypography.kt` (`OrionTvType`).
- tvOS: `../ios/OrionFont.swift` (`OrionTv`).

Constrained devices: ship `Orion-Regular`, `Orion-Medium`, `Orion-SemiBold`, `Orion-Bold` and `OrionDisplay-Bold`
(about 0.9 MB as TTF, 0.33 MB as WOFF2). Add script subsets only for the markets you serve (`fonts/subsets`).
''')
print('integration files generated')
