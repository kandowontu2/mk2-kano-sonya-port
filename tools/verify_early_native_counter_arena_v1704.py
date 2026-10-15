"""Current real campaign: source-bound native shadow rows and exact saved arena passes.

Not all artistic poses, unsampled phases, arena special finishers or full port.
"""
import argparse,hashlib,json,re,struct,sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import verify_early_native_counter_campaign_v1702 as campaign
import verify_native_ground_throw_source_v1598 as corrected_source
import verify_native_campaign_palette_v1580 as palettes
import verify_native_uppercut_screen_cull_v1589 as culls
import verify_early_native_kintaro_cull_v1703 as boss
import verify_active_launch_cpu_display_v1525 as native
import inspect_native_shadow_rows_v635 as rows
ROOT=campaign.ROOT
native.raster.HEX|={'cursor','size','xy','b14','b10','a0','a1','a3','a7','world','camera','display'}
_native_data=native.raster.data
_data_cache={}
def data_once(folder):
    key=str(Path(folder).resolve())
    if key not in _data_cache:
        _data_cache.clear()
        _data_cache[key]=_native_data(folder)
    return _data_cache[key]
native.raster.data=data_once
rows.data=data_once

def need(ok,label):
    if not ok:raise ValueError(label)

def verify(folder):
    bound=campaign.verify(folder);need(bound['passed'],'Exact source, input policy and native campaign: '+str(bound['errors']))
    pins=bound.pop('inputHashes');log_before=campaign.digest(folder/'run.log')
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    side=launch['human_slot'];human_id={'kano':17,'sonya':18}[launch['player']]
    guest,_,payload=corrected_source.expected();palettes.sources(guest,pins)
    groups,*_=native.raster.data(folder)
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
    geometry=[]
    transforms={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE_TRANSFORM']}
    if transforms:
        need(set(transforms)==set(queues),'Exactly one actual world/camera/display record per FIFO publication')
        original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        first=(0xff804000-0xff800000)//8;last=(0xff804430-0xff800000)//8
        need(guest[first:last]==original[first:last],'Entire actual native coordinate/cache/FIFO instruction path unchanged')
        pins[str(ROOT/'mk2/mk2-maincpu.bin')]=campaign.digest(ROOT/'mk2/mk2-maincpu.bin')
        def xy(v):return v&0xffff,(v>>16)&0xffff
        signed=lambda v:v-65536 if v&0x8000 else v
        for key,q in queues.items():
            t=transforms[key];part=parts[key][q['part']]
            need(t['actor']==q['actor'] and t['main']==q['main'] and t['slot']==q['slot'] and
                 t['world']==((q['y']&0xffff)<<16)|(q['x']&0xffff) and t['x']==q['x'] and t['y']==q['y'] and
                 t['floor']==q['floor'],'Actual published integer world position and owning physical floor')
            x,y=xy(t['world']);cx,cy=xy(t['camera']);bx,by=xy(t['display'])
            if not t['a7']&1:x-=cx;y-=cy
            x-=part['dx'];y-=part['dy']
            cmd=q['command']>>16
            if cmd&16:x+=part['width']-1
            if cmd&32:y+=part['height']-1
            x+=bx;y+=by
            need((q['xy']&1023,(q['xy']>>16)&511)==(x&1023,y&511),
                 'Every emitted XY exactly derives from actual world, conditional camera, native cache offsets, flips and display base')
            if q['slot']==side:
                need(t['floor']==t['stageY']-{17:134,18:135}[human_id],
                     'Every true human Main floor uses its native character anchor in the actual arena')
                native_floor=t['stageY']+5+signed(by)-(signed(cy) if not t['a7']&1 else 0)
                geometry.append(dict(frame=q['frame'],cursor=q['cursor'],slot=q['slot'],pose=q['pose'],
                                     action=q['action'],worldY=q['y'],floor=q['floor'],stageY=t['stageY'],
                                     nativeFloorVRAM=native_floor&511,rawNativeFloorVRAM=native_floor,
                                     publishedXY=q['xy'],physicalGrounded=q['y']==q['floor']))
    print('Exact original FIFO/cache/graphics and actual geometry checked',flush=True)
    stream=rows.inspect(folder)
    need(stream['rowStreamVerified'] and not stream['failures'] and not stream['oversized_rows'],
         'All original compressed imported shadow rows and copy cadence independently verify')
    need((side,human_id) in map(tuple,stream['identities']),'New real human owns native shadow components')
    print('Exact compressed native shadow rows checked; replaying saved native passes',flush=True)
    video=native.raster.inspect(folder)
    need(video['frames']==len(groups['FLOOR_SNAP'])==groups['FLOOR_RESULT'][0]['snapshots'],
         'All retained exact native snapshots accounted')
    need(all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records']),
         'Every original sampled DMA/CPU pass through exact native flip matches full VRAM, screen and shadows')
    print('Native raster replay completed: '+str(video['frames'])+' saved frames',flush=True)
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};palette_checks=0;grounded=[];palette_contexts=defaultdict(int);palette_records=[]
    for snap in groups['FLOOR_SNAP']:
        colors=np.fromfile(folder/displays[snap['frame']]['palette_file'],dtype='<u4')
        for r in groups['FLOOR_QUEUE_DISPATCH']:
            if r['slot']!=side or dmas[r['event']]['frame']!=snap['frame']-1:continue
            q=queues[r['queue_frame'],r['cursor']];ids=[None,None];ids[side-1]=human_id
            try:context=palettes.check(q,colors,guest,tuple(ids),side)
            except Exception as error:raise ValueError('Actual palette at frame '+str(snap['frame'])+' arena '+str(snap['arena'])+' pose '+hex(q['pose'])+': '+str(error))from error
            palette_checks+=1;palette_contexts[context['kind']]+=1
            palette_records.append(dict(context,frame=snap['frame'],arena=snap['arena'],slot=side,actor=q['actor'],main=q['main'],pose=q['pose'],action=q['action']))
    need(palette_checks>=len(groups['FLOOR_SNAP']),'Exact actual own costume palettes across saved campaign frames')
    boss_context=boss.build_context(folder,guest,payload) if folder.name=='audit_v1700_current_kano_p1_early_native_counter' else None
    if boss_context:pins.update(boss_context['pins'])
    native_culls=[];boss_culls=[];visible_frames=0
    for r in video['records']:
        body=r['body'][side]
        if body['pixels']==0:
            if boss_context:
                boss_culls.append(boss.prove(boss_context,groups,r,side,human_id,guest,payload))
            else:native_culls.append(culls.prove(groups,r,side,human_id,guest,payload))
        else:
            need(body['pixels']>100 and body['mismatches']==0 and body.get('id')==human_id,'Own real imported body visible and exact in every non-culled sample')
            visible_frames+=1
        if body.get('grounded'):
            grounded.append(dict(frame=r['frame'],arena=r['arena'],action=body['action'],sole=body['sole'],native_ground=body['native_ground'],offset=body['sole']-body['native_ground']))
    need(campaign.digest(folder/'run.log')==log_before,'Entire actual log unchanged across all independent checks')
    pins[str((folder/'run.log').resolve())]=log_before
    arenas=sorted({r['arena'] for r in video['records']})
    return dict(passed=True,candidate=launch['candidate'],fighter=launch['player'],human_slot=side,actualArenaIDs=arenas,
                allNineRegularArenasSampled=arenas==list(range(9)),exactScanouts=video['frames'],
                exactCachePartChecks=exact_parts,nativeShadowComponents=stream['components'],nativeShadowCopies=stream['checked_copies'],
                fullOwnedPaletteChecks=palette_checks,exactVisibleOwnBodyFrames=visible_frames,sourceBoundOriginalUppercutCulls=native_culls,sourceBoundOriginalKintaroLaunchCulls=boss_culls,exactNativePaletteContexts=dict(palette_contexts),nativePaletteRecords=palette_records,groundedSoleObservations=grounded,
                nativeCoordinatePublicationsChecked=len(transforms),originalWorldCameraCacheProjectionExact=bool(transforms),
                everyObservedHumanFloorUsesNativeAnchor=bool(transforms),nativePublishedGeometry=geometry,
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
    print(json.dumps({k:v for k,v in report.items() if k not in('inputHashes','records','groundedSoleObservations','nativePublishedGeometry','nativePaletteRecords','scope')},indent=2))
    raise SystemExit(0 if report['passed'] else 1)
