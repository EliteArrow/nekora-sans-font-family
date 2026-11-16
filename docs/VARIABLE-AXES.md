# Orion — variable axes

`fonts/variable/Orion-VF.ttf` has four axes. All of them are true interpolation between drawn masters: no axis is
produced by scaling, skewing or emboldening.

| Axis | Tag | Min | Default | Max | Registered | Effect |
|---|---|---:|---:|---:|---|---|
| Weight | `wght` | 100 | 400 | 900 | yes | Stroke weight, counters, spacing and kerning |
| Width | `wdth` | 75 | 100 | 125 | yes | Letter width with re-proportioned stems and counters |
| Optical size | `opsz` | 10 | 14 | 72 | yes | x-height, spacing, stroke contrast and aperture for the rendered size |
| Grade | `GRAD` | −50 | 0 | 100 | no (convention shared with Roboto Flex and others) | Stroke weight only; advances and kerning never change |

## Masters

21 masters, all with identical point structure (`sources/masters/*.ufo`, `sources/designspace/Orion.designspace`):

| Group | Locations | Count |
|---|---|---:|
| Weight × width at opsz 14 | wght {100, 400, 900} × wdth {75, 100, 125} | 9 |
| Optical size | opsz {10, 72} × wght {100, 400, 900} | 6 |
| Grade | GRAD {−50, 100} × wght {100, 400, 900} | 6 |

Optical size and grade are drawn at normal width only. At other widths their effect is the same delta added to the width
masters. This keeps the file small (766 KB TTF, 308 KB WOFF2) and is the reason the extreme corners of the designspace are
tested separately (see below).

There is no `avar` table: axis values map linearly to the design between masters, with one bend at 400.

## Measured behaviour (units per 1000 em, from the built font)

| Location | Capital stem | x-height | O width | n advance | Mean lowercase advance | Word space |
|---|---:|---:|---:|---:|---:|---:|
| wght 100 | 27 | 518 | 680 | 571 | 515 | 249 |
| wght 200 | 47 | 519 | 684 | 574 | 517 | 251 |
| wght 300 | 68 | 521 | 688 | 576 | 519 | 254 |
| wght 400 (default) | 88 | 522 | 692 | 579 | 522 | 256 |
| wght 500 | 110 | 524 | 703 | 584 | 528 | 261 |
| wght 600 | 131 | 527 | 714 | 589 | 535 | 266 |
| wght 700 | 153 | 529 | 726 | 595 | 541 | 272 |
| wght 800 | 174 | 532 | 737 | 600 | 548 | 277 |
| wght 900 | 196 | 534 | 748 | 605 | 555 | 282 |
| wdth 75 | 82 | 522 | 546 | 459 | 414 | 203 |
| wdth 125 | 92 | 522 | 827 | 679 | 614 | 303 |
| wdth 75, wght 900 | 157 | 534 | 598 | 482 | 442 | 225 |
| wdth 125, wght 900 | 214 | 534 | 875 | 704 | 646 | 329 |
| opsz 10 | 92 | 530 | 702 | 614 | 549 | 268 |
| opsz 24 | 88 | 520 | 691 | 572 | 517 | 254 |
| opsz 36 | 87 | 517 | 690 | 564 | 511 | 251 |
| opsz 72 | 85 | 510 | 688 | 540 | 494 | 244 |
| GRAD −50 | 80 | 522 | 684 | 579 | 522 | 256 |
| GRAD +50 | 96 | 522 | 700 | 579 | 522 | 256 |
| GRAD +100 | 104 | 522 | 708 | 579 | 522 | 256 |

Things to read from the table:

- **Weight** multiplies the stem by 7.3 from Thin to Black while the mean advance grows by only 8 %: weight is drawn, not expanded.
- **Width** changes the round width by −21 % / +20 % but the stem by only −7 % / +5 %: width is not horizontal scaling.
- **Optical size** moves x-height (530 → 510), spacing (n advance 614 → 540) and stem (92 → 85) together.
- **Grade** changes the stem from 80 to 104 while `n advance`, `mean advance` and `word space` stay at exactly the same value.
  The grade masters copy every advance width, anchor, component offset and kerning value from their GRAD 0 sibling, and
  `qa/qa_interpolation.py` verifies it for all glyphs at 6 base locations × 5 grades.

## Named instances

27 instances in `fvar` (all at opsz 14, GRAD 0): the nine weights Thin 100, ExtraLight 200, Light 300, Regular 400, Medium 500,
SemiBold 600, Bold 700, ExtraBold 800, Black 900, each at Normal (wdth 100), Condensed (wdth 75) and Extended (wdth 125).

`STAT` axis values: weights by name (Regular linked to Bold); width `Cond` 75, `Normal` 100, `Ext` 125; optical size ranges
`Capt` 10–12, `Text` 12–28, `Disp` 28–72; grade `G-50`, `G0`, `G100`. Labels are abbreviated so that composed style names stay
inside the name-length limits that FontBakery checks.

## Static families cut from the variable font

| Family | Fixed axes | Files |
|---|---|---|
| Orion | wdth 100, opsz 14, GRAD 0 | 9 TTF (autohinted), 9 OTF (CFF), 9 WOFF2 |
| Orion Display | wdth 100, opsz 72, GRAD 0 | 9 TTF (autohinted), 9 WOFF2 |
| Orion Condensed | wdth 75, opsz 14, GRAD 0 | 9 TTF (autohinted), 9 WOFF2 |

## Usage

```css
.title   { font-family: 'Orion'; font-weight: 700; font-stretch: 100%; font-variation-settings: 'opsz' 72, 'GRAD' 0; }
.rail    { font-weight: 500; font-stretch: 85%; }              /* condensed for dense rails */
.focused { font-variation-settings: 'opsz' 36, 'GRAD' 80; }    /* darker, same width */
.caption { font-optical-sizing: auto; }                         /* opsz follows font-size in px */
```

Platform snippets for Android, Apple platforms, Tizen, webOS and Roku are in `integration/`.

## Interpolation safety

`qa/qa_interpolation.py` instantiates the font at 91 locations, including all 16 corners of the designspace, and, for every
glyph, removes overlaps and compares the number of outer contours and counters with the default master. It also checks counter
area floors, monotonic weight and width, and collisions between 2,704 letter pairs at 8 extreme locations. Results are in
QA-REPORT.md. Two limits are worth knowing:

- The variable TrueType file keeps overlapping contours (flagged with `OVERLAP_SIMPLE` / `OVERLAP_COMPOUND`), as variable fonts
  normally do. Renderers that ignore the flags can show light seams at overlaps under some zoom levels. The static files have
  overlaps removed.
- Optical size and grade at non-default widths are extrapolated sums of deltas, not drawn masters. They pass the topology
  tests, but they have had less visual review than the nine weight × width masters.
