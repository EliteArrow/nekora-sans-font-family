# Orion build scripts

Orion's outlines are not stored as hand-edited drawings. They are produced by the parametric generator in `orion/`
and written to the UFO masters in `../masters`. Edit the generator (or the UFOs, if you prefer to take over by hand)
and rebuild.

```bash
pip install -r requirements.txt
python3 build.py all                 # sources -> variable font -> statics -> OTF -> WOFF2 -> subsets
python3 build.py sources vf          # only regenerate the UFOs and the variable font
python3 ../../qa/run_all.py          # full QA
python3 ../../specimens/src/build_specimens.py
```

`build.py` writes to the project root two levels up (override with `ORION_ROOT=/some/dir`).

| Module | Contents |
|---|---|
| `orion/params.py` | Axes, master locations, the parameter tables (stems, widths, sidebearings, tensions) per weight × optical size, width and grade rules |
| `orion/geom.py` | Geometry kernel: stroke-band primitive, terminal cuts, superelliptic curves, the glyph builder `G` |
| `orion/parts.py` | Glyph registry and shared parts: rings, arches, bowls, hooks, diagonals, terminals |
| `orion/latin_lc.py`, `latin_uc.py`, `latin_ext.py` | Latin lowercase, capitals and figures, extended letters |
| `orion/greek.py`, `cyrillic.py` | Greek (monotonic) and Cyrillic |
| `orion/symbols.py`, `marks.py` | Punctuation, currency, math, arrows, interface symbols; combining marks and stacks |
| `orion/charset.py`, `glyphset.py` | Character set, composites from Unicode decomposition, anchors, per-master assembly |
| `orion/kerning.py` | Profile-based class kerning |
| `orion/features.py` | OpenType feature code (GSUB); kern / mark / mkmk come from ufo2ft's writers |
| `orion/ufo.py` | UFO 3 and designspace writer |
| `tools/proof.py` | Quick proof straight from the generator: `python3 tools/proof.py "Text|more" "wght=700/wght=900,opsz=72" out.png 110 1500` |
| `tools/outline_debug.py` | Outline plot with handles: `python3 tools/outline_debug.py "S,three" "wght=900" out.png` |
| `tools/render_vf.py`, `tools/contact_sheet.py` | Render text or a glyph contact sheet from the built variable font |

Adding a glyph: write a function decorated with `@glyph('name', 0xCODE)` that draws from the `Params` object only (never from
absolute numbers that ignore weight or width). Every master then gets a structurally identical outline, which is what keeps
the designspace interpolable. Run `python3 ../../qa/run_all.py interpolation` afterwards.
