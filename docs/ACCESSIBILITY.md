# Orion — accessibility and legibility

A typeface cannot make an interface accessible by itself, but it sets the ceiling. This document says what Orion does for
legibility, what was measured, and what remains the product team's responsibility. Every measurement here is a software
simulation produced by `qa/qa_accessibility.py`. None of it replaces testing with viewers, including viewers with low
vision, on real televisions.

## 1. Design measures

| Need | What Orion does |
|---|---|
| Recognition at distance | x-height 0.746 of cap height at text size, rising to 0.757 at optical size 10; open apertures on `a c e s`; counters checked for a minimum area at every tested instance |
| Low-resolution and compressed rendering | Low stroke contrast, superelliptic bowls, large squircle dots, spacing that opens by 17 % at optical size 10 |
| Character confusion | Distinct `I l 1`, `O 0`, `S 5`, `B 8`, `6 9`; `r n` kerned open; optional slashed zero and serifed I |
| Light text on dark backgrounds | Regular stem 88 units (heavier than a print text face); grade axis to thin or thicken strokes without reflow |
| Text over video | `GRAD +40` subtitle preset, intended to be used with a scrim or outline |
| Numbers | Cap-height figures, tabular set, raised colon between figures |
| User overrides | No ligatures and no negative default tracking at text sizes, so WCAG 1.4.12 spacing overrides only add space |

## 2. Confusable pairs under simulated blur

Method: each pair is rasterised at 64 px, blurred to simulate 20/20, 20/40 and 20/80 acuity at the same visual angle, aligned,
and scored as 1 − normalised cross-correlation. 0 means identical shapes; higher is more distinct. The same script was run on
Inter and Roboto Flex (and on the user's licensed Gotham and Netflix Sans files) for scale; reference numbers are in
`qa/accessibility/accessibility-data.json`.

| Pair | Orion 20/20 | Orion 20/40 | Orion 20/80 | Inter 20/40 |
|---|---:|---:|---:|---:|
| I / l | 0.132 | 0.148 | 0.135 | 0.096 |
| I / 1 | 0.133 | 0.189 | 0.138 | 0.138 |
| l / 1 | 0.206 | 0.167 | 0.184 | 0.110 |
| O / 0 | 0.451 | 0.384 | 0.281 | 0.203 |
| S / 5 | 0.218 | 0.112 | 0.068 | 0.097 |
| B / 8 | 0.149 | 0.091 | 0.053 | 0.078 |
| 6 / 9 | 0.324 | 0.227 | 0.099 | 0.133 |
| rn / m | 0.106 | 0.050 | 0.042 | 0.125 |
| c / e | 0.175 | 0.149 | 0.104 | 0.123 |

Reading: Orion separates eight of the nine pairs at least as well as the median of the reference families under 20/40 blur.
**`rn / m` is the exception.** It sits at the pass threshold and is clearly weaker than Inter. The tailed `l` and narrow `0`
are the strongest results. If your content has many `rn` sequences at small sizes (`modern`, `return`, `Fernsehen`), keep to
the minimum sizes below and avoid negative tracking.

## 3. Viewing distance

x-height visual angle for each TV preset, computed for 32–75 inch 16:9 panels at 1–4 m. The test uses a floor of 10
arc-minutes of x-height (9 for caption and metadata) over a set of typical viewing situations, and reports the worst case
separately. The floor is a deliberately conservative working threshold chosen for this project, not an external standard.

| Preset | Size (px at 1080p) | Minimum over typical viewing (arcmin) | Worst case: 32 inch at 4 m |
|---|---:|---:|---:|
| displayXL | 96 | 31.8 | 15.9 |
| displayL | 72 | 23.8 | 11.9 |
| headlineL | 56 | 18.5 | 9.3 |
| headlineM | 44 | 14.6 | 7.3 |
| titleL | 36 | 11.9 | 6.0 |
| titleM | 32 | 10.6 | 5.3 |
| bodyL | 30 | 9.9 | 5.0 |
| bodyM | 28 | 9.3 | 4.6 |
| labelL | 30 | 9.9 | 5.0 |
| labelM | 28 | 9.3 | 4.6 |
| caption | 24 | 7.9 | 4.0 |
| metadata | 24 | 7.9 | 4.0 |
| numeric | 28 | 9.3 | 4.6 |
| subtitle | 46 | 15.2 | 7.6 |

Seven of the fourteen TV presets fall slightly under the test floor in the least favourable typical case, and the suite
reports them as warnings rather than hiding them. They are standard 10-foot-UI sizes, and the floor is conservative, but the
conclusion is practical: **body, label, caption and metadata presets are minimums, not targets.** On small sets viewed from far
away, nothing below Headline M is comfortably readable in any typeface. Offer a text-size setting that scales the whole
canvas by 1.15 and 1.3.

## 4. Contrast

Contrast depends on colour, not on the font. The specimen palette was checked against WCAG 2.2: all text pairs exceed 4.5 : 1
(the lowest is light metadata on a light surface at 4.95 : 1), the focus rings exceed 3 : 1, and subtitles on the scrim reach
17.4 : 1. The full list is in DESIGN-SYSTEM.md. Thin and ExtraLight are display weights: do not use them below 48 px on
television or 32 px on phones whatever the contrast ratio is.

## 5. Small sizes

FreeType rasterisation tests (`qa/qa_rendering.py`) check that the counters of `a e g o b d p q B D O P R 0 6 8 9` stay open:

| Style | Unhinted: all counters open from | Autohinted static: all counters open from | Recommended floor |
|---|---:|---:|---:|
| Light | 13 px per em | 10 | 13 |
| Regular, Medium | 12 (`a` closes at 11) | 10 | 12 |
| Bold | 10 | 14 (`e` at 10, `a` at 13) | 14 |
| Black | 12 | 18 (`a` and `e` close at several sizes below) | 18 |
| Condensed Regular / Bold | 12 / 14 | 10 / 14 | 12 / 14 |

These are greyscale software results. LCD panels with sharpening or noise reduction can do better or worse.

## 6. Subtitles and captions

- Use the `subtitle` preset: Medium, `GRAD +40`, 46 px at 1080p, line height 58 px.
- Always draw a background: a 75 % black box, or an outline plus shadow. `specimens/ott-tv/subtitles.png` shows four treatments
  over bright, dark, saturated and high-frequency backgrounds.
- Let viewers change size, colour, background and edge style. Caption regulations in several markets (for example the FCC's
  closed-caption display rules in the United States) require user controls of this kind, including a choice of font styles.
  Orion does not provide monospaced, serif, casual, cursive or small-capital styles, so a caption system that must offer the
  full set needs additional families. Check the rules that apply to your markets; this document is not legal advice.
- Two lines of at most 42 characters fit the title-safe width at 46 px.

## 7. Text spacing and resizing

- WCAG 1.4.12: with line height 1.5, paragraph spacing 2 em, letter spacing 0.12 em and word spacing 0.16 em, the tallest ink in
  the font (1.253 em) fits the line box, and no glyph changes form because there are no ligature features.
  `specimens/typography-scale/text-spacing-override.png` shows two presets with the overrides and at 200 %.
- WCAG 1.4.4: every preset keeps a line height of at least 1.08 em. Vietnamese and other stacked-accent text should use
  1.25 em or more, which the body presets do.

## 8. What Orion does not solve

- It has no dyslexia-specific alternates and makes no claim about dyslexia.
- It has not been tested with users, with screen magnifiers on TV platforms, or on physical panels.
- The simulations model blur, not glare, motion, HDR tone mapping or chroma subsampling.
- Platform text-scaling settings (Android font scale, Dynamic Type) must still be honoured by the app; the presets are the
  100 % values.
