# Orion on Android, Android TV / Google TV and Fire TV

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
