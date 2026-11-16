import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import orion.glyphset_load
from orion.quick import sheet
L=lambda **k: dict(dict(wght=400,wdth=100,opsz=14,GRAD=0),**k)
txt=sys.argv[1].split('|'); 
locs=[L(**dict((kv.split('=')[0],float(kv.split('=')[1])) for kv in a.split(',') if kv)) for a in sys.argv[2].split('/')]
sheet(txt, locs, sys.argv[3], size=int(sys.argv[4]) if len(sys.argv)>4 else 110, width=int(sys.argv[5]) if len(sys.argv)>5 else 1500)
