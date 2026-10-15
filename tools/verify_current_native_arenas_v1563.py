"""Current real campaign: source-bound native shadow rows and exact saved arena passes.

Not all artistic poses, unsampled phases, arena special finishers or full port.
"""
import argparse,hashlib,json,re,struct,sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import verify_native_floor_campaign_v1562 as campaign
import verify_active_launch_cpu_display_v1525 as native
import inspect_native_shadow_rows_v635 as rows
ROOT=campaign.ROOT
native.raster.HEX|={'cursor','size','xy','b14','b10','a0','a1','a3','a7'}
rows.data=native.raster.data

def need(ok,label):
    if not ok:raise ValueError(label)

def verify(folder):
    bound=campaign.verify(folder);need(bound['passed'],'Exact source, input policy and native campaign: '+str(bound['errors']))
    pins=bound.pop('inputHashes');log=(folder/'run.log').read_text(encoding='utf-8-sig')
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    side=launch['human_slot'];human_id={'kano':17,'sonya':18}[launch['player']]
    guest,_,payload=native.grab.expected_guest();groups,*_=native.raster.data(folder)
    need(groups['FLOOR_SNAP'] and len(groups['FLOOR_RESULT'])==1,'Actual terminal sampled native drawing')
    image=bytearray(native.graphics_model.graphics(pins))
    for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        need(payload[header:header+4]==magic,'Original current native effect allocation')
        first,count,destination=struct.unpack_from('<III',payload,header+4)
        need(first==source and destination==dest and count>0,'Exact current effect graphics bounds')
        image[dest:dest+count]=payload[source:source+count]
    for r in groups['FLOOR_GFX']:
        need(0<=r['first']<r['first']+r['bytes']<=len(image) and
             bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],
             'Every actual whole-scene ROM/UI/effect graphics stream equals independently reconstructed source')
    queues={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE']}
    need(len(queues)==len(groups['FLOOR_QUEUE']),'Unique native FIFO publications')
    parts=defaultdict(list)
    for r in groups['FLOOR_QUEUE_PART']:parts[r['frame'],r['cursor']].append(r)
    by_cursor=defaultdict(list)
    for r in queues.values():by_cursor[r['cursor']].append(r)
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    dmas={r['event']:r for r in groups['FLOOR_DMA']}
    need(set(regs)==set(dmas),'Every native DMA has real register/iterator context')
    exact_parts=0
    for event,d in dmas.items():
        candidates=[q for q in by_cursor[regs[event]['b14']+192] if q['frame']<=d['frame']]
        q=max(candidates,key=lambda r:r['frame']) if candidates else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        need((event in dispatch)==owned and d['slot']==(q['slot'] if owned else 0),
             'Every actual DMA ownership is exact FIFO, not shared palette/effect guesses')
        if not owned:continue
        r=dispatch[event];slot=r['slot']
        need(q['slot']==slot and q['actor']==r['actor'] and q['main']==r['main'] and
             q['cursor']==r['cursor']==regs[event]['b14']+192 and q['frame']==r['queue_frame'] and
             q['owner']==q['actor'] and (slot!=side or q['id']==q['roster']==human_id),
             'True native fighter publication remains physically owned')
        expected=native.group(q,payload,guest);actual=parts[q['frame'],q['cursor']]
        need(len(expected)==len(actual) and all(all(a[k]==v for k,v in e.items()) for a,e in zip(actual,expected)),
             'Every cached part exactly matches the actual ROM composite descriptor')
        need(q['pc']==0xff804420 and q['row']==q['cache']+q['part']*112 and q['part'] in range(len(expected)),
             'Original native cache iterator and FIFO publication instruction')
        part=actual[q['part']]
        need(q['source']==d['source']==part['source'] and q['size']&0xffff==d['width']==part['width'] and
             q['size']>>16==d['height']==part['height'] and q['command']>>16==d['command']==part['command']|0x8002 and
             q['xy']&1023==d['x'] and(q['xy']>>16)&511==d['y'] and q['bank']&0x7f00==d['palette'],
             'Exact queued native source/size/flags/position/palette arrives at DMA unchanged')
        exact_parts+=len(expected)
    stream=rows.inspect(folder)
    need(stream['rowStreamVerified'] and not stream['failures'] and not stream['oversized_rows'],
         'All original compressed imported shadow rows and copy cadence independently verify')
    need((side,human_id) in map(tuple,stream['identities']),'New real human owns native shadow components')
    video=native.raster.inspect(folder)
    need(video['frames']==len(groups['FLOOR_SNAP'])==groups['FLOOR_RESULT'][0]['snapshots'],
         'All retained exact native snapshots accounted')
    need(all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records']),
         'Every original sampled DMA/CPU pass through exact native flip matches full VRAM, screen and shadows')
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};palette_checks=0;grounded=[]
    for snap in groups['FLOOR_SNAP']:
        colors=np.fromfile(folder/displays[snap['frame']]['palette_file'],dtype='<u4')
        for r in groups['FLOOR_QUEUE_DISPATCH']:
            if r['slot']!=side or dmas[r['event']]['frame']!=snap['frame']-1:continue
            q=queues[r['queue_frame'],r['cursor']];ids=[None,None];ids[side-1]=human_id
            native.check_owned_body_palette(q,colors,guest,tuple(ids),side);palette_checks+=1
    need(palette_checks>=len(groups['FLOOR_SNAP']),'Exact actual own costume palettes across saved campaign frames')
    for r in video['records']:
        body=r['body'][side]
        need(body['pixels']>100 and body['mismatches']==0 and body.get('id')==human_id,'Own real imported body visible and exact in every sample')
        if body.get('grounded'):
            grounded.append(dict(frame=r['frame'],arena=r['arena'],action=body['action'],sole=body['sole'],native_ground=body['native_ground'],offset=body['sole']-body['native_ground']))
    arenas=sorted({r['arena'] for r in video['records']})
    return dict(passed=True,candidate=native.NAME,fighter=launch['player'],human_slot=side,actualArenaIDs=arenas,
                allNineRegularArenasSampled=arenas==list(range(9)),exactScanouts=video['frames'],
                exactCachePartChecks=exact_parts,nativeShadowComponents=stream['components'],nativeShadowCopies=stream['checked_copies'],
                fullOwnedPaletteChecks=palette_checks,groundedSoleObservations=grounded,
                nativeCampaign=bound,records=video['records'],inputHashes=pins,allMovePhaseFloorAccepted=False,
                fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    need(not args.output.exists(),'Never overwrite evidence')
    try:report=verify(args.folder)
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    if report['passed']:
        for path in args.folder.rglob('*'):
            if path.is_file():report['inputHashes'][str(path.resolve())]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        for module in tuple(sys.modules.values()):
            value=getattr(module,'__file__',None)
            if value:
                path=Path(value).resolve()
                if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':report['inputHashes'][str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    args.output.parent.mkdir(exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in('inputHashes','records','groundedSoleObservations','scope')},indent=2))
    raise SystemExit(0 if report['passed'] else 1)
