"""Both human slots: every captured blocked Bicycle scene, native shadow/erase."""
import json
import sys
import traceback
from pathlib import Path
import current_bicycle_block_render_contract_v3361 as render
import verify_current_bicycle_block_display_state_v3359 as state
import verify_native_cpu_ring_erase_v2985 as erase

ROOT=state.ROOT;OUT=ROOT/'audit_v3363_current_bicycle_block_render_erase_checked';need=state.need

def run():
    expected=state.current.expected_current()
    state.current.assembly.NAME=state.current.current.CANDIDATE
    state.current.assembly.expected=lambda:expected
    path=state.OUT/'report.json';proof=json.loads(path.read_text())
    need(proof['passed'] and proof['physicalFixtures']==2 and proof['actualBothPhysicalSlotsBlockedChipAndRecoveryAccepted'],
         'Actual current independently verified both-slot blocked capture')
    pins=dict(proof['inputHashes']);pins[str(path)]=state.current.assembly.sha(path)
    for file,digest in pins.items():need(state.current.assembly.sha(file)==digest,'Executed state/source/capture bytes unchanged')
    cases=[]
    erase.source_contract()
    for side in (1,2):
        scene=render.verify(side)
        need(scene['passed'] and scene['sampledFrames']==67 and scene['allOriginalBicyclePosesVisible'],
             'Every source-derived blocked startup/cycle pose, native body/shadow/physical palette and scene')
        folder=ROOT/f'audit_v3358_current_bicycle_block_display_p{side}_kano'
        erased=erase.inspect(folder,expected[0],state.current.current.CANDIDATE)
        need(erased['passed'] and erased['continuousExactFlips']==67 and erased['oneInitialBaseOnly'] and
             not erased['laterBuffersUsedAsAnchors'],'Every native erase/shift/flip from one initial base, no later buffer anchors')
        for table in (scene['inputHashes'],erased['inputHashes']):
            for file,digest in table.items():
                need(file not in pins or pins[file]==digest,'Consistent actual body/shadow/erase source pins');pins[file]=digest
        cases.append(dict(side=side,case=folder.name,scene=scene,erase=erased))
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).suffix=='.py'and Path(file).resolve().is_relative_to(ROOT/'tools'):
            pins[str(Path(file).resolve())]=state.current.assembly.sha(file)
    for file,digest in pins.items():need(state.current.assembly.sha(file)==digest,'Executed rendering sources and actual captured bytes unchanged')
    return dict(passed=True,candidate=state.current.current.CANDIDATE,cases=cases,physicalFixtures=2,
                fullCapturedBlockedNativeBodyPaletteShadowEraseAccepted=True,
                sampledFrames=sum(c['scene']['sampledFrames']for c in cases),
                exactScreenPixels=sum(c['scene']['exactScreenPixels']for c in cases),
                nativeShadowCopies=sum(c['scene']['nativeShadowCopies']for c in cases),
                sourceBoundProjections=sum(c['scene']['sourceBoundProjections']for c in cases),
                continuousExactFlips=sum(c['erase']['continuousExactFlips']for c in cases),
                fullDefenderHorizontalPushAndAudioAccepted=False,allCPUOrArenasKOOverlapAccepted=False,
                newGameBuildOrRawAudioCopies=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite executed native body/shadow/erase evidence')
    try:result=run()
    except Exception as error:result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in ('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if result['passed']else 1)
