"""Actual current opposite-character physical both-Down Tomb, exact mixed audio.

Whole5790 cold RAM collector and full source mixing. Whole original physical
inputs/health/action/801cleanup/269phase and victim-role voice gates retained.
"""
import argparse,gzip,hashlib,inspect,json,traceback
from pathlib import Path
import run_current_pressed_tomb_winner_mix_v5790 as base
import current_cross_pressed_tomb_state_v5855 as pressed
import current_cross_tomb_branches_v5837 as cross_voice
import qualify_current_cross_pressed_tomb_audio_v5857 as source
ROOT,need,sha=base.ROOT,base.need,base.sha
current,model,runtime=base.current,base.model,base.runtime
LUA='mk2ks_current_cross_pressed_tomb_campaign_v5854.lua'
OBSERVER=base.OBSERVER
once=base.once
EXTRA_INPUTS=('mk2ks_current_cross_pressed_tomb_driver_v5852.lua',
 'mk2ks_current_cross_pressed_tomb_provenance_v5853.lua','tools/current_cross_pressed_tomb_state_v5855.py',
 'tools/run_current_cross_pressed_tomb_audio_v5856.py','tools/qualify_current_cross_pressed_tomb_audio_v5857.py',
 'tools/current_cross_tomb_branches_v5837.py','tools/run_current_pressed_tomb_winner_mix_v5790.py',
 'tools/assemble_current_pressed_tomb_full_scene_v5831.py')

def adapt(code):
 body=once(inspect.getsource(base.adapt),'audit_v5794_current_pressed_tomb_winner_mix_',
  'audit_v5859_current_cross_pressed_tomb_winner_mix_')
 need(body.count('mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua')==2,'Original controller and explicit original source pin')
 body=body.replace('mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua','mk2ks_current_cross_pressed_tomb_driver_v5852.lua')
 body=once(body,'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_current_cross_pressed_tomb_provenance_v5853.lua')
 namespace=dict(vars(base),current=current,model=model,source=source,LUA=LUA,OBSERVER=OBSERVER)
 exec(compile(body,__file__+'::whole5790_cross_pressed_capture_adapter','exec'),namespace)
 code=namespace['adapt'](code)
 before='    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}'
 return once(code,before,'    files.update(ROOT/p for p in '+repr(EXTRA_INPUTS)+')\n'+before)

collector_source=inspect.getsource(base.collector)
collector_scope=dict(vars(base),__file__=__file__,__doc__=__doc__,adapt=adapt,pressed=pressed,
 current=current,model=model,source=source,LUA=LUA,OBSERVER=OBSERVER)
exec(compile(collector_source,__file__+'::whole5790_current_cross_pressed_factory','exec'),collector_scope)
collector=collector_scope['collector']
voice_models=cross_voice.voice_models
run_source=once(inspect.getsource(base.run),' phase_faults=pressed.pressed_phase_faults(text,fighter,side,guest)',
 ' phase_faults=pressed.pressed_phase_faults(text,fighter,side,guest)\n source_faults=pressed.source_faults(text,guest,fighter,side)')
run_source=once(run_source,'  actualPressedPhaseFaultsRejected=phase_faults,sourceQualifiedNativeLateVictimVoice=voice,',
 '  actualPressedPhaseFaultsRejected=phase_faults,actualPressedSourceWriterFaultsRejected=source_faults,sourceQualifiedNativeLateVictimVoice=voice,')
run_scope=dict(vars(base),__file__=__file__,__doc__=__doc__,collector=collector,pressed=pressed,
 current=current,model=model,source=source,voice_models=voice_models,LUA=LUA,OBSERVER=OBSERVER)
exec(compile(run_source,__file__+'::whole5790_actual_cross_pressed_run','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 folder=ROOT/f'audit_v5859_current_cross_pressed_tomb_winner_mix_{args.fighter}_p{args.side}_samples'
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():(folder/'audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
