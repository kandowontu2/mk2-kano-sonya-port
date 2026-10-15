"""Source-bound scaling model unit/regression checks, not gameplay acceptance."""
import json,hashlib,itertools
from pathlib import Path
from collections import defaultdict
import numpy as np
import inspect_native_scaled_arena_v1716 as new
import inspect_natural_arena_floor_v635_v4 as old
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1718_scaled_raster_units_checked'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def setup(cls,buffers):
 r=cls(ROOT,defaultdict(list),buffers,{})
 r.words=np.full((512,512),0x4567,dtype=np.uint16)
 r.body=np.zeros((512,512),dtype=np.uint8);r.shadow=np.zeros((512,512),dtype=bool)
 return r
def pack(values):
 return bytes(values)
def check():
 src=ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp'
 build=json.loads((ROOT/'diagnostic_v1597_native_ground_throw/build-info.json').read_text())
 matching=[h for p,h in build['input_hashes'].items()if Path(p).name=='midtunit_v.cpp']
 assert len(matching)==1 and sha(src)==matching[0]
 text=src.read_text();assert all(s in text for s in ('tx = pre / xstep;','tx = ((startskip - ix) / xstep) * xstep;','tx = (ix >> 8) - tx;','iy += m_dma_state.ystep;'))
 w,h=20,8;indices=np.fromfunction(lambda y,x:(x+3*y)%9,(h,w),dtype=int).astype(np.uint8)
 cases=[]
 for mode,flip,xstep,ystep in itertools.product((2,8,12),(0,16,32,48),(128,288,512),(128,288,512)):
  command=mode|flip;source=0x10000000
  buffers={f'{source:08X}_{command:04X}_{w}_{h}':dict(offset=0,data=pack(indices.ravel()).hex())}
  d=dict(source=source,command=command,width=w,height=h,scaleX=xstep,scaleY=ystep,x=100,y=100,skip=0,
   left=0,right=511,top=0,bottom=511,color=47,palette=0x1200,slot=1)
  r=setup(new.Replay,buffers);r.dma(d)
  expected=np.full((512,512),0x4567,dtype=np.uint16)
  for dy,iy in enumerate(range(0,h*256,ystep)):
   for dx,ix in enumerate(range(0,w*256,xstep)):
    pixel=1 if mode==12 else int(indices[iy>>8,ix>>8])
    if pixel:expected[100+(-dy if flip&32 else dy),100+(-dx if flip&16 else dx)]=(47 if mode in(8,12)else pixel)|0x1200
  assert np.array_equal(r.words,expected),'Independent fixed-point nearest source sampling '+str((mode,flip,xstep,ystep))
  cases.append((mode,flip,xstep,ystep))
 regressions=0
 for mode,flip,skip in itertools.product((2,8),(0,16,32,48),(0,0x204)):
  command=mode|flip|0x80|0x40
  # Actual compressed rows: 2 preskip, 3 postskip, 15 stored pixels.
  raw=pack([v for row in indices for v in [0x32,*row[2:17]]])
  buffers={f'{source:08X}_{command:04X}_{w}_{h}':dict(offset=0,data=raw.hex())}
  d.update(command=command,scaleX=256,scaleY=256,skip=skip)
  a,b=setup(old.Replay,buffers),setup(new.Replay,buffers)
  a.dma(d);b.scaled_dma(d)
  assert all(np.array_equal(getattr(a,k),getattr(b,k))for k in ('words','body','shadow')),'Exact unit-scale compressed/skip compatibility'
  regressions+=1
 pins={str(p.resolve()):sha(p)for p in (src,Path(__file__),Path(new.__file__),Path(old.__file__))}
 return dict(passed=True,independentScaleModeFlipCases=len(cases),exactCompressedUnitScaleRegressions=regressions,
  inputHashes=pins,sourceMatchesCurrentCompiledInputs=True,fullPortAcceptance=False)
if __name__=='__main__':
 assert not OUT.exists();report=check();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
