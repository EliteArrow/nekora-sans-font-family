# Orion — Unicode coverage

Generated from the built font (`qa/qa_unicode.py` → `qa/unicode/coverage-manifest.json`). 899 glyphs, 774 encoded characters.
The full list of code points is in `qa/unicode/codepoints.txt`.

## Scripts

| Script | Characters |
|---|---:|
| Common (punctuation, figures, symbols) | 203 |
| Latin | 383 |
| Inherited (combining marks) | 19 |
| Greek | 71 |
| Cyrillic | 98 |

## Blocks

“Assigned” is the number of characters Unicode assigns in the block; Orion covers what its target languages and interface use need, not whole blocks.

| Block | Range | Covered | Assigned in block |
|---|---|---:|---:|
| Basic Latin | U+0020-007E | 95 | 95 |
| Latin-1 Supplement | U+00A0-00FF | 95 | 96 |
| Latin Extended-A | U+0100-017F | 128 | 128 |
| Latin Extended-B | U+0180-024F | 41 | 208 |
| IPA Extensions | U+0250-02AF | 1 | 96 |
| Spacing Modifier Letters | U+02B0-02FF | 8 | 80 |
| Combining Diacritical Marks | U+0300-036F | 19 | 112 |
| Greek and Coptic | U+0370-03FF | 73 | 135 |
| Cyrillic | U+0400-04FF | 98 | 256 |
| Latin Extended Additional | U+1E00-1EFF | 97 | 256 |
| General Punctuation | U+2000-206F | 30 | 111 |
| Superscripts and Subscripts | U+2070-209F | 17 | 42 |
| Currency Symbols | U+20A0-20CF | 13 | 33 |
| Letterlike Symbols | U+2100-214F | 4 | 80 |
| Number Forms | U+2150-218F | 6 | 60 |
| Arrows | U+2190-21FF | 16 | 112 |
| Mathematical Operators | U+2200-22FF | 13 | 256 |
| Miscellaneous Technical | U+2300-23FF | 1 | 256 |
| Control Pictures | U+2400-243F | 1 | 39 |
| Geometric Shapes | U+25A0-25FF | 14 | 96 |
| Miscellaneous Symbols | U+2600-26FF | 2 | 256 |
| Dingbats | U+2700-27BF | 2 | 192 |

## Languages

A language is listed as supported only when every letter of its alphabet (both cases), its required punctuation and its diacritics are encoded and shape correctly in HarfBuzz. The check compares each repertoire in `qa/qa_unicode.py` with the font’s character map.

### Required by the brief (all complete)

| Language | Letters checked | Missing |
|---|---:|---|
| English | 52 | none |
| Spanish | 68 | none |
| French | 86 | none |
| German | 62 | none |
| Italian | 72 | none |
| Portuguese | 76 | none |
| Dutch | 74 | none |
| Polish | 64 | none |
| Czech | 82 | none |
| Slovak | 86 | none |
| Hungarian | 70 | none |
| Romanian | 66 | none |
| Turkish | 57 | none |
| Vietnamese | 187 | none |
| Greek | 71 | none |
| Russian | 67 | none |
| Ukrainian | 66 | none |
| Bulgarian | 60 | none |
| Serbian (Cyrillic) | 60 | none |
| Serbian (Latin) | 54 | none |

### Also covered

| Language | Letters checked | Missing |
|---|---:|---|
| Catalan | 75 | none |
| Danish | 58 | none |
| Norwegian | 70 | none |
| Swedish | 58 | none |
| Finnish | 62 | none |
| Icelandic | 64 | none |
| Estonian | 54 | none |
| Latvian | 66 | none |
| Lithuanian | 64 | none |
| Croatian | 54 | none |
| Slovenian | 50 | none |
| Albanian | 54 | none |
| Maltese | 56 | none |
| Indonesian / Malay | 52 | none |
| Filipino | 54 | none |
| Swahili | 52 | none |
| Welsh | 98 | none |
| Irish | 46 | none |
| Azerbaijani (Latin) | 63 | none |
| Belarusian | 64 | none |
| Macedonian | 62 | none |

## Known gaps inside the supported scripts

- **Greek** is monotonic only. Polytonic Greek (U+1F00–1FFF) is not included.
- **Cyrillic** covers U+0400–045F plus `Ґ ґ`. Kazakh, Tajik, Bashkir and other extended Cyrillic letters are not included. Bulgarian localised letterforms (`locl` for `BGR`) are not drawn; Bulgarian uses the international forms.
- **Polish** uses the standard acute; a steeper *kreska* variant is not provided.
- **Vietnamese** is complete for precomposed and decomposed text. In decomposed input, `i` with dot below followed by a top mark keeps its dot.
- **Latin Extended-B** is covered only for Romanian, Pinyin tone letters, Vietnamese horn letters and a few others (41 of 208).
- **Symbols**: the arrow, geometric-shape and math sets are the interface subset listed in the block table, not complete blocks. There are no emoji and no box-drawing characters.
- Soft hyphen (U+00AD) is intentionally not encoded; shaping engines handle it without a glyph.

## Scripts that are not supported

Orion contains no glyphs for: Arabic, Hebrew, Devanagari, Thai, Hangul, Hiragana, Katakana, Han, Bengali, Tamil, Georgian, Armenian. Text in these scripts will fall back.

### Recommended fallback stack

Pair Orion with a companion family that has similar proportions (x-height about 0.52 em, low contrast) and matching weights. The Noto Sans families are designed as a consistent set across scripts and are a practical default:

| Script | Companion | Notes |
|---|---|---|
| Arabic | Noto Sans Arabic (UI variant where available) | Raise line height to at least 1.5; no letter-spacing |
| Hebrew | Noto Sans Hebrew | |
| Devanagari, Bengali, Tamil | Noto Sans Devanagari / Bengali / Tamil | Line height 1.5–1.6 for stacked conjuncts and vowel signs |
| Thai | Noto Sans Thai (looped) or Noto Sans Thai UI | Line height at least 1.5 for tone marks |
| Chinese, Japanese, Korean | Noto Sans CJK SC / TC / JP / KR, or the platform CJK font | Use the platform font on TV to save tens of megabytes |
| Georgian, Armenian | Noto Sans Georgian / Armenian | |

```css
font-family: 'Orion', 'Noto Sans Arabic', 'Noto Sans Hebrew', 'Noto Sans Devanagari', 'Noto Sans Thai',
             'Noto Sans CJK SC', system-ui, sans-serif;
```

Mixed-script lines take their line height from the tallest font in the line. Set an explicit line height on the container (the presets do) so that rows do not jump when a fallback font appears. The fallback pairings above are recommendations; they have not been tested together with Orion on devices.
