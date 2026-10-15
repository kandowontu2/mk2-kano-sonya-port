"""Missing actual cross Tomb timings: complete native scene and floor shadows.

Entire5847 cold RAM transport and original3648 one-base CPU/DMA/shift/VRAM/
palette/RGB/body/cache/composite/projection/ground/shadow/retirement+30 gates.
Only independently observed ordinary timing controls and their actual audio
references change. No prescribed RNG/native state, proxy, recordings or builds.
"""
import argparse,gzip,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import run_current_cross_tomb_render_ram_v5847 as original
import run_current_cross_tomb_timing_audio_v5877 as timing
import verify_current_cross_tomb_timing_audio_v5881 as audio_proof
ROOT,need,sha=original.ROOT,original.need,original.sha
current,model,old,native,branches=original.current,original.model,original.old,original.native,original.branches
once=timing.once
OBSERVER=ROOT/'mk2ks_current_cross_tomb_timing_display_ram_v5885.lua'
contract_source=original.contract_source
scene_scope=dict(vars(old),model=model,native=native,gzip=gzip)
exec(compile(contract_source,__file__+'::whole3648_missing_cross_scene','exec'),scene_scope)
scene_contract=scene_scope['scene_contract']

def paths(fighter,side):
 need(fighter in ('kano','sonya')and side in (1,2),'Actual true character and physical slot')
 return ROOT/f'audit_v5887_current_cross_tomb_timing_{fighter}_p{side}_render_ram',ROOT/f'audit_v5888_current_cross_tomb_timing_{fighter}_p{side}_render_checked'

controls_source=original.controls.source
need(controls_source.count('mk2ks_current_cross_tomb_provenance_v5834.lua')==2,
 'Exactly the full passive observer source target and complete wrapper reference')
controls_source=controls_source.replace('mk2ks_current_cross_tomb_provenance_v5834.lua',
 'mk2ks_current_cross_tomb_timing_provenance_v5871.lua',2)
controls_source=once(controls_source,
 '-- Original3624 RAM-only sinks; actual opposite-character PC-qualified driver.',
 '-- Original3624 RAM-only sinks; actual opposite-character PC-qualified timing driver.')
controls_source=once(controls_source,'@complete3624_native_cross_scene_RAM_sinks_5846',
 '@complete3624_native_cross_timing_scene_RAM_sinks_5885')
controls_scope=dict(vars(original.base),__file__=__file__,__doc__=__doc__,model=model,native=native,
 timing=timing,OBSERVER=OBSERVER,contract_source=contract_source)
exec(compile(controls_source,__file__+'::whole5847_timing_observer_preflight','exec'),controls_scope)
controls=controls_scope['controls'];controls.source=controls_source
preflight_source=original.preflight.source
preflight_scope=dict(vars(original.base),controls=controls,native=native,model=model)
exec(compile(preflight_source,__file__+'::whole5847_model_and_proxy_checks','exec'),preflight_scope)
preflight=preflight_scope['preflight'];preflight.source=preflight_source

run_source=original.run.source
changes=(
 ('audit_v5843_current_cross_tomb_audio_checked/report.json','audit_v5882_current_cross_tomb_timing_audio_checked/report.json'),
 ("matrix['actualCurrentBothCharactersBothSidesOppositeTombEnabledWinnerMixAccepted']",
  "matrix['actualCurrentBothCharactersBothSidesMissingCrossTombEnabledWinnerMixAccepted']"),
 ('mk2ks_current_cross_tomb_driver_v5833.lua','mk2ks_current_cross_tomb_timing_driver_v5870.lua'),
 ('mk2ks_current_cross_tomb_provenance_v5834.lua','mk2ks_current_cross_tomb_timing_provenance_v5871.lua'),
 ("MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(CASE))",
  "MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(CASE),MK2KS_TOMB_COMMAND_DELAY=str(timing.physical_delay(fighter,side)))"),
 ("    phase_faults=audio_proof.phase_faults(text,guest,fighter,side)if branch['nativeDrop']else []",
  "    phase_faults=audio_proof.phase_faults(text,guest,fighter,side)if branch['nativeDrop']else []\n    physical_proof=audio_proof.physical_gate(text,guest,fighter,side)\n    physical_faults=audio_proof.timing_faults(text,guest,fighter,side)"),
 ('actualCurrentOppositeNativeTombWholeRenderPaletteShadowEraseAccepted=True',
  'actualCurrentMissingCrossNativeTombWholeRenderPaletteShadowEraseAccepted=True'),
 ('nativeCrossPaletteSelectors=palettes,actualEarnedFaultsRejected=earned_faults,',
  'nativeCrossPaletteSelectors=palettes,actualPhysicalInputTimingProof=physical_proof,actualPhysicalTimingFaultsRejected=physical_faults,actualEarnedFaultsRejected=earned_faults,'),
)
for before,after in changes:run_source=once(run_source,before,after)
run_scope=dict(vars(original.base),__file__=__file__,__doc__=__doc__,paths=paths,preflight=preflight,
 controls=controls,scene_contract=scene_contract,model=model,native=native,branches=branches,timing=timing,
 OBSERVER=OBSERVER,audio_proof=audio_proof)
exec(compile(run_source,__file__+'::whole5847_actual_missing_cross_timing_scene','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 CASE,OUT=paths(args.fighter,args.side)
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Never overwrite actual complete native scene outcome');OUT.mkdir()
 need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Bounded text compressed before write')
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','nativeScene','nativeBranch')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
