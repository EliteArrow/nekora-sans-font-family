"""Reference audit: measures METRICS ONLY (no outlines are copied or exported)."""
import sys, json, os, glob
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

def contour_bounds(gs, name):
    rec = DecomposingRecordingPen(gs); gs[name].draw(rec)
    out=[]; cur=None
    from fontTools.pens.boundsPen import BoundsPen
    bp=None
    for op,args in rec.value:
        if op=='moveTo':
            bp=BoundsPen(gs); bp.moveTo(*args)
        elif op in('lineTo','curveTo','qCurveTo'):
            getattr(bp,op)(*args)
        elif op in('closePath','endPath'):
            getattr(bp,op)()
            if bp.bounds: out.append(bp.bounds)
    return out

def measure(font, loc=None):
    gs = font.getGlyphSet(location=loc) if loc else font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font['head'].unitsPerEm
    s = 1000.0/upm
    def b(ch):
        g = cmap.get(ord(ch))
        if not g: return None
        bp = BoundsPen(gs); gs[g].draw(bp); return bp.bounds
    def adv(ch):
        g = cmap.get(ord(ch)); return gs[g].width*s if g else None
    r = {}
    r['cap'] = b('H')[3]*s; r['xh'] = b('x')[3]*s; r['asc'] = b('l')[3]*s; r['desc'] = b('p')[1]*s
    r['fig'] = b('0')[3]*s
    I = b('I'); l=b('l')
    r['stemUC'] = (I[2]-I[0])*s; r['stemLC'] = (l[2]-l[0])*s
    for ch in 'oO':
        cb = contour_bounds(gs, cmap[ord(ch)])
        if len(cb)==2:
            cb.sort(key=lambda t:(t[2]-t[0]), reverse=True); o,i = cb
            r[ch+'_w'] = (o[2]-o[0])*s; r[ch+'_h']=(o[3]-o[1])*s
            r[ch+'_vstroke'] = (i[0]-o[0])*s; r[ch+'_hstroke']=(o[3]-i[3])*s
            r[ch+'_overshoot'] = -o[1]*s
    for ch in 'nHoOatesg0':
        bb=b(ch); a=adv(ch)
        r['adv_'+ch]=round(a,1); r['lsb_'+ch]=round(bb[0]*s,1); r['rsb_'+ch]=round(a-bb[2]*s,1)
    hy=b('-'); r['hyphen_th']=(hy[3]-hy[1])*s
    pd=b('.'); r['period_w']=(pd[2]-pd[0])*s
    import string
    advs=[adv(c) for c in string.ascii_lowercase]; r['avg_lc_adv']=sum(advs)/26
    advs=[adv(c) for c in string.ascii_uppercase]; r['avg_uc_adv']=sum(advs)/26
    r['space']=adv(' ')
    return {k:(round(v,1) if isinstance(v,float) else v) for k,v in r.items()}

def info(path):
    f = TTFont(path, lazy=True)
    d = {'file':os.path.basename(path),'upm':f['head'].unitsPerEm,'glyphs':f['maxp'].numGlyphs,
         'codepoints':len(f.getBestCmap()), 'outline':'CFF' if 'CFF ' in f else 'glyf'}
    nm=f['name']
    d['family']=nm.getDebugName(1); d['license']=(nm.getDebugName(13) or '')[:160]; d['copyright']=(nm.getDebugName(0) or '')[:120]
    o=f['OS/2']; h=f['hhea']
    d['typo']=(o.sTypoAscender,o.sTypoDescender,o.sTypoLineGap); d['hhea']=(h.ascent,h.descent,h.lineGap); d['win']=(o.usWinAscent,o.usWinDescent)
    d['fsType']=o.fsType
    for t in ('GSUB','GPOS'):
        if t in f:
            d[t]=sorted({fr.FeatureTag for fr in f[t].table.FeatureList.FeatureRecord})
    if 'fvar' in f:
        d['axes']=[(a.axisTag,a.minValue,a.defaultValue,a.maxValue) for a in f['fvar'].axes]
        d['instances']=len(f['fvar'].instances)
    d['tables']=sorted(f.keys())
    return f,d

if __name__=='__main__':
    root=sys.argv[1]; out={}
    for p in sorted(glob.glob(root+'/**/*.[ot]tf',recursive=True)):
        f,d=info(p)
        try:
            if 'fvar' in f:
                axes={a.axisTag:(a.minValue,a.defaultValue,a.maxValue) for a in f['fvar'].axes}
                d['m_default']=measure(f)
                for w in (100,400,700,900):
                    if axes['wght'][0]<=w<=axes['wght'][2]:
                        loc={'wght':w}
                        d['m_wght%d'%w]=measure(f,loc)
                if 'opsz' in axes:
                    for oz in (axes['opsz'][0],axes['opsz'][2]):
                        d['m_opsz%g'%oz]=measure(f,{'opsz':oz})
                if 'wdth' in axes:
                    for wd in (axes['wdth'][0],axes['wdth'][2]):
                        d['m_wdth%g'%wd]=measure(f,{'wdth':wd})
                if 'GRAD' in axes:
                    for g in (axes['GRAD'][0],axes['GRAD'][2]):
                        d['m_GRAD%g'%g]=measure(f,{'GRAD':g})
            else:
                d['m']=measure(f)
        except Exception as e:
            d['measure_error']=repr(e)
        out[d['file']]=d
    json.dump(out,open(sys.argv[2],'w'),indent=1)
    for k,d in out.items():
        print('==',k,d['upm'],d['glyphs'],d['codepoints'],d['outline'],d.get('axes',''))
        print('  lic:',d['license'][:90],'| fsType',d['fsType'])
        print('  typo',d['typo'],'hhea',d['hhea'],'win',d['win'])
        print('  GSUB',d.get('GSUB'),'\n  GPOS',d.get('GPOS'))
        for mk in [x for x in d if x.startswith('m')and x!='measure_error']:
            m=d[mk]; print('  ',mk,{k:m[k] for k in ('cap','xh','asc','desc','stemUC','stemLC','o_w','o_vstroke','o_hstroke','O_w','O_vstroke','O_hstroke','o_overshoot','adv_n','lsb_n','rsb_n','adv_o','lsb_o','adv_H','lsb_H','adv_O','lsb_O','avg_lc_adv','avg_uc_adv','space','hyphen_th','period_w','fig','adv_0') if k in m})
        if 'measure_error' in d: print('  ERR',d['measure_error'])
