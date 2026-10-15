"""Source-bound original off-top uppercut cull, not a missing-body waiver."""
import struct
from pathlib import Path
import verify_native_arena_geometry_v1583 as arena
import build_mk2ks_mk3 as layout

def prove(groups,record,side,identity,guest,payload):
    frame=record['frame']-1
    assert record['body'][side]['pixels']==0 and record['body'][side]['mismatches']==0
    assert not any(q['frame']==frame and q['slot']==side for q in groups['FLOOR_QUEUE'])
    assert not any(q['slot']==side and q['frame']==frame for q in groups['FLOOR_QUEUE_DISPATCH'])
    previous=[q for q in groups['FLOOR_QUEUE']if q['slot']==side and frame-2<=q['frame']<frame]
    assert previous,'An actually rendered physical uppercut trajectory must precede the cull'
    previous=max(previous,key=lambda q:q['frame'])
    assert previous['id']==previous['roster']==identity and previous['action']==0x503 and not previous['facing']&1
    observations=[s for s in groups['SHADOW_COMPONENT']if s['frame']==frame and s['slot']==side]
    assert observations,'Actual native cache/world/floor observations during cull required'
    by_component={}
    fields=('actor','main','owner','id','row','cache','component','first_source','width','height','xoff','yoff','command','x','y','floor','stageY','displayY','cameraY')
    for row in observations:
        assert row['id']==identity and row['actor']==row['owner']==previous['actor']and row['main']==previous['main']and row['cache']==previous['cache']
        assert row['row']==row['cache']+row['component']*112 and row['floor']==row['stageY']-{17:134,18:135}[identity]
        if row['component']in by_component:assert all(row[k]==by_component[row['component']][k]for k in fields)
        else:by_component[row['component']]=row
    assert sorted(by_component)==list(range(len(by_component)))and 0<len(by_component)<12
    parts=[by_component[i]for i in sorted(by_component)]
    assert all(s['y']<s['floor']and s['y']<previous['y']for s in parts),'Actual upward hurt movement, not a grounded hidden actor'
    assert all((s['x'],s['y'],s['floor'],s['cameraY'],s['displayY'])==(parts[0]['x'],parts[0]['y'],parts[0]['floor'],parts[0]['cameraY'],parts[0]['displayY'])for s in parts)
    # Require the complete observed cache to match a terminated native ROM
    # composite in this true character's own declared animation allocation.
    # No sampled pixels are used to choose the expected artwork or geometry.
    fighter={17:'kano',18:'sonya'}[identity];base=layout.HYBRID_FILE_BASES[fighter]
    matches=[]
    for offset in range(base,base+0x4000,2):
        pose=layout.DONOR_TMS_BASE+offset*8
        try:expected=arena.native.group(dict(pose=pose,facing=previous['facing']),payload,guest)
        except (ValueError,struct.error):continue
        if len(expected)==len(parts)and all((e['source'],e['width'],e['height'],e['dx'],e['dy'],e['command'])==
            (s['first_source'],s['width'],s['height'],s['xoff'],s['yoff'],s['command'])for e,s in zip(expected,parts)):
            matches.append(pose)
    assert matches,'Complete native cache must independently match owned ROM composite parts'
    original=(arena.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    first=(0xff8042a0-0xff800000)//8;last=(0xff804340-0xff800000)//8
    assert guest[first:last]==original[first:last],'Original native clipping comparisons unchanged'
    rectangles=[]
    for s in parts:
        top=s['y']-s['yoff']-s['cameraY'];bottom=top+s['height']-1
        assert bottom<0,'Every complete cached body part must lie above the native visible area'
        rectangles.append(dict(component=s['component'],source=s['first_source'],worldY=s['y'],
            cacheYOff=s['yoff'],cameraY=s['cameraY'],top=top,bottom=bottom,width=s['width'],height=s['height']))
    return dict(frame=record['frame'],arena=record['arena'],slot=side,id=identity,actor=previous['actor'],main=previous['main'],
        priorActualUppercutFrame=previous['frame'],originalClippingInstructionPathUnchanged=True,
        completeOwnedROMCompositeMatches=matches,actualPartRectangles=rectangles,kind='original_off_top_uppercut_cull')
