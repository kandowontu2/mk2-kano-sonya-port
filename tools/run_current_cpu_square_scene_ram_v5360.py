"""Original whole native scene capture; corrected host method/window bindings only."""
import inspect,json,traceback
from pathlib import Path
import run_current_cpu_square_scene_ram_v5357 as original
import current_cpu_scene_ram_contract_v5360 as scene
ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v5361_current_cpu_square_scene_ram'
OUT=ROOT/'audit_v5362_current_cpu_square_scene_ram_checked'
def run():
 source=inspect.getsource(original.run)
 before='for frame in(2279,2287,2288,2297,2313,2317,2345,2348):'
 need(source.count(before)==1,'Preview uses actual last native observed field')
 source=source.replace(before,'for frame in(2279,2287,2288,2297,2313,2317,2345,2347):',1)
 namespace=dict(original.run.__globals__,FOLDER=FOLDER,OUT=OUT,scene=scene,__file__=__file__)
 paths=[Path(original.__file__),Path(scene.original.__file__),ROOT/'audit_v5359_current_cpu_square_scene_ram_checked/report.json']
 pins={str(p):sha(p)for p in paths}
 exec(compile(source,__file__+'::entire_original_native_scene_capture','exec'),namespace)
 report=namespace['run']()
 for p,h in pins.items():need(sha(p)==h,'Original capture/binding/failed evidence unchanged');report['inputHashes'][p]=h
 return report
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual native scene replay')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','continuous','fullRAMRGBBindings')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
