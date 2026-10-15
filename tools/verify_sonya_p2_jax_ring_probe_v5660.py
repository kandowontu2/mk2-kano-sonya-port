"""Whole real Jax Ring encounter and11actual state/input/native winner faults."""
import inspect,json,traceback
from types import SimpleNamespace
import verify_sonya_p2_kitana_ring_probe_v5639 as previous
import run_sonya_p2_jax_ring_bound_probe_v5658 as capture
import run_current_sonya_p2_campaign_v5628 as context
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5661_sonya_p2_jax_ring_probe_checked'

def make_replay():
 source=inspect.getsource(previous.original.replay)
 changes=[
  ("((f['stage']=='9' and f['cpu_id']==f['cpu_roster']=='5') or",
   "((f['stage']=='2' and f['cpu_id']==f['cpu_roster']=='4') or\n              (f['stage']=='4' and f['cpu_id']==f['cpu_roster']=='11') or\n              (f['stage']=='9' and f['cpu_id']==f['cpu_roster']=='5') or"),
  ("(r['stage']=='9' and r['id']==r['roster']=='5') or",
   "(r['stage']=='2' and r['id']==r['roster']=='4') or\n          (r['stage']=='4' and r['id']==r['roster']=='11') or\n          (r['stage']=='9' and r['id']==r['roster']=='5') or"),
  ("int(r['stage']) in (9,12)","int(r['stage']) in (2,4,9,12)")]
 for before,after in changes:
  need(source.count(before)==1,'Single full original physical replay context extension')
  source=source.replace(before,after,1)
 scope=dict(vars(previous.original),__file__=__file__)
 exec(compile(source,__file__+'::entire_native_Ring_spacing_Kitana_and_Jax','exec'),scope)
 return scope['replay']

def native_gate(text,guest):
 source=inspect.getsource(previous.native_gate)
 changes=[("r['stage']=='2'","r['stage']=='4'"),
  ('18 if side==2 else 4','18 if side==2 else 11'),
  ("end['stage']=='3'","end['stage']=='5'"),
  ("end['stage']=='2'","end['stage']=='4'"),
  ('==[0,1,2,3]','==[0,1,2,3,4,5]'),('==[0,1,2]','==[0,1,2,3,4]')]
 for before,after in changes:
  need(source.count(before)==(2 if before=="r['stage']=='2'"else 1),'Whole native winner context adaptation')
  source=source.replace(before,after)
 source=source.replace('Kitana','Jax').replace('MK2_KITANA_RING_PROBE_BOUNDARY','MK2_JAX_RING_PROBE_BOUNDARY')
 scope=dict(vars(previous),__file__=__file__)
 exec(compile(source,__file__+'::entire_native_winner_and_stage_Jax','exec'),scope)
 return scope['native_gate'](text,guest)

def run():
 source=inspect.getsource(previous.run)
 before="r['tag']=='WIN'and r['stage']=='2'"
 need(source.count(before)==1,'Actual native Jax winner faults use real Jax rows')
 source=source.replace(before,"r['tag']=='WIN'and r['stage']=='4'",1)
 source=source.replace('audit_v5633_current_sonya_p2_kitana_prefix_checked','audit_v5656_sonya_p2_jax_input_bound_checked')
 source=source.replace('trueVictimID=4','trueVictimID=11')
 carrier=SimpleNamespace(OUT=capture.OUT,LUA=capture.LUA,CONTROLLERS=capture.CONTROLLERS,
  __file__=capture.__file__,native=context.native,qualify_payload_metadata_warning=context.qualify_payload_metadata_warning)
 scope=dict(vars(previous),__file__=__file__,capture=carrier,OUT=OUT,make_replay=make_replay,native_gate=native_gate)
 exec(compile(source,__file__+'::entire_actual_Jax_encounter_and11faults','exec'),scope)
 return scope['run']()

if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal, never rerun a live job')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable real Jax encounter verdict');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
