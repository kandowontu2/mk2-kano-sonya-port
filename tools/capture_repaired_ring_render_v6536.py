"""Whole existing CPU Ring hit/block/miss capture on repaired native identifiers.

Only candidate context and fresh evidence destination change. Original physical
inputs, whole native damage/state gates, source-qualified continuous CPU/DMA/
shift/scanout renderer, one initial base and no target reseeding stay unchanged.
"""
import argparse,inspect,json,sys,traceback
from pathlib import Path
from types import SimpleNamespace
import native_projectile_identifiers_context_v6509 as candidate
import capture_current_cpu_ring_render_v6377 as hit
import capture_current_cpu_ring_mirror_render_v6389 as blocked
import capture_current_cpu_ring_miss_render_v6412 as missed
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
BRANCHES={'hit':hit,'block':blocked,'miss':missed}

def folder(branch):return ROOT/f'audit_v6537_repaired_ring_{branch}_ram'

def init_model(branch):
 module=BRANCHES[branch]
 model=blocked.model if branch=='block' else hit.model
 source=inspect.getsource(hit.previous.init_model)
 before='(17,17)';need(source.count(before)==1,'Exact actual physical actor tuple in whole original model')
 source=source.replace(before,'(18,18)' if branch=='block' else '(17,18)',1)
 scope=dict(hit.previous.init_model.__globals__,model=model,terminal=SimpleNamespace(current=candidate))
 exec(compile(source,__file__+'::whole_original_model_repaired_guest_'+branch,'exec'),scope)
 return scope['init_model']()

def prepare(branch):
 module=BRANCHES[branch];function=module.prepare()
 # This is a fresh isolated Python process. Bind only this generated collector
 # function's context; do not edit/mutate any previously executed module source.
 scope=function.__globals__
 need(scope['current'].NAME==candidate.old.NAME,'Original actual collector baseline before scoped candidate binding')
 scope.update(current=candidate,FOLDER=folder(branch),init_model=lambda:init_model(branch))
 scope['extra_pins'].update({Path(__file__).resolve(),Path(candidate.__file__).resolve(),
                            ROOT/'audit_v6535_repaired_candidate_progress/report.json'})
 need(scope['LUA']==module.LUA and scope['CHAIN']==module.CHAIN,
      'Entire original branch-specific physical policy and observers unchanged')
 return function

def main(branch,preflight=False):
 need(not folder(branch).exists() and not hit.previous.terminal.process_tools.census(),'Fresh actual capture, no conflicting native game')
 function=prepare(branch)
 if preflight:
  guest,build,scene,transport,pins=init_model(branch)
  reference=blocked.REFERENCE if branch=='block' else missed.REFERENCE if branch=='miss' else ROOT/'audit_v3430_current_cpu_ring_kano/run.log'
  phase=missed.miss.full_phase if branch=='miss' else blocked.full_phase if branch=='block' else hit.full_phase
  result=phase(reference.read_text(encoding='utf-8-sig'),guest)
  need(build==ROOT/candidate.NAME and scene.guest==guest and guest==candidate.expected(),
       'Entire source-qualified model now binds independently reconstructed actual repaired candidate')
  print(json.dumps(dict(preflightPassed=True,branch=branch,newNativeBoots=0,candidate=candidate.NAME,phase=result['ring'])),flush=True)
  return
 return function()

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--branch',required=True,choices=BRANCHES);p.add_argument('--preflight',action='store_true');a=p.parse_args()
 try:main(a.branch,a.preflight)
 except Exception as e:
  failure=dict(passed=False,branch=a.branch,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder(a.branch).exists():(folder(a.branch)/'host_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
