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
import verify_cpu_recovery_v635_v4 as ordinary
import verify_cpu_followup_v635_v2 as special
import verify_ring_native_lookup_v1342 as current
import verify_native_grab_audio_v1415 as grab
import verify_current_ground_shadow_v1269 as graphics_model
import numpy as np
from verify_finish_display_v798 import check_owned_body_palette
ROOT=current.ROOT;NAME=grab.NAME
raster.HEX=raster.HEX|{'cursor','row','size','xy','b14','b10','a0','a1','a3','a7'}

CASES={'audit_v1419_cpu_queue_kano':('kano','blade'),
       'audit_v1419_cpu_queue_sonya':('sonya','ordinary')}

def matched(folder,inputs):
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    require(launch['exit_code']==0 and launch['candidate']==build['name']==NAME and
            launch['assistance']=='none'and launch['cheats_enabled']is False,'Actual current native cold case')
    require(launch['executable_sha256']==build['executable_sha256']=='01EF3950691A890BAA41723D99935E44A28B09A7431EA78EC5DBF8E0E90630C3'and
            launch['payload_sha256']==build['payload_sha256']=='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D','Matched current source-built files')
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    require(before==launch['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Complete executed input manifest')
    for p,h in before.items():
        require(current.digest(p)==h,'Changed executed input '+p);inputs[p]=h
        if Path(p).suffix in('.lua','.json','.ps1'):
            frozen=folder/'input_sources'/Path(p).name
            require(current.digest(frozen)==h,'Changed frozen observer');inputs[str(frozen)]=h
    path=grab.OUT/'report.json';data=json.loads(path.read_text())
    require(data['passed']and data['candidate']==NAME and data['wholeGuestIndependentlyReconstructed']and data['sourceDeltaOnlyDeclaredNativeGrabCues'],'Whole current source/guest contract')
    inputs[str(path)]=current.digest(path)
    for p,h in data['inputHashes'].items():require(current.digest(p)==h,'Changed source proof input');inputs[p]=h


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
        if slot==2:expected_id=ordinary.HUMANS[proof['player']]
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
            if slot==1:held[owner['pose']].add(dma['frame'])
            else:held_victim[owner['pose']].add(dma['frame'])
    require(wanted<=set(held),'Every distinct original held CPU pose actually draws')
    return dict(body_draws=body_draws,cached_components_checked=components,
                distinct_held_CPU_poses=[f'{p:08X}' for p in sorted(wanted)],
                distinct_held_victim_poses=[f'{p:08X}' for p in sorted(held_victim)])


def verify(folder,player,profile):
    inputs={};matched(folder,inputs)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    require(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation',log,re.I),'No native/observer error')
    # v7's observation schema and native instruction contracts are unchanged;
    # only genuine human approach buttons differ from v5/v6. Validate the pure
    # special contract directly, then independently require its full launch.
    proof=ordinary.verify_log(log,player) if profile=='ordinary' else special.verify_log(log,player,profile)
    require(proof['passed'],'Complete actual native pair/follow-up: '+str(proof['errors']))
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    require(launch['player']==player and launch['cpu_slot']==1 and launch['human_slot']==2,
            'Actual matched cold CPU/human case metadata')
    for name in ('mk2ks_cpu_recovery_probe_v1399.lua','mk2ks_cpu_pair_display_probe_v1399.lua'):
        text=(folder/'input_sources'/name).read_text()
        require(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',text),'Read-only observer: '+name)
    runner=(folder/'input_sources/run_current_cpu_pair_display_v1399.ps1').read_text()
    require('-nocheat' in runner and '-noautoframeskip -frameskip 0' in runner,'Unassisted complete native drawing enabled')
    visual=(folder/'input_sources/mk2ks_cpu_pair_display_probe_v1399.lua').read_text()
    require("dofile('mk2ks_cpu_recovery_probe_v1399.lua')" in visual,'Exact nested input scenario')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    require(hashlib.sha256(original).hexdigest().upper()=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
            'Exact original native program/picture data')
    payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    groups,_,_,_,_=raster.data(folder)
    guest,_,expected_payload=grab.expected_guest();require(payload==expected_payload,'Current complete payload')
    image=bytearray(graphics_model.graphics(inputs))
    for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        require(payload[header:header+4]==magic,'Native effect allocation')
        start,count,destination=struct.unpack_from('<III',payload,header+4)
        require(start==source and destination==dest and count>0,'Native graphics range')
        image[dest:dest+count]=payload[source:source+count]
    for r in groups['FLOOR_GFX']:
        require(bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],'Actual whole-scene graphics source including native effects')
    cache=check_composites(groups,payload,guest,{**proof,'log':log})
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
                    if r['slot']==1 and dmas[r['event']]['frame']+1 in snap_frames and
                    proof['start']<r['queue_frame']<=proof['release']}
    require({int(p,16) for p in cache['distinct_held_CPU_poses']}<=captured_poses,
            'Every distinct held CPU pose represented by an exact native displayed sample')
    palettes=0;ids=(17,ordinary.HUMANS[player])
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
    for snap in groups['FLOOR_SNAP']:
        actual=np.fromfile(folder/displays[snap['frame']]['palette_file'],dtype='<u4')
        for r in groups['FLOOR_QUEUE_DISPATCH']:
            if dmas[r['event']]['frame']!=snap['frame']-1:continue
            q=queues[r['queue_frame'],r['cursor']]
            if ids[q['slot']-1]in(17,18):
                check_owned_body_palette(q,actual,guest,ids,q['slot']);palettes+=1
    require(palettes>100,'Both original physical costumes across actual native samples')
    return dict(passed=True,player=player,target=proof['target'],paired=proof,cache=cache,
                sampled_frames=drawn['frames'],exact_screen_pixels=sum(r['display_pixels'] for r in drawn['records']),
                exact_body_pixels=sum(b['pixels'] for r in drawn['records'] for b in r['body'].values()),
                records=drawn['records'],fullPhysicalPaletteSamples=palettes,inputHashes=inputs,
                scope='current_Kano_CPU_choke_against_Kano_and_Sonya_native_handoffs_followup_and_sampled_display_not_all_moves_victims_slots_art_audio_or_goal',
                CPU_acceptance=False,fullPortAcceptance=False)


def report():
    cases={name:verify(ROOT/name,player,profile) for name,(player,profile) in CASES.items()}
    inputs={}
    for name,case in cases.items():
        inputs.update(case.pop('inputHashes'))
        for path in (ROOT/name).rglob('*'):
            if path.is_file():inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':
                inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    path=ROOT/'mk2/mk2-maincpu.bin';inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    return dict(passed=True,candidate=NAME,cases=cases,inputHashes=inputs,fullPortAcceptance=False,CPU_acceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    require(not args.output.exists(),'Refusing to overwrite evidence')
    proof=report();args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=proof['passed'],frames=sum(c['sampled_frames'] for c in proof['cases'].values()),
                         body_pixels=sum(c['exact_body_pixels'] for c in proof['cases'].values()),
                         screen_pixels=sum(c['exact_screen_pixels'] for c in proof['cases'].values())),indent=2))
