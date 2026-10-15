"""Complete6051 air matrix; qualify native duplicate victim lookup, not discard it.

Original victim selection and cooperative flight can both request main63 in
the release field. Preserve every event/owner/opcode and the full pose proof.
Retain the failed one-call assertion and target the callback fault on the
ordinary followup whose A6 reset is actually claimed.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_current_air_throw_roles_v6051 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
OUT=ROOT/'audit_v6056_current_air_native_lookup_checked'

def state_gate(b,guest,payload):
 source=inspect.getsource(earlier.state_gate)
 before="need(len(selected)==1,'Main63 resolves through actual living victim animation root')"
 after="need(1<=len(selected)<=2,'Main63 resolves through actual living victim root; original selection plus cooperative flight may both look up this row')"
 need(source.count(before)==1,'Only bounded native duplicate lookup assertion changes')
 source=source.replace(before,after,1)
 scope=dict(earlier.state_gate.__globals__)
 exec(compile(source,__file__+'::entire_state_and_physics_with_native_duplicate_lookup','exec'),scope)
 return scope['state_gate'](b,guest,payload)

def bindings():
 scope=dict(earlier.bindings.__globals__,state_gate=state_gate)
 exec(compile(inspect.getsource(earlier.bindings),__file__+'::whole_body_shadow_with_entire_physical_gate','exec'),scope)
 return scope['bindings']()

def run():
 failures=[ROOT/'audit_v6052_current_air_throw_roles_checked/report.json',ROOT/'audit_v6054_current_air_followup_fault_checked/report.json']
 need(all(not json.loads(p.read_text())['passed']for p in failures),'Both actual failed test assumptions retained')
 source=inspect.getsource(earlier.run)
 before="if r.get('kind')=='physics')if label=='wrong_actual_callback'else 0"
 after="if r.get('kind')=='physics'and r.get('driver')=='followup')if label=='wrong_actual_callback'else 0"
 need(source.count(before)==1,'Actual normal-followup callback fault target');source=source.replace(before,after,1)
 scope=dict(earlier.run.__globals__,OUT=OUT,__file__=__file__,bindings=bindings,state_gate=state_gate)
 exec(compile(source,__file__+'::whole_air_matrix_all_fields_and_faults','exec'),scope)
 report=scope['run']()
 for p in(*failures,Path(earlier.__file__).resolve(),ROOT/'tools/qualify_current_air_followup_fault_v6053.py'):
  report['inputHashes'][str(p)]=sha(p)
 report.update(retainedNativeLookupAndMutationAssumptionFailures=[str(p)for p in failures],allNativeLookupEventsRetained=True)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable whole native airborne proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
