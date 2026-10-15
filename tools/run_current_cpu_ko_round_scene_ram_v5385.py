"""Whole original KO/round capture with explicit recorder sandbox binding."""
import inspect,json,traceback
from pathlib import Path
import run_current_cpu_ko_round_scene_ram_v5382 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v5386_current_cpu_ko_round_scene_ram'
OUT=ROOT/'audit_v5387_current_cpu_ko_round_scene_ram_checked'
LUA=ROOT/'mk2ks_cpu_ko_round_scene_ram_v5385.lua'
def run():
 paths=[Path(original.__file__),ROOT/'mk2ks_cpu_ko_round_scene_ram_v5382.lua',ROOT/'audit_v5384_current_cpu_ko_round_scene_ram_checked/report.json',ROOT/'audit_v5383_current_cpu_ko_round_scene_ram/stderr.log']
 need(not json.loads(paths[2].read_text())['passed']and "nil value (global 'MK2KS_TOMB_RAM_SAVE')"in paths[3].read_text(),'Preserve actual original recorder sandbox failure')
 pins={str(p):sha(p)for p in paths}
 namespace=dict(original.run.__globals__,FOLDER=FOLDER,OUT=OUT,LUA=LUA,__file__=__file__)
 exec(compile(inspect.getsource(original.run),__file__+'::entire_original_physical_KO_round_capture_bound_RAM_sinks','exec'),namespace)
 report=namespace['run']()
 for p,h in pins.items():need(sha(p)==h,'Original actual failure/source immutable');report['inputHashes'][p]=h
 report.update(originalSandboxRAMSinksExplicitlyBound=True,preservedExecutedRecorderSandboxFailure=str(paths[2]))
 return report
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual KO round recorder proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','continuous','fullRAMRGBBindings','wholeNativeHealth','wholeNativeState','phase')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
