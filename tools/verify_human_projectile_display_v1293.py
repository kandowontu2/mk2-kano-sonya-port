"""Actual current knife/ring release, original-art phases and native lifecycle.

Cold physical commands, source-bound whole guest/graphics, native child Main,
original FIFO components/palettes and exact complete sampled display passes.
Normal Dead Pool/Sub-Zero hit cases only; no all-victim/audio/full-port claim.
"""
import argparse,json,re,struct
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_metadata_build_v1254 as current
import verify_current_ground_shadow_v1269 as ground
import verify_human_special_matrix as human
import inspect_secondary_display_v1231 as raster
from verify_cpu_pair_display_v635_v3 import group
from verify_finish_display_v798 import check_owned_body_palette,check_latch
from inspect_natural_arena_floor_v602 import decoder
ROOT=current.ROOT
raster.HEX=raster.HEX|{'parent_main','native_actor_owner','victim','victim_main'}

def read(raw,address,fmt,base):
    at=(address-base)//8;assert address>=base and (address-base)%8==0 and at+struct.calcsize(fmt)<=len(raw)
    return struct.unpack_from(fmt,raw,at)

def source_groups(raw,address,base):
    result=[]
    for part in range(12):
        ptr=read(raw,address+part*32,'<I',base)[0]
        if not ptr:break
        result.append((ptr,read(raw,ptr,'<4hIHI',base)))
    assert result and len(result)<12,'Complete terminated original-art composite'
    return result

def independent_art(payload,image,pins):
    donor_path=ROOT/'mk3/mk3-maincpu.bin';donor=donor_path.read_bytes();pins[str(donor_path)]=current.digest(donor_path)
    assert pins[str(donor_path)]=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    original_gfx=image[0xc00000:0x1e00000]
    # Decode independently with the actual native scanner, not the converter's
    # pixel packer/renderer or a sampled screenshot as expected artwork.
    def pixels(source,command,w,h,data):
        first=source//8;count=(source%8+w*h*((command>>12)&7 or 8)+(h*8 if command&128 else 0)+7)//8+8
        assert 0<=first and first+count<=len(data)
        key=f'{source:08X}_{command:04X}_{w}_{h}'
        return decoder({key:dict(offset=source,first=first,bytes=count,data=data[first:first+count].hex())})(source,command,w,h)
    body={'knife':tuple(range(0xff82f400,0xff82f6a1,0x60)),
          'ring':(0xff83dbe0,0xff83dc40,0xff83dca0,0xff83dd00,0xff83dec0)}
    sequences={};pieces=0
    for move,index in (('knife',0),('ring',1)):
        body_seq=list(read(payload,0xfe800000+(0x1c2100+index*0x40)*8,'<'+str(len(body[move])+1)+'I',0xfe800000))
        assert body_seq==[p-0x1000000 for p in body[move]]+[0],'Whole original release body sequence'
        child_ptr=read(payload,0xfe800000+(0x1c2180+index*0x60)*8,'<I',0xfe800000)[0]
        intro_count=6 if index==0 else 1;flight_count=10 if index==0 else 4
        seq=list(read(payload,0xfe800000+(0x1c2180+index*0x60)*8,'<'+str(intro_count+1+flight_count+3)+'I',0xfe800000))
        assert seq[intro_count]==0 and seq[-3:]==[1,0xfe800000+(0x1c2180+index*0x60+4*(intro_count+1))*8,0]
        intro=seq[:intro_count] if index==0 else []
        flight=seq[intro_count+1:-3]
        impacts=list(read(payload,0xfe800000+(0x1c1300+index*0x40)*8,'<'+str((6 if index==0 else 7)+1)+'I',0xfe800000));assert impacts[-1]==0;impacts=impacts[:-1]
        original_intro=(0xff82ec40,0xff82eca0,0xff82ece0,0xff82ed40,0xff82edc0,0xff82ee20)if index==0 else ()
        original_flight=tuple(range(0xff82ee80,0xff82f100,0x40))if index==0 else tuple(range(0xff83e100,0xff83e200,0x40))
        original_impact=(0xff82f100,0xff82f140,0xff82f180,0xff82f1c0,0xff82f200,0xff82f260)if index==0 else(0xff83e200,0xff83e240,0xff83e280,0xff83e340,0xff83e440,0xff83e520,0xff83e5c0)
        for phase,converted,sources in (('body',body_seq[:-1],body[move]),('intro',intro,original_intro),('flight',flight,original_flight),('impact',impacts,original_impact)):
            assert len(converted)==len(sources),'All original-art phase groups retained'
            for address,original in zip(converted,sources):
                actual=source_groups(payload,address,0xfe800000);expected=source_groups(donor,original,0xff800000)
                assert len(actual)==len(expected),'All original multipart pieces retained'
                for (_,a),(_,e)in zip(actual,expected):
                    w,h,x,y,source,command,palette=a;ew,eh,ex,ey,es,ec,ep=e
                    pivot=(-100,-72)if index==0 and phase in('intro','flight')else(0,0)
                    assert (w,h,x,y)==(ew,eh,ex+pivot[0],ey+pivot[1]),'Original dimensions and intended native pivot '+phase
                    assert command==(ec if phase=='body'else 0x6000)
                    assert source==(es+0x10000000)if phase=='body'else source<0x10000000
                    offset=source-0xa000000 if source>=0x10000000 else source
                    assert np.array_equal(pixels(offset,command|0x8002,w,h,image),pixels(es,ec|0x8002,ew,eh,original_gfx)),'Every original donor sprite index differs '+phase
                    pieces+=1
        sequences[move]=dict(body=body_seq[:-1],intro=intro,flight=flight,impact=impacts)
    return sequences,pieces

def verify_publications(groups,actors,spawn,retirement,poses,sources):
    """Account for every native actor, including recycled untracked slots."""
    all_rows=groups['FLOOR_ALL_QUEUE'];tracked=groups['FLOOR_QUEUE']
    inventory={(q['frame'],q['cursor']):q for q in all_rows}
    assert len(inventory)==len(all_rows)>len(tracked),'Whole native publication inventory'
    tracked_map={(q['frame'],q['cursor']):q for q in tracked}
    assert len(tracked_map)==len(tracked),'Unique tracked FIFO publications'
    common=('actor','source','pose','cache','id','body','facing','bank','pc')
    for key,q in tracked_map.items():
        assert key in inventory and all(inventory[key][k]==q[k]for k in common),'Tracked publication differs from independent full inventory'
    recycled=[]
    for key,q in inventory.items():
        assert q['pc']==0xff804420,'Actual original FIFO publication entry'
        if q['actor']in actors.values():
            assert key in tracked_map and tracked_map[key]['slot']in(1,2),'Physical actor publication hidden by observer'
        elif q['actor']==spawn['actor'] and spawn['frame']<=q['frame']<retirement['frame']:
            assert key in tracked_map and tracked_map[key]['slot']==3,'Live child publication hidden by observer'
        if q['frame']>retirement['frame']:
            assert q['pose']not in poses and q['source']not in sources,'Projectile art still published after native cleanup'
            if q['actor']==spawn['actor']:recycled.append(q)
    assert any(q['frame']>retirement['frame']for q in inventory.values()),'Native post-cleanup publication inventory required'
    return dict(total=len(inventory),tracked=len(tracked),postCleanup=sum(q['frame']>retirement['frame']for q in inventory.values()),
        recycledAddressPublications=len(recycled),recycledKinds=sorted({(q['id'],q['pose'],q['cache'])for q in recycled}))

def phase_order(queues,sequences,side):
    phases={}
    for phase,slot in(('body',side),('intro',3),('flight',3),('impact',3)):
        expected=sequences[phase]
        samples=sorted({(q['frame'],q['pose'])for q in queues if q['slot']==slot and q['pose']in expected})
        by_frame=defaultdict(set)
        for frame,pose in samples:by_frame[frame].add(pose)
        assert all(len(poses)==1 for poses in by_frame.values()),'Conflicting actor poses within one native field'
        ordered=[]
        for frame,pose in samples:
            if not ordered or ordered[-1]['pose']!=pose:ordered.append(dict(pose=pose,first=frame,last=frame))
            else:ordered[-1]['last']=frame
        poses=[r['pose']for r in ordered]
        if phase=='flight':
            # Native contact can end flight before the ten-frame knife cycle.
            # Prove the actually executed prefix/cycles, not nonexistent frames;
            # long miss cases must separately cover every rotation group.
            assert poses and poses==[expected[i%len(expected)]for i in range(len(poses))],'Original flight rotation order'
        else:assert poses==expected,'Complete original '+phase+' order'
        phases[phase]=ordered
    return phases

def verify(move,side):
    folder=ROOT/f'audit_v1291_projectile_{move}_p{side}';pins={}
    def pin(path,wanted=None):
        path=Path(path);actual=current.digest(path);assert wanted is None or actual==wanted,'Changed evidence '+str(path);pins[str(path)]=actual
    metadata_path=current.OUT/'report.json';metadata=json.loads(metadata_path.read_text());pin(metadata_path)
    assert metadata['passed'] and metadata['candidate']==current.CANDIDATE and metadata['nativeROMAuditAccepted']
    for file,wanted in metadata['inputHashes'].items():pin(file,wanted)
    build=json.loads((ROOT/current.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    assert launch['exit_code']==0 and launch['candidate']==current.CANDIDATE and launch['move']==move and launch['side']==side
    assert launch['victim']=='sub_zero' and launch['assistance']=='none' and launch['cheats_enabled']is False and launch['air']is False
    assert launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256']
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'));assert before==launch['input_hashes']
    for file,wanted in before.items():
        pin(file,wanted)
        if Path(file).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
    for file,wanted in build['input_hashes'].items():assert before.get(file)==wanted
    for file in ('mk2ks_human_special_matrix_v3.lua','mk2ks_human_projectile_full_display_v1289.lua'):
        source=(folder/'input_sources'/file).read_text()
        assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',source),'Read-only actual input/render observation'
    log=(folder/'run.log').read_text(encoding='utf-8-sig');baseline=ROOT/f'audit_v1252_human_{move}_p{side}'
    assert not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|stack traceback|access violation',log,re.I)
    event_lines=lambda text:[line for line in text.splitlines()if line.startswith('MK2_HSPECIAL_')]
    oldlog=(baseline/'run.log').read_text(encoding='utf-8-sig');pin(baseline/'run.log')
    assert event_lines(log)==event_lines(oldlog),'Full rendering observer changed actual input/native state chronology'
    state=human.verify_log(log,move,side)
    for file in('special_before.png','special_recovered.png','special_final.png'):
        assert (folder/'snap'/file).read_bytes()==(baseline/'snap'/file).read_bytes(),'Full observer changed actual native scene';pin(baseline/'snap'/file)
    guest,_,_,payload=current.reconstruct();assert (folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest differs from independent native reconstruction'
    image=bytearray(ground.graphics(pins))
    for header,source,destination,magic in((0x1c0000,0x1c4000,0x1e04000,b'KFX1'),(0x1c1000,0x1e6000,0x1e50000,b'KPI1'),(0x1c2000,0x1f4000,0x1e60000,b'KPJ1')):
        assert payload[header:header+4]==magic,'Native graphics allocation header'
        start,count,dest=struct.unpack_from('<III',payload,header+4)
        assert start==source and dest==destination and 0<count and source+count<=len(payload) and destination+count<=len(image)
        image[destination:destination+count]=payload[source:source+count]
    sequences,pieces=independent_art(payload,bytes(image),pins)
    groups,_,_,_,_=raster.data(folder);origin=groups['FLOOR_BEGIN'];result=groups['FLOOR_RESULT']
    assert len(origin)==len(result)==1 and origin[0]['origin']==state['entry'] and result[0]['origin']==state['entry']
    start=state['entry'];identity=17 if move=='knife'else 18;ids=(identity,8)if side==1 else(8,identity)
    first=groups['FLOOR_STATE'][0];actors={s:first[f'p{s}']for s in(1,2)};mains={s:first[f'main{s}']for s in(1,2)}
    allocation=groups['FLOOR_CHILD_ALLOC'];spawn=groups['FLOOR_CHILD_SPAWN'];retirement=groups['FLOOR_CHILD_RETIRE']
    assert len(allocation)==len(spawn)==len(retirement)==1,'One original independent child allocation/scheduler/removal'
    allocation,spawn,retirement=allocation[0],spawn[0],retirement[0]
    assert allocation['entry']==0xff8b6530 and spawn['entry']==0xff8b5fb0 and retirement['entry']==0xff8b6820
    assert allocation['frame']==spawn['frame']==start+(3 if move=='knife'else 15)
    assert allocation['actor']==spawn['actor']==retirement['actor']!=actors[side] and spawn['main']==retirement['main']!=mains[side]
    assert spawn['parent']==retirement['parent']==actors[side] and spawn['parent_main']==retirement['parent_main']==mains[side]
    assert spawn['id']==spawn['roster']==identity and spawn['native_actor_owner']==actors[side] and spawn['victim']==actors[3-side] and spawn['victim_main']==mains[3-side]
    projectile_poses=set(sequences[move]['intro']+sequences[move]['flight']+sequences[move]['impact'])
    projectile_sources={descriptor[4]for pose in projectile_poses for _,descriptor in source_groups(payload,pose,0xfe800000)}
    publication_inventory=verify_publications(groups,actors,spawn,retirement,projectile_poses,projectile_sources)
    for r in groups['FLOOR_GFX']:
        first,last=r['first'],r['first']+r['bytes'];assert 0<=first<last<=len(image)
        assert bytes.fromhex(r['data'])==image[first:last],'Every captured graphics byte must match independent ROM/UI/projectile source, including zero lookahead'
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']};parts=defaultdict(list)
    for p in groups['FLOOR_QUEUE_PART']:parts[p['frame'],p['cursor']].append(p)
    published=defaultdict(list)
    for q in queues.values():published[q['cursor']].append(q)
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']};regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    assert len(queues)==len(groups['FLOOR_QUEUE']) and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH']) and len(regs)==len(groups['FLOOR_DMA'])
    draws=defaultdict(int);dispatched=defaultdict(list)
    for d in groups['FLOOR_DMA']:
        candidates=[q for q in published[regs[d['event']]['b14']+192]if q['frame']<=d['frame']];q=max(candidates,key=lambda q:q['frame'])if candidates else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        assert (d['event']in dispatch)==owned and d['slot']==(q['slot']if owned else 0),'Recompute every FIFO-to-DMA actor classification'
        if not owned:continue
        publication=dispatch[d['event']];assert q==queues[publication['queue_frame'],publication['cursor']]
        assert all(publication[k]==q[k]for k in('actor','main','slot'))
        slot=q['slot'];physical=slot if slot<=2 else side
        assert slot in(1,2,3) and q['id']==q['roster']==ids[physical-1] and q['parent']==actors[physical]
        assert q['actor']==q['owner']==(actors[slot]if slot<=2 else spawn['actor']) and q['main']==(mains[slot]if slot<=2 else spawn['main'])
        assert q['kind']==(0 if slot<=2 else 1)and q['bank']&0x7f00==d['palette']and q['multipart']==1
        expected=group(q,payload,guest);observed=parts[q['frame'],q['cursor']]
        assert len(expected)==len(observed)and all(all(p[k]==value for k,value in e.items())for p,e in zip(observed,expected))
        assert q['row']==q['cache']+q['part']*112 and q['pc']==0xff804420 and q['part']in range(len(expected))
        p=expected[q['part']]
        assert q['source']==d['source']==p['source']and q['size']&65535==d['width']==p['width']and q['size']>>16==d['height']==p['height']
        assert q['command']>>16==d['command']==p['command']|0x8002 and q['xy']&1023==d['x']and q['xy']>>16&511==d['y']
        draws[slot]+=1;dispatched[d['frame']].append(q)
    assert draws[side]>100 and draws[3]>10,'Actual own physical fighter and projectile both drawn'
    phases=phase_order(list(queues.values()),sequences[move],side)
    print(move+f'_p{side} sources/native ownership accepted; replaying whole sampled scenes',flush=True)
    drawn=raster.inspect(folder);assert drawn['frames']>100 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records'])
    visible=defaultdict(set);palette_samples=0
    for r in drawn['records']:
        for q in dispatched[r['frame']-1]:
            if r['body'][q['slot']]['pixels']>0:visible[q['slot']].add(q['pose'])
    assert set(sequences[move]['body'])<=visible[side],'Every original launch body pose actually visible'
    assert set(sequences[move]['intro'])<=visible[3]and set(sequences[move]['impact'])<=visible[3],'Every original intro/impact group actually visible'
    executed_child={q['pose']for q in queues.values()if q['slot']==3}
    assert executed_child<=visible[3],'Every actually executed projectile group visible before collision/removal'
    for display in groups['FLOOR_DISPLAY']:
        actual=np.fromfile(folder/display['palette_file'],dtype='<u4')
        for q in dispatched[display['frame']-1]:
            if q['slot']==side:check_owned_body_palette(q,actual,guest,ids,side)
            elif q['slot']==3:
                raw=payload if 0xfe800000<=q['pose']<0xff800000 else guest;base=0xfe800000 if raw is payload else 0xff800000
                first_descriptor=read(raw,q['pose'],'<I',base)[0];pal=read(raw,first_descriptor+112,'<I',base)[0]
                promp=payload if 0xfe800000<=pal<0xff800000 else guest;pbase=0xfe800000 if promp is payload else 0xff800000
                count=read(promp,pal,'<H',pbase)[0];assert count==64
                words=read(promp,pal+16,'<64H',pbase)
                expected=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<dest for s,dest in((10,16),(5,8),(0,0)))for c in words],dtype=np.uint32)
                bank=q['bank']&0x7f00;assert np.array_equal(actual[bank:bank+64],expected),'Full native projectile palette'
                palette_samples+=1
    assert palette_samples>20 and not any(d['slot']==3 and d['frame']>retirement['frame']for d in groups['FLOOR_QUEUE_DISPATCH'])
    after=[r for r in drawn['records']if r['frame']>retirement['frame']+1]
    assert len(after)>10 and all(r['body'][3]['pixels']==0 for r in after),'No newly drawn projectile after original removal'
    held=[];snaps={r['frame']:r for r in groups['FLOOR_SNAP']};displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
    for h in groups['FLOOR_HELD']:
        display=displays[h['frame']];image_rgb=np.asarray(Image.open(folder/'snap'/snaps[h['frame']]['file']).convert('RGB'))
        bound=check_latch(image_rgb,(folder/h['file']).read_bytes(),(folder/display['palette_file']).read_bytes(),h['start'],h['control'],h['tap'])
        held.append(dict(frame=h['frame'],pixels=bound['pixels'],DMAReconstructed=False))
    assert result[0]['snapshots']==drawn['frames']+len(held)==len(snaps),'All actual native samples accounted'
    for path in folder.rglob('*'):
        if path.is_file():pin(path)
    for file in('verify_human_projectile_display_v1283.py','verify_human_projectile_display_v1284.py','verify_human_projectile_display_v1288.py','verify_human_projectile_display_v1292.py','verify_human_projectile_display_v1293.py','inspect_secondary_display_v1231.py','verify_current_ground_shadow_v1269.py','verify_human_special_matrix.py','verify_native_metadata_build_v1254.py','verify_cpu_pair_display_v635_v3.py','verify_finish_display_v798.py','inspect_natural_arena_floor_v602.py'):
        pin(ROOT/'tools'/file)
    return dict(passed=True,candidate=current.CANDIDATE,move=move,side=side,state=state,originalDonorPiecesCompared=pieces,
        allocation=allocation,spawn=spawn,retirement=retirement,publicationInventory=publication_inventory,nativePhaseOrder=phases,
        allFlightRotationGroupsVisible=set(sequences[move]['flight'])<=visible[3],nativeDraws=dict(draws),visiblePoses={s:[f'{p:08X}'for p in sorted(v)]for s,v in visible.items()},
        replayed=drawn,heldScanout=held,fullProjectilePaletteSamples=palette_samples,postRetirementSamples=len(after),inputHashes=pins,
        currentHitProjectileSampledNativeRenderLifetimeAccepted=True,allMoveArtAccepted=False,allVictimsAccepted=False,audioAccepted=False,allArenasAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('move',choices=('knife','ring'));parser.add_argument('side',type=int,choices=(1,2));args=parser.parse_args()
    out=ROOT/f'audit_v1293_projectile_{args.move}_p{args.side}_render_checked';assert not out.exists()
    try:report=verify(args.move,args.side)
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(args.move+f'_p{args.side} passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed']else 1)
