# Orion integration

`tokens/orion-type-presets.json` is the single source of truth for the type scale. Run `python3 tokens/build_tokens.py` after
editing it; the script regenerates every file below.

| Folder | Files | Platform |
|---|---|---|
| `css/` | `orion.css` | Web, and the base for TV web apps: variable `@font-face`, static fallback, preset classes, feature utilities |
| `react/` | `orionTypography.ts`, `OrionText.tsx` | React on any web target |
| `android/` | `OrionTypography.kt`, `res/font/*.xml`, README | Phone, tablet, Android TV, Google TV, Fire TV |
| `ios/` | `OrionFont.swift`, README | iOS, iPadOS, tvOS |
| `tv-platforms/` | `web-tv/orion-tv.css`, `roku/`, README | Tizen, webOS, Roku, with a support matrix |

The samples are reference code. They were written against the platform documentation and were not compiled or run on devices.
