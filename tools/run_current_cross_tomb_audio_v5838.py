"""Whole bounded current audio capture; ordinary Kano/Sonya opposite selections.

Every sample stays in RAM. No builds, source copies, forced branches or states.
Original health/input/action/801cleanup and full source mixing are retained.
"""
import argparse,gzip,hashlib,inspect,json,time,traceback
from pathlib import Path
import run_current_tomb_winner_mix_v5781 as base
import current_payload_metadata_context_v5229 as current
import current_tomb_winner_mix_fault_model_v5789 as model
import current_cross_tomb_state_v5836 as state
import current_cross_tomb_branches_v5837 as branches
import qualify_current_cross_tomb_audio_v5839 as source
ROOT,need,sha=current.ROOT,current.need,current.sha
runtime=base.runtime
LUA='mk2ks_current_cross_tomb_campaign_v5835.lua'
OBSERVER=base.OBSERVER
fields=base.fields
once=base.once
EXTRA_INPUTS=('mk2ks_current_cross_tomb_driver_v5833.lua',
 'mk2ks_current_cross_tomb_provenance_v5834.lua','tools/current_cross_tomb_state_v5836.py',
 'tools/current_cross_tomb_branches_v5837.py','tools/run_current_cross_tomb_audio_v5838.py',
 'tools/qualify_current_cross_tomb_audio_v5839.py','tools/run_current_tomb_winner_mix_v5781.py',
 'tools/current_tomb_winner_mix_fault_model_v5789.py','tools/verify_tomb_mirror_native_branches_v4357.py',
 'tools/verify_native_tomb_scream_roles_v4394.py')

def adapt(code):
 body=once(inspect.getsource(base.adapt),'audit_v5784_current_tomb_winner_mix_',
  'audit_v5841_current_cross_tomb_winner_mix_')
 namespace=dict(vars(base),current=current,model=model,source=source,LUA=LUA,OBSERVER=OBSERVER)
 exec(compile(body,__file__+'::whole5781_current_cross_adapter','exec'),namespace)
 code=namespace['adapt'](code)
 code=once(code,'mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_current_cross_tomb_driver_v5833.lua')
 code=once(code,'mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_current_cross_tomb_provenance_v5834.lua')
 before='    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}'
 return once(code,before,'    files.update(ROOT/p for p in '+repr(EXTRA_INPUTS)+')\n'+before)

collector_source=once(inspect.getsource(base.collector),
 'namespace=dict(vars(runtime),__file__=__file__,adapt=adapt,current=current,model=model,source_module=source,',
 'namespace=dict(vars(runtime),__file__=__file__,adapt=adapt,current=current,model=model,source_module=source,state=state,')
collector_scope=dict(vars(base),__file__=__file__,adapt=adapt,current=current,model=model,source=source,
 state=state,LUA=LUA,OBSERVER=OBSERVER)
exec(compile(collector_source,__file__+'::whole5781_factory_actual_cross','exec'),collector_scope)
collector=collector_scope['collector']

run_source=inspect.getsource(base.run)
need(run_source.count('runtime.state.')==2,'Both original full earned state and negative contract callsites')
run_source=run_source.replace('runtime.state.','state.')
run_source=once(run_source,' gate,fault=model.dac_models(len(headers));',
 " phase=branches.branch(text,guest,fighter,side)\n branch_faults=branches.faults(text,guest,fighter,side)\n voice,voice_faults=branches.voice_proof(text,guest,fighter,side,phase)\n gate,fault=model.dac_models(len(headers));")
run_source=once(run_source,"need(waveform['passed'],","need(waveform['passed']and waveform['actualMixedRawPCMByteFaultSuiteAccepted'],")
run_source=once(run_source,'  actualEarnedStateFaultsRejected=state_faults,pcmHeaders=headers,',
 '  actualEarnedStateFaultsRejected=state_faults,sourceQualifiedNativeBranch=phase,actualOriginalBranchFaultsRejected=branch_faults,sourceQualifiedNativeLateVictimVoice=voice,actualLateVictimVoiceFaultsRejected=voice_faults,actualMixedRawPCMByteFaultSuiteAccepted=True,pcmHeaders=headers,')
run_source=once(run_source,"if k!='actualCallbackSourceClocks'","if k not in('actualCallbackSourceClocks','expectedWinnerCallbackStates')")
run_scope=dict(vars(base),__file__=__file__,current=current,model=model,state=state,branches=branches,
 source=source,collector=collector,LUA=LUA,OBSERVER=OBSERVER)
exec(compile(run_source,__file__+'::whole5781_actual_cross_run','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 folder=ROOT/f'audit_v5841_current_cross_tomb_winner_mix_{args.fighter}_p{args.side}_samples'
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():(folder/'audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
