"""Whole paired air matrix with native same/next-field cooperative handoff.

Stock Jax, like Kano, hands off through the original peer task. Depending on
physical player ordering that peer runs in this field or the next. Keep exact
damage/handoff timing and all actual living victim events/body/shadow fields.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_current_air_native_lookup_v6055 as prior
import qualify_current_air_throw_roles_v6051 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
OUT=ROOT/'audit_v6060_current_air_cooperative_handoff_checked'

def state_gate(b,guest,payload):
 source=inspect.getsource(earlier.state_gate)
 for before,after in(
  ("need(len(selected)==1,'Main63 resolves through actual living victim animation root')",
   "need(1<=len(selected)<=2,'Every actual main63 lookup bound to living victim; native selection and cooperative flight may both request it')"),
  ("handoff['frame']==damage['frame']==flight['frame']and h(handoff,'a7')==0xff8da830",
   "handoff['frame']==damage['frame']and int(flight['frame'])in(int(handoff['frame']),int(handoff['frame'])+1)and h(handoff,'a7')==0xff8da830")):
  need(source.count(before)==1,'One exact native cooperative event assertion adaptation');source=source.replace(before,after,1)
 scope=dict(earlier.state_gate.__globals__)
 exec(compile(source,__file__+'::entire_state_physics_actual_cooperative_handoff','exec'),scope)
 return scope['state_gate'](b,guest,payload)

def bindings():
 scope=dict(prior.bindings.__globals__,state_gate=state_gate)
 exec(compile(inspect.getsource(prior.bindings),__file__+'::whole_paired_body_shadow_gate','exec'),scope)
 return scope['bindings']()

def run():
 failed=prior.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and 'Stock Jax takes original native living-victim flight'in failure['error'],
      'Actual same-field-only native task assumption failure retained')
 scope=dict(prior.run.__globals__,OUT=OUT,__file__=__file__,bindings=bindings,state_gate=state_gate)
 exec(compile(inspect.getsource(prior.run),__file__+'::whole_native_matrix_all_fields_and_faults','exec'),scope)
 report=scope['run']()
 for p in(failed,Path(prior.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 report.update(retainedSameFieldOnlyHandoffAssumptionFailure=str(failed),originalCooperativeSameOrNextFieldHandoffAccepted=True)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete native airborne qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
