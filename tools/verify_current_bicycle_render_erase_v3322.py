"""Current real CPU Bicycle hit, complete captured native art/shadow/erase."""
import json
import sys
import traceback
from pathlib import Path
import verify_current_cpu_square_v3280 as current
import verify_current_cpu_launch_jump_v3319 as state
import current_bicycle_render_contract_v3321 as render
import verify_native_cpu_ring_erase_v2985 as erase
ROOT=current.ROOT;OUT=ROOT/'audit_v3323_current_cpu_bicycle_hit_render_erase_checked';need=current.need

def run():
    expected=current.expected_current()
    current.assembly.NAME=current.current.CANDIDATE;current.assembly.expected=lambda:expected
    proof_path=state.OUT/'report.json';proof=json.loads(proof_path.read_text())
    need(proof['passed'] and proof['candidate']==current.current.CANDIDATE and proof['actualNativeBicycleContactDamageAndSeparateRecoveryAccepted'],'Real current whole-source contact proof required')
    pins=dict(proof['inputHashes']);pins[str(proof_path)]=current.assembly.sha(proof_path)
    for file,digest in pins.items():need(current.assembly.sha(file)==digest,'Actually captured and executed proof inputs unchanged')
    scene=render.verify()
    need(scene['passed'] and scene['candidate']==current.current.CANDIDATE and scene['sampledFrames']==109 and
         scene['allOriginalBicyclePosesVisible'],'Every native paired body/animation/palette/shadow/full scene')
    erase.source_contract();erased=erase.inspect(ROOT/state.CASE,expected[0],current.current.CANDIDATE)
    need(erased['passed'] and erased['continuousExactFlips']==109 and erased['oneInitialBaseOnly'] and not erased['laterBuffersUsedAsAnchors'],
         'Every original chronological erase/pre-buffer/flip from one initial base')
    for table in (scene['inputHashes'],erased['inputHashes']):
        for file,digest in table.items():
            need(file not in pins or pins[file]==digest,'Consistent actual input pin');pins[file]=digest
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=current.assembly.sha(file)
    for file,digest in pins.items():need(current.assembly.sha(file)==digest,'Executed render/erase source and captured bytes unchanged')
    return dict(passed=True,candidate=current.current.CANDIDATE,case=state.CASE,physicalFixtures=1,
                actualBicycleDamage=22,sampledFrames=scene['sampledFrames'],exactScreenPixels=scene['exactScreenPixels'],
                nativeShadowCopies=scene['nativeShadowCopies'],sourceBoundProjections=scene['sourceBoundProjections'],
                continuousExactFlips=erased['continuousExactFlips'],originalOwnAndVictimBicyclePosesVisible=True,
                fullCapturedNativeBodyPaletteShadowAndChronologicalEraseAccepted=True,
                fullMovePhaseAndHorizontalPushAccepted=False,allCPUContextsArenasKOOverlapAudioAccepted=False,
                gameBytesChanged=False,fullPortAcceptance=False,scene=scene,erase=erased,inputHashes=pins)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite current native evidence')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('scene','erase','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
