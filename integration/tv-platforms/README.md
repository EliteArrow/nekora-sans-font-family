# Orion on television platforms

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
