"""Consecutive positive native move drawing/scanout and compressed-shadow proof.

Exact captured pre-pass CPU/DMA through flip, ROM/cache/palette/geometry,
and original shadow source stepping. Inter-pass erasure, universal artwork,
all victims/arenas/defenses/repeated moves/audio are not certified here.
"""
import argparse,json,re,struct,sys
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_ground_throw_source_v1598 as current
import verify_human_special_matrix as human
import verify_human_special_phases_v1767 as phase
import verify_current_ground_shadow_v1269 as graphics_model
import verify_native_campaign_palette_v1580 as palettes
import inspect_secondary_display_v1231 as raster
import inspect_native_shadow_rows_v635 as shadow
from verify_cpu_pair_display_v635_v3 import group
from verify_native_floor_display_v602 import check_latch
ROOT=current.ROOT
raster.HEX|={'world','camera','display','parent_main','native_actor_owner','victim','victim_main','dest','native_offset','pitch','shape','status','raster_control','psize','convdp_io','clipLow','clipHigh'}
shadow.data=raster.data

def need(ok,message):
    if not ok:raise ValueError(message)

def verify(folder):
    pins={};result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(result['candidate']==current.NAME and result['exit_code']==0 and result['assistance']=='none'and result['cheats_enabled']is False,'Actual terminal physical-input capture')
    need(result['victim']=='sub_zero'and result['side']in(1,2),'Actual bounded positive native fixture')
    need(result['executable_sha256']==build['executable_sha256']=='9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695'and result['payload_sha256']==build['payload_sha256'],'Current source-built files')
    need(before==result['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Complete executed source manifest')
    for p,h in before.items():
        need(phase.sha(p)==h,'Changed executed input '+p);pins[p]=h
        if Path(p).suffix in('.lua','.ps1','.json'):
            frozen=folder/'input_sources'/Path(p).name;need(phase.sha(frozen)==h,'Changed frozen input');pins[str(frozen)]=h
    source=(folder/'input_sources/mk2ks_human_special_full_render_v1804.lua').read_text()
    start='-- BEGIN v1804 full-render read-only observer\n';end='-- END v1804 full-render read-only observer\n'
    need(source.count(start)==source.count(end)==1,'One observer-only appended block')
    first=source.index(start);last=source.index(end)+len(end);block=source[first:last]
    need(source[:first]==(ROOT/'mk2ks_human_special_matrix_v3.lua').read_text()and last==len(source),'Entire physical input scenario exact, observation appended only')
    need(not re.search(r':write_|set_value|clear_value|load_?state|dofile|\.value\s*=(?!=)',block),'Observer reads only; baseline exclusively owns physical controls')
    need(phase.sha(ROOT/'mk2ks_human_special_matrix_v3.lua')=='374EFA1A16F9EEACC8F458F814DFFD29C144AAB972FDEB20973BD3EB94180EFF','Immutable accepted physical input driver')
    log=(folder/'run.log').read_text(encoding='utf-8-sig');move,side,air=result['move'],result['side'],result['air']
    need(not re.search(r'LUA ERROR|Lua error|WRONG CHECKSUMS|fatal error|access violation|stack traceback',log,re.I),'No runtime errors')
    baseline=ROOT/f'audit_v1620_human_{move}{"_air"if air else""}_p{side}'
    events=lambda t:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',line)for line in t.splitlines()if line.startswith('MK2_HSPECIAL_')]
    need(events(log)==events((baseline/'run.log').read_text(encoding='utf-8-sig')),'Every actual native input, pose, collision, health, recovery and ordinary follow-up remains unchanged')
    pins[str(baseline/'run.log')]=phase.sha(baseline/'run.log');state=human.verify_log(log,move,side,air)
    for filename in('special_before.png','special_recovered.png','special_final.png'):
        need((folder/'snap'/filename).read_bytes()==(baseline/'snap'/filename).read_bytes(),'Complete original before/recovered/final scene unchanged');pins[str(baseline/'snap'/filename)]=phase.sha(baseline/'snap'/filename)
    guest,_,payload=current.expected();need((folder/'guest_maincpu.bin').read_bytes()==guest,'Every initialized guest byte equals independent current reconstruction')
    proofpath=current.OUT/'report.json';proof=json.loads(proofpath.read_text());need(proof['passed']and proof['wholeActualGuestExactlyTwoPatches'],'Exact current guest/source provenance')
    pins[str(proofpath)]=phase.sha(proofpath)
    for p,h in proof['inputHashes'].items():need(phase.sha(p)==h,'Changed source proof');pins[p]=h
    oldsrc=ROOT/graphics_model.current.CANDIDATE/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    nowsrc=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    declaration=lambda p:p.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0]
    need(declaration(oldsrc)==declaration(nowsrc),'Imported graphics declarations unchanged from independently decoded ROM model')
    image=bytearray(graphics_model.graphics(pins))
    for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        need(payload[header:header+4]==magic,'Current native effect graphics header')
        first,count,destination=struct.unpack_from('<III',payload,header+4)
        need(first==source and destination==dest and count>0 and source+count<=len(payload)and dest+count<=len(image),'Complete bounded native effect graphics')
        image[dest:dest+count]=payload[source:source+count]
    groups,buffers,*_=raster.data(folder)
    for r in groups['FLOOR_GFX']:
        need(0<=r['first']<r['first']+r['bytes']<=len(image)and bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],'All actual scene/body/shadow/effect graphics bytes equal independent ROM model')
    origin=groups['FLOOR_BEGIN'];final=groups['FLOOR_RESULT'];recovery=groups['FLOOR_RECOVERY']
    need(len(origin)==len(final)==len(recovery)==1 and origin[0]['origin']==state['entry']and final[0]['origin']==state['entry']and final[0]['recovered']==recovery[0]['recovered']==state['recovered'],'Actual native activation and independently observed original recovery')
    command=human.rows(log,'RESULT')[0]['command'];expected=list(range(command+1,state['recovered']+14));snaps=groups['FLOOR_SNAP']
    need([r['frame']for r in snaps]==expected and final[0]['snapshots']==len(expected),'Every consecutive special-phase and 13-field cleanup scanout retained')
    ids=(human.SPECS[move][0],8)if side==1 else(8,human.SPECS[move][0]);identity=ids[side-1]
    first=groups['FLOOR_STATE'][0];actors={s:first[f'p{s}']for s in(1,2)};mains={s:first[f'main{s}']for s in(1,2)}
    for r in groups['FLOOR_STATE']:
        need(r['mode']==2 and all(r[f'p{s}']==actors[s]and r[f'main{s}']==mains[s]and r[f'roster{s}']==ids[s-1]and r[f'state{s}']==1 for s in(1,2)),'True physical fighters throughout observed special scene')
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']};parts=defaultdict(list);published=defaultdict(list)
    need(len(queues)==len(groups['FLOOR_QUEUE']),'Unique native FIFO publications')
    for p in groups['FLOOR_QUEUE_PART']:parts[p['frame'],p['cursor']].append(p)
    for q in queues.values():published[q['cursor']].append(q)
    inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_QUEUE']}
    need(len(inventory)==len(groups['FLOOR_ALL_QUEUE']),'Complete unambiguous native publication inventory')
    for key,q in inventory.items():
        if q['actor']in actors.values():need(key in queues and all(queues[key][k]==q[k]for k in('actor','source','pose','cache','id','body','facing','bank','pc')),'Every physical body publication accounted, not palette-based ownership')
    transforms={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE_TRANSFORM']}
    need(set(transforms)==set(queues),'Every physical/child publication has native coordinate registers')
    geometry=0
    for key,q in queues.items():
        if q['slot']not in(1,2):continue
        s=q['slot'];need(q['actor']==q['owner']==actors[s]and q['main']==mains[s]and q['id']==q['roster']==ids[s-1],'Actual true-ID physical draw owner')
        composition=group(q,payload,guest);actual=parts[key]
        need(len(actual)==len(composition)and all(all(a[k]==v for k,v in e.items())for a,e in zip(actual,composition)),'Every cached multipart piece equals its actual ROM pose descriptor')
        need(q['row']==q['cache']+q['part']*112 and q['pc']==0xff804420 and q['part']in range(len(composition)),'Original native cache publication cursor')
        part=composition[q['part']];t=transforms[key]
        need(t['slot']==s and t['actor']==q['actor']and t['main']==q['main']and t['world']==((q['y']&65535)<<16)|(q['x']&65535),'Actual native world-position registers')
        need(t['floor']==q['floor']==t['stageY']-{17:134,18:135,8:131}[ids[s-1]],'Original character-owned floor anchors maintained')
        xy=lambda v:(v&65535,(v>>16)&65535)
        x,y=xy(t['world']);cx,cy=xy(t['camera']);bx,by=xy(t['display'])
        if not t['a7']&1:x-=cx;y-=cy
        x-=part['dx'];y-=part['dy'];cmd=q['command']>>16
        if cmd&16:x+=part['width']-1
        if cmd&32:y+=part['height']-1
        need((q['xy']&1023,(q['xy']>>16)&511)==((x+bx)&1023,(y+by)&511),'Exact native world/camera/cache/flip/display coordinate projection')
        geometry+=1
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']};registers={r['event']:r for r in groups['FLOOR_DMA_REGS']};dmas={r['event']:r for r in groups['FLOOR_DMA']}
    need(len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH'])and set(registers)==set(dmas),'Complete original DMA register/dispatch context')
    drawn_by_frame=defaultdict(list);parts_drawn=0
    for event,d in dmas.items():
        candidates=[q for q in published[registers[event]['b14']+192]if q['frame']<=d['frame']];q=max(candidates,key=lambda r:r['frame'])if candidates else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        need((event in dispatch)==owned and d['slot']==(q['slot']if owned else 0),'Every actual DMA ownership recomputed by original FIFO, including shared-palette effects')
        if not owned:continue
        need(dispatch[event]['actor']==q['actor']and dispatch[event]['main']==q['main']and dispatch[event]['slot']==q['slot'],'Published actor/process dispatch binding')
        if q['slot']not in(1,2):continue
        e=group(q,payload,guest)[q['part']]
        need(q['source']==d['source']==e['source']and q['size']&65535==d['width']==e['width']and q['size']>>16==d['height']==e['height']and q['command']>>16==d['command']==e['command']|0x8002,'Every physical source/dimensions/command preserved from pose through DMA')
        need(q['xy']&1023==d['x']and(q['xy']>>16)&511==d['y']and q['bank']&0x7f00==d['palette'],'Every physical coordinate/palette bank reaches DMA unchanged')
        drawn_by_frame[d['frame']].append(q);parts_drawn+=1

    # The exact native pre-clip path, not a visibility exception by move/frame.
    candidates=groups['FLOOR_CANDIDATE'];need(candidates,'Actual original pre-clip decisions retained')
    first=(0xff804160-0xff800000)//8;last=(0xff804430-0xff800000)//8
    original_path=ROOT/'mk2/mk2-maincpu.bin';original=original_path.read_bytes()
    need(guest[first:last]==original[first:last],'Entire original native multipart clipping/publication code unchanged');pins[str(original_path)]=phase.sha(original_path)
    signed=lambda n:(n&65535)-65536 if n&32768 else n&65535
    clip_xy=lambda n:(signed(n),signed(n>>16))
    target_fields={f-1 for f in expected}
    candidates=[c for c in candidates if c['frame']in target_fields]
    physical=[q for q in groups['FLOOR_QUEUE']if q['slot']in(1,2)and q['frame']in target_fields]
    qmap={(q['frame'],q['slot'],q['part']):q for q in physical}
    need(len(qmap)==len(physical),'Unique physical publication per native part/field')
    by_candidate=defaultdict(list);visible_candidates=set();clipped_counts=defaultdict(int);edge_clipped_counts=defaultdict(int)
    for c in candidates:
        key=(c['frame'],c['slot'],c['part']);s=c['slot']
        need(s in(1,2)and c['id']==c['roster']==ids[s-1]and c['owner']==c['actor'],'Pre-clip true fighter/process ownership')
        composition=group(c,payload,guest);e=composition[c['part']]
        need(c['pc']==0xff8042b0 and c['row']==c['cache']+112*c['part'],'Exact native clipping caller/cache iterator')
        need((c['source'],c['size'],c['command'])==(e['source'],e['width']|(e['height']<<16),(e['command']|0x8002)<<16),'Pre-clip source matches complete real native composite')
        need(c['clipLow']==0 and c['clipHigh']==0x00fe0190,'Actual original native viewport bounds')
        x,y=clip_xy(c['xy']);w,h=e['width'],e['height']
        visible=x+w>0 and y+h>0 and x<400 and y<254
        if x<0 or y<0 or x+w>400 or y+h>254:edge_clipped_counts[c['frame'],s]+=1
        need((key in qmap)==visible,'Every original source rectangle publishes exactly iff it intersects native viewport')
        if visible:
            visible_candidates.add(key);q=qmap[key]
            for field in('actor','main','owner','id','roster','pose','facing','body','cache','row','source','size','command'):
                need(q[field]==c[field],'Exact clipping-to-publication identity '+field)
            bx,by=xy(c['display']);cmd=c['command']>>16
            ex=(x+(w-1 if cmd&16 else 0)+bx)&65535;ey=(y+(h-1 if cmd&32 else 0)+by)&65535
            need(q['xy']==ex|(ey<<16),'Native clipping coordinates reach final flipped display-base publication exactly')
        else:clipped_counts[c['frame'],s]+=1
        by_candidate[c['frame'],s].append(c)
    need(visible_candidates==set(qmap)and set(by_candidate)=={(f,s)for f in target_fields for s in(1,2)},'Every physical composite evaluated in each actual draw field')
    for key,rows in by_candidate.items():
        need([c['part']for c in rows]==list(range(len(group(rows[0],payload,guest)))),'No missing pre-clip body part, including wholly culled actors')
    wholly_culled={key for key,rows in by_candidate.items()if clipped_counts[key]==len(rows)}
    native_culled_frames=[]

    stream=shadow.inspect(folder);need(stream['rowStreamVerified']and not stream['failures']and not stream['oversized_rows'],'Every compressed owned shadow source/quarter-height copy/caller/coordinate independently verified')
    need((side,identity)in map(tuple,stream['identities']),'Declared real fighter owns actual floor-shadow copies')
    palettes.sources(guest,pins)
    print(folder.name+' exact source/cache/native coordinates and '+str(stream['checked_copies'])+' shadow copies; replaying consecutive scenes',flush=True)
    video=raster.inspect(folder)
    need(all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records']),'Every native pre-pass CPU/DMA through display flip and captured scene/shadow pixel must match exactly')
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};snapshot_map={r['frame']:r for r in snaps};held=[];palette_checks=0;contexts=defaultdict(int);sole_observations=[]
    for r in video['records']:
        body=r['body'][side];key=(r['frame']-1,side)
        if body['pixels']<=100:
            need((body['pixels']==0 and key in wholly_culled)or(body['pixels']>0 and edge_clipped_counts[key]>0),'Low/absent body pixels must be caused by actual source-bound viewport clipping')
            native_culled_frames.append(dict(frame=r['frame'],nativeDrawField=key[0],pixels=body['pixels'],clippedParts=clipped_counts[key],edgeClippedParts=edge_clipped_counts[key],whollyCulled=key in wholly_culled))
        need(body['mismatches']==0,'Every visible original body pixel remains source-exact even at viewport edges')
        need(r['shadow_pixels']>0 and r['shadow_mismatches']==0,'Actual imported floor shadow visible and exact throughout modeled move phases')
        colors=np.fromfile(folder/displays[r['frame']]['palette_file'],dtype='<u4')
        need(colors[15]==0,'Original shadow pen is actually black')
        for q in drawn_by_frame[r['frame']-1]:
            if q['slot']==side:
                context=palettes.check(q,colors,guest,ids,side);palette_checks+=1;contexts[context['kind']]+=1
        body=r['body'][side]
        if body.get('grounded'):sole_observations.append(dict(frame=r['frame'],pose=None,action=body['action'],sole=body['sole'],nativeGround=body['native_ground'],offset=body['sole']-body['native_ground']))
    for h in groups['FLOOR_HELD']:
        display=displays[h['frame']];picture=np.asarray(Image.open(folder/'snap'/snapshot_map[h['frame']]['file']).convert('RGB'))
        value=check_latch(picture,(folder/h['file']).read_bytes(),(folder/display['palette_file']).read_bytes(),h['start'],h['control'],h['tap'])
        held.append(dict(frame=h['frame'],pixels=value['pixels'],reason=h['reason'],DMAReconstructed=False))
    need(video['frames']+len(held)==len(expected)and palette_checks>=video['frames'],'Every consecutive captured scene and real owned costume palette accounted')
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=phase.sha(path)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file:
            path=Path(file).resolve()
            if path.is_relative_to(ROOT/'tools')and path.suffix=='.py':pins[str(path)]=phase.sha(path)
    return dict(passed=True,candidate=current.NAME,move=move,side=side,air=air,state=state,
      exactConsecutiveScanouts=len(expected),exactNativeReplayedPasses=video['frames'],heldOriginalScanouts=held,
      actualPhysicalCompositeDraws=parts_drawn,exactNativeCoordinatePublications=geometry,
      nativeShadowCopies=stream['checked_copies'],nativeShadowComponents=stream['components'],fullOwnedPaletteChecks=palette_checks,nativePaletteContexts=dict(contexts),
      currentPositiveConsecutiveNativeRenderAccepted=True,allMoveGroundShadowAccepted=False,allVictimArenaDefenseRenderAccepted=False,
      interPassEraseAcceptance=False,universalArtisticPoseGroundingAcceptance=False,audioAcceptance=False,fullPortAcceptance=False,
      sourceBoundNativeClippedParts=sum(clipped_counts.values()),nativeLowOrFullyCulledBodyFrames=native_culled_frames,
      groundedSoleObservations=sole_observations,records=video['records'],inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    need(not args.output.exists(),'Never overwrite evidence')
    try:report=verify(args.folder)
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','records','groundedSoleObservations')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
