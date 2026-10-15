"""Current true-ID cross Pit: full native plus winner audio, only RAM buffers.

Entire5838 cold collector and5781 full native source mixer/DAC/ROM pipeline.
Original seven earned arenas/own command/801states/1100cleanup required.
Source-exact raw PCM is not a substitute for subsequent cinematic voice,
cue/priority/source ownership and full render/floor-shadow qualification.
"""
import argparse,gzip,hashlib,inspect,json,time,traceback
from pathlib import Path
from types import SimpleNamespace
import run_current_cross_tomb_audio_v5838 as original
import current_cross_pit_earned_state_v5893 as state
import qualify_current_cross_pit_audio_v5895 as source
ROOT,need,sha=original.ROOT,original.need,original.sha
current,model=original.current,original.model
once,fields=original.once,original.fields
LUA='mk2ks_current_pit_winner_mix_campaign_v5892.lua'
OBSERVER='mk2ks_current_pit_winner_mix_observer_v5891.lua'
EXTRA_INPUTS=original.EXTRA_INPUTS+(
 LUA,OBSERVER,'tools/current_cross_pit_earned_state_v5893.py',
 'tools/run_current_cross_pit_winner_mix_v5894.py','tools/qualify_current_cross_pit_audio_v5895.py')

def adapt(code):
 changes=(
  ('audit_v5841_current_cross_tomb_winner_mix_','audit_v5897_current_cross_pit_winner_mix_'),
  (original.LUA,LUA),("MK2KS_STAGE_ARENA='1'","MK2KS_STAGE_ARENA='6'"),
  ('    files.update(ROOT/p for p in '+repr(original.EXTRA_INPUTS)+')',
   '    files.update(ROOT/p for p in '+repr(EXTRA_INPUTS)+')'),
 )
 for before,after in changes:code=once(code,before,after)
 return code

def collector():
 previous,_=original.collector();code=adapt(previous.source)
 namespace=dict(previous.__globals__,__file__=__file__,__doc__=__doc__,state=state,
  source=source,model=model,current=current,OBSERVER=OBSERVER)
 exec(compile(code,__file__+'::whole5838_current_Pit_RAM_audio','exec'),namespace)
 fn=namespace['capture'];fn.source=code
 return fn,hashlib.sha256(code.encode()).hexdigest().upper()

run_source=inspect.getsource(original.base.run)
run_source=once(run_source,'runtime.state.check_log(text,fighter,side,1,guest=guest)',
 'runtime.state.check_log(text,fighter,side,6,guest=guest)')
run_source=once(run_source,"need(waveform['passed'],",
 "need(waveform['passed']and waveform['actualMixedRawPCMByteFaultSuiteAccepted'],")
run_source=once(run_source,'nativeEarnedTombState=native,','nativeEarnedPitState=native,')
run_source=once(run_source,'actualEarnedStateFaultsRejected=state_faults,pcmHeaders=headers,',
 'actualEarnedStateFaultsRejected=state_faults,actualMixedRawPCMByteFaultSuiteAccepted=True,pcmHeaders=headers,')
run_source=once(run_source,"if k!='actualCallbackSourceClocks'","if k not in ('actualCallbackSourceClocks','expectedWinnerCallbackStates')")
run_scope=dict(vars(original.base),__file__=__file__,__doc__=__doc__,current=current,
 runtime=SimpleNamespace(state=state),model=model,source=source,collector=collector,LUA=LUA,OBSERVER=OBSERVER)
exec(compile(run_source,__file__+'::whole5781_actual_current_cross_Pit_audio','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 folder=ROOT/f'audit_v5897_current_cross_pit_winner_mix_{args.fighter}_p{args.side}_samples'
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():(folder/'audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
