"""Performance benchmarks: file sizes, glyph complexity, parse / shape / raster timings (software, this machine)."""
import os, sys, json, time, glob, io
import uharfbuzz as hb
import freetype
from fontTools.ttLib import TTFont
from common import *
from corpus import LANGUAGE_SAMPLES


def kb(p): return round(os.path.getsize(p) / 1024, 1)


def main():
    R = Report('performance')
    sizes = {}
    for p in sorted(glob.glob(os.path.join(ROOT, 'fonts', '**', '*.*'), recursive=True)):
        if p.endswith(('.ttf', '.otf', '.woff2')):
            sizes[os.path.relpath(p, os.path.join(ROOT, 'fonts'))] = kb(p)
    vf_ttf = sizes['variable/Orion-VF.ttf']; vf_w2 = sizes['variable/Orion-VF.woff2']
    R.ok('variable TTF under 1 MB (%.0f KB)' % vf_ttf, vf_ttf < 1024, vf_ttf)
    R.ok('variable WOFF2 under 400 KB (%.0f KB)' % vf_w2, vf_w2 < 400, vf_w2)
    lat = sizes.get('subsets/latin/Orion-VF.latin.woff2')
    R.ok('Latin variable subset under 160 KB (%.0f KB)' % lat, lat < 160, lat)
    st = [v for k, v in sizes.items() if k.startswith('webfonts/')]
    R.ok('static WOFF2 files under 120 KB each (max %.0f KB)' % max(st), max(st) < 120, max(st))
    f = TTFont(VF); glyf = f['glyf']
    pts = [glyf[g].numberOfContours and len(glyf[g].coordinates) if not glyf[g].isComposite() else 0 for g in f.getGlyphOrder()]
    simple = [p for p in pts if p]
    comp = sum(1 for g in f.getGlyphOrder() if glyf[g].isComposite())
    stats = dict(glyphs=len(pts), composite_glyphs=comp, simple_glyphs=len(simple), mean_points=round(sum(simple) / len(simple), 1), max_points=max(simple),
                 gvar_kb=round(len(f.getTableData('gvar')) / 1024, 1), gpos_kb=round(len(f.getTableData('GPOS')) / 1024, 1), glyf_kb=round(len(f.getTableData('glyf')) / 1024, 1))
    R.ok('outline complexity: mean %.0f points per simple glyph, max %d' % (stats['mean_points'], stats['max_points']), stats['mean_points'] < 80 and stats['max_points'] < 400, stats)
    data = open(VF, 'rb').read()
    t = time.perf_counter()
    for _ in range(20):
        hb.Font(hb.Face(data))
    t_face = (time.perf_counter() - t) / 20 * 1000
    font = hb.Font(hb.Face(data))
    text = ' '.join(LANGUAGE_SAMPLES.values())
    t = time.perf_counter(); n = 0
    for _ in range(30):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf); n += len(buf.glyph_infos)
    t_shape = time.perf_counter() - t
    font.set_variations({'wght': 650, 'wdth': 90, 'opsz': 24, 'GRAD': 20})
    t = time.perf_counter(); n2 = 0
    for _ in range(30):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf); n2 += len(buf.glyph_infos)
    t_shape_var = time.perf_counter() - t
    face = freetype.Face(VF); face.set_pixel_sizes(0, 32)
    t = time.perf_counter(); k = 0
    for ch in (text * 3):
        face.load_char(ch, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING); k += 1
    t_raster = time.perf_counter() - t
    face.set_var_design_coords([650, 90, 24, 20])
    t = time.perf_counter()
    for ch in (text * 3):
        face.load_char(ch, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
    t_raster_var = time.perf_counter() - t
    sface = freetype.Face(os.path.join(STATIC, 'Orion', 'Orion-Regular.ttf')); sface.set_pixel_sizes(0, 32)
    t = time.perf_counter()
    for ch in (text * 3):
        sface.load_char(ch, freetype.FT_LOAD_RENDER)
    t_raster_static = time.perf_counter() - t
    bench = dict(hb_face_create_ms=round(t_face, 3), hb_shape_glyphs_per_s=int(n / t_shape), hb_shape_glyphs_per_s_at_instance=int(n2 / t_shape_var),
                 ft_raster_glyphs_per_s_default=int(k / t_raster), ft_raster_glyphs_per_s_at_instance=int(k / t_raster_var),
                 ft_raster_glyphs_per_s_static_hinted=int(k / t_raster_static))
    R.ok('HarfBuzz shaping throughput > 100k glyphs/s', bench['hb_shape_glyphs_per_s'] > 100000, bench)
    R.ok('FreeType rasterisation (32 px, uncached) > 5k glyphs/s at a variable instance', bench['ft_raster_glyphs_per_s_at_instance'] > 5000, bench)
    R.save(dict(sizes_kb=sizes, glyph_stats=stats, benchmarks=bench))


if __name__ == '__main__':
    main()
