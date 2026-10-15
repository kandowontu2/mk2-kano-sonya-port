"""Real earned KO through next round; compact RAM deltas, no disk media."""
import inspect,json,traceback
from pathlib import Path
import numpy as np
import run_current_cpu_square_scene_ram_v5357 as original
import current_cpu_ko_round_scene_contract_v5382 as scene
import current_tomb_ram_model_v3642 as transport
ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v5383_current_cpu_ko_round_scene_ram'
OUT=ROOT/'audit_v5384_current_cpu_ko_round_scene_ram_checked'
LUA=ROOT/'mk2ks_cpu_ko_round_scene_ram_v5382.lua'

def run():
 source=inspect.getsource(original.run)
 before="ram={};rawproofs=[];memory_log=[]"
 need(source.count(before)==1,'Transport decoder only, not native replay anchors')
 source=source.replace(before,before+';delta_transport=transport.Transport()',1)
 before="if line.startswith('MK2_SCENE_RAM '):\n     fields=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(fields.pop('hex'));label=fields['label']"
 after="""if line.startswith(('MK2_TOMB_RAM_BUFFER ','MK2_TOMB_RAM_PIXELS ')):
     fields=dict(re.findall(r'(\\w+)=([^\\s]+)',line));encoded=next(process.stdout).strip();label=fields['file']
     if line.startswith('MK2_TOMB_RAM_BUFFER '):raw=delta_transport.decode(fields,encoded)
     else:
      need(fields['encoding']=='u32le_numeric_hex'and fields['width']=='400'and fields['height']=='254'and len(encoded)==406400*2,'Complete original native snapshot renderer RAM field')
      raw=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').astype('<u4').tobytes()"""
 need(source.count(before)==1,'Only raw media I/O replaced with complete original delta transport')
 source=source.replace(before,after,1)
 before='for frame in(2279,2287,2288,2297,2313,2317,2345,2348):'
 need(source.count(before)==1,'Bounded eight actual transition preview fields')
 source=source.replace(before,'for frame in(3001,3022,3060,3208,3209,3210,3306,3340):',1)
 paths=[Path(original.__file__),Path(scene.__file__),Path(scene.original.__file__),Path(scene.hud.__file__),Path(transport.__file__),
  ROOT/'mk2ks_cpu_square_scene_ram_v5357.lua',ROOT/'mk2ks_native_tomb_ram_v3624.lua',ROOT/'audit_v5381_current_cpu_square_audio_progress/progress.json']
 pins={str(p):sha(p)for p in paths}
 namespace=dict(original.run.__globals__,FOLDER=FOLDER,OUT=OUT,LUA=LUA,scene=scene,transport=transport,np=np,__file__=__file__)
 exec(compile(source,__file__+'::whole_original_native_physical_scene_KO_round_RAM_delta_transport','exec'),namespace)
 report=namespace['run']()
 for p,h in pins.items():need(sha(p)==h,'Original source/model/transport/evidence unchanged');report['inputHashes'][p]=h
 report.update(originalRAMDeltaTransportOnly=True,transportPreviousBuffersNeverNativeReplayAnchors=True)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual KO/round proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','continuous','fullRAMRGBBindings','wholeNativeHealth','wholeNativeState','phase')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
