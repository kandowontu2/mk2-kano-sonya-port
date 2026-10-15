"""Actual two-human idle/mobility soles bound to original display flips and VRAM."""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from inspect_natural_arena_floor_v602 import decoder
from inspect_ground_presentation import rows as ground_rows
from verify_native_floor_display_v602 import check_latch

def rows(log,tag):
    if tag!='SHADOW_COMPONENT':return ground_rows(log,tag)
    output=[]
    for line in log.splitlines():
        if not line.startswith('MK2_GROUND_SHADOW_COMPONENT '):continue
        raw=dict(re.findall(r'(\w+)=([^\s]+)',line))
        output.append({k:(v if k in ('fighter','assistance')else int(v,16 if k in
            ('actor','main','owner','cache','row','first_source','command')else 10))for k,v in raw.items()})
    return output

def check_shadow_rows(log,buffers):
    dmas={r['event']:r for r in rows(log,'DMA')}
    components=defaultdict(list)
    component_rows=rows(log,'SHADOW_COMPONENT')
    shadow_events={d['event']for d in dmas.values()if 0x10000000<=d['source']<0x1a000000 and d['command']&15==8}
    assert shadow_events=={r['event']for r in component_rows},'Every own row has actual native cache evidence'
    for r in component_rows:
        assert r['id']in(17,18)and r['owner']==r['actor'],'Actual owned fighter projection'
        assert r['row']==r['cache']+r['component']*0x70,'Native component cache row'
        components[r['frame'],r['row']].append(r)
    checked=0
    for key,copies in components.items():
        first=copies[0];source,command,w,h=(first[k]for k in ('first_source','command','width','height'))
        assert all(all(r[k]==first[k]for k in ('slot','id','actor','main','owner','cache','first_source','width','height','command'))for r in copies),'Stable native component within row projection'
        record=buffers[f'{source:08X}_{command|0x8002:04X}_{w}_{h}']
        raw=bytes.fromhex(record['data']);bit=record['offset']%8;origin=bit;starts=[]
        bpp=(command>>12)&7 or 8
        assert bpp==6 and command&0x80,'Native six-bit compressed rows'
        for y in range(h):
            starts.append(source+bit-origin)
            assert bit+8<=len(raw)*8,'Complete row header'
            header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255
            pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
            assert pre+post<=w,'Nonnegative original scanner row width'
            bit+=8+bpp*(w-pre-post);assert bit<=len(raw)*8,'Full row stream'
        indices=list(range(0,4*(h//4),4));assert indices;indices.append(indices[-1])
        actual=[dmas[r['event']]for r in copies]
        assert len(actual)==len(indices),'Original quarter-height cadence plus final duplicated row'
        first_y=actual[0]['y'];first_x=actual[0]['x']
        expected=[(starts[y],command|0x8008,w,1,first_x,(first_y+i)&511,0,15,0xff801610 if i==len(indices)-1 else 0xff8015a0)for i,y in enumerate(indices)]
        observed=[tuple(d[k]for k in ('source','command','width','height','x','y','palette','color','pc'))for d in actual]
        assert observed==expected,'Every native source row/command/palette/colour/coordinate/caller matches independent compressed stream'
        checked+=len(actual)
    assert checked>0,'Actually projected native rows'
    return {'components':len(components),'copies':checked,'owned_events':{r['event']:r['slot']for r in component_rows},'rowStreamVerified':True}


def inspect(folder):
    folder=Path(folder)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    assert not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback',log,re.I)
    fields={(r['frame'],r['slot']):r for r in rows(log,'FIELD')}
    pre={r['frame']:r for r in rows(log,'PRE')}
    owners={(r['frame'],r['slot']):r for r in rows(log,'OWNER')}
    dmas=defaultdict(list)
    for r in rows(log,'DMA'):dmas[r['frame']].append(r)
    buffers={r['key']:r for r in rows(log,'GFX')}
    decode=decoder(buffers)
    native=check_shadow_rows(log,buffers)
    records=[]
    for snap in rows(log,'SNAP'):
        frame=snap['frame']
        image=np.asarray(Image.open(folder/'snap'/snap['file']).convert('RGB'))
        words=np.fromfile(folder/snap['vram_file'],dtype='<u2').reshape(512,512)
        number=lambda key:int(snap[key],16) if isinstance(snap[key],str) else snap[key]
        assert snap['flip_frame']==frame and snap['phase']=='frame_done'
        bound=check_latch(image,words.tobytes(),(folder/snap['palette_file']).read_bytes(),
                          number('start'),number('control'),number('tap'))
        native_black=int(np.fromfile(folder/snap['palette_file'],dtype='<u4')[15])==0
        page,col=bound['row'],bound['column']
        assert pre[frame-1]['phase']=='before_first_dma'
        expected=np.fromfile(folder/pre[frame-1]['file'],dtype='<u2').reshape(512,512).copy()
        owner=np.zeros((512,512),dtype=np.uint8)
        shadow_owner=np.zeros((512,512),dtype=np.uint8)
        for d in dmas[frame-1]:
            c,w,h=d['command'],d['width'],d['height']
            mode=c&15
            assert mode in (2,8,12) and d['skip']==0 and d['scaleX']in(0,256) and d['scaleY']in(0,256)
            if not w or not h:continue
            indices=np.zeros((h,w),dtype=np.uint8)if mode==12 else decode(d['source'],c,w,h)
            sy,sx=np.where(np.ones((h,w),dtype=bool)if mode==12 else indices!=0)
            x=(d['x']+(-sx if c&16 else sx))&1023
            y=(d['y']+(-sy if c&32 else sy))&511
            inside=(x>=d['left'])&(x<=d['right'])&(y>=d['top'])&(y<=d['bottom'])&(x<512)
            x,y,sy,sx=(a[inside]for a in(x,y,sy,sx))
            pens=np.full(len(x),d['color'],dtype=np.uint16)if mode in (8,12)else indices[sy,sx].astype(np.uint16)
            expected[y,x]=pens|d['palette']
            owner[y,x]=(1 if d['palette']==0x200 else 2)if mode==2 and d['palette']in(0x200,0x300)else 0
            shadow_owner[y,x]=native['owned_events'].get(d['event'],0)
        crop=lambda a:a[page:page+254,col:col+400]
        bodies={}
        for slot in (1,2):
            a=fields[frame-1,slot]
            actual_owner=owners[frame-1,slot]
            assert a['id']==a['roster'] and a['owner']==a['actor'] and a['state']==1
            mask=crop(owner)==slot
            mismatch=mask&(crop(expected)!=crop(words))
            assert mask.any(),'Actual whole-body pixels in displayed field'
            y,x=np.where(mask)
            ground=actual_owner['stageY']+5+actual_owner['displayY']-actual_owner['cameraY']-page
            bodies[slot]=dict(id=a['id'],pixels=int(mask.sum()),mismatches=int(mismatch.sum()),
                sole=int(y.max()),native_ground=ground,sole_relative_native_ground=int(y.max())-ground,
                object_y=a['y'],floor=a['floor'],vx=a['vx'],vy=a['vy'],gravity=a['gravity'],action=a['action'],
                grounded=a['y']==a['floor'],stationary=a['vx']==a['vy']==a['gravity']==0,
                pose=f"{a['pose']:08X}")
        records.append(dict(frame=frame,age=snap['age'],stage=fields[frame-1,1]['stage'],vram_mismatches=int((expected!=words).sum()),
                            display_pixels=bound['pixels'],body=bodies,
                            owned_shadow_pixels={slot:int((crop(shadow_owner)==slot).sum())for slot in(1,2)},
                            owned_shadow_mismatches=int(((crop(shadow_owner)>0)&(crop(expected)!=crop(words))).sum()),
                            native_shadow_pen_black=native_black))
    idle=[r for r in records if r['age']<=96 and all(a['grounded'] and a['stationary'] for a in r['body'].values())]
    sole_ranges={slot:sorted({r['body'][slot]['sole'] for r in idle}) for slot in (1,2)}
    return dict(scope='Current Dead Pool two-human idle/jump/crouch/walk soles against stock Kitana and actual native owned shadow rows; not all-arena grounding acceptance',
                native_shadow_components=native['components'],native_shadow_copies=native['copies'],native_shadow_row_stream_verified=native['rowStreamVerified'],
                samples=len(records),idle_samples=len(idle),idle_sole_rows=sole_ranges,
                idle_native_ground_offsets={slot:sorted({r['body'][slot]['sole_relative_native_ground'] for r in idle}) for slot in (1,2)},
                body_mismatches=sum(a['mismatches']for r in records for a in r['body'].values()),
                vram_mismatches=sum(r['vram_mismatches']for r in records),
                records=records,fullPortAcceptance=False,floorAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    args=parser.parse_args()
    print(json.dumps(inspect(args.folder),indent=2))
