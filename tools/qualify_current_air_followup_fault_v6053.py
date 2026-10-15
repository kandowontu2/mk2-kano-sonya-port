"""Whole6051 proof with the callback fault placed on an actual followup jump.

Retain the failed initial-jump mutation: that record was outside the declared
normal-followup reset proof. Do not change native evidence or drop any fields.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_current_air_throw_roles_v6051 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
OUT=ROOT/'audit_v6054_current_air_followup_fault_checked'

def run():
 failed=earlier.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and 'Actual state semantic fault accepted: wrong_actual_callback'in failure['error'],
      'Actual wrong-scope mutation failure retained')
 source=inspect.getsource(earlier.run)
 before="if r.get('kind')=='physics')if label=='wrong_actual_callback'else 0"
 after="if r.get('kind')=='physics'and r.get('driver')=='followup')if label=='wrong_actual_callback'else 0"
 need(source.count(before)==1,'Only mutation target changes to actual claimed ordinary followup jump')
 source=source.replace(before,after,1)
 scope=dict(earlier.run.__globals__,OUT=OUT,__file__=__file__)
 exec(compile(source,__file__+'::whole_air_matrix_actual_followup_fault','exec'),scope)
 report=scope['run']()
 for p in(failed,Path(earlier.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 report.update(retainedWrongScopeMutationFailure=str(failed),actualFollowupCallbackMutationRejected=True)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable whole current airborne proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
