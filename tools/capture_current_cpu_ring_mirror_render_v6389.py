"""Actual current CPU Sonya mirror Ring chip, full native scene in RAM.

Retain entire6377 terminal-first capture and original1997 physical inputs.
Select true human Sonya through those controls, not character/AI/RNG writes.
Earlier3467 is a comparison trajectory, never current runtime admission.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_cpu_ring_render_v6377 as prior
import current_cpu_ring_mirror_render_model_v6388 as model
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
FOLDER=ROOT/'audit_v6390_current_cpu_ring_mirror_render_ram'
LUA=prior.LUA
CHAIN=prior.CHAIN
REFERENCE=ROOT/'audit_v3467_current_cpu_ring_sonya/run.log'


def init_model():
 source=inspect.getsource(prior.previous.init_model)
 need(source.count('(17,17)')==1,'Only explicit both-Sonya physical tuple changes')
 source=source.replace('(17,17)','(18,18)',1)
 scope=dict(prior.previous.init_model.__globals__,model=model)
 exec(compile(source,__file__+'::whole_current_guest_GFX_Sonya_mirror_roles','exec'),scope)
 return scope['init_model']()


def full_phase(text,guest):
 source=inspect.getsource(prior.full_phase)
 need(source.count("'kano'")==4,'Only genuine human identity changes in original phase/health/state/pair contracts')
 source=source.replace("'kano'","'sonya'")
 scope=dict(prior.full_phase.__globals__)
 exec(compile(source,__file__+'::whole_native_ring_phase_health_state_mirror','exec'),scope)
 return scope['full_phase'](text,guest)


def prepare():
 source=inspect.getsource(prior.prepare)
 before="  \"MK2KS_TEST_BOOT_FRAME='960'\":"
 need(source.count(before)==1,'One added normal physical human-selection parameter')
 source=source.replace(before,"  \"MK2KS_TEST_FIGHTER='kano'\":\"MK2KS_TEST_FIGHTER='sonya'\",\n"+before,1)
 before="audit_v3432_current_cpu_ring_checked/report.json"
 need(source.count(before)==1,'Complete earlier qualified original mirror source pins')
 source=source.replace(before,'audit_v3469_current_cpu_ring_mirror_checked/report.json',1)
 before='audit_v3430_current_cpu_ring_kano/run.log'
 need(source.count(before)==2,'Earlier mirror reference and pin both replaced, not the current qualification')
 source=source.replace(before,'audit_v3467_current_cpu_ring_sonya/run.log')
 scope=dict(prior.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,CHAIN=CHAIN,
            model=model,init_model=init_model,full_phase=full_phase)
 exec(compile(source,__file__+'::whole6377_terminal_first_actual_current_mirror_capture','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 need(not FOLDER.exists() and not prior.previous.terminal.process_tools.census(),'Fresh actual job, no native process live')
 function=prepare()
 if preflight:
  guest,_,scene,_,_=init_model();old=REFERENCE.read_text(encoding='utf-8-sig')
  positive=full_phase(old,guest)
  ring=positive['ring']['acceptedRings'][0]
  need(ring['blocked'] and ring['damage']==6 and ring['victim']==18,'Original mirror guard/chip branch on actual reconstructed current guest')
  print(json.dumps(dict(preflightPassed=True,newNativeBoots=0,wholeModelSourceSHA256=model.MODEL_SOURCE_SHA256,earlierPhaseOnCurrentGuest=ring)),flush=True);return
 return function()


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if FOLDER.exists():(FOLDER/'host_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
