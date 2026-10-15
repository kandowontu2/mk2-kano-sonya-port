"""Exact original scene scanout using native snapshot renderer without disk media."""
import hashlib,inspect,json,traceback
from pathlib import Path
import numpy as np
import run_current_cpu_square_scene_ram_v5357 as original
import current_cpu_scene_ram_contract_v5363 as scene
ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v5367_current_cpu_square_scene_ram'
OUT=ROOT/'audit_v5368_current_cpu_square_scene_ram_checked'
LUA=ROOT/'mk2ks_cpu_square_scene_ram_v5366.lua'

def run():
 source=inspect.getsource(original.run)
 before='for frame in(2279,2287,2288,2297,2313,2317,2345,2348):'
 need(source.count(before)==1,'Actual original final observed field')
 source=source.replace(before,'for frame in(2279,2287,2288,2297,2313,2317,2345,2347):',1)
 paths=[Path(original.__file__),Path(scene.__file__),Path(scene.original.__file__),Path(scene.binding.__file__),Path(scene.hud.__file__),
  ROOT/'mk2ks_cpu_square_scene_ram_v5357.lua',ROOT/'audit_v5365_current_cpu_square_scene_ram_checked/report.json',
  ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp',ROOT/'mame-mkp/src/emu/video.cpp',ROOT/'mame-mkp/src/emu/screen.cpp']
 pins={str(p):sha(p)for p in paths}
 failure=json.loads(paths[6].read_text())
 need(not failure['passed']and failure['error']=="ValueError('Every screenshot pixel matches the actual newly displayed VRAM and palette')",'Preserved real wrong bitmap RAM transport failure')
 native_latch=scene.original.check_latch
 records=[]
 def checked_latch(image,raw,palette,start,control,tap):
  address=start if control&0x400 else start^0xfffc
  row=(address>>4)&511;column=((((address&0x7c)<<4)|(tap&0x3fff))*2)&511
  words=np.frombuffer(raw,dtype='<u2').reshape(512,512)[row:row+254,column:column+400]&0x7fff
  colors=np.frombuffer(palette,dtype='<u4')[words]
  expected=np.stack(((colors>>16)&255,(colors>>8)&255,colors&255),axis=2).astype(np.uint8)
  differences=np.any(image!=expected,axis=2)
  record=dict(call=len(records)+1,row=row,column=column,mismatchedPixels=int(differences.sum()),
   actualRGBSHA256=hashlib.sha256(image.tobytes()).hexdigest().upper(),expectedRGBSHA256=hashlib.sha256(expected.tobytes()).hexdigest().upper())
  if differences.any():
   y,x=np.argwhere(differences)[0];record.update(firstMismatch=[int(x),int(y)],actual=image[y,x].tolist(),expected=expected[y,x].tolist())
  records.append(record)
  (FOLDER/'snapshot_binding_diagnostics.json').write_text(json.dumps(records,indent=2)+'\n')
  return native_latch(image,raw,palette,start,control,tap)
 scene.original.check_latch=checked_latch
 namespace=dict(original.run.__globals__,FOLDER=FOLDER,OUT=OUT,LUA=LUA,scene=scene,__file__=__file__)
 exec(compile(source,__file__+'::original_complete_scene_snapshot_renderer_RAM','exec'),namespace)
 try:report=namespace['run']()
 finally:scene.original.check_latch=native_latch
 for p,h in pins.items():need(sha(p)==h,'All original sources and failure unchanged');report['inputHashes'][p]=h
 report.update(originalSnapshotRendererRAMTransport=True,screenWorkingBitmapNotUsed=True,
  preservedExecutedWrongBitmapTransportFailure=str(paths[6]),snapshotSourceFiles=[str(p)for p in paths[-3:]])
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable snapshot-renderer scene proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','continuous','fullRAMRGBBindings')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
