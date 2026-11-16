"""Render text from the variable font at axis locations (FreeType via Pillow).
usage: vf.py font.ttf out.png size width "text|text" "wght=700,wdth=100,opsz=14,GRAD=0/..." [dark]"""
import sys
from PIL import Image, ImageDraw, ImageFont
font, out, size, W = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
lines = sys.argv[5].split('|'); locs = sys.argv[6].split('/')
dark = len(sys.argv) > 7
rows = []
for lc in locs:
    d = dict(wght=400, wdth=100, opsz=14, GRAD=0)
    for kv in lc.split(','):
        if kv: k, v = kv.split('='); d[k] = float(v)
    f = ImageFont.truetype(font, size)
    axes = [a['name'] if isinstance(a['name'], str) else a['name'].decode() for a in f.get_variation_axes()]
    order = {'Weight': 'wght', 'Width': 'wdth', 'Optical Size': 'opsz', 'Grade': 'GRAD'}
    f.set_variation_by_axes([d[order[a]] for a in axes])
    for ln in lines:
        rows.append((f, ln))
lh = int(size * 1.34); pad = int(size * 0.3)
img = Image.new('L', (W, pad * 2 + lh * len(rows)), 16 if dark else 255)
dr = ImageDraw.Draw(img)
for i, (f, ln) in enumerate(rows):
    dr.text((pad, pad + i * lh), ln, font=f, fill=235 if dark else 0)
img.save(out)
