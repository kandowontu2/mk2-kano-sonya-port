"""Bounded original fatality FIFO/components and exact sampled scanout.

Held transition samples have direct scanout binding only, NOT DMA replay.
This proves two P1 cases, not all victims, slots, audio or finisher completeness.
"""
import argparse
import hashlib
import json
import re
import sys
import struct
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import inspect_finish_display_v680_v1 as raster
from verify_cpu_pair_display_v635_v3 import group, require
from verify_native_candidate_v680 import ROOT, NAME, matched
from verify_native_floor_display_v602 import check_latch

raster.HEX |= {'parent','cursor','row','size','xy','b14','b10','a0','a1','a3','a7','entry','frame_table','descriptor','field','before',
               'p1','p2','main1','main2',
               'word_F0','word_140','word_160','word_1A0','word_1D0'}
raster.STR |= {'words','reason'}
CASES={'audit_v691_finish_retirement_kano_sonya':(17,18),
       'audit_v691_finish_retirement_sonya_raiden':(18,7)}


def composites(groups,payload,original,ids,guest):
    parts=defaultdict(list)
    for r in groups['FLOOR_QUEUE_PART']:parts[r['frame'],r['cursor']].append(r)
    queues={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE']}
    require(len(queues)==len(groups['FLOOR_QUEUE']),'Unique actual FIFO publications')
    by_cursor=defaultdict(list)
    for q in queues.values():by_cursor[q['cursor']].append(q)
    for rows in by_cursor.values():rows.sort(key=lambda q:q['frame'])
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    registers={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    require(len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH']),'Unique actual dispatch')
    require(len(registers)==len(groups['FLOOR_DMA_REGS'])==len(groups['FLOOR_DMA']),
            'Every native DMA has an actual register observation')
    singles={(r['frame'],r['cursor']):r for r in groups['FLOOR_SINGLE_DESCRIPTOR']}
    require(len(singles)==len(groups['FLOOR_SINGLE_DESCRIPTOR']),'Unique native single-frame descriptors')
    poses=defaultdict(set);draws=defaultdict(int);orb_frames=set()
    for d in groups['FLOOR_DMA']:
        published=[q for q in by_cursor[registers[d['event']]['b14']+192] if q['frame']<=d['frame']]
        q=published[-1] if published else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        require((d['event'] in dispatch)==owned and d['slot']==(q['slot'] if owned else 0),
                'Exact queue classifier recomputed for every DMA, never palette-only')
        if not owned:continue
        publication=dispatch[d['event']]
        require(publication['cursor']==q['cursor'] and publication['queue_frame']==q['frame']
                and publication['actor']==q['actor'] and publication['main']==q['main']
                and publication['slot']==q['slot'],'Exact original published actor reaches consumer')
        require(q['bank']&0x7f00==d['palette'],'Actual actor palette reaches native DMA')
        if q['slot'] in (1,2):
            require(q['id']==q['roster']==ids[q['slot']-1], 'No proxy fighter or victim ID')
            require(q['parent']==q['actor'] and q['kind']==0,'Physical fighter, not effect object')
        else:
            require(q['kind']==1 and q['actor']!=q['parent'],'Separate attached effect object')
        if q['multipart']:
            expected=group(q,payload,original)
            observed=parts[q['frame'],q['cursor']]
            require(len(expected)==len(observed) and
                    all(all(p[k]==v for k,v in e.items()) for p,e in zip(observed,expected)),
                    'Every component equals actual ROM composite, offsets and native flip')
            require(q['pc']==0xff804420 and q['row']==q['cache']+q['part']*112 and
                    q['part'] in range(len(expected)), 'Original full component cache iterator')
            p=observed[q['part']]
        else:
            require(q['slot']==3 and q['kind']==1 and q['pose']==0 and q['body']&2==0 and
                    q['row']==q['part']==0,'Actual native single-frame branch, not fake multipart pose')
            s=singles[q['frame'],q['cursor']]
            require(s['descriptor']==q['cache'] and s['actor']==q['actor'] and s['slot']==q['slot'],
                    'Own single-frame descriptor and actor observed at publication')
            ptr=q['cache'];off=(ptr-0xff800000)//8
            require(0xfffb1800<=ptr<0xfffb2000 and (ptr-0xfffb1800)%256==0,
                    'Own right-facing kiss frame, no descriptor substitute')
            raw=bytes.fromhex(s['data'])
            require(s['bytes']==32 and len(raw)==32 and raw==guest[off:off+32],
                    'Entire single-frame descriptor equals actual guest ROM bytes')
            w,h,dx,dy,source,command=struct.unpack_from('<HHhhIH',raw)
            p=dict(source=source,width=w,height=h,command=(command&~0x30)|(q['facing']&0x30))
            orb_frames.add(ptr)
        require(q['source']==d['source']==p['source'] and
                q['size']&65535==d['width']==p['width'] and q['size']>>16==d['height']==p['height'] and
                q['command']>>16==d['command']==(p['command']|0x8002) and
                q['xy']&1023==d['x'] and (q['xy']>>16)&511==d['y'],
                'Actual queued source/size/command/position unchanged at native DMA')
        poses[q['slot']].add(q['pose']);draws[q['slot']]+=1
    require(draws[1]>100 and draws[2]>100,'Both physical fighters actually draw')
    if ids[0]==17:
        require({0xfe9b24f0,0xfe9b2550,0xfe9b25b0,0xfe9b2610,0xfe9b2670,
                 0xfe9b26d0,0xfe9b2730,0xfe9b2790,0xfe9b2810}<=poses[1], 'All Kano arm phases actually draw')
        require({0xfe9b22d0,0xfe9b2310,0xfe9b2350,0xfe9b23d0,0xfe9b2430,0xfe9b2490}==poses[3],
                'All six separate skeleton composites actually draw')
        require({0xfe9b2d10,0xfe9b2db0,0xfe9b2e50,0xfe9b2ef0,0xfe9b2f70,0xfe9b2fb0}<=poses[2],
                'Own headed/headless/collapse victim phases actually draw')
    else:
        require({0xfffb1800+i*256 for i in range(8)}==orb_frames,'All eight actual own single-frame orb sprites draw')
        require({0xfe8402c0,0xfe840340,0xfe8403c0,0xfe840440,0xfe8404c0,0xfe840540,
                 0xfe8405c0,0xfe840640,0xfe8406c0,0xfe840740,0xfe8407a0,
                 0xfe83d500,0xfe83d560,0xfe83d5a0,0xfe83d600,0xfe83d660,0xfe83d6a0,0xfe83d700,0xfe83d760}<=poses[1],
                'All Sonya kiss and concurrent outro phases actually draw')
        require({0xfe9b0ae0,0xfe9b0b20,0xfe9b0b60,0xfe9b0ba0,0xfe9b0be0,0xfe9b0c20,0xfe9b0c60,
                 0xfe9b0ca0,0xfe9b0ce0,0xfe9b0d40,0xfe9b0da0,0xfe9b0e00,0xfe9b0e60,0xfe9b0ec0,0xfe9b0f20}<=poses[2],
                'All fifteen independent burning-victim composites actually draw')
    return {'draws':dict(draws),'poses':{s:[f'{p:08X}' for p in sorted(v)] for s,v in poses.items()},
            'single_frames':[f'{p:08X}' for p in sorted(orb_frames)]}


def verify(folder,ids):
    inputs={};matched(folder,inputs)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    require(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation',log,re.I),'No game/observer error')
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    damage=json.loads((folder/'native_damage_verification.json').read_text(encoding='utf-8-sig'))
    require(launch['passed'] and damage['passed'] and damage['complete_native_rounds']==2 and
            damage['native_writer_pc']=='FF836700','Real two-round native wins and input activation')
    wrapper_name='mk2ks_finish_display_v680_v5.lua'
    wrapper=(folder/'input_sources'/wrapper_name).read_text()
    require(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',wrapper),'Read-only observer')
    groups,_,_,_,_=raster.data(folder)
    require(len(groups['FLOOR_BEGIN'])==1 and len(groups['FLOOR_RESULT'])==1,'One bounded native fatality')
    begin=groups['FLOOR_BEGIN'][0];result=groups['FLOOR_RESULT'][0]
    require(begin['id']==ids[0] and begin['entry']==(0xfffaae00 if ids[0]==17 else 0xfffab200)
            and begin['frame']==begin['origin']==result['origin'],'Own actual native action starts window')
    guest_path=ROOT/'audit_v684_pit_guest_rom_integrity'/NAME/'guest_maincpu.bin'
    guest=guest_path.read_bytes();guest_hash=hashlib.sha256(guest).hexdigest().upper()
    require(guest_hash=='8395DD271BA3A8B8FABED892E9C3E14E2BA51EC8D952A041BA667AFB8015010D',
            'Exact whole current guest ROM, including patched single-frame tables')
    inputs[str(guest_path)]=guest_hash
    cache=composites(groups,(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),
                     (ROOT/'mk2/mk2-maincpu.bin').read_bytes(),ids,guest)
    drawn=raster.inspect(folder)
    require(all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records']),
            'Every retained prior pass and full scanout exactly reconstructed')
    # The positive requirement is rendered coverage of each choreography pose,
    # not merely allocation, state assignment or a correct invisible DMA.
    publications={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE']}
    dispatched=defaultdict(list)
    for d in groups['FLOOR_QUEUE_DISPATCH']:
        dispatched[d['frame']].append(publications[d['queue_frame'],d['cursor']])
    visible=defaultdict(set)
    for record in drawn['records']:
        for q in dispatched[record['frame']-1]:
            if record['body'][q['slot']]['pixels']>0:
                visible[q['slot']].add(q['pose'] if q['multipart'] else q['cache'])
    for slot in (1,2,3):
        # Include ordinary pre-action dizzy/victory poses recorded in the same
        # window; each also needs a positively visible native sampled field.
        wanted={int(p,16) for p in cache['poses'].get(slot,[]) if int(p,16)!=0}
        if slot==3:wanted|={int(p,16) for p in cache['single_frames']}
        require(wanted<=visible[slot], 'Each actual fighter/victim/effect pose positively visible: '+str(slot))
    states=groups['FLOOR_STATE'];retired=groups['FLOOR_RETIRED']
    require(len(retired)==1 and len(states)==961 and [r['frame'] for r in states]==list(range(begin['origin'],begin['origin']+961)),
            'Every native actor state retained, no missing retirement interval')
    teardown=retired[0]['frame']
    require(teardown==min(r['frame'] for r in states if r['p1']==r['p2']==0) and
            retired[0]['mode']==3 and retired[0]['winner']==1 and retired[0]['health2']==0,
            'Actual native retirement of both physical fighters after own fatality win')
    require({r['field'] for r in groups['FLOOR_POINTER_STORE'] if r['value']==0 and r['frame']<=teardown}=={0x01060220,0x01060df0},
            'Actual native stores release both physical fighter pointers')
    require(teardown>begin['origin']+150, 'Native scene transition follows completed fatality action')
    require(not any(d['slot']==3 for d in groups['FLOOR_QUEUE_DISPATCH'] if d['frame']>teardown),
            'Attached effect is not published after native scene teardown')
    after=[r for r in drawn['records'] if r['frame']>teardown+1]
    require(len(after)>5 and all(r['body'][3]['pixels']==0 for r in after),
            'Post-retirement passes contain no new attached-effect draws; native wipe may retain old scene pixels')
    held=[]
    snaps={r['frame']:r for r in groups['FLOOR_SNAP']}
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
    for h in groups['FLOOR_HELD']:
        require(h['frame']==h['snapshot'] and h['reason']=='no_current_flip_or_prior_DMA',
                'Explicit held transition, not relabeled reconstructed')
        image=np.asarray(Image.open(folder/'snap'/snaps[h['frame']]['file']).convert('RGB'))
        d=displays[h['frame']]
        require(all(h[k]==d[k] for k in ('start','control','tap')),'Held sample actual display registers')
        bound=check_latch(image,(folder/h['file']).read_bytes(),(folder/d['palette_file']).read_bytes(),
                          h['start'],h['control'],h['tap'])
        held.append({'frame':h['frame'],'last_flip':h['last_flip'],'pixels':bound['pixels'],
                     'DMA_reconstructed':False})
    require(result['snapshots']==drawn['frames']+len(held)==len(snaps), 'Every requested sample accounted')
    return dict(passed=True,ids=ids,cache=cache,replayed=drawn,held_transition_scanout=held,
                visible_poses={s:[f'{p:08X}' for p in sorted(v)] for s,v in visible.items()},
                native_teardown_frame=teardown,post_transition_replayed_samples=len(after),
                child_update_records=len(groups['FLOOR_CHILD_UPDATE']),
                child_publication_discovery=groups['FLOOR_CHILD_INSTRUCTION'],inputHashes=inputs,
                scope='Two actual P1 fatality composite/sample paths; held transitions only direct scanout; not all victims/slots/audio/finishers/art acceptance',
                fatalityAcceptance=False,fullPortAcceptance=False)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=CASES);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();require(not a.output.exists(),'Refuse overwriting evidence')
    selected={a.case:CASES[a.case]} if a.case else CASES
    cases={name:verify(ROOT/name,ids) for name,ids in selected.items()}
    inputs={}
    for name,c in cases.items():
        inputs.update(c.pop('inputHashes'))
        for path in (ROOT/name).rglob('*'):
            if path.is_file():inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).is_relative_to(ROOT/'tools'):
            inputs[str(Path(file))]=hashlib.sha256(Path(file).read_bytes()).hexdigest().upper()
    report=dict(passed=True,cases=cases,inputHashes=inputs,fullPortAcceptance=False)
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({n:dict(passed=c['passed'],frames=c['replayed']['frames'],
                            held=len(c['held_transition_scanout'])) for n,c in cases.items()},indent=2))
