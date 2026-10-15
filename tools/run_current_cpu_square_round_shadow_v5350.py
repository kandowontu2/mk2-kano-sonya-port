"""Original entire Square RAM collector with native round observer, direct source binding."""
import inspect,json,traceback
from pathlib import Path
import run_current_cpu_square_shadow_v5341 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v5352_current_cpu_sonya_square_observed'
def run():
 source=inspect.getsource(original.run)
 source=source.replace('audit_v5342_current_cpu_sonya_square_human_','audit_v5351_current_cpu_sonya_square_human_')
 before=" namespace=dict(original.collector.__globals__,LUA=LUA,__file__=__file__,CHAIN=CHAIN)"
 after=""" inner="namespace=dict(original.capture.__globals__,native=current,LUA=LUA,__file__=__file__,original=original)"
 need(source.count(inner)==1,'Exact inner source inventory binding')
 source=source.replace(inner,inner[:-1]+',CHAIN=CHAIN)',1)
 namespace=dict(original.collector.__globals__,LUA=LUA,__file__=__file__,CHAIN=CHAIN)"""
 need(source.count(before)==1,'Single inner inventory scope correction');source=source.replace(before,after,1)
 paths=[ROOT/'mk2ks_cpu_square_shadow_v5341.lua',ROOT/'mk2ks_cpu_square_round_shadow_v5347.lua',
  Path(original.__file__),ROOT/'tools/run_current_cpu_square_shadow_v5344.py',
  ROOT/'audit_v5346_current_cpu_sonya_square_observed/report.json',ROOT/'tools/run_current_cpu_square_round_shadow_v5347.py',
  ROOT/'audit_v5349_current_cpu_sonya_square_observed/report.json']
 pins={str(p):sha(p)for p in paths}
 need(not json.loads(paths[-1].read_text())['passed'],'Preserve executed host re-binding failure')
 namespace=dict(original.run.__globals__,LUA=ROOT/'mk2ks_cpu_square_round_shadow_v5347.lua',__file__=__file__)
 exec(compile(source,__file__+'::direct_entire_original_Square_RAM_collector','exec'),namespace)
 report=namespace['run']()
 for p,h in pins.items():need(sha(p)==h,'Every nested observer/failed evidence unchanged');report['inputHashes'][p]=h
 report.update(originalCPUExitNotReplaced=True,observerDoesNotAbortEarnedNativeRoundTransition=True,
  preservedObserverAbortFailure=str(paths[4]))
 return report
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current native capture')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
