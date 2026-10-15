"""Whole actual scene; precise no-file guard admits native RAM snapshot API."""
import inspect,json,traceback
from pathlib import Path
import run_current_cpu_square_scene_ram_v5366 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v5370_current_cpu_square_scene_ram'
OUT=ROOT/'audit_v5371_current_cpu_square_scene_ram_checked'
LUA=ROOT/'mk2ks_cpu_square_scene_ram_v5369.lua'
def run():
 paths=[Path(original.__file__),ROOT/'mk2ks_cpu_square_scene_ram_v5366.lua',ROOT/'audit_v5368_current_cpu_square_scene_ram_checked/report.json',ROOT/'audit_v5367_current_cpu_square_scene_ram/stderr.log']
 pins={str(p):sha(p)for p in paths}
 need(not json.loads(paths[2].read_text())['passed']and 'No persistent ROM/VRAM/RGB media'in paths[3].read_text(),'Preserve actual overbroad RAM API guard failure')
 namespace=dict(original.run.__globals__,FOLDER=FOLDER,OUT=OUT,LUA=LUA,__file__=__file__)
 exec(compile(inspect.getsource(original.run),__file__+'::entire_original_RAM_snapshot_binding','exec'),namespace)
 report=namespace['run']()
 for p,h in pins.items():need(sha(p)==h,'Immutable original API binding and failure');report['inputHashes'][p]=h
 report['preservedExecutedRAMSnapshotGuardFailure']=str(paths[2])
 return report
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable full RAM snapshot scene')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','continuous','fullRAMRGBBindings')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
