"""Actual missing cross Tomb timings: full native and winner audio in RAM.

Whole5838 cold collector/source resampler/native DAC/ROM and original cross
earned/branch/voice gates retained. The actual previously observed ordinary
controller delays supply P1held and P2random-drop inputs, never native state.
Full raw PCM/DAC/guest/ROM remain in RAM; only bounded gzip/digests are saved.
"""
import argparse,gzip,hashlib,inspect,json,re,time,traceback
from pathlib import Path
import run_current_cross_tomb_audio_v5838 as original
import find_current_cross_tomb_native_branches_v5872 as search
import verify_current_cross_tomb_audio_v5842 as prior_proof
import qualify_current_cross_tomb_timing_audio_v5878 as source
ROOT,need,sha=original.ROOT,original.need,original.sha
current,model,state,branches=original.current,original.model,original.state,original.branches
base,runtime=original.base,original.runtime
LUA='mk2ks_current_cross_tomb_timing_audio_v5876.lua'
OBSERVER=original.OBSERVER
fields,once=original.fields,original.once
PROFILE_PATH=ROOT/'audit_v5875_current_cross_tomb_native_timing_progress/progress.json'
EXTRA_INPUTS=original.EXTRA_INPUTS+('mk2ks_current_cross_tomb_timing_driver_v5870.lua',
 'mk2ks_current_cross_tomb_timing_provenance_v5871.lua','tools/find_current_cross_tomb_native_branches_v5872.py',
 'tools/run_current_cross_tomb_timing_audio_v5877.py','tools/qualify_current_cross_tomb_timing_audio_v5878.py',
 'tools/verify_current_cross_tomb_audio_v5842.py','audit_v5875_current_cross_tomb_native_timing_progress/progress.json')

def selected_profile(fighter,side):
 profile=json.loads(PROFILE_PATH.read_text())
 need(profile['passed']and profile['goalStatus']=='active'and
  profile['actualMissingCrossP1HeldAndP2RandomDropStatesAccepted']and not profile['fullPortAcceptance'],
  'Actual whole current ordinary-input timing observations, not prescribed native RNG')
 return next(p for p in profile['selectedActualMissingBranchProfiles']if p['fighter']==fighter and p['physicalSlot']==side)

def physical_delay(fighter,side):
 return selected_profile(fighter,side)['physicalCommandDelay']

def qualify_timing(text,guest,fighter,side):
 profile=selected_profile(fighter,side)
 config=[fields(l)for l in text.splitlines()if l.startswith('MK2_TOMB_TIMING_CONFIGURATION ')]
 need(config==[dict(delay=str(profile['physicalCommandDelay']),writes='0',assistance='none')],
  'One actual declared ordinary physical command delay, no state/RNG assistance')
 phase=branches.branch(text,guest,fighter,side)
 need(phase==profile['nativeBranch']and phase['nativeDrop']==(side==2),
  'Entire actual independently observed native branch/owned victim/motion/cleanup, no outcome normalization')
 return dict(passed=True,physicalCommandDelay=profile['physicalCommandDelay'],
  independentCapture=profile['capture'],originalNativeStateAndRNGUntouched=True,nativeBranch=phase)

def adapt_existing(code):
 changes=(
  ('audit_v5841_current_cross_tomb_winner_mix_','audit_v5880_current_cross_tomb_timing_winner_mix_'),
  (original.LUA,LUA),
  ("controller='mk2ks_current_cross_tomb_driver_v5833.lua'","controller='mk2ks_current_cross_tomb_timing_driver_v5870.lua'"),
  ("ROOT/'mk2ks_current_cross_tomb_provenance_v5834.lua'","ROOT/'mk2ks_current_cross_tomb_timing_provenance_v5871.lua'"),
  ('    files.update(ROOT/p for p in '+repr(original.EXTRA_INPUTS)+')',
   '    files.update(ROOT/p for p in '+repr(EXTRA_INPUTS)+')'),
  ("MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder))",
   "MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder),MK2KS_TOMB_COMMAND_DELAY=str(physical_delay(fighter,side)))"),
  ("                if line.startswith(('MK2_NATIVE_DAC_RAM ','MK2_NATIVE_DCS_ROM ')):",
   """                if line.startswith('MK2_TOMB_TIMING_GUEST '):
                    h=fields(line);raw=bytes.fromhex(h.pop('hex'))
                    need(h==dict(frame='1',bytes='1048576')and raw==guest,'Whole additional initialized timing guest independently verified in RAM')
                    log.write('MK2_TOMB_TIMING_GUEST_DIGEST frame=1 bytes=1048576 sha256='+hashlib.sha256(raw).hexdigest().upper()+'\\n')
                elif line.startswith(('MK2_NATIVE_DAC_RAM ','MK2_NATIVE_DCS_ROM ')):"""),
 )
 for before,after in changes:code=once(code,before,after)
 return code

adapt_source=inspect.getsource(original.adapt)
adapt_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,source=source)
exec(compile(adapt_source,__file__+'::whole5838_source_adapter','exec'),adapt_scope)
original_adapt=adapt_scope['adapt']

def adapt(code):
 return adapt_existing(original_adapt(code))

collector_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,adapt=adapt,source=source)
exec(compile(original.collector_source,__file__+'::whole5838_cold_capture_factory','exec'),collector_scope)
original_collector=collector_scope['collector']

def collector():
 fn,digest=original_collector()
 fn.__globals__.update(physical_delay=physical_delay,__doc__=__doc__)
 return fn,digest

run_source=once(original.run.source,' phase=branches.branch(text,guest,fighter,side)',
 ' phase=branches.branch(text,guest,fighter,side)\n timing_proof=qualify_timing(text,guest,fighter,side)\n phase_faults=prior_proof.phase_faults(text,guest,fighter,side)if phase[\'nativeDrop\']else []')
run_source=once(run_source,'  actualEarnedStateFaultsRejected=state_faults,sourceQualifiedNativeBranch=phase,',
 '  actualEarnedStateFaultsRejected=state_faults,actualPhysicalCommandDelayProof=timing_proof,actualRandomPhaseFaultsRejected=phase_faults,sourceQualifiedNativeBranch=phase,')
run_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,source=source,collector=collector,
 qualify_timing=qualify_timing,prior_proof=prior_proof,LUA=LUA,OBSERVER=OBSERVER)
exec(compile(run_source,__file__+'::whole5838_actual_missing_cross_audio','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 folder=ROOT/f'audit_v5880_current_cross_tomb_timing_winner_mix_{args.fighter}_p{args.side}_samples'
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():(folder/'audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
