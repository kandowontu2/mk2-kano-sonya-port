"""Actual current CPU grab composite -> owned cache -> DMA -> native scanout.

All sampled drawing passes are exact. Distinct held poses and complete native
paired state chronology are checked separately; unsampled rendered fields and
all artistic/cinematic/audio/whole-port fidelity remain outside this scope.
"""
import argparse
import hashlib
import json
import re
import struct
import sys
from collections import defaultdict
from pathlib import Path

import inspect_natural_arena_floor_v635_v4 as raster
import verify_physical_p2_cpu_pair_v1456 as ordinary
import verify_repeated_sonya_cpu_v1463 as repeated
import verify_cpu_followup_v1423 as special
import verify_ring_native_lookup_v1342 as current
import verify_active_launch_timer_v1520 as grab
import verify_current_ground_shadow_v1269 as graphics_model
import numpy as np
from verify_finish_display_v798 import check_owned_body_palette
import verify_current_interrupt_v1870 as active_launch
import verify_ball_register_source_v1837 as active
ROOT=active.ROOT;NAME=active.NAME
raster.HEX=raster.HEX|{'cursor','row','size','xy','b14','b10','a0','a1','a3','a7'}

def matched(folder,inputs):
    inputs.update(active_launch.source_pins())
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    require(launch['exit_code']==0 and launch['candidate']==build['name']==NAME and
            launch['assistance']=='none' and launch['cheats_enabled']is False,'Actual current native cold case')
    require(launch['executable_sha256']==build['executable_sha256']=='34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E' and
            launch['payload_sha256']==build['payload_sha256']=='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D','Matched current source-built files')
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    require(before==launch['input_hashes'] and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Complete executed input manifest')
    required={'mk2ks_cpu_recovery_probe_v1459.lua','mk2ks_cpu_pair_display_probe_v1459.lua','run_current_cpu_pair_display_v1875.ps1','build-info.json'}
    require(required<={Path(p).name for p in before},'All executed nested drivers tracked')
    for p,h in before.items():
        require(current.digest(p)==h,'Changed executed input '+p);inputs[p]=h
        if Path(p).suffix in('.lua','.json','.ps1'):
            frozen=folder/'input_sources'/Path(p).name
            require(current.digest(frozen)==h,'Changed frozen observer');inputs[str(frozen)]=h
    # Windows accepts mixed separator spellings in the original runner's keys.
    # Preserve every raw key/hash and additionally resolve aliases for lookup.
    normalized={}
    for p,h in before.items():
        key=str(Path(p).resolve())
        require(key not in normalized or normalized[key]==h,'Conflicting manifest aliases')
        normalized[key]=h
    require(normalized.get(str((ROOT/NAME/'mkport_candidate.exe').resolve()))==build['executable_sha256'] and
            normalized.get(str((ROOT/NAME/'roms/mk2ks/mk2ks.mdata').resolve()))==build['payload_sha256'],'Executed current binaries individually pinned')

def require(condition,label):
    if not condition:raise ValueError(label)


def group(owner,payload,original):
    def read(address,fmt):
        raw,base=(payload,0xfe800000) if 0xfe800000<=address<0xff800000 else (original,0xff800000)
        require(address>=base and (address-base)%8==0,'Actual aligned ROM composite address')
        off=(address-base)//8
        require(off>=0 and off+struct.calcsize(fmt)<=len(raw),'Actual ROM composite bounds')
        return struct.unpack_from(fmt,raw,off)
    result=[]
    for part in range(12):
        ptr=read(owner['pose']+part*32,'<I')[0]
        if ptr==0:break
        w,h,dx,dy,source,command=read(ptr,'<HHhhIH')
        if owner['facing']&16:dx=w-dx
        if owner['facing']&32:dy=h-dy
        result.append(dict(part=part,width=w,height=h,dx=dx,dy=dy,source=source,
                           command=(command&~0x30)|(owner['facing']&0x30)))
    require(bool(result) and len(result)<12,'Complete actual terminated fighter composite')
    return result


def check_composites(groups,payload,original,proof):
    parts=defaultdict(list)
    for r in groups['FLOOR_QUEUE_PART']:parts[r['frame'],r['cursor']].append(r)
    queues={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE']}
    require(len(queues)==len(groups['FLOOR_QUEUE']),'Unambiguous actual FIFO publications')
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    require(len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH']),'One actual FIFO cursor per owned DMA')
    require(len(regs)==len(groups['FLOOR_DMA_REGS']),'One actual register observation per DMA')
    dma_events={r['event'] for r in groups['FLOOR_DMA']}
    require(set(regs)==dma_events and set(dispatch)<=dma_events,'Complete native DMA register coverage')
    by_cursor=defaultdict(list)
    for q in queues.values():by_cursor[q['cursor']].append(q)
    for published in by_cursor.values():published.sort(key=lambda q:q['frame'])
    # Recompute the observer's queue classifier for EVERY command. An omitted
    # dispatch or slot=0 must not silently turn a real fighter into scenery.
    # Same-palette effects remain unowned; palette is never the classifier.
    for dma in groups['FLOOR_DMA']:
        published=[q for q in by_cursor[regs[dma['event']]['b14']+192] if q['frame']<=dma['frame']]
        q=published[-1] if published else None
        owned=bool(q and dma['command']&15==2 and q['source']==dma['source'])
        require((dma['event'] in dispatch)==owned and dma['slot']==(q['slot'] if owned else 0),
                'Complete exact FIFO classification, including same-palette non-body effects')
    held=defaultdict(set);held_victim=defaultdict(set);components=0;body_draws=0
    steps=ordinary.rows(proof['log'],'EVENT')
    steps=[r for r in steps if r['kind']=='step' and r['cycle']==proof['cycle']]
    wanted={r['group'] for r in steps}
    for dma in groups['FLOOR_DMA']:
        if dma['command']&15!=2 or dma['slot'] not in (1,2):continue
        require(dma['event'] in dispatch,'Exact actual queue-to-DMA cursor, not palette ownership')
        d=dispatch[dma['event']]
        owner=queues[d['queue_frame'],d['cursor']];slot=dma['slot']
        require(owner['cursor']==regs[dma['event']]['b14']+192 and owner['slot']==slot==d['slot'] and
                owner['actor']==d['actor'] and owner['main']==d['main'],
                'Original six-word FIFO iterator binds the actual published actor')
        expected_id=17 if proof['target']=='kano' else 18
        if slot==proof['human_slot']:expected_id=ordinary.HUMANS[proof['player']]
        require(owner['id']==owner['roster']==expected_id and owner['owner']==owner['actor'] and
                0x01000000<=owner['actor']<0x01100000 and 0x01000000<=owner['main']<0x01100000 and
                owner['bank']&0x7f00==dma['palette'],'True CPU/human sprite and palette ownership')
        expected=group(owner,payload,original);observed=parts[owner['frame'],owner['cursor']]
        require(len(observed)==len(expected),'Every native cached component recorded')
        require(all(all(p[k]==v for k,v in e.items()) for p,e in zip(observed,expected)),
                'Exact actual ROM composite descriptors, cached offsets and native flip bits')
        require(owner['pc']==0xff804420 and owner['row']==owner['cache']+owner['part']*112 and
                owner['part'] in range(len(expected)),
                'Actual original cache iterator and MMTM six-word publication instruction')
        part=observed[owner['part']]
        require(owner['source']==dma['source']==part['source'] and
                owner['size']&0xffff==dma['width']==part['width'] and
                owner['size']>>16==dma['height']==part['height'] and
                owner['command']>>16==dma['command']==(part['command']|0x8002) and
                owner['xy']&1023==dma['x'] and (owner['xy']>>16)&511==dma['y'],
                'Exact original queued size/source/command/XY reaches native DMA unchanged')
        body_draws+=1;components+=len(expected)
        if proof['start']<owner['frame']<=proof['release']:
            if slot==proof['CPU_slot']:held[owner['pose']].add(dma['frame'])
            else:held_victim[owner['pose']].add(dma['frame'])
    require(wanted<=set(held),'Every distinct original held CPU pose actually draws')
    return dict(body_draws=body_draws,cached_components_checked=components,
                distinct_held_CPU_poses=[f'{p:08X}' for p in sorted(wanted)],
                distinct_held_victim_poses=[f'{p:08X}' for p in sorted(held_victim)])


def verify(folder,player,model):
    inputs={};matched(folder,inputs)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    require(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation',log,re.I),'No native/observer error')
    # v7's observation schema and native instruction contracts are unchanged;
    # only genuine human approach buttons differ from v5/v6. Validate the pure
    # special contract directly, then independently require its full launch.
    proof=model.verify_log(log,player)
    require(proof['passed'],'Complete actual native pair/follow-up: '+str(proof['errors']))
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    require(launch['player']==player and launch['cpu_slot']==model.CPU_SLOT and launch['human_slot']==model.HUMAN_SLOT,
            'Actual matched cold CPU/human case metadata')
    version=1459
    for name in (f'mk2ks_cpu_recovery_probe_v{version}.lua',f'mk2ks_cpu_pair_display_probe_v{version}.lua'):
        text=(folder/'input_sources'/name).read_text()
        require(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',text),'Read-only observer: '+name)
    runner=(folder/'input_sources/run_current_cpu_pair_display_v1875.ps1').read_text()
    require('-nocheat' in runner and '-noautoframeskip -frameskip 0' in runner,'Unassisted complete native drawing enabled')
    visual=(folder/f'input_sources/mk2ks_cpu_pair_display_probe_v{version}.lua').read_text()
    require(f"dofile('mk2ks_cpu_recovery_probe_v{version}.lua')" in visual,'Exact nested input scenario')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    require(hashlib.sha256(original).hexdigest().upper()=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
            'Exact original native program/picture data')
    payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    groups,_,_,_,_=raster.data(folder)
    guest,_,expected_payload=active.expected();require(payload==expected_payload,'Current complete payload')
    image=bytearray(graphics_model.graphics(inputs))
    for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        require(payload[header:header+4]==magic,'Native effect allocation')
        start,count,destination=struct.unpack_from('<III',payload,header+4)
        require(start==source and destination==dest and count>0,'Native graphics range')
        image[dest:dest+count]=payload[source:source+count]
    for r in groups['FLOOR_GFX']:
        require(bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],'Actual whole-scene graphics source including native effects')
    caches=[check_composites(groups,payload,guest,{**pair,'log':log})for pair in proof['pairs']]
    cache=caches[0]
    drawn=raster.inspect(folder)
    result=groups['FLOOR_RESULT']
    require(len(result)==1 and result[0]['schema']==1 and result[0]['snapshots']==drawn['frames'],
            'All retained frame-done snapshots accounted')
    require(result[0]['origin']==proof['start'],'First real grab owns this display window')
    require(drawn['frames']>40 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records']),
            'Every saved prior-pass native DMA/CPU write and exact displayed pixel matches')
    require(all(r['body'][slot]['pixels']>100 and r['body'][slot]['mismatches']==0
                for r in drawn['records'] for slot in (1,2)),
            'Both actual composited bodies visible and exact through sampled sequence')
    snap_frames={r['frame'] for r in drawn['records']}
    queues={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE']}
    dmas={r['event']:r for r in groups['FLOOR_DMA']}
    captured_poses={queues[r['queue_frame'],r['cursor']]['pose'] for r in groups['FLOOR_QUEUE_DISPATCH']
                    if r['slot']==model.CPU_SLOT and dmas[r['event']]['frame']+1 in snap_frames and
                    proof['start']<r['queue_frame']<=proof['release']}
    for pair,paired_cache in zip(proof['pairs'],caches):
        paired_poses={queues[r['queue_frame'],r['cursor']]['pose']for r in groups['FLOOR_QUEUE_DISPATCH']
                      if r['slot']==model.CPU_SLOT and dmas[r['event']]['frame']+1 in snap_frames and
                      pair['start']<r['queue_frame']<=pair['release']}
        require({int(p,16)for p in paired_cache['distinct_held_CPU_poses']}<=paired_poses,
                'Every held CPU phase in EACH actual full repeated pair has an exact native displayed sample')
    palettes=0;physical_ids=[None,None];physical_ids[model.CPU_SLOT-1]=17 if proof['target']=='kano'else 18;physical_ids[model.HUMAN_SLOT-1]=ordinary.HUMANS[player];ids=tuple(physical_ids)
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
    for snap in groups['FLOOR_SNAP']:
        actual=np.fromfile(folder/displays[snap['frame']]['palette_file'],dtype='<u4')
        for r in groups['FLOOR_QUEUE_DISPATCH']:
            if dmas[r['event']]['frame']!=snap['frame']-1:continue
            q=queues[r['queue_frame'],r['cursor']]
            if ids[q['slot']-1]in(17,18):
                check_owned_body_palette(q,actual,guest,ids,q['slot']);palettes+=1
    require(palettes>100,'Both original physical costumes across actual native samples')
    return dict(passed=True,player=player,target=proof['target'],paired=proof,cache=cache,repeatedPairCaches=caches,
                sampled_frames=drawn['frames'],exact_screen_pixels=sum(r['display_pixels'] for r in drawn['records']),
                exact_body_pixels=sum(b['pixels'] for r in drawn['records'] for b in r['body'].values()),
                records=drawn['records'],fullPhysicalPaletteSamples=palettes,inputHashes=inputs,
                scope='two_actual_consecutive_P1_native_CPU_contacts_all_held_fields_native_individual_handoffs_full_flag_health_stream_and_sampled_display_not_all_moves_victims_art_audio_or_goal',
                CPU_acceptance=False,fullPortAcceptance=False)


def report(folder,player):
    case=verify(folder,player,repeated)
    inputs=case.pop('inputHashes')
    for path in folder.rglob('*'):
        if path.is_file():inputs[str(path)]=current.digest(path)
    active_launch.module_pins(inputs)
    return dict(passed=True,candidate=NAME,case=folder.name,proof=case,inputHashes=inputs,
                originalStateRasterContractsUnchanged=True,fullPortAcceptance=False,CPU_acceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',required=True)
    parser.add_argument('--player',choices=tuple(ordinary.HUMANS),required=True)
    parser.add_argument('--output',required=True);args=parser.parse_args()
    require(re.fullmatch(r'audit_v\d+_[a-z0-9_]+',args.case)and re.fullmatch(r'audit_v\d+_[a-z0-9_]+',args.output),'Exact versioned evidence leaves')
    folder=ROOT/args.case;output=ROOT/args.output
    require(not output.exists(),'Refusing to overwrite evidence')
    try:proof=report(folder,args.player)
    except Exception as error:
        pins={str(path):current.digest(path)for path in folder.rglob('*')if path.is_file()}
        active_launch.module_pins(pins)
        proof=dict(passed=False,error=repr(error),candidate=NAME,case=folder.name,inputHashes=pins,fullPortAcceptance=False,CPU_acceptance=False)
    output.mkdir();(output/'report.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({key:proof[key]for key in ('passed','candidate','case','error')if key in proof}),flush=True)
    if proof['passed']:
        print(json.dumps({key:proof['proof'][key]for key in ('sampled_frames','exact_body_pixels','exact_screen_pixels','fullPhysicalPaletteSamples')}),flush=True)
    raise SystemExit(0 if proof['passed']else 1)
