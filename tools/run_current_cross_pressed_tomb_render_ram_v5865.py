"""Current opposite-character physical both-Down Tomb: whole scene and shadows.

Whole5827 cold RAM collector, whole4401 pressed scene and all original3648
FIFO/body/projection/ground/compressed-shadow/retirement gates retained. Only
actual cross selection, opposite victim, reference and normal palettes change.
No game writes, RNG normalization, later target anchors or raw media copies.
"""
import argparse,gzip,hashlib,inspect,json,subprocess,traceback
from pathlib import Path
import run_current_pressed_tomb_render_ram_v5827 as base
import run_current_cross_pressed_tomb_audio_v5856 as timing
import current_cross_pressed_tomb_state_v5855 as native
import verify_current_cross_pressed_tomb_audio_v5860 as audio_proof
ROOT,need,sha=base.ROOT,base.need,base.sha
current,model,old=base.current,base.model,base.old
NAME=current.NAME
original_pressed=base.original_pressed
original_contract_source=base.original_contract_source
OBSERVER=ROOT/'mk2ks_current_cross_pressed_tomb_display_ram_v5864.lua'
once=timing.once
contract_source=base.contract_source
scene_scope=dict(vars(old),model=model,native=native,gzip=gzip)
exec(compile(contract_source,__file__+'::whole4401_actual_cross_pressed_scene','exec'),scene_scope)
scene_contract=scene_scope['scene_contract']

def paths(fighter,side):
 need(fighter in('kano','sonya')and side in(1,2),'Exact real character/physical slot')
 return ROOT/f'audit_v5866_current_cross_pressed_tomb_{fighter}_p{side}_render_ram',ROOT/f'audit_v5867_current_cross_pressed_tomb_{fighter}_p{side}_render_checked'

controls_source=inspect.getsource(base.controls)
controls_source=once(controls_source,
 '"dofile(\'mk2ks_stage_branch_provenance_v1722.lua\')":"dofile(\'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua\')"',
 '"dofile(\'mk2ks_stage_branch_provenance_v1722.lua\')":"dofile(\'mk2ks_current_cross_pressed_tomb_provenance_v5853.lua\')"')
begin=controls_source.index("    expected=(ROOT/'mk2ks_pressed_mirror_display_ram_v4400.lua')")
end=controls_source.index("    need(OBSERVER.read_text()==expected",begin)
expected_block="""    expected=(ROOT/'mk2ks_current_pressed_tomb_display_ram_v5828.lua').read_text().replace(
      '-- Original3624 RAM-only sinks; only its driver target becomes true mirrors.',
      '-- Original3624 RAM-only sinks; actual opposite-character physical both-Down driver.').replace(
      'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_current_cross_pressed_tomb_provenance_v5853.lua').replace(
      '@complete3624_native_pressed_mirror_scene_RAM_sinks_5828','@complete3624_native_cross_pressed_scene_RAM_sinks_5864')
"""
controls_source=controls_source[:begin]+expected_block+controls_source[end:]
controls_scope=dict(vars(base),__file__=__file__,__doc__=__doc__,model=model,native=native,timing=timing,
 OBSERVER=OBSERVER,contract_source=contract_source)
exec(compile(controls_source,__file__+'::whole5827_passive_cross_pressed_observer','exec'),controls_scope)
controls=controls_scope['controls'];controls.source=controls_source

preflight_source=inspect.getsource(base.preflight)
preflight_scope=dict(vars(base),controls=controls,native=native,model=model)
exec(compile(preflight_source,__file__+'::whole5827_model_and_proxy_checks','exec'),preflight_scope)
preflight=preflight_scope['preflight'];preflight.source=preflight_source

run_source=inspect.getsource(base.run)
changes=(
 ("identity=17 if fighter=='kano'else 18;ids=(identity,identity)",
  "identity=17 if fighter=='kano'else 18;ids=tuple(identity if slot==side else 35-identity for slot in(1,2))"),
 ('audit_v5796_current_pressed_tomb_enabled_winner_mix_checked/report.json',
  'audit_v5861_current_cross_pressed_tomb_enabled_audio_checked/report.json'),
 ("matrix['actualCurrentBothCharactersBothSidesPressedTombEnabledWinnerMixAccepted']",
  "matrix['actualCurrentBothCharactersBothSidesCrossPressedTombEnabledWinnerMixAccepted']"),
 ('mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua','mk2ks_current_cross_pressed_tomb_driver_v5852.lua'),
 ('mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_current_cross_pressed_tomb_provenance_v5853.lua'),
 ("need(palettes=={1:[False],2:[True]},'Normal native mirror selection gives exactly P1normal/P2alternate, no forced flags')",
  "need(palettes=={1:[False],2:[False]},'Actual different-character selection gives normal palettes in both physical slots, no forced flags')"),
 ('actualCurrentPressedMirrorNativeTombWholeRenderPaletteShadowEraseAccepted=True',
  'actualCurrentCrossPressedNativeTombWholeRenderPaletteShadowEraseAccepted=True'),
 ('nativeMirrorPaletteSelectors=palettes,',
  'nativeCrossPaletteSelectors=palettes,actualEarnedFaultsRejected=earned_faults,actualPressedPhaseFaultsRejected=phase_faults,actualPressedSourceWriterFaultsRejected=source_faults,actualPhysicalInputFaultsRejected=input_faults,'),
 ("    palettes={n:sorted({bool(q['body']&64)for q in scene.groups['FLOOR_QUEUE']if q['slot']==n})for n in(1,2)}",
  "    earned_faults=native.actual_faults(text,fighter,side,guest)\n    phase_faults=native.pressed_phase_faults(text,fighter,side,guest)\n    source_faults=native.source_faults(text,guest,fighter,side)\n    input_faults=audio_proof.input_faults(text,guest,fighter,side)\n    palettes={n:sorted({bool(q['body']&64)for q in scene.groups['FLOOR_QUEUE']if q['slot']==n})for n in(1,2)}"),
 ('true mirror complete native scene RAM','actual cross pressed complete native scene RAM'),
 ('mirror {len(scene.records)} whole fields exact','cross pressed {len(scene.records)} whole fields exact'),
)
for before,after in changes:run_source=once(run_source,before,after)
run_scope=dict(vars(base),__file__=__file__,__doc__=__doc__,paths=paths,preflight=preflight,controls=controls,
 scene_contract=scene_contract,model=model,native=native,timing=timing,
 OBSERVER=OBSERVER,audio_proof=audio_proof)
exec(compile(run_source,__file__+'::whole5827_actual_opposite_pressed_current_scene','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 CASE,OUT=paths(args.fighter,args.side)
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Never overwrite actual native whole-scene outcome');OUT.mkdir()
 need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Bounded text compressed before write')
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','nativeScene','nativeBranch')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
