# Orion specimens

Every image is rendered by headless Chromium from `fonts/variable/Orion-VF.woff2` (see `src/build_specimens.py`). TV screens are
1920 × 1080 at 1:1, so text is rasterised at the pixel sizes a 1080p television UI would use. They are software renderings, not
photographs of a panel. Titles, people and synopses are invented; artwork is CSS gradients.

| Folder | Files |
|---|---|
| `glyph-sheets/` | `character-set`, `numerals-symbols-punctuation`, `opentype-features` |
| `variable-axis/` | `weight`, `width`, `optical-size`, `grade`, `combined-axes` |
| `typography-scale/` | `type-scale-tv`, `type-scale-desktop`, `type-scale-mobile`, `kerning`, `multilingual`, `text-spacing-override` |
| `ott-tv/` | `tv-home-dark`, `tv-home-bright`, `hero-titles`, `card-grid`, `detail-synopsis`, `playback-controls`, `subtitles` |
| `mobile/` | `mobile-ui` |
| `comparison/` | `reference-metrics` (numbers only; no reference font is rendered) |
| `html/` | The page behind each image, plus `tester.html`, an interactive axis tester. Open them from this folder so the relative font path resolves |
