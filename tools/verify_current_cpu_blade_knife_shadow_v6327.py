"""Direct complete body/shadow gate with numeric mode7 publication binding.

Preserve every executed earlier rejection, including adapter syntax error.
No layered quoted-source edits, native reruns or pose/cadence concessions.
"""
import inspect,json
from pathlib import Path
import verify_current_cpu_blade_knife_shadow_v6319 as prior
ROOT,need=prior.ROOT,prior.need
OUT=ROOT/'audit_v6328_current_cpu_blade_knife_body_shadow_checked'


def main():
 extraPins=[ROOT/f'audit_v{n}_current_cpu_blade_knife_body_shadow_checked/failure.json'for n in(6320,6324,6326)]
 need(all(not json.loads(p.read_text())['passed']for p in extraPins),'All real earlier host-check rejections preserved')
 extraPins.extend(ROOT/f'tools/verify_current_cpu_blade_knife_shadow_v{n}.py'for n in(6319,6323,6325))
 source=inspect.getsource(prior.state_gate)
 before='  if actual:\n'
 after="""  if not actual:
   need(frame==2441 and target['mode']==7,'Only actual native refill lacks a live-pair callback')
   candidate=next(q for q in b['rows']['MK2_HPHASE_CANDIDATE']if int(q['frame'])==frame and int(q['slot'])==slot and q['part']=='0')
   need(all(body.num(r,k)==body.num(candidate,k)for k in('actor','main','owner','id','roster','pose','body')),
        'Refill post pose/identity binds actual independent native body publication')
   projection=next(q for q in b['rows']['MK2_HPHASE_PROJECTION']if int(q['frame'])==frame and int(q['slot'])==slot)
   world=int(projection['world'],16)
   need((int(r['x']),int(r['y']))==(body.short(world),body.short(world>>16)),
        'Refill post location binds independent native shadow world registers')
  if actual:
"""
 need(source.count(before)==1,'Single original missing-field strengthening');source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT,extraPins=extraPins)
 exec(compile(source,__file__+'::whole_original_post_gate_numeric_mode7','exec'),scope)
 exec(compile(inspect.getsource(prior.bindings),__file__+'::whole_original_body_shadow_binding','exec'),scope)
 source=inspect.getsource(prior.main)
 before='for path in(PARENT,';need(source.count(before)==1,'All original source/failure pins retained')
 source=source.replace(before,'for path in(*extraPins,PARENT,',1)
 exec(compile(source,__file__+'::whole_original_positive_and_actual_fault_matrix','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
