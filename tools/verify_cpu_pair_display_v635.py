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
from verify_native_candidate_v635 import ROOT,NAME,matched

CASES={
    'audit_v666_cpu_display_kano_cage':('cage','ordinary'),
    'audit_v666_cpu_display_kano_raiden':('raiden','ordinary'),
    'audit_v666_cpu_display_sonya_mirror':('sonya','bicycle'),
    'audit_v666_cpu_display_sonya_kano':('kano','square'),
    'audit_v666_cpu_display_sonya_liu':('liu_kang','square'),
}


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
    for r in groups['FLOOR_CACHE_PART']:parts[r['event'],r['slot']].append(r)
    owners=defaultdict(list)
    for r in groups['FLOOR_OWNER']:owners[r['event'],r['slot']].append(r)
    held=defaultdict(set);held_victim=defaultdict(set);components=0;body_draws=0
    steps=ordinary.rows(proof['log'],'EVENT')
    steps=[r for r in steps if r['kind']=='step' and r['cycle']==proof['cycle']]
    wanted={r['group'] for r in steps}
    for dma in groups['FLOOR_DMA']:
        if dma['command']&15!=2 or dma['slot'] not in (1,2):continue
        key=dma['event'],dma['slot'];found=owners[key]
        require(len(found)==1,'Exactly one actual owner of each body DMA')
        owner=found[0];slot=dma['slot']
        expected_id=17 if proof['target']=='kano' else 18
        if slot==2:expected_id=ordinary.HUMANS[proof['player']]
        require(owner['id']==owner['roster']==expected_id and owner['owner']==owner['actor'] and
                0x01000000<=owner['actor']<0x01100000 and 0x01000000<=owner['main']<0x01100000 and
                owner['bank']&0x7f00==dma['palette'],'True CPU/human sprite and palette ownership')
        expected=group(owner,payload,original);observed=parts[key]
        require(len(observed)==len(expected),'Every native cached component recorded')
        require(all(all(p[k]==v for k,v in e.items()) for p,e in zip(observed,expected)),
                'Exact actual ROM composite descriptors, cached offsets and native flip bits')
        require(any(dma['source']==p['source'] and dma['width']==p['width'] and
                    dma['height']==p['height'] and dma['command']==(p['command']|0x8002)
                    for p in observed),'Owned original cached component really reaches native DMA')
        body_draws+=1;components+=len(expected)
        if proof['start']<dma['frame']<=proof['release']:
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
    proof=ordinary.verify(folder,player) if profile=='ordinary' else special.verify_log(log,player,profile)
    require(proof['passed'],'Complete actual native pair/follow-up: '+str(proof['errors']))
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    require(launch['player']==player and launch['cpu_slot']==1 and launch['human_slot']==2,
            'Actual matched cold CPU/human case metadata')
    for name in ('mk2ks_cpu_recovery_probe_v7.lua','mk2ks_cpu_pair_display_probe_v3.lua'):
        text=(folder/'input_sources'/name).read_text()
        require(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',text),'Read-only observer: '+name)
    runner=(folder/'input_sources/run_cpu_pair_display_v3.ps1').read_text()
    require('-nocheat' in runner and '-noautoframeskip -frameskip 0' in runner,'Unassisted complete native drawing enabled')
    visual=(folder/'input_sources/mk2ks_cpu_pair_display_probe_v3.lua').read_text()
    require("dofile('mk2ks_cpu_recovery_probe_v7.lua')" in visual,'Exact nested input scenario')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    require(hashlib.sha256(original).hexdigest().upper()=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
            'Exact original native program/picture data')
    payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    groups,_,_,_,_=raster.data(folder)
    cache=check_composites(groups,payload,original,{**proof,'log':log})
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
    owners_by_frame=defaultdict(list)
    for r in groups['FLOOR_OWNER']:owners_by_frame[r['frame'],r['slot']].append(r)
    captured_poses={r['pose'] for frame in snap_frames for r in owners_by_frame[frame-1,1]
                    if proof['start']<frame-1<=proof['release']}
    require({int(p,16) for p in cache['distinct_held_CPU_poses']}<=captured_poses,
            'Every distinct held CPU pose represented by an exact native displayed sample')
    return dict(passed=True,player=player,target=proof['target'],paired=proof,cache=cache,
                sampled_frames=drawn['frames'],exact_screen_pixels=sum(r['display_pixels'] for r in drawn['records']),
                exact_body_pixels=sum(b['pixels'] for r in drawn['records'] for b in r['body'].values()),
                records=drawn['records'],inputHashes=inputs,
                scope='five_current_CPU_grab_held_pose_and_followup_display_paths_not_unsampled_fields_all_moves_victims_slots_art_audio_or_goal',
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
