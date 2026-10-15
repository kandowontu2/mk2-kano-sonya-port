"""Fault qualification targets an actual held leg field, not unproven intro art.

Keep6277's accepted fault failure: paired state begins before its first held
pose. The original verifier does not claim every introductory pose. Corrupt
the first real held field derived from the native step event instead.
"""
import inspect,json,traceback
from pathlib import Path
import inventory_current_cpu_leg_choices_v6276 as wrapper_prior
ROOT,need,sha=wrapper_prior.ROOT,wrapper_prior.need,wrapper_prior.sha
OUT=ROOT/'audit_v6279_current_cpu_leg_choice_inventory'

def held_mutation(text,tag,key,value,predicate=lambda r:True):
 if tag=='MK2_CPU_PAIR_FIELD'and key=='pose':
  step=next(r for r in wrapper_prior.prior.pair.rows(text,'EVENT')if r['kind']=='step')
  original_predicate=predicate
  predicate=lambda r:int(r['frame'])==step['frame']+1 and original_predicate(r)
 return wrapper_prior.prior.mutate_field(text,tag,key,value,predicate)

def main():
 priorFailure=wrapper_prior.OUT/'failure.json'
 need(priorFailure.exists()and 'fault accepted leg_pose_changed'in json.loads(priorFailure.read_text())['error'],'Preserve actual ineffective introductory-pose fault qualification')
 source=inspect.getsource(wrapper_prior.main)
 changes={
  'failed,Path(prior.__file__),Path(__file__).resolve(),Path(pair.__file__)':
   'failed,Path(prior.__file__),Path(wrapper_prior.__file__),priorFailure,Path(__file__).resolve(),Path(pair.__file__)',
  'scope=dict(prior.main.__globals__,__file__=__file__,OUT=OUT,prior=prior,failed=failed,gate=gate)':
   'scope=dict(prior.main.__globals__,__file__=__file__,OUT=OUT,prior=prior,failed=failed,gate=gate,mutate_field=held_mutation,wrapper_prior=wrapper_prior,priorFailure=priorFailure)',
 }
 for before,after in changes.items():need(source.count(before)==1,'Only actual held fault target and immutable attempt pins');source=source.replace(before,after,1)
 scope=dict(wrapper_prior.main.__globals__,__file__=__file__,OUT=OUT,wrapper_prior=wrapper_prior,priorFailure=priorFailure,held_mutation=held_mutation)
 exec(compile(source,__file__+'::whole_prior_inventory_actual_first_held_fault','exec'),scope);scope['main']()

if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
