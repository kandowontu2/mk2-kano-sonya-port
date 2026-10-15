"""Fresh normal-input Bicycle forward-step outcome; whole source/state/HP proof."""
import json
import sys
import traceback
from pathlib import Path
import current_launch_capture_contract_v3298 as capture
import verify_current_cpu_square_v3280 as current
import verify_native_cpu_mobility_inventory_v3038 as choices
import native_cpu_bicycle_round_boundary_contract_v3127 as missed
from current_jump_capture_contract_v3310 import responses as launch_responses

ROOT=current.ROOT
OUT=ROOT/'audit_v3313_current_cpu_bicycle_launch_response_checked'
CASE='audit_v3297_current_cpu_bicycle_launch_response'
need=current.need

def run():
    expected=current.expected_current()
    capture.assembly.NAME=current.current.CANDIDATE
    capture.assembly.expected=lambda:expected
    pins={}
    log,guest,case=capture.capture(ROOT/CASE,pins)
    native=choices.native_choices(log,guest,'kano')
    need(len(native)==1 and native[0]['move']=='bicycle' and not native[0]['nativeContact'],
         'Actual one naturally selected Bicycle miss; never relabel ordinary damage as contact')
    phase=missed.verify(log,guest)
    responses=launch_responses(log)
    active=[r for r in responses if r['advancing']]
    need(active and all(r['policy']=='close_on_launch' and r['cpu_action']==0x204 and r['gap']>68 and
                       r['advancing']==1 and r['guarding']==0 and r['writes']==0 and r['assistance']=='none'
                       for r in active), 'Actual legal forward-button response during native launch')
    need(case['health']['allModePhysicalFields']==3602 and case['cold']['human_id']==17 and
         case['cold']['cpu_id']==18 and case['selection']['checks']==50 and case['selection']['errors']==0,
         'Entire physical native ID/state/HP history from actual native selection')
    need(native[0]['firstRandomResult']==134 and native[0]['secondRandomResult'] is None and
         phase['start']==2663 and phase['ready']==2724 and phase['fields']==61,
         'Unmodified native first-choice branch and complete original miss, not prescribed RNG/move')
    pin=lambda p:pins.update({str(Path(p).resolve()):current.assembly.sha(p)})
    for file,digest in capture.assembly.source_check().items():
        need(file not in pins or pins[file]==digest,'Consistent independent assembly source');pins[file]=digest
    for old,new,from_path,to_path in capture.LINKS:
        pin(ROOT/old);pin(ROOT/new)
    pin(ROOT/'mk2ks_physical_p2_cpu_continuation_v3289.lua')
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools') and Path(file).suffix=='.py':pin(file)
    for file,digest in pins.items():need(current.assembly.sha(file)==digest,'Actual source/capture unchanged')
    case.update(case=CASE,nativeChoices=native,phase=phase,actualForwardInputFields=len(active),
                minimumGapDuringAdvancing=min(r['gap']for r in active))
    return dict(passed=True,candidate=current.current.CANDIDATE,case=case,
                actualPhysicalFixtures=1,wholeGuestPayloadStateHealthAndNativeChoicesAccepted=True,
                actualBicycleMissAccepted=True,candidateBicycleHitOrBlockedAccepted=False,
                nativeControllerOnly=True,CPUMoveOrRNGPrescribed=False,
                fullMoveRasterShadowEraseAudioAccepted=False,gameBytesChanged=False,
                fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual input-only outcome proof')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ('case','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if value['passed'] else 1)
