"""Glyph contact sheet rendered by FreeType from a built font.
usage: sheet.py font.ttf out.png "wght=400,..." [start] [count] [cell]"""
import sys, freetype
from PIL import Image, ImageDraw
from fontTools.ttLib import TTFont
path, out = sys.argv[1], sys.argv[2]
loc = dict(wght=400, wdth=100, opsz=14, GRAD=0)
if len(sys.argv) > 3:
    for kv in sys.argv[3].split(','):
        if kv: k, v = kv.split('='); loc[k] = float(v)
start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
count = int(sys.argv[5]) if len(sys.argv) > 5 else 400
cell = int(sys.argv[6]) if len(sys.argv) > 6 else 78
tt = TTFont(path, lazy=True); order = tt.getGlyphOrder()
face = freetype.Face(path)
if 'fvar' in tt:
    face.set_var_design_coords([loc[a.axisTag] for a in tt['fvar'].axes])
px = int(cell * 0.52)
face.set_pixel_sizes(0, px)
cols = 24
names = order[start:start + count]
rows = (len(names) + cols - 1) // cols
img = Image.new('L', (cols * cell, rows * cell), 255)
d = ImageDraw.Draw(img)
for i, n in enumerate(names):
    gid = start + i
    face.load_glyph(gid, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
    bm = face.glyph.bitmap
    cx, cy = (i % cols) * cell, (i // cols) * cell
    if bm.width and bm.rows:
        g = Image.frombytes('L', (bm.width, bm.rows), bytes(bm.buffer))
        adv = face.glyph.advance.x / 64
        x = cx + int((cell - adv) / 2) + face.glyph.bitmap_left
        y = cy + int(cell * 0.66) - face.glyph.bitmap_top
        img.paste(0, (x, y), g)
    d.rectangle([cx, cy, cx + cell - 1, cy + cell - 1], outline=225)
img.save(out)
print(len(order), 'glyphs; sheet', start, start + len(names))
