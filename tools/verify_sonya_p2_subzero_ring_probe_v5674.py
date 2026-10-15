"""Whole real Sub-Zero Ring encounter, retained independent native/input gates."""
import inspect,json,traceback
from types import SimpleNamespace
import verify_sonya_p2_jax_ring_probe_v5660 as previous
import verify_sonya_p2_kitana_ring_probe_v5639 as original
import run_sonya_p2_subzero_ring_probe_v5672 as capture
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5675_sonya_p2_subzero_ring_probe_checked'


def make_replay():
 source=inspect.getsource(previous.make_replay)
 for before,after in [
  ("(f['stage']=='4' and f['cpu_id']==f['cpu_roster']=='11') or",
   "(f['stage']=='4' and f['cpu_id']==f['cpu_roster']=='11') or\\n              (f['stage']=='7' and f['cpu_id']==f['cpu_roster']=='8') or"),
  ("(r['stage']=='4' and r['id']==r['roster']=='11') or",
   "(r['stage']=='4' and r['id']==r['roster']=='11') or\\n          (r['stage']=='7' and r['id']==r['roster']=='8') or"),
  ('int(r[\'stage\']) in (2,4,9,12)','int(r[\'stage\']) in (2,4,7,9,12)')]:
  need(source.count(before)==1,'One ordinary whole Ring factory context extension '+before)
  source=source.replace(before,after,1)
 scope=dict(vars(previous),__file__=__file__)
 exec(compile(source,__file__+'::entire_native_Ring_spacing_context8','exec'),scope)
 return scope['make_replay']()


def native_gate(text,guest):
 source=inspect.getsource(original.native_gate)
 for before,after in [("r['stage']=='2'","r['stage']=='7'"),
  ('18 if side==2 else 4','18 if side==2 else 8'),
  ("end['stage']=='3'","end['stage']=='8'"),("end['stage']=='2'","end['stage']=='7'"),
  ('==[0,1,2,3]','==list(range(9))'),('==[0,1,2]','==list(range(8))')]:
  need(source.count(before)==(2 if before=="r['stage']=='2'"else 1),'Whole native true Sub-Zero context adaptation')
  source=source.replace(before,after)
 source=source.replace('Kitana','SubZero').replace('MK2_KITANA_RING_PROBE_BOUNDARY','MK2_SUBZERO_RING_PROBE_BOUNDARY')
 scope=dict(vars(original),__file__=__file__)
 exec(compile(source,__file__+'::entire_actual_native_SubZero_winner_gate','exec'),scope)
 return scope['native_gate'](text,guest)


def run():
 source=inspect.getsource(original.run)
 for before,after in [("r['tag']=='WIN'and r['stage']=='2'","r['tag']=='WIN'and r['stage']=='7'"),
  ('audit_v5633_current_sonya_p2_kitana_prefix_checked','audit_v5670_current_sonya_p2_subzero_prefix_checked'),
  ('trueVictimID=4','trueVictimID=8')]:
  need(source.count(before)==1,'Whole actual context proof adaptation '+before)
  source=source.replace(before,after,1)
 scope=dict(vars(original),__file__=__file__,capture=capture,OUT=OUT,
  make_replay=make_replay,native_gate=native_gate)
 exec(compile(source,__file__+'::entire_SubZero_encounter_and11actual_faults','exec'),scope)
 return scope['run']()


if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal; never restart on timeout')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable real Sub-Zero verdict');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
