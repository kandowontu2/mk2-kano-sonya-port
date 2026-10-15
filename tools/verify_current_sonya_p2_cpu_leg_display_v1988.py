"""Current physical P2 Sonya leg grab and actual ordinary follow-up on Kano.

Every consecutive retained native scanout, complete physical FIFO/cache/DMA,
queued projection, costume palette and original compressed shadow is checked.
This is one natural Dead Pool case, not all CPU moves/arenas/audio/campaign.
"""
import json,re,struct
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_current_physical_p2_cpu_v1916 as state
import verify_current_ground_shadow_v1859 as graphics
import inspect_ball_register_erase_v1843 as erase
import inspect_current_cpu_knife_raster_v1975 as raster
import inspect_native_shadow_rows_v635 as shadow
import verify_human_projectile_display_v1352 as art
from verify_finish_display_v798 import check_owned_body_palette
from verify_native_floor_display_v602 import check_latch
from verify_restart_pair import LEG_OWN,LEG_GROUPS

ROOT=state.ROOT;CASE=ROOT/'audit_v1987_current_sonya_p2_cpu_leg_display_kano'
OUT=ROOT/'audit_v1988_current_sonya_p2_cpu_leg_display_checked'
shadow.data=raster.data

def verify():
    pins=state.launch.source_pins();guest,_,payload=state.launch.current.expected()
    meta=state.matched(CASE,pins);assert meta['player']=='kano'
    assert(meta['boot_frame'],meta['confirm_age'],meta['approach'])==(604,264,'guard_until_close')
    assert (CASE/'guest_maincpu.bin').read_bytes()==guest,'Whole current guest independently reconstructed'
    log=(CASE/'run.log').read_text(encoding='utf-8-sig')
    baseline=ROOT/state.CASES['kano'];old=(baseline/'run.log').read_text(encoding='utf-8-sig')
    prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_')
    assert [r for r in log.splitlines()if r.startswith(prefixes)]==[r for r in old.splitlines()if r.startswith(prefixes)],'Added observation leaves the entire original physical trajectory unchanged'
    pins[str(baseline/'run.log')]=state.sha(baseline/'run.log')
    typed=state.verify_log(log,'kano',guest);pair=typed['originalContract']
    assert pair['target']=='sonya'and pair['native_followup']['kind']=='ordinary'
    observer=(CASE/'input_sources/mk2ks_physical_p2_cpu_leg_display_v1985.lua').read_text()
    assert "dofile('mk2ks_cpu_recovery_probe_v1438.lua')"in observer
    assert not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',observer)
    required={'mk2ks_cpu_recovery_probe_v1438.lua','mk2ks_physical_p2_cpu_leg_display_v1985.lua',
        'run_current_physical_p2_cpu_leg_display_v1986.ps1','34010gfx.hxx','34010ops.hxx'}
    assert required<={Path(p).name for p in meta['input_hashes']}
    image=bytearray(graphics.graphics(pins))
    for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),
        (0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        assert payload[header:header+4]==magic
        start,count,destination=struct.unpack_from('<III',payload,header+4)
        assert start==source and destination==dest and count>0 and source+count<=len(payload)and dest+count<=len(image)
        image[dest:dest+count]=payload[source:source+count]
    raster.source(pins)
    groups,buffers,_,_,owners=raster.data(CASE)
    for r in groups['FLOOR_GFX']:
        assert 0<=r['first']<r['first']+r['bytes']<=len(image)
        assert bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],'All body/scene/shadow/effect graphics independently source-bound'
    begin=groups['FLOOR_BEGIN'];result=groups['FLOOR_RESULT'];assert len(begin)==len(result)==1
    assert begin[0]['origin']==result[0]['origin']==pair['start'] and begin[0]['id']==18
    terminal=state.original.rows(log,'RESULT')[0]['frame']
    expected=list(range(pair['start']+1,terminal+1))
    assert [r['frame']for r in groups['FLOOR_SNAP']]==expected and result[0]['snapshots']==len(expected)
    first=groups['FLOOR_STATE'][0];actors={s:first[f'p{s}']for s in(1,2)};mains={s:first[f'main{s}']for s in(1,2)}
    ids=(17,18);anchors={17:134,18:135}
    assert all(r['mode']==2 and all(r[f'p{s}']==actors[s]and r[f'main{s}']==mains[s]and r[f'roster{s}']==ids[s-1]
        and r[f'state{s}']==(1 if s==1 else 0)for s in(1,2))for r in groups['FLOOR_STATE'])
    assert not groups['FLOOR_CHILD_SPAWN']and not groups['FLOOR_CHILD_ALLOC']and not groups['FLOOR_CHILD_RETIRE']
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
    inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_QUEUE']}
    assert len(queues)==len(groups['FLOOR_QUEUE'])and len(inventory)==len(groups['FLOOR_ALL_QUEUE'])>len(queues)
    parts=defaultdict(list);published=defaultdict(list)
    for p in groups['FLOOR_QUEUE_PART']:parts[p['frame'],p['cursor']].append(p)
    for q in queues.values():published[q['cursor']].append(q)
    for key,q in inventory.items():
        if q['actor']in actors.values():assert key in queues and queues[key]['slot']in(1,2),'No actual physical publication omitted'
    transforms={(t['frame'],t['cursor']):t for t in groups['FLOOR_QUEUE_TRANSFORM']}
    assert set(transforms)==set(queues)
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();lo,hi=((a-0xff800000)//8 for a in(0xff804040,0xff804470))
    assert guest[lo:hi]==original[lo:hi],'Original native camera/cache/flip/display FIFO projection code unchanged'
    signed=lambda v:(v&65535)-65536 if v&32768 else v&65535
    geometry=0
    for key,q in queues.items():
        s=q['slot'];assert s in(1,2)and q['actor']==q['owner']==q['parent']==actors[s]and q['main']==mains[s]
        assert q['id']==q['roster']==ids[s-1]and q['kind']==0 and q['multipart']==1
        composition=art.group(q,payload,guest);actual=parts[key]
        assert len(actual)==len(composition)and all(all(p[k]==v for k,v in e.items())for p,e in zip(actual,composition))
        assert q['row']==q['cache']+112*q['part']and q['pc']==0xff804420
        p=composition[q['part']];t=transforms[key]
        assert t['world']==((q['y']&65535)<<16)|(q['x']&65535)
        assert t['floor']==q['floor']==t['stageY']-anchors[ids[s-1]]
        x,y=signed(t['world']),signed(t['world']>>16)
        if not t['a7']&1:x-=signed(t['camera']);y-=signed(t['camera']>>16)
        x-=p['dx'];y-=p['dy'];command=q['command']>>16
        if command&16:x+=p['width']-1
        if command&32:y+=p['height']-1
        x+=signed(t['display']);y+=signed(t['display']>>16)
        assert(q['xy']&1023,q['xy']>>16&511)==(x&1023,y&511),'Each body part uses its actual queued projection, not late camera reads'
        geometry+=1
    dmas={d['event']:d for d in groups['FLOOR_DMA']};regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    assert set(regs)==set(dmas)and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH'])
    drawn=defaultdict(list);held=defaultdict(set)
    for event,d in dmas.items():
        candidates=[q for q in published[regs[event]['b14']+192]if q['frame']<=d['frame']]
        q=max(candidates,key=lambda r:r['frame'])if candidates else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        assert(event in dispatch)==owned and d['slot']==(q['slot']if owned else 0),'Every FIFO dispatch recomputed, never inferred from palette'
        if not owned:continue
        pub=dispatch[event];assert queues[pub['queue_frame'],pub['cursor']]==q and all(pub[k]==q[k]for k in('actor','main','slot'))
        p=art.group(q,payload,guest)[q['part']]
        assert d['source']==p['source']and(d['width'],d['height'])==(p['width'],p['height'])and d['command']==p['command']|0x8002
        assert(q['xy']&1023,q['xy']>>16&511,q['bank']&0x7f00)==(d['x'],d['y'],d['palette'])
        drawn[d['frame']].append(q)
        if pair['start']<q['frame']<=pair['release']:held[q['slot']].add(q['pose'])
    assert set(LEG_OWN)<=held[2]and set(LEG_GROUPS[17])<=held[1],'All five complete own and victim leg-grab poses executed'
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();donor_path=ROOT/'mk3/mk3-maincpu.bin';pins[str(donor_path)]=state.sha(donor_path)
    assert pins[str(donor_path)]=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    donor_pieces=0
    for pose in set(LEG_OWN)|set(LEG_GROUPS[17]):
        actual=art.source_groups(payload,pose,0xfe800000);native=art.source_groups(donor,pose+0x1000000,0xff800000)
        assert len(actual)==len(native)
        for(_,a),(_,n)in zip(actual,native):
            assert a[:4]==n[:4]and a[4]==n[4]+0x10000000 and a[5]==n[5],'Every held imported donor descriptor retained'
            donor_pieces+=1
    shadows=shadow.inspect(CASE)
    assert shadows['rowStreamVerified']and not shadows['failures']and not shadows['oversized_rows']and set(map(tuple,shadows['identities']))=={(1,17),(2,18)}
    print('Complete CPU pair/source/FIFO/projection and '+str(shadows['checked_copies'])+' original shadow copies pass; replaying consecutive scenes',flush=True)
    video=raster.inspect(CASE)
    assert all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records'])
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};snaps={r['frame']:r for r in groups['FLOOR_SNAP']}
    visible=defaultdict(set);palette_checks=0
    for r in video['records']:
        colors=np.fromfile(CASE/displays[r['frame']]['palette_file'],dtype='<u4');assert colors[15]==0
        for q in drawn[r['frame']-1]:
            check_owned_body_palette(q,colors,guest,ids,q['slot']);palette_checks+=1
            if r['body'][q['slot']]['pixels']>100:visible[q['slot']].add(q['pose'])
    assert set(LEG_OWN)<=visible[2]and set(LEG_GROUPS[17])<=visible[1],'Every complete actual held pose has an exact visible scanout'
    held_scanouts=[]
    for h in groups['FLOOR_HELD']:
        frame=h['frame'];display=displays[frame]
        rgb=np.asarray(Image.open(CASE/'snap'/snaps[frame]['file']).convert('RGB'))
        bound=check_latch(rgb,(CASE/h['file']).read_bytes(),(CASE/display['palette_file']).read_bytes(),h['start'],h['control'],h['tap'])
        held_scanouts.append(dict(frame=frame,pixels=bound['pixels'],DMAReconstructed=False))
    assert video['frames']+len(held_scanouts)==len(expected)and palette_checks>len(expected)
    state.launch.module_pins(pins)
    return dict(passed=True,candidate=state.launch.NAME,state=typed,sampledFrames=len(expected),exactReplayedFrames=video['frames'],
        exactScreenPixels=sum(r['display_pixels']for r in video['records'])+sum(r['pixels']for r in held_scanouts),
        exactOwnedPixels=sum(b['pixels']for r in video['records']for b in r['body'].values()),fullPhysicalPaletteChecks=palette_checks,
        nativeShadowCopies=shadows['checked_copies'],nativeShadowComponents=shadows['components'],sourceBoundProjections=geometry,
        originalHeldDonorPieces=donor_pieces,heldOriginalScanouts=held_scanouts,allFiveHeldOwnAndVictimPosesVisible=True,
        records=video['records'],inputHashes=pins,interPassEraseAccepted=False,allCPUAccepted=False,
        allMoveGroundShadowAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=verify()
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('passed','error','sampledFrames','exactReplayedFrames','exactScreenPixels','nativeShadowCopies')if k in result}),flush=True)
    raise SystemExit(0 if result['passed']else 1)
