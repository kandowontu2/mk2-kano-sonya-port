"""Bind actual mode7 post pose/location to complete drawing observations.

Preserve the6320 accepted-post-pose counterexample. All body/shadow mechanics
and faults remain unchanged; the one real refill field gains missing binding.
No additional native process or altered captured evidence.
"""
import inspect,json
from pathlib import Path
import verify_current_cpu_blade_knife_shadow_v6319 as prior
ROOT,need=prior.ROOT,prior.need
OUT=ROOT/'audit_v6324_current_cpu_blade_knife_body_shadow_checked'


def main():
 failure=ROOT/'audit_v6320_current_cpu_blade_knife_body_shadow_checked/failure.json'
 need(json.loads(failure.read_text())['error']=="ValueError('Accepted actual body/shadow fault knife:post_pose')",
      'Original executed missing-mode7-pose-binding fault retained')
 source=inspect.getsource(prior.state_gate)
 before='  if actual:\n'
 after="""  if not actual:
   need(frame==2441 and target['mode']==7,'Only actual native refill lacks a live-pair callback')
   candidate=next(q for q in b['rows']['MK2_HPHASE_CANDIDATE']if int(q['frame'])==frame and int(q['slot'])==slot and q['part']=='0')
   need(all(r[k]==candidate[k]for k in('actor','main','owner','id','roster','pose','body')),
        'Refill post pose/identity binds actual independent native body publication')
   projection=next(q for q in b['rows']['MK2_HPHASE_PROJECTION']if int(q['frame'])==frame and int(q['slot'])==slot)
   world=int(projection['world'],16)
   need((int(r['x']),int(r['y']))==(body.short(world),body.short(world>>16)),
        'Refill post location binds independent native shadow world registers')
  if actual:
"""
 need(source.count(before)==1,'Single exact missing-field strengthening');source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT,failure=failure,prior_module=prior)
 exec(compile(source,__file__+'::entire_original_post_gate_plus_mode7_binding','exec'),scope)
 exec(compile(inspect.getsource(prior.bindings),__file__+'::whole_original_body_shadow_binding','exec'),scope)
 source=inspect.getsource(prior.main)
 before='for path in(PARENT,baseline_path,Path(__file__),'
 after='for path in(failure,Path(prior_module.__file__),PARENT,baseline_path,Path(__file__),'
 need(source.count(before)==1,'Original source and executed counterexample pinned');source=source.replace(before,after,1)
 exec(compile(source,__file__+'::entire_original_positive_and_real_fault_matrix','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
