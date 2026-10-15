"""Whole corrected3172 natural CPU Bicycle contact and bounded phase evidence."""
import json
import sys
import traceback
from pathlib import Path
import current_jump_capture_contract_v3310 as capture
import verify_current_cpu_square_v3280 as current
import verify_native_cpu_mobility_inventory_v3038 as choices
import native_cpu_bicycle_hit_contract_v3317 as phase
ROOT=current.ROOT
OUT=ROOT/'audit_v3320_current_cpu_bicycle_launch_jump_checked'
CASE='audit_v3308_current_cpu_bicycle_launch_jump'
need=current.need

def run():
    expected=current.expected_current()
    capture.assembly.NAME=current.current.CANDIDATE
    capture.assembly.expected=lambda:expected
    pins={};log,guest,case=capture.capture(ROOT/CASE,pins)
    native=choices.native_choices(log,guest,'kano')
    need(len(native)==2 and native[0]['move']=='bicycle' and native[0]['nativeContact'] and
         native[1]['move']=='square' and not native[1]['nativeContact'],'One actual Bicycle contact followed by distinct later Square miss')
    typed=phase.verify(log,guest)
    active=[r for r in capture.responses(log)if r['advancing']]
    need([r['frame']for r in active]==[2664,2665,2666] and all(r['policy']=='jump_on_launch' and r['cpu_action']==0x204 and
         r['gap']>68 and r['advancing']==1 and r['guarding']==0 and r['writes']==0 and r['assistance']=='none'for r in active),
         'Only three ordinary forward-jump input fields; CPU move and RNG never prescribed')
    need(case['health']['allModePhysicalFields']==3602 and case['cold']['human_id']==17 and case['cold']['cpu_id']==18 and
         case['selection']['checks']==50 and case['selection']['errors']==0,'Complete actual selected identities, native health and state history')
    need(native[0]['firstRandomResult']==134 and native[0]['secondRandomResult']is None and
         typed['start']==2663 and typed['hit']==2680 and typed['damage']==22 and typed['ready']==2742 and typed['victimReady']==2767,
         'Unmodified native first-chance branch, actual original damage and distinct physical recoveries')
    for file,digest in capture.assembly.source_check().items():
        need(file not in pins or pins[file]==digest,'Consistent independent full assembly source');pins[file]=digest
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':
            pins[str(Path(file).resolve())]=current.assembly.sha(file)
    for file,digest in pins.items():need(current.assembly.sha(file)==digest,'Actual source and captured bytes unchanged')
    case.update(case=CASE,nativeChoices=native,phase=typed,actualForwardJumpInputFields=len(active))
    return dict(passed=True,candidate=current.current.CANDIDATE,case=case,actualPhysicalFixtures=1,
                wholeGuestPayloadStateHealthAndNativeChoicesAccepted=True,actualNativeBicycleContactDamageAndSeparateRecoveryAccepted=True,
                startupSeekPairedLiftFloatReleaseAndVerticalFallAccepted=True,fullHorizontalNativePushReplayAccepted=False,
                fullMovePhaseRasterShadowEraseAudioAccepted=False,allCPUOrKOOrArenasAccepted=False,
                nativeControllerOnly=True,CPUMoveOrRNGPrescribed=False,gameBytesChanged=False,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable real native contact evidence')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('case','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
