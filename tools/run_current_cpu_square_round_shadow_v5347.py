"""Whole original CPU capture, observer-only normal round boundary adaptation."""
import inspect,json,traceback
import run_current_cpu_square_shadow_v5344 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5349_current_cpu_sonya_square_observed'
def run():
 failed=previous.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and failure['error']=="ValueError('No native/observer/action/recovery failure')",'Preserve actual observer-imposed normal round abort')
 source=inspect.getsource(previous.run)
 source=source.replace('audit_v5345_current_cpu_sonya_square_human_','audit_v5348_current_cpu_sonya_square_human_')
 namespace=dict(previous.run.__globals__,__file__=__file__)
 # Explicitly pass the round-aware Lua through the previous complete collector binding.
 import run_current_cpu_square_shadow_v5341 as base
 namespace['previous']=type('BoundOriginal',(),dict(run=base.run,OUT=base.OUT,__file__=base.__file__))
 # previous.run builds globals from base.run; bind only immutable observation script and target leaf.
 scoped_globals=dict(base.run.__globals__,LUA=ROOT/'mk2ks_cpu_square_round_shadow_v5347.lua')
 exec(compile(inspect.getsource(base.run),__file__+'::entire_Square_transport_round_observer','exec'),scoped_globals)
 namespace['previous'].run=scoped_globals['run']
 exec(compile(source,__file__+'::entire_capture_preserving_original_CPU_exit','exec'),namespace)
 report=namespace['run']()
 for p in(failed,previous.__file__,ROOT/'mk2ks_cpu_square_round_shadow_v5347.lua'):
  report['inputHashes'][str(p)]=sha(p)
 report.update(originalCPUExitNotReplaced=True,observerDoesNotAbortEarnedNativeRoundTransition=True,preservedObserverAbortFailure=str(failed))
 return report
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual native round capture')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
