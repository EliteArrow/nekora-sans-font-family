"""Outline debug plot: python dbg.py "S,three,five" "wght=900" out.png"""
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import orion.glyphset_load
from orion.quick import make
from orion.params import Params
from orion.geom import cubic_pt
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
names=sys.argv[1].split(',')
loc=dict(wght=400,wdth=100,opsz=14,GRAD=0)
for kv in sys.argv[2].split(','):
    if kv: k,v=kv.split('='); loc[k]=float(v)
P=Params(**loc)
fig,axs=plt.subplots(1,len(names),figsize=(5.2*len(names),6.4))
if len(names)==1: axs=[axs]
for ax,nm in zip(axs,names):
    g=make(P,nm)
    for ci,c in enumerate(g.contours):
        prev=c[-1][-1]; xs=[prev[0]]; ys=[prev[1]]
        for s in c:
            if s[0]=='l': xs.append(s[1][0]); ys.append(s[1][1])
            else:
                for i in range(1,17):
                    p=cubic_pt(prev,s[1],s[2],s[3],i/16); xs.append(p[0]); ys.append(p[1])
                ax.plot([prev[0],s[1][0]],[prev[1],s[1][1]],'-',color='#bbb',lw=.6); ax.plot([s[3][0],s[2][0]],[s[3][1],s[2][1]],'-',color='#bbb',lw=.6)
                ax.plot([s[1][0],s[2][0]],[s[1][1],s[2][1]],'.',color='#999',ms=3)
            prev=s[-1]
        ax.fill(xs,ys,alpha=.13,color='C%d'%(ci%10)); ax.plot(xs,ys,'-',color='C%d'%(ci%10),lw=1)
        ax.plot([s[-1][0] for s in c],[s[-1][1] for s in c],'o',color='C%d'%(ci%10),ms=3)
    for y in (0,P.xh,P.cap,P.asc,P.desc): ax.axhline(y,color='#ddd',lw=.5)
    ax.axvline(0,color='#ddd',lw=.5); ax.axvline(g.w,color='#ddd',lw=.5)
    ax.set_aspect('equal'); ax.set_title(nm,fontsize=9); ax.tick_params(labelsize=6)
plt.tight_layout(); plt.savefig(sys.argv[3],dpi=110)
