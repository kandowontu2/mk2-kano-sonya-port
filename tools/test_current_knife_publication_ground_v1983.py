"""Reject wrong-phase camera and shifted knife geometry in in-memory copies.

The actual capture, sprites, build and previous reports remain immutable.
These counterexamples are verifier tests, never emulator-state assistance.
"""
import json
from pathlib import Path
from unittest.mock import patch
import verify_current_knife_publication_ground_v1981 as model

ROOT=model.ROOT;OUT=ROOT/'audit_v1983_current_knife_publication_ground_counterexamples'

def run():
    path=model.OUT/'report.json';proof=json.loads(path.read_text())
    assert proof['passed']and proof['knifeReleaseContactAccepted']and not proof['allMoveGroundShadowAccepted']
    pins=dict(proof['inputHashes']);pins[str(path)]=model.current.state.launch.sha(path)
    for file,wanted in pins.items():assert model.current.state.launch.sha(file)==wanted
    actual_data=model.current.raster.data(model.CASE)
    group,buffer,a,b,owners=actual_data
    tests=[]
    def row(groups,tag,where):
        found=[i for i,r in enumerate(groups[tag])if all(r.get(k)==v for k,v in where.items())]
        assert len(found)==1,(tag,where,len(found))
        i=found[0];return groups[tag][i]
    def reject(name,change):
        changed={tag:[dict(r)for r in rows]for tag,rows in group.items()}
        change(changed)
        with patch.object(model.current.raster,'data',return_value=(changed,buffer,a,b,owners)):
            try:model.inspect()
            except(AssertionError,ValueError,KeyError,IndexError)as error:
                tests.append(dict(name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
            else:raise AssertionError('Accepted corruption '+name)
        print('Rejected '+str(len(tests))+': '+name,flush=True)
    cursor=0x0101cd00
    transform=lambda groups:row(groups,'FLOOR_QUEUE_TRANSFORM',{'frame':2549,'cursor':cursor})
    queue=lambda groups:row(groups,'FLOOR_QUEUE',{'frame':2549,'cursor':cursor})
    dma=lambda groups:row(groups,'FLOOR_DMA',{'event':1500})
    def wrong_camera(groups):
        t=transform(groups);t['camera']=(t['camera']&65535)|((-14&65535)<<16);t['cameraY']=-14
    reject('later_draw_camera_substituted_for_publication_camera',wrong_camera)
    reject('packed_and_observed_camera_disagree',lambda g:transform(g).update(cameraY=-14))
    def wrong_display(groups):
        t=transform(groups);t['display']=(t['display']&65535)|(255<<16);t['displayY']=255
    reject('display_base_shifted_one_pixel',wrong_display)
    def wrong_floor(groups):
        transform(groups)['floor']=83;queue(groups)['floor']=83
    reject('character_floor_shifted_one_pixel',wrong_floor)
    reject('actual_DMA_y_shifted_one_pixel',lambda g:dma(g).update(y=364))
    reject('actual_DMA_x_shifted_one_pixel',lambda g:dma(g).update(x=267))
    reject('published_xy_shifted_one_pixel',lambda g:queue(g).update(xy=queue(g)['xy']+65536))
    reject('native_projection_camera_bypass',lambda g:transform(g).update(a7=transform(g)['a7']|1))
    reject('wrong_native_facing',lambda g:queue(g).update(facing=queue(g)['facing']^16))
    reject('wrong_actual_sprite_source',lambda g:dma(g).update(source=dma(g)['source']+8))
    def missing(groups):
        groups['FLOOR_DMA']=[r for r in groups['FLOOR_DMA']if r['event']!=1500]
    reject('missing_original_body_component_DMA',missing)
    baseline=model.inspect()
    assert baseline['records']==proof['records'],'Real capture still passes with the same observations'
    for file,wanted in pins.items():assert model.current.state.launch.sha(file)==wanted,'Original evidence changed'
    model.current.state.launch.launch.module_pins(pins)
    return dict(passed=True,candidate=proof['candidate'],counterexamples=tests,inputHashes=pins,
        originalCapturesUnchanged=True,gameBytesChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=run()
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=result['passed'],counterexamples=len(result.get('counterexamples',[])),error=result.get('error'))),flush=True)
    raise SystemExit(0 if result['passed']else 1)


