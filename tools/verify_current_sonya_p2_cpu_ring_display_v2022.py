"""Current natural P2 Sonya ring: complete native collision and exact scene.

All five original release body poses, four flight poses, seven impact holds,
physical FIFO ownership, full queued projections, cache/source/DMA/palettes,
native shadows and thirty post-retirement scenes are independently checked.
No universal contacts, CPU/arena/audio/campaign/ending/full-port acceptance.
"""
import json,re,struct
from collections import defaultdict
from pathlib import Path
import numpy as np
import current_sonya_cpu_ring_contract_v2021 as state
import inspect_ball_register_erase_v1843 as erase
import inspect_current_cpu_knife_raster_v1975 as scaled
import verify_current_ground_shadow_v1859 as graphics
import verify_human_projectile_display_v1352 as art
import inspect_native_shadow_rows_v635 as shadow
from verify_finish_display_v798 import check_owned_body_palette

ROOT=state.ROOT;CASE=ROOT/'audit_v2016_current_sonya_p2_cpu_ring_display_kano'
OUT=ROOT/'audit_v2022_current_sonya_p2_cpu_ring_display_checked'
raster=erase.raster;shadow.data=raster.data

def verify():
    pins=state.launch.launch.source_pins();guest,_,payload=state.launch.launch.current.expected()
    meta=state.launch.matched(CASE,pins);assert meta['player']=='kano'
    assert (CASE/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest equals independent source reconstruction'
    log=(CASE/'run.log').read_text(encoding='utf-8-sig');old=(ROOT/'audit_v2010_sonya_p2_cpu_jump_guard_kano/run.log').read_text(encoding='utf-8-sig')
    prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_')
    assert [r for r in log.splitlines()if r.startswith(prefixes)]==[r for r in old.splitlines()if r.startswith(prefixes)],'Read-only drawing observer leaves every original physical state/input unchanged'
    pins[str(ROOT/'audit_v2010_sonya_p2_cpu_jump_guard_kano/run.log')]=state.launch.sha(ROOT/'audit_v2010_sonya_p2_cpu_jump_guard_kano/run.log');timeline=state.verify(log,guest)
    observer=(CASE/'input_sources/mk2ks_physical_p2_cpu_ring_display_v2014.lua').read_text()
    assert "dofile('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')"in observer
    assert not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',observer)
    required={'mk2ks_cpu_recovery_probe_v1438.lua','mk2ks_physical_p2_cpu_continuation_v1997.lua',
        'mk2ks_physical_p2_cpu_round_trace_v1998.lua','mk2ks_physical_p2_cpu_overlap_trace_v1999.lua',
        'mk2ks_physical_p2_cpu_ring_trace_v2013.lua','mk2ks_physical_p2_cpu_ring_display_v2014.lua','run_current_physical_p2_cpu_ring_display_v2015.ps1'}
    assert required<={Path(file).name for file in meta['input_hashes']}
    scaled.source(pins)
    image=bytearray(graphics.graphics(pins))
    for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),
        (0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        assert payload[header:header+4]==magic
        start,count,destination=struct.unpack_from('<III',payload,header+4)
        assert start==source and destination==dest and count>0 and start+count<=len(payload)and dest+count<=len(image)
        image[dest:dest+count]=payload[source:source+count]
    sequences,pieces=art.independent_art(payload,bytes(image),pins);seq=sequences['ring']
    groups,*_=raster.data(CASE)
    for r in groups['FLOOR_GFX']:
        assert 0<=r['first']<r['first']+r['bytes']<=len(image)
        assert bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],'Every actual scene, body, shadow and knife graphics byte source-bound'
    origin=state.one(groups['FLOOR_BEGIN'],'One continuous display origin')['origin']
    result=state.one(groups['FLOOR_RESULT'],'One display terminal')
    assert origin==result['origin']==timeline['start']and result['recovered']==timeline['ownReady']
    actions=groups['FLOOR_ACTION'];assert [r['frame']for r in actions]==[r['start']for r in [timeline]]
    expected=list(range(origin+1,timeline['lastScene']+1))
    driver=(CASE/'input_sources/mk2ks_physical_p2_cpu_continuation_v1997.lua').read_text()
    cold=state.one(state.P.rows_prefix(log,'MK2_P2CPU_COLD_LIVE '),'Cold native fight')
    assert 'first_live+1800'in driver and result['frame']==cold['frame']+1800
    assert 'math.max(observed_recovery,child.retired)+30'in observer
    assert [r['frame']for r in groups['FLOOR_SNAP']]==expected and not groups['FLOOR_HELD']
    spawns=groups['FLOOR_CHILD_SPAWN'];retires=groups['FLOOR_CHILD_RETIRE'];alloc=groups['FLOOR_CHILD_ALLOC']
    assert len(spawns)==len(retires)==len(alloc)==1
    first=groups['FLOOR_STATE'][0];actors={s:first[f'p{s}']for s in(1,2)};mains={s:first[f'main{s}']for s in(1,2)}
    for born,dead,allocation,knife in zip(spawns,retires,alloc,[timeline]):
        assert allocation['frame']==born['frame']==knife['birth']and dead['frame']==knife['retirement']
        assert allocation['actor']==born['actor']==dead['actor']and born['main']==dead['main']
        assert(born['parent'],born['parent_main'],born['native_actor_owner'],born['victim'],born['victim_main'])==(actors[2],mains[2],actors[2],actors[1],mains[1])
        assert born['id']==born['roster']==18 and born['entry']==0xff8b5fb0 and dead['entry']==0xff8b6820
    for r in groups['FLOOR_STATE']:
        assert r['mode']==2 and all(r[f'p{s}']==actors[s]and r[f'main{s}']==mains[s]and
            r[f'roster{s}']==(17 if s==1 else 18)and r[f'state{s}']==(1 if s==1 else 0)for s in(1,2))
    assert not groups['FLOOR_POINTER_STORE'],'No hidden physical actor replacement in this ring window'
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']};inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_QUEUE']}
    assert len(queues)==len(groups['FLOOR_QUEUE'])and len(inventory)==len(groups['FLOOR_ALL_QUEUE'])>len(queues)
    parts=defaultdict(list);published=defaultdict(list)
    for p in groups['FLOOR_QUEUE_PART']:parts[p['frame'],p['cursor']].append(p)
    for q in queues.values():published[q['cursor']].append(q)
    poses=set(seq['intro']+seq['flight']+seq['impact'])
    sources={descriptor[4]for pose in poses for _,descriptor in art.source_groups(payload,pose,0xfe800000)}
    for key,q in inventory.items():
        if q['actor']in actors.values():assert key in queues and queues[key]['slot']in(1,2),'No physical publication hidden by classifier'
        for born,dead in zip(spawns,retires):
            if q['actor']==born['actor']and born['frame']<=q['frame']<=dead['frame']:
                assert key in queues and queues[key]['slot']==3,'No live projectile publication hidden by classifier'
        if not any(born['frame']<=q['frame']<=dead['frame']for born,dead in zip(spawns,retires)):
            assert q['pose']not in poses and q['source']not in sources,'No knife/impact art outside either actual child lifetime'
    dmas={d['event']:d for d in groups['FLOOR_DMA']};regs={r['event']:r for r in groups['FLOOR_DMA_REGS']};dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    assert len(regs)==len(dmas)==len(groups['FLOOR_DMA'])and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH'])
    by_draw=defaultdict(list);draws=defaultdict(int)
    transforms={(t['frame'],t['cursor']):t for t in groups['FLOOR_QUEUE_TRANSFORM']}
    assert set(transforms)==set(queues)
    signed=lambda v:(v&65535)-65536 if v&32768 else v&65535
    projection_checks=0
    for key,q in queues.items():
        s=q['slot'];t=transforms[key]
        assert s in(1,2,3)and all(t[k]==q[k]for k in('slot','actor','main'))
        assert all(q[k]==inventory[key][k]for k in('actor','source','pose','cache','id','body','facing','bank','pc'))
        assert q['id']==q['roster']==(17 if s==1 else 18)and q['multipart']==1 and q['owner']==q['actor']
        assert q['parent']==actors[2 if s==3 else s]
        if s in(1,2):
            assert(q['actor'],q['main'],q['kind'])==(actors[s],mains[s],0)
            assert t['floor']==q['floor']==t['stageY']-(134 if s==1 else 135)
        else:
            assert(q['actor'],q['main'],q['kind'])==(spawns[0]['actor'],spawns[0]['main'],1)
            assert spawns[0]['frame']<=q['frame']<=retires[0]['frame']
        composition=art.group(q,payload,guest);actual=parts[key]
        assert len(actual)==len(composition)and all(all(p[k]==v for k,v in e.items())for p,e in zip(actual,composition))
        assert q['row']==q['cache']+112*q['part']and q['pc']==0xff804420
        p=composition[q['part']]
        assert t['world']==((q['y']&65535)<<16)|(q['x']&65535)
        x,y=signed(t['world']),signed(t['world']>>16)
        if not t['a7']&1:x-=signed(t['camera']);y-=signed(t['camera']>>16)
        x-=p['dx'];y-=p['dy'];command=q['command']>>16
        if command&16:x+=p['width']-1
        if command&32:y+=p['height']-1
        x+=signed(t['display']);y+=signed(t['display']>>16)
        assert(q['xy']&1023,q['xy']>>16&511)==(x&1023,y&511),'Every part uses actual queued camera and display geometry'
        projection_checks+=1
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=((at-0xff800000)//8 for at in(0xff804040,0xff804470))
    assert guest[lo:hi]==original[lo:hi],'Stock body/cache/camera FIFO code unchanged'
    for event,d in dmas.items():
        candidates=[q for q in published[regs[event]['b14']+192]if q['frame']<=d['frame']]
        q=max(candidates,key=lambda r:r['frame'])if candidates else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        assert(event in dispatch)==owned and d['slot']==(q['slot']if owned else 0),'Every native ownership classified by actual FIFO, never palette alone'
        if not owned:continue
        key=q['frame'],q['cursor'];pub=dispatch[event]
        assert all(pub[k]==q[k]for k in('actor','main','slot'))and queues[pub['queue_frame'],pub['cursor']]==q
        s=q['slot'];assert s in(1,2,3)and q['id']==q['roster']==(17 if s==1 else 18) and q['multipart']==1
        assert key in inventory and all(q[k]==inventory[key][k]for k in('actor','source','pose','cache','id','body','facing','bank','pc'))
        assert q['parent']==actors[2 if s==3 else s]and q['owner']==q['actor']
        if s in(1,2):assert(q['actor'],q['main'],q['kind'])==(actors[s],mains[s],0)
        else:
            born=state.one([r for r in spawns if r['actor']==q['actor']],'Actual independent child publication')
            dead=state.one([r for r in retires if r['actor']==q['actor']],'That exact child retirement')
            assert q['main']==born['main']and q['kind']==1 and born['frame']<=q['frame']<=dead['frame']
        composition=art.group(q,payload,guest);actual=parts[key]
        assert len(actual)==len(composition)and all(all(p[k]==v for k,v in e.items())for p,e in zip(actual,composition)),'Every owned actual cache piece equals original-art source composite'
        assert q['row']==q['cache']+q['part']*112 and q['pc']==0xff804420 and q['part']in range(len(composition))
        p=composition[q['part']]
        assert q['source']==d['source']==p['source']and q['size']&65535==d['width']==p['width']and q['size']>>16==d['height']==p['height']
        assert q['command']>>16==d['command']==p['command']|0x8002 and q['xy']&1023==d['x']and q['xy']>>16&511==d['y']and q['bank']&0x7f00==d['palette']
        if s in(1,2):
            t=transforms[key];assert t['floor']==q['floor']==t['stageY']-(134 if s==1 else 135)
            assert t['world']==((q['y']&65535)<<16)|(q['x']&65535)
        draws[s]+=1;by_draw[d['frame']].append(q)
    assert draws[1]>50 and draws[2]>50 and draws[3]>30
    streams=shadow.inspect(CASE)
    assert streams['rowStreamVerified']and not streams['failures']and not streams['oversized_rows']and set(map(tuple,streams['identities']))=={(1,17),(2,18)}
    print('Original donor pieces, complete owned FIFO/cache/DMA, '+str(streams['checked_copies'])+' native shadow copies passed; replaying complete ring scenes',flush=True)
    video=raster.inspect(CASE)
    assert video['frames']==len(expected)==result['snapshots']
    assert all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records'])
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};visible=defaultdict(set);palette_checks=0;soles=[]
    for r in video['records']:
        colors=np.fromfile(CASE/displays[r['frame']]['palette_file'],dtype='<u4');assert colors[15]==0,'Actual floor-shadow pen black'
        for q in by_draw[r['frame']-1]:
            if r['body'][q['slot']]['pixels']>0:visible[q['slot'],next((i+1 for i,k in enumerate([timeline])if k['start']<q['frame']<=k['retirement']),0)].add(q['pose'])
            if q['slot']in(1,2):check_owned_body_palette(q,colors,guest,(17,18),q['slot']);palette_checks+=1
            else:
                descriptor=art.read(payload,q['pose'],'<I',0xfe800000)[0];pal=art.read(payload,descriptor+112,'<I',0xfe800000)[0]
                raw,base=(payload,0xfe800000)if 0xfe800000<=pal<0xff800000 else(guest,0xff800000)
                count=art.read(raw,pal,'<H',base)[0];assert count==64
                words=art.read(raw,pal+16,'<64H',base)
                expected_colors=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<dest for s,dest in((10,16),(5,8),(0,0)))for c in words],dtype=np.uint32)
                bank=q['bank']&0x7f00;assert np.array_equal(colors[bank:bank+64],expected_colors),'Whole actually owned ring palette'
                palette_checks+=1
        for s in(1,2):
            b=r['body'][s]
            if b.get('grounded')and b['pixels']>100:soles.append(dict(frame=r['frame'],slot=s,action=b['action'],sole=b['sole'],nativeGround=b['native_ground'],offset=b['sole']-b['native_ground']))
    phase_coverage=[]
    for i,knife in enumerate([timeline],1):
        assert set(seq['body'])<=visible[2,i]and set(seq['intro']+seq['impact'])<=visible[3,i],'Every complete body/intro/impact phase visible for this actual ring'
        executed={q['pose']for q in queues.values()if q['slot']==3 and knife['birth']<=q['frame']<=knife['retirement']}
        assert executed<=visible[3,i],'Every actually executed flight/contact phase visible'
        after=[r for r in video['records']if knife['retirement']+1<r['frame']<=knife['retirement']+15]
        assert len(after)>=10 and all(r['body'][3]['pixels']==0 for r in after),'No new projectile drawn after retirement'
        phase_coverage.append(dict(serial=i,bodyPoses=len(seq['body']),introPoses=len(seq['intro']),impactPoses=len(seq['impact']),actualChildPoses=len(executed),postRetirementSamples=len(after)))
    state.launch.launch.module_pins(pins)
    return dict(passed=True,candidate=state.launch.launch.NAME,state=timeline,originalDonorPiecesCompared=pieces,
        sampledFrames=video['frames'],exactScreenPixels=sum(r['display_pixels']for r in video['records']),
        exactOwnedPixels=sum(b['pixels']for r in video['records']for b in r['body'].values()),
        nativeDraws=dict(draws),sourceBoundProjections=projection_checks,nativeShadowCopies=streams['checked_copies'],nativeShadowComponents=streams['components'],
        completePhaseCoverage=phase_coverage,fullOwnedPaletteChecks=palette_checks,lateCameraDebugSolesNotAcceptance=soles,
        allRetainedScenesExact=True,originalPhysicalTrajectoryUnchanged=True,noPhysicalPointerReplacement=True,inputHashes=pins,
        interPassEraseAccepted=False,allMoveGroundShadowAccepted=False,allArenaAudioCPUAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=verify()
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('passed','error','sampledFrames','exactScreenPixels','nativeShadowCopies','completePhaseCoverage')if k in result}),flush=True)
    raise SystemExit(0 if result['passed']else 1)
