"""Actual Square/mirror one-initial-base continuous native screen-clear replay.

Unmodified v1843/v2985 chronological CPU/DMA/shift-load/FILL contract applies
to the actual contact capture. Later expected framebuffers never become anchors.
"""
import json,traceback
from pathlib import Path
import verify_native_cpu_ring_erase_v2985 as model
import verify_native_cpu_square_hit_render_v3044 as render

ROOT=model.ROOT;OUT=ROOT/'audit_v3047_native_cpu_square_hit_erase_checked'

def report():
    model.source_contract();pins={};cases={};guest,old,_,_,_=model.assembly.expected()
    model.scaled.source(pins)
    for key,(name,build,player)in render.CASES.items():
        path=ROOT/f'audit_v3045_native_cpu_square_hit_render_{key}_checked/report.json'
        scene=json.loads(path.read_text());model.need(scene['passed']and scene['allOriginalSquarePosesVisible']and not scene['fullPortAcceptance'],
            'Actual complete Square source/body/palette/shadow/raster proof')
        for file,wanted in scene['inputHashes'].items():
            model.need(file not in pins or pins[file]==wanted,'Consistent actual erase input');pins[file]=wanted
        pins[str(path)]=model.sha(path)
        case=model.inspect(ROOT/name,guest if build=='new'else old,scene['candidate'])
        model.need(case['passed']and case['oneInitialBaseOnly']and not case['laterBuffersUsedAsAnchors']and
            case['continuousExactFlips']==scene['sampledFrames'],'Every original continuous pre-buffer/flip/clear exact')
        case.update(case=name,candidate=scene['candidate'])
        for file,wanted in case['inputHashes'].items():
            model.need(file not in pins or pins[file]==wanted,'Consistent actual continuous erase input');pins[file]=wanted
        cases[key]=case;print(key+': every continuous native Square pre-buffer/flip/clear exact',flush=True)
    pins[str(Path(__file__).resolve())]=model.sha(__file__)
    for file,wanted in pins.items():model.need(model.sha(file)==wanted,'Actual captured native erase evidence unchanged '+file)
    return dict(passed=True,cases=cases,continuousExactPreBuffers=sum(c['continuousExactPreBuffers']for c in cases.values()),
        continuousExactFlips=sum(c['continuousExactFlips']for c in cases.values()),nativeShiftTransfers=sum(c['nativeShiftTransfers']for c in cases.values()),
        originalContinuousReplayContractUnchanged=True,oneInitialBaseOnlyPerActualFixture=True,laterBuffersUsedAsAnchors=False,
        actualPhysicalFixtures=1,gameChanged=False,allArenaMoveCPUOrMorphsAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    model.need(not OUT.exists(),'Immutable actual Square continuous erase proof')
    try:value=report()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('cases','inputHashes','scope')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
