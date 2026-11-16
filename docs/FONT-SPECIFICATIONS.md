# Orion — font specifications

Version 1.000. All numbers in this file are read from the binaries in `fonts/`.

## Identity

| Field | Value |
|---|---|
| Family name | Orion |
| Sub-families cut as statics | Orion (text), Orion Display, Orion Condensed |
| Version | 1.000 |
| Vendor ID | `ORIN` (placeholder, not registered with Microsoft) |
| Designer / manufacturer strings | The Orion Project Authors (parametric design generated with Claude) / The Orion Project |
| Licence string | SIL Open Font License 1.1 (see LICENSE.md, including the note on the name) |
| Embedding (`fsType`) | 0, installable embedding |
| Classification | Sans-serif, geometric with humanist corrections |

## Files

| Path | Format | Count | Size | Use |
|---|---|---:|---|---|
| `fonts/variable/Orion-VF.ttf` | Variable TrueType, 4 axes | 1 | 766 KB | Apps: Android, Apple platforms, desktop |
| `fonts/variable/Orion-VF.woff2` | WOFF2 of the above | 1 | 308 KB | Web, Tizen, webOS |
| `fonts/static/Orion/` | Static TrueType, autohinted | 9 | 175–177 KB each | Roku, old Android, engines without variable support |
| `fonts/static/OrionDisplay/` | Static TrueType, opsz 72 | 9 | 175–178 KB each | Titles on static-only platforms |
| `fonts/static/OrionCondensed/` | Static TrueType, wdth 75 | 9 | 174–177 KB each | Dense rails on static-only platforms |
| `fonts/static-otf/` | Static OpenType CFF (text family) | 9 | 154–155 KB each | Design tools, print |
| `fonts/webfonts/` | WOFF2 of the 27 static TrueType files | 27 | 63–65 KB each | Web fallback |
| `fonts/subsets/<script>/` | Variable WOFF2 per script, all four axes kept | 6 files | Latin 135 KB, Latin Extended 78 KB, Vietnamese 29 KB, Greek 45 KB, Cyrillic 71 KB, symbols 16 KB (WOFF2) | `unicode-range` loading; `orion-subsets.css` |

## Glyph set

- 899 glyphs, 774 encoded characters, 132 unencoded glyphs (alternates, small figures, tabular forms, capital punctuation and marks).
- Scripts: Latin 383 characters, Greek 71, Cyrillic 98, common symbols and punctuation 203, combining marks 19.
- Coverage by block and language: UNICODE-COVERAGE.md.

## Metrics (units per em 1000)

| Metric | Value |
|---|---:|
| Cap height (`OS/2.sCapHeight`) | 700 |
| x-height (`OS/2.sxHeight`, text master) | 522 |
| Ascender / descender of letters | 742 / −204 |
| `hhea` ascent / descent / line gap | 1000 / −250 / 0 |
| `OS/2` typo ascender / descender / line gap | 1000 / −250 / 0 |
| `OS/2` win ascent / descent | 989 / 270 |
| `USE_TYPO_METRICS` (fsSelection bit 7) | set |
| Tallest / deepest ink in any master | 986 / −267 |
| Underline position / thickness | −100 / 60 |
| Default line height | 1.25 em on every platform |

The three metric sets agree, so line height is the same in browsers, on Android, on Apple platforms and in Windows
applications. The 1.25 em default line box contains every letter, including stacked Vietnamese capitals such as `Ẩ Ỗ` (the
tallest letters reach 978) and letters with marks below. Only the integral sign and the dong sign in the heaviest weights reach
below −250 (to −267 at Black with GRAD +100); they stay inside the win descent of 270, so nothing is clipped.

## Tables

`GDEF GPOS GSUB HVAR MVAR OS/2 STAT cmap fvar gasp glyf gvar head hhea hmtx loca maxp meta name post prep`

- `gasp` requests symmetric smoothing with grid-fitting at all sizes; `prep` holds the standard instruction that enables it.
- `meta` declares design and supported languages `Latn, Grek, Cyrl`.
- The variable font is unhinted. Static TrueType files are autohinted with ttfautohint, which hints the vertical direction only
  (it aligns x-height, cap height and baselines; it does not snap vertical stems). Static OpenType CFF files are unhinted.

## OpenType features

| Tag | What it does |
|---|---|
| `kern` | Class kerning, about 8,200 pairs per master, interpolated |
| `mark`, `mkmk` | Mark-to-base and mark-to-mark attachment for 19 combining marks (including stacked marks) |
| `ccmp` | Dotless `i j` before top marks, capital mark forms, Vietnamese double-accent composition, horn handling |
| `locl` | Romanian and Moldovan `Ș ș Ț ț` in place of cedilla forms; Catalan `l·l`; Serbian and Macedonian `б` |
| `case` | Capital-height dashes, brackets, guillemets, `¿ ¡ @ ·` and colon |
| `calt` | Raises the colon between figures (`00:59:48`) |
| `tnum`, `pnum` | Tabular and proportional figures, with tabular period, comma and colon |
| `zero` | Slashed zero |
| `frac` | Arbitrary fractions from `digits/digits`, multi-digit numerators and denominators |
| `numr`, `dnom`, `sups`, `subs`, `sinf` | Small figures: numerators, denominators, superiors, inferiors |
| `ordn` | `a` and `o` directly after a figure become `ª º` |
| `ss01` | Serifed capital I |
| `ss02` | Plain l without tail |
| `ss03` | Single-storey a |

Scripts and languages declared: `DFLT`; `latn` (default, `ROM`, `MOL`, `CAT`); `grek`; `cyrl` (default, `SRB`, `MKD`).
There is no `liga` feature: no default pair collides, and interface text is often tracked. Features that the brief listed but
that would have been empty were not created. Each feature above is exercised by `qa/qa_shaping.py` with HarfBuzz.

## Naming

- Variable font: family `Orion`, style `Regular`, PostScript `Orion-Regular`, variations prefix `Orion`.
- Statics: `Orion-<Weight>`, `OrionDisplay-<Weight>`, `OrionCondensed-<Weight>` with Regular and Bold style-linked and the other
  weights carrying typographic family and sub-family names (name IDs 16 and 17), so that all nine weights group under one family in applications.

## Build toolchain

| Tool | Version | Role |
|---|---|---|
| Python | 3.13 | Parametric generator (`sources/build-scripts/orion/`) |
| ufoLib2 / defcon | 0.19.1 / 0.12.2 | UFO 3 masters |
| fontmake / ufo2ft | 3.12.2 / 3.11.0 | Compilation, feature writers for kern, mark, mkmk and GDEF |
| fontTools | 4.67.0 | varLib, instancer, subsetter, WOFF2 |
| skia-pathops | 0.9.2 | Overlap removal for statics |
| ttfautohint-py | 0.6.1 | Hinting of static TrueType files |
| uharfbuzz | 0.57.0 | Shaping tests |
| freetype-py | 2.3.0 | Rasterisation tests |
| opentype-sanitizer | 9.2.0 | OTS validation of every binary |
| FontBakery | 1.1.0 | Universal profile checks |
| Chromium via Playwright | 1.63.0 | Specimen rendering |

`python3 sources/build-scripts/build.py all` regenerates the sources and every binary; `python3 qa/run_all.py` reruns the tests.
