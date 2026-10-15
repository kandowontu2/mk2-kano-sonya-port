"""Source-derived current plane plus complete raw/integer coordinate binding.

Preserve both executed host-check failures. Add the missing independent raw
coordinate invariant and reject real faults; do not rerun or edit native data.
"""
import inspect,json
from pathlib import Path
import verify_current_kano_cpu_ball_v6294 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha


def main():
 plane_failure=ROOT/'audit_v6295_current_kano_cpu_ball_checked/failure.json'
 raw_failure=ROOT/'audit_v6297_current_kano_cpu_ball_checked/failure.json'
 need(not json.loads(plane_failure.read_text())['passed']and
      json.loads(raw_failure.read_text())['error']=='ValueError: Accepted actual CPU ball fault: roll_height',
      'Both original executed host-check rejections retained')
 compiled=ROOT/prior.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 text=compiled.read_text()
 need('constexpr unsigned mk2_ground_contact_extension = 5;'in text and
      'emit(ball_attack, {57, 14 - mk2_ground_contact_extension - 1, 72, 31, 0x1417, 0x1805, 0, 0, 1});'in text,
      'Current compiled constructor independently derives plane8')
 scope=dict(prior.__dict__,__file__=__file__,OUT=ROOT/'audit_v6299_current_kano_cpu_ball_checked',
            prior_module=prior,plane_failure=plane_failure,raw_failure=raw_failure,compiled=compiled)
 source=inspect.getsource(prior.gate)
 changes={
  '(57,9,72,31,0x1417,0x1805,0,0,1)':'(57,14-5-1,72,31,0x1417,0x1805,0,0,1)',
  "for f in range(start+1,end+1):\n  r=by[f];need":
   "for f in range(start+1,end+1):\n  r=by[f]\n  coordinate=lambda v:(v&65535)-65536 if v&32768 else v&65535\n  need((r['x'],r['y'],r['vxpos'],r['vypos'])==tuple(coordinate(r[k]>>16)for k in('xraw','yraw','vxraw','vyraw')),'Every actual raw/integer two-body coordinate agrees')\n  need",
  "'Every constant-speed native rolling field with finite push suppression')":
   "'Every constant-speed native rolling field with finite push suppression')\n  need(r['yraw']==first['yraw'],'Entire constant raw roll height, not only integer plane')",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Exact original strengthening/current-plane adaptation');source=source.replace(before,after,1)
 exec(compile(source,__file__+'::whole_original_ball_gate_source_plane_and_raw_coordinates','exec'),scope)
 source=inspect.getsource(prior.main)
 before='for p in (PARENT,Path(__file__).resolve(),'
 after='for p in (plane_failure,raw_failure,compiled,Path(prior_module.__file__).resolve(),ROOT/\'tools/verify_current_kano_cpu_ball_v6296.py\',PARENT,Path(__file__).resolve(),'
 need(source.count(before)==1,'Pin original source and all executed corrections/rejections')
 source=source.replace(before,after,1)
 exec(compile(source,__file__+'::whole_original_fault_matrix_and_native_terminal_reuse','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  out=ROOT/'audit_v6299_current_kano_cpu_ball_checked';out.mkdir(exist_ok=True)
  (out/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
