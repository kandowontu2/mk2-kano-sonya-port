"""Current opposite-character Tomb: whole native scene, grounding and shadows.

Whole5820 cold RAM transport and original3648 scene gate retained. Only actual
cross selection/reference/state and natural non-mirror palettes change. Both
actual RNG outcomes are checked, never normalized or forced to match a fixture.
"""
import argparse,gzip,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import run_current_held_tomb_render_ram_v5820 as base
import run_current_cross_tomb_audio_v5838 as timing
import current_cross_tomb_state_v5836 as native
import current_cross_tomb_branches_v5837 as branches
import verify_current_cross_tomb_audio_v5842 as audio_proof
ROOT,need,sha=base.ROOT,base.need,base.sha
current=base.current
model=base.model
old=base.old
OBSERVER=ROOT/'mk2ks_current_cross_tomb_display_ram_v5846.lua'
once=timing.once
contract_source=base.contract_source
scene_scope=dict(vars(old),model=model,native=native,gzip=gzip)
exec(compile(contract_source,__file__+'::whole3648_actual_cross_scene','exec'),scene_scope)
scene_contract=scene_scope['scene_contract']

def paths(fighter,side):
 need(fighter in('kano','sonya')and side in(1,2),'Exact real character/physical slot')
 return ROOT/f'audit_v5848_current_cross_tomb_{fighter}_p{side}_render_ram',ROOT/f'audit_v5849_current_cross_tomb_{fighter}_p{side}_render_checked'

controls_source=inspect.getsource(base.controls)
controls_source=once(controls_source,
 '"dofile(\'mk2ks_stage_branch_provenance_v1722.lua\')":"dofile(\'mk2ks_tomb_mirror_provenance_ram_v4341.lua\')"',
 '"dofile(\'mk2ks_stage_branch_provenance_v1722.lua\')":"dofile(\'mk2ks_current_cross_tomb_provenance_v5834.lua\')"')
begin=controls_source.index("    expected=(ROOT/'mk2ks_tomb_mirror_display_ram_v4359.lua')")
end=controls_source.index("    need(OBSERVER.read_text()==expected",begin)
expected_block="""    expected=(ROOT/'mk2ks_current_held_tomb_display_ram_v5821.lua').read_text().replace(
      '-- Original3624 RAM-only sinks; only its driver target becomes true mirrors.',
      '-- Original3624 RAM-only sinks; actual opposite-character PC-qualified driver.').replace(
      'mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_current_cross_tomb_provenance_v5834.lua').replace(
      '@complete3624_native_held_mirror_scene_RAM_sinks_5821','@complete3624_native_cross_scene_RAM_sinks_5846')
"""
controls_source=controls_source[:begin]+expected_block+controls_source[end:]
controls_scope=dict(vars(base),__file__=__file__,model=model,native=native,timing=timing,
 OBSERVER=OBSERVER,contract_source=contract_source)
exec(compile(controls_source,__file__+'::whole5820_passive_cross_observer','exec'),controls_scope)
controls=controls_scope['controls'];controls.source=controls_source

preflight_source=inspect.getsource(base.preflight)
preflight_scope=dict(vars(base),controls=controls,native=native,model=model)
exec(compile(preflight_source,__file__+'::whole5820_model_and_proxy_checks','exec'),preflight_scope)
preflight=preflight_scope['preflight'];preflight.source=preflight_source

run_source=inspect.getsource(base.run)
changes=(
 ("identity=17 if fighter=='kano'else 18;ids=(identity,identity)",
  "identity=17 if fighter=='kano'else 18;ids=tuple(identity if slot==side else 35-identity for slot in(1,2))"),
 ('audit_v5786_current_enabled_tomb_winner_mix_checked/report.json',
  'audit_v5843_current_cross_tomb_audio_checked/report.json'),
 ("matrix['actualCurrentBothCharactersBothSidesHeldTombEnabledWinnerMixAccepted']",
  "matrix['actualCurrentBothCharactersBothSidesOppositeTombEnabledWinnerMixAccepted']"),
 ("need(not branch_reference['nativeDrop']and branch_reference['nativeMotion']['continuousArena1MotionCallbacks']>400,\n         'Exactly the real original held branch, no drop or pressed substitution')",
  "need(branch_reference['passed']and branch_reference['trueVictim']==35-identity and\n      ((branch_reference['nativeDrop']and branch_reference['nativeMotion']['phase']['checkedConsecutiveCallbacks']==269)or\n       (not branch_reference['nativeDrop']and branch_reference['nativeMotion']['continuousArena1MotionCallbacks']>400)),\n         'Exactly the actual original observed unpressed cross branch, not prescribed held/drop/button outcome')"),
 ('mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_current_cross_tomb_driver_v5833.lua'),
 ('mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_current_cross_tomb_provenance_v5834.lua'),
 ("need(not branch['nativeDrop']and branch==branch_reference,\n      'Exact actual independently-qualified unpressed held phase, not a random or pressed drop')",
  "need(branch==branch_reference,\n      'Exact independently qualified actual cross RNG/PC/IO/actor/Main/motion/retirement, no held/drop normalization')\n    earned_faults=native.actual_faults(text,fighter,side,guest)\n    branch_faults=branches.faults(text,guest,fighter,side)\n    phase_faults=audio_proof.phase_faults(text,guest,fighter,side)if branch['nativeDrop']else []"),
 ("need(palettes=={1:[False],2:[True]},'Normal native mirror selection gives exactly P1normal/P2alternate, no forced flags')",
  "need(palettes=={1:[False],2:[False]},'Actual different-character selection gives normal palettes in both physical slots, no forced flags')"),
 ('actualCurrentHeldMirrorNativeTombWholeRenderPaletteShadowEraseAccepted=True',
  'actualCurrentOppositeNativeTombWholeRenderPaletteShadowEraseAccepted=True'),
 ('nativeMirrorPaletteSelectors=palettes,',
  'nativeCrossPaletteSelectors=palettes,actualEarnedFaultsRejected=earned_faults,actualOriginalBranchFaultsRejected=branch_faults,actualDropPhaseFaultsRejected=phase_faults,'),
 ('true mirror complete native scene RAM','actual cross complete native scene RAM'),
 ('mirror {len(scene.records)} whole fields exact','cross {len(scene.records)} whole fields exact'),
)
for before,after in changes:run_source=once(run_source,before,after)
run_scope=dict(vars(base),__file__=__file__,paths=paths,preflight=preflight,controls=controls,
 scene_contract=scene_contract,model=model,native=native,branches=branches,timing=timing,
 OBSERVER=OBSERVER,audio_proof=audio_proof)
exec(compile(run_source,__file__+'::whole5820_actual_opposite_current_scene','exec'),run_scope)
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
