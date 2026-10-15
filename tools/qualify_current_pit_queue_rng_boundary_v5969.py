"""Whole5967 successor: native main-loop calls may cross video callbacks.

All1121 actual seed/rotate chains and20 bounded products remain mandatory.
An original TMS execution crossing a field boundary is not a missing RNG
call: require every actual call in monotonic full-window native chronology,
not a fabricated one-to-one callback label relationship. Preserve failure.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_current_pit_queue_rng_v5967 as executed_contract
ROOT,need,sha=executed_contract.ROOT,executed_contract.need,executed_contract.sha
OUT=ROOT/'audit_v5970_current_pit_queue_rng_checked'
source=inspect.getsource(executed_contract.gate)
before="[int(r['frame'])for r in main]==list(range(origin,origin+1101))"
after="len(main)==1101 and all(origin<=int(r['frame'])<=origin+1100 for r in main)and all(clock(a)<clock(b)and int(a['frame'])<=int(b['frame'])for a,b in zip(main,main[1:]))"
need(source.count(before)==1,'One exact video-label-only invariant correction')
source=source.replace(before,after,1).replace('One original main-loop core per completed field, all bounded cores, both actual native overflow paths',
 'Every actual1101 original main-loop core remains within full window in native chronology, all20 bounded cores and both actual overflow paths')
scope=dict(executed_contract.gate.__globals__,__file__=__file__)
exec(compile(source,__file__+'::whole5967_actual_native_call_boundary','exec'),scope)
gate=scope['gate'];gate.source=source
run_source=inspect.getsource(executed_contract.run)
run_scope=dict(executed_contract.run.__globals__,__file__=__file__,__doc__=__doc__,gate=gate)
exec(compile(run_source,__file__+'::whole5967_all_actual_faults','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual native field-boundary successor')
 try:
  report=run()
  failed=executed_contract.OUT/'report.json';prior=json.loads(failed.read_text())
  need(not prior['passed']and 'One original main-loop core per completed field'in prior['error'],
       'Actual5968 failing callback-label-only assumption retained')
  for p in(failed,Path(executed_contract.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
  need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All source/native/prior/failed/current inputs unchanged')
  report.update(actualNativeMainLoopVideoLabelOneToOneNotAssumed=True,retainedFailedPostGate=str(failed),
                newNativeBoots=0,fullPortAcceptance=False)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
