"""Separate current knife sole geometry from native layer occlusion.

Read-only inspection of the immutable v1972 capture. No gameplay or asset
changes. Original donor descriptors/pixels are independent of final masks.
Reports observations, not universal grounding or finished-port acceptance.
"""
import json,struct
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_current_cpu_knife_display_v1978 as current
from verify_native_floor_display_v602 import check_latch

ROOT=current.ROOT;CASE=current.CASE
OUT=ROOT/'audit_v1980_current_knife_sole_layers'

def inspect():
    proof_path=ROOT/'audit_v1978_current_cpu_knife_display_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed']
    pins=dict(proof['inputHashes'])
    for file,wanted in pins.items():
        assert current.state.launch.sha(file)==wanted,'Changed accepted visual input '+file
    pins[str(proof_path)]=current.state.launch.sha(proof_path)
    guest,_,payload=current.state.launch.launch.current.expected()
    assert (CASE/'guest_maincpu.bin').read_bytes()==guest
    image=bytearray(current.graphics.graphics(pins))
    for header in(0x1c0000,0x1c1000,0x1c2000,0x1d0000):
        source,count,dest=struct.unpack_from('<III',payload,header+4)
        image[dest:dest+count]=payload[source:source+count]
    sequences,pieces=current.art.independent_art(payload,bytes(image),pins)
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    groups,buffers,_,_,owners=current.raster.data(CASE)
    replay=current.scaled.Replay(CASE,groups,buffers,owners)
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
    dispatch={q['event']:q for q in groups['FLOOR_QUEUE_DISPATCH']}
    snaps={r['frame']:r for r in groups['FLOOR_SNAP']}
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
    latches={r['event']:r for r in groups['FLOOR_LATCH']if r['flip_frame']==r['snapshot']}
    pre={r['frame']:r for r in groups['FLOOR_PRE_FRAME']}
    selected={f for f in snaps if any(k['start']<f<=k['start']+26 for k in proof['state']['knives'])}
    windows=[(pre[l['snapshot']-1]['event'],event)for event,l in latches.items()if l['snapshot']in selected]
    events=sorted([(kind,r)for kind in('FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU','FLOOR_FLIP')for r in groups[kind]
        if any(first<=r['event']<=last for first,last in windows)],key=lambda v:v[1]['event'])
    records=[];own=None;geometry=None;erased={};parts=[]
    for kind,d in events:
        if kind=='FLOOR_PRE_FRAME':
            replay.apply(kind,d);own=np.zeros((512,512),dtype=bool);geometry=None;erased={};parts=[]
            continue
        if kind!='FLOOR_FLIP':
            before=(replay.body==2).copy()
            replay.apply(kind,d)
            removed=before&(replay.body!=2)
            if removed.any():
                name=('shadow'if kind=='FLOOR_DMA'and d['command']&15==8 else
                    'foreground_or_other_DMA'if kind=='FLOOR_DMA'else'CPU')
                erased.setdefault(name,np.zeros((512,512),dtype=bool));erased[name]|=removed
            if kind=='FLOOR_DMA'and d['slot']==2 and d['command']&15==2:
                pub=dispatch[d['event']];q=queues[pub['queue_frame'],pub['cursor']]
                if q['pose']not in sequences['knife']['body']:continue
                shape=current.art.group(q,payload,guest)[q['part']]
                original_pose=q['pose']+0x1000000
                _,descriptor=current.art.source_groups(donor,original_pose,0xff800000)[q['part']]
                w,h,dx,dy,source,command,palette=descriptor
                assert(w,h)==(shape['width'],shape['height'])
                assert shape['source']==source+0x10000000 and command&~0x30==shape['command']&~0x30
                assert shape['dx']==(w-dx if q['facing']&16 else dx)
                assert shape['dy']==(h-dy if q['facing']&32 else dy)
                # Original geometry from independently decoded source pixels.
                pixels=replay.decode(d['source'],d['command'],w,h)
                sy,sx=np.where(pixels!=0)
                relative=(-sy if q['facing']&32 else sy)-shape['dy']
                maximum=int(relative.max())
                geometry=maximum if geometry is None else max(geometry,maximum)
                isolated=current.scaled.Replay(CASE,groups,buffers,owners)
                isolated.words=np.zeros((512,512),dtype=np.uint16)
                isolated.body=np.zeros((512,512),dtype=np.uint8)
                isolated.shadow=np.zeros((512,512),dtype=bool)
                isolated.projected=np.zeros((512,512),dtype=bool)
                isolated.dma(d);own|=isolated.body==2
                parts.append(dict(event=d['event'],pose=q['pose'],part=q['part'],originalPose=original_pose,
                    donorDy=dy,actualDy=shape['dy'],height=h,originalLocalBottom=maximum))
            continue
        if d['event']not in latches:continue
        latch=latches[d['event']];frame=latch['snapshot']
        if frame not in selected or not parts:continue
        actual=np.fromfile(CASE/latch['file'],dtype='<u2').reshape(512,512)
        assert np.array_equal(replay.words,actual),'Final replay remains exact'
        display=displays[frame]
        rgb=np.asarray(Image.open(CASE/'snap'/snaps[frame]['file']).convert('RGB'))
        bound=check_latch(rgb,actual.tobytes(),(CASE/display['palette_file']).read_bytes(),d['value'],d['control'],d['tap'])
        row,col=bound['row'],bound['column'];crop=lambda a:a[row:row+254,col:col+400]
        visible=crop(replay.body==2);unoccluded=crop(own)
        actor=[a for a in groups['FLOOR_OWNER']if a['frame']==frame-1 and a['slot']==2][-1]
        assert actor['y']==actor['floor'] and actor['id']==17
        ground=actor['stageY']+5+actor['displayY']-actor['cameraY']-row
        original_bottom=actor['y']+geometry+actor['displayY']-actor['cameraY']-row
        rawsole=int(np.where(unoccluded)[0].max());sole=int(np.where(visible)[0].max())
        lost=unoccluded&~visible
        attribution={kind:int((crop(mask)&lost).sum())for kind,mask in erased.items()}
        records.append(dict(frame=frame,pose=parts[0]['pose'],actorY=actor['y'],floor=actor['floor'],nativeGround=ground,
            originalCompositeSole=original_bottom,unoccludedSole=rawsole,finalSole=sole,
            originalOffset=original_bottom-ground,unoccludedOffset=rawsole-ground,finalOffset=sole-ground,
            occludedBodyPixels=int(lost.sum()),occlusion=attribution,parts=parts))
    assert len(records)>30 and set(r['pose']for r in records)==set(sequences['knife']['body'])
    current.state.launch.launch.module_pins(pins)
    pins[str(Path(__file__).resolve())]=current.state.launch.sha(Path(__file__).resolve())
    return dict(passed=True,candidate=proof['candidate'],records=records,donorPiecesCompared=pieces,
        allEightBodyPosesInspected=True,observationOnly=True,inputHashes=pins,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=inspect()
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    if result['passed']:
        print(json.dumps(dict(passed=True,frames=len(result['records']),raised=[{k:r[k]for k in('frame','pose','originalOffset','unoccludedOffset','finalOffset','occlusion')}for r in result['records']if r['finalOffset']<-2])))
    else:print(json.dumps({k:result[k]for k in('passed','error')}))
    raise SystemExit(0 if result['passed']else 1)
