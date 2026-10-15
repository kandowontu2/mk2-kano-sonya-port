"""Current naturally selected P2 Sonya square miss, complete native scanout.

Every actual startup/seek/fall/landing scene is independently reconstructed
with physical FIFO ownership, queued projection, original donor animation,
palettes and compressed floor shadows. Thirty post-regain fields are retained, including the mirror's real later
Leg Grab branch; exact raster there is not full Leg Grab phase acceptance.
This does not prove all square contacts, CPU moves, arenas, audio or full port.
"""
import argparse,json,re,struct
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
import native_cpu_square_startup_contract_v3005 as square
import verify_native_cpu_square_locks_v3008 as model

ROOT=state.ROOT
CASES={'new_sonya':('audit_v3004_native_cpu_square_locks_new_sonya_original_retreat','new','sonya'),
 'old_kano':('audit_v3004_native_cpu_square_locks_old_kano_guard_wait_jump_guard','old','kano')}
shadow.data=raster.data

def verify(key):
    name,build,player=CASES[key];CASE=ROOT/name;victim_id=state.original.HUMANS[player]
    proof_path=model.OUT/'report.json';proof=json.loads(proof_path.read_text())
    assert proof['passed']and proof['cases'][key]['originalPhysicalAndNativeEventsUnchanged']
    pins=dict(proof['inputHashes']);pins[str(proof_path)]=model.inventory.assembly.sha(proof_path)
    guest,old,payload,_,_=model.inventory.assembly.expected();guest=guest if build=='new'else old
    meta=json.loads((CASE/'result.json').read_text(encoding='utf-8-sig'));assert meta['player']==player
    assert (CASE/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest independently reconstructed'
    log=(CASE/'run.log').read_text(encoding='utf-8-sig')
    typed=square.verify(log,guest,player);pair=typed
    assert typed==proof['cases'][key]['phase']
    assert pair['damage']==0 and not pair['allCPUAccepted']
    observer=(CASE/'input_sources/mk2ks_physical_p2_cpu_square_display_v2039.lua').read_text()
    assert "dofile('mk2ks_physical_p2_cpu_square_trace_v2038.lua')"in observer
    assert not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',observer)
    required={'mk2ks_cpu_recovery_probe_v1438.lua','mk2ks_physical_p2_cpu_square_display_v2039.lua',
        'run_native_cpu_square_locks_v3001.ps1','mk2ks_physical_p2_cpu_square_trace_v2038.lua','mk2ks_physical_p2_cpu_round_trace_v1998.lua','mk2ks_physical_p2_cpu_continuation_v1997.lua','mk2ks_physical_p2_cpu_overlap_trace_v1999.lua','mk2ks_physical_p2_cpu_choice_trace_v2035.lua','34010gfx.hxx','34010ops.hxx'}
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
    assert result[0]['recovered']==pair['ready']
    recovery=groups['FLOOR_RECOVERY'];assert len(recovery)==1 and recovery[0]['frame']==pair['ready']
    terminal=state.original.rows(log,'RESULT')[0]['frame']
    # The immutable input driver exits in register_frame at its terminal callback,
    # before that field reaches frame_done. Every completed native scanout is retained.
    driver=(CASE/'input_sources/mk2ks_physical_p2_cpu_continuation_v1997.lua').read_text()
    assert "if first_live and frame>=first_live+1800 then manager.machine:exit();return end"in driver
    assert terminal==state.original.rows_prefix(log,'MK2_P2CPU_COLD_LIVE ')[0]['frame']+1800,'Source-bound terminal after first ordinary regain and thirty callbacks'
    expected=list(range(pair['start']+1,pair['ready']+31))
    assert 'observed_recovery+30'in observer and 'f<=window_end()'in observer
    assert [r['frame']for r in groups['FLOOR_SNAP']]==expected and result[0]['snapshots']==len(expected)
    first=groups['FLOOR_STATE'][0];actors={s:first[f'p{s}']for s in(1,2)};mains={s:first[f'main{s}']for s in(1,2)}
    ids=(victim_id,18);anchors={17:134,18:135}
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
    common=('actor','source','pose','cache','id','body','facing','bank','pc')
    for key,q in queues.items():
        assert key in inventory and all(q[k]==inventory[key][k]for k in common),'Every tracked physical publication equals independent full inventory'
        t=transforms[key]
        assert all(t[k]==q[k]for k in('slot','actor','main')),'Projection registers belong to that same actual publication'
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
        if pair['start']<q['frame']<=pair['ready']:held[q['slot']].add(q['pose'])
    assert square.POSES-{0xfe835bc0}<=held[2],'All actual original startup and full cycling square poses executed'
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();donor_path=ROOT/'mk3/mk3-maincpu.bin';pins[str(donor_path)]=state.sha(donor_path)
    assert pins[str(donor_path)]=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    donor_pieces=0
    for pose in square.POSES:
        actual=art.group(dict(pose=pose,facing=0),payload,guest);native=art.source_groups(donor,square.POSE_DONORS[pose],0xff800000)
        assert len(actual)==len(native)
        for a,(_,n)in zip(actual,native):
            assert (a['width'],a['height'],a['dx'],a['dy'])==n[:4]and a['source']==n[4]+0x10000000 and a['command']==n[5],'Every square imported donor descriptor retained'
            donor_pieces+=1
    shadows=shadow.inspect(CASE)
    assert shadows['rowStreamVerified']and not shadows['failures']and not shadows['oversized_rows']and set(map(tuple,shadows['identities']))=={(1,victim_id),(2,18)}
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
    assert square.POSES<=visible[2],'Every startup and cycling square pose has an exact visible scanout'
    held_scanouts=[]
    for h in groups['FLOOR_HELD']:
        frame=h['frame'];display=displays[frame]
        rgb=np.asarray(Image.open(CASE/'snap'/snaps[frame]['file']).convert('RGB'))
        bound=check_latch(rgb,(CASE/h['file']).read_bytes(),(CASE/display['palette_file']).read_bytes(),h['start'],h['control'],h['tap'])
        held_scanouts.append(dict(frame=frame,pixels=bound['pixels'],DMAReconstructed=False))
    assert video['frames']+len(held_scanouts)==len(expected)and palette_checks>len(expected)
    state.launch.module_pins(pins)
    return dict(passed=True,candidate=meta['candidate'],state=typed,sampledFrames=len(expected),exactReplayedFrames=video['frames'],
        exactScreenPixels=sum(r['display_pixels']for r in video['records'])+sum(r['pixels']for r in held_scanouts),
        exactOwnedPixels=sum(b['pixels']for r in video['records']for b in r['body'].values()),fullPhysicalPaletteChecks=palette_checks,
        nativeShadowCopies=shadows['checked_copies'],nativeShadowComponents=shadows['components'],sourceBoundProjections=geometry,
        originalHeldDonorPieces=donor_pieces,heldOriginalScanouts=held_scanouts,allOriginalSquarePosesVisible=True,
        records=video['records'],inputHashes=pins,interPassEraseAccepted=False,allCPUAccepted=False,
        allMoveGroundShadowAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('key',choices=tuple(CASES));args=parser.parse_args()
    OUT=ROOT/f'audit_v3013_native_cpu_square_render_{args.key}_checked'
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=verify(args.key)
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('passed','error','sampledFrames','exactReplayedFrames','exactScreenPixels','nativeShadowCopies')if k in result}),flush=True)
    raise SystemExit(0 if result['passed']else 1)
