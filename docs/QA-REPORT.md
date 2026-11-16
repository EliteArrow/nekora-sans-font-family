# Orion — QA report

Version 1.000. Everything in sections A–C is produced by scripts in `qa/` run against the shipped binaries in `fonts/`.
Rerun with `python3 qa/run_all.py`; machine-readable results are in `qa/reports/*.json` and the generated summary is
`qa/reports/QA-SUMMARY.md`. Section D separates what was tested from what was not.

## A. Result summary

| Suite | Script | PASS | WARN | FAIL | SKIP |
|---|---|---:|---:|---:|---:|
| Integrity | `qa_integrity.py` | 806 | 0 | 0 | 0 |
| Interpolation | `qa_interpolation.py` | 14 | 1 | 0 | 0 |
| Shaping | `qa_shaping.py` | 74 | 0 | 0 | 1 |
| Unicode | `qa_unicode.py` | 51 | 0 | 0 | 0 |
| Rendering | `qa_rendering.py` | 25 | 0 | 0 | 0 |
| Accessibility | `qa_accessibility.py` | 45 | 7 | 0 | 0 |
| Performance | `qa_performance.py` | 7 | 0 | 0 | 0 |
| **Total** | | **1,022** | **8** | **0** | **1** |

FontBakery 1.1.0, universal profile:

| Target | Fonts | PASS | WARN | FAIL | ERROR | SKIP |
|---|---:|---:|---:|---:|---:|---:|
| Orion-VF.ttf | 1 | 102 | 2 | 0 | 0 | 19 |
| Orion static TTF | 9 | 670 | 15 | 0 | 0 | 326 |
| Orion Display static TTF | 9 | 676 | 18 | 0 | 0 | 326 |
| Orion Condensed static TTF | 9 | 679 | 15 | 0 | 0 | 326 |
| Orion static OTF | 9 | 595 | 9 | 0 | 0 | 407 |

SKIP in FontBakery means the check does not apply (for example italic or CJK checks).

## B. What each suite checks

**Integrity (806).** For the 37 TrueType and OpenType files (variable, 27 static TTF, 9 static OTF): the OpenType Sanitizer
accepts the file; table checksums are correct; required tables are present and every table decompiles; `.notdef` is glyph 0;
every character-map target exists; glyph names are unique; no advance is negative; glyph bounds are sane; names, PostScript
names and style linking are valid; `fsType` is 0; typo and `hhea` metrics are equal, `USE_TYPO_METRICS` is set and win metrics
cover the glyph bounds; the file loads in FreeType and HarfBuzz; the variable font has the four axes, their ranges, 27 named
instances and a matching `STAT`. For the 28 WOFF2 files: sanitiser, and decompression to the same tables and outlines as the
source TTF. For the 6 `unicode-range` subsets: sanitiser, all four axes kept, and sample text from the subset's own range shapes
without `.notdef`. Installed statics resolve through fontconfig.

**Interpolation (15).** `fontTools.varLib.interpolatable` reports no structural incompatibility across the 21 masters.
At 91 designspace locations, including all 16 corners, each of 888 outline glyphs is instantiated, overlaps are removed, and the
count of outer contours and counters is compared with the default: stable everywhere. Counter area never drops below 1,200
square units. Ink area rises monotonically with weight; advances rise monotonically with width. Weight is not emboldening
(stem × 7.3 while advance × 1.06); width is not scaling (round width × 1.51 while stem × 1.12 from narrowest to widest); optical
size changes x-height, stem and spacing together; grade changes the stem (80 → 104) and leaves every advance and kerning value
unchanged at 6 base locations × 5 grades. 2,704 letter pairs show no collision at 8 extreme locations with kerning applied.

**Shaping (75).** HarfBuzz tests of kerning (17 reference pairs, magnitudes, untouched straight pairs, the opened `r n` pair,
kerning at five variable locations, Greek and Cyrillic pairs), mark attachment and stacked marks, decomposed versus precomposed
Vietnamese, dotless `i j`, every GSUB feature in FONT-SPECIFICATIONS.md, language-specific forms (`ROM`, `MOL`, `CAT`, `SRB`,
`MKD`), the 23 interface strings from the brief and 21 language samples (no `.notdef`, no zero-width or overlapping clusters).

**Unicode (51).** Character repertoires of 41 languages against the character map; the 20 required repertoires are complete.
Block and script manifest written to `qa/unicode/`.

**Rendering (25).** FreeType rasterisation of static files in three modes (unhinted, hinted, light): counters of 17 critical
glyphs stay open from the documented size per weight; stems of `H I L l` are consistent to within 0.75 px; the variable font
rasterises at 63 locations × 3 sizes; language samples do not clip outside ascent 1000 / descent −250; 54 visual-regression
baselines (`qa/rendering/baseline/`) match the previous run byte for byte.

**Accessibility (52).** Confusable pairs under simulated blur, viewing-distance geometry of the TV presets, WCAG contrast of the
specimen palette, line-height floors and WCAG 1.4.12 text-spacing checks. Details and tables: ACCESSIBILITY.md.

**Performance (7).** File sizes (variable TTF 766 KB, variable WOFF2 308 KB, Latin subset 135 KB, static WOFF2 at most 65 KB),
outline complexity (mean 24 points per simple glyph, maximum 100), HarfBuzz shaping throughput above 100,000 glyphs per second
and FreeType rasterisation above 5,000 glyphs per second at a variable instance, measured in this build container
(not on TV hardware).

## C. Open items

### Warnings from the Orion suites (8)

1. **Slivers after overlap removal (interpolation).** In six Vietnamese capitals with circumflex or breve plus hook above
   (`Ẩ Ẳ Ể Ổ` and the two `.case` mark stacks), removing overlaps at some instances leaves fragments of 13–94 square units
   where the hook touches the lower mark. They are invisible at interface sizes. The static build drops fragments under 250
   square units; the variable font keeps overlaps and is not affected.
2. **Seven TV presets under the viewing-angle floor (accessibility).** bodyL 9.9, bodyM 9.3, labelL 9.9, labelM 9.3, numeric 9.3
   against a floor of 10 arc-minutes; caption and metadata 7.9 against 9. These are the sizes of the presets, not a defect of the
   outlines. ACCESSIBILITY.md treats these presets as minimums and recommends a text-size setting.

### Skipped (1)

- **Bidirectional text.** Orion has no right-to-left script, so there is nothing to test.

### FontBakery warnings (accepted)

| Check | Where | Explanation |
|---|---|---|
| `mandatory_avar_table` | variable font | No `avar`: the weight axis maps linearly to the masters. Stems at each named weight are listed in VARIABLE-AXES.md |
| `overlapping_path_segments` | variable font | The variable font keeps overlapping contours by design and flags them |
| `overlapping_path_segments` | static TTF | Overlap removal leaves a few zero-length segments in `k K 6` and glyphs built from them. They do not render |
| `contour_count` | static TTF | A heuristic comparing contour counts with typical fonts. Orion draws `β`, `₩`, `₱` and a few others with a different, valid number of contours |
| `unreachable_glyphs` | static OTF | Mark glyphs reached only through GPOS anchors are reported by this check for CFF builds |

### Defects found by QA during development and fixed

Thin bowls vanishing at Thin Extended Display; `ß` and `β` with detached strokes; percent zeros drawn at full weight; a
contour-direction flip in `э`; grade altering advances; chevrons overhanging; ogonek detached on `ę ǫ Ų`; fractions colliding
with the bar in heavy weights; `£` with a broken hook in Bold and Black; `@`, `Ŀ`, `⌫` and breve stacks merging at the
Black Condensed Display corner; stubby terminals on Black `S s 3 5`; non-monotonic line length across weight; Black `a e`
counters closing at small sizes; static fonts failing FontBakery on underline thickness and `fsSelection`. Each is covered by a
test that now passes.

## D. Device and platform compatibility

Nothing in this project was tested on physical hardware. The table states exactly what kind of evidence exists.

| Platform | Evidence | Status |
|---|---|---|
| Chromium (desktop, headless, version shipped with Playwright 1.63) | All specimens rendered from the variable WOFF2 with all four axes, kerning and features | **Verified in software** |
| FreeType 2 (hinted, unhinted, light) | Rendering suite on static and variable files | **Verified in software** |
| HarfBuzz | Shaping suite | **Verified in software** |
| OTS (the sanitiser used by Chromium and Firefox) | All 71 font files accepted | **Verified in software** |
| Android, Android TV, Google TV (API 26+) | Android text uses FreeType and HarfBuzz, which were tested here; variable-font APIs exist from API 26 | **Expected to work; not run on a device or emulator** |
| Fire TV | Android-based; same reasoning | **Untested** |
| iOS, iPadOS, tvOS, macOS (Core Text) | No Apple renderer was available. Core Text has its own rasteriser, variation handling and overlap treatment | **Untested** |
| Windows (DirectWrite, GDI) | No Windows renderer was available. Static TTFs are autohinted for it | **Untested** |
| Samsung Tizen web apps | Not run. Samsung's specification page lists Chromium M63 for 2019 sets up to M130 for 2026, and appears to list `font-variation-settings` from Tizen 6.5 (2022) | **Untested; static fallback provided for older sets** |
| LG webOS web apps | Not run. LG lists Chromium 38 for webOS 3.x, 53 for 4.x, 68 for 5.x, 79 for 6.x, 87 for webOS 22, 94 for 23, 108 for 24. Variable fonts arrived in Chromium 62, so webOS 5 and later should support them | **Untested; static fallback provided for webOS 3–4** |
| Roku | Not run. Roku's `Font` node loads TrueType or OpenType files packaged with the app and exposes only `uri` and `size`, so static files are used | **Untested** |
| Physical panels (LCD, OLED, 720p to 4K, sharpening, overscan) | None | **Untested** |

Sources for the platform facts are listed in OVERVIEW.md.

Before release on any platform: install the fonts on at least one device per platform and model year tier, view the specimen
pages in `specimens/html/` (web platforms) or a build of the integration samples, and check the smallest presets, the Black
weight, subtitles over video, and the Vietnamese, Greek and Cyrillic samples.

## E. Reproducibility

A clean rebuild from `sources/build-scripts` into an empty directory produced a variable font whose tables are byte-identical
to the shipped file except `head` (timestamp and checksum).
