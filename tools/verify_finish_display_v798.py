"""Bounded original fatality FIFO/components and exact sampled scanout.

Held transition samples have direct scanout binding only, NOT DMA replay.
This proves four current v786 physical-slot cases and applicable native palettes,
not all victims, audio, donor art fidelity or finisher completeness.
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
from verify_native_candidate_v798 import ROOT, NAME, matched
from verify_native_floor_display_v602 import check_latch

raster.HEX |= {'parent','cursor','row','size','xy','b14','b10','a0','a1','a3','a7','entry','frame_table','descriptor','field','before',
               'p1','p2','main1','main2',
               'word_F0','word_140','word_160','word_1A0','word_1D0'}
raster.STR |= {'words','reason'}
CASES={'audit_v797_kano_sonya_p1':(17,18),
       'audit_v797_kano_subzero_p2':(8,17),
       'audit_v797_sonya_raiden_p1':(18,7),
       'audit_v797_sonya_mirror_p2':(18,18)}


def composites(groups,payload,original,ids,guest,side):
    own,victim=side,3-side
    begin=groups['FLOOR_BEGIN'][0]
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
            require(q['slot']==3 and q['parent']==begin['actor'] and q['main']==begin['main'] and
                    q['roster']==ids[own-1] and q['owner'] in (q['parent'],q['actor']),
                    'Actual effect ancestry belongs to its own physical winner Main, never victim/proxy')
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
            frame_base=0xfffb2000 if q['facing']&16 else 0xfffb1800
            require(frame_base<=ptr<frame_base+2048 and (ptr-frame_base)%256==0,
                    'Own native facing-specific kiss frame, no descriptor substitute')
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
    if ids[own-1]==17:
        require({0xfe9b24f0,0xfe9b2550,0xfe9b25b0,0xfe9b2610,0xfe9b2670,
                 0xfe9b26d0,0xfe9b2730,0xfe9b2790,0xfe9b2810}<=poses[own], 'All Kano arm phases actually draw')
        require({0xfe9b22d0,0xfe9b2310,0xfe9b2350,0xfe9b23d0,0xfe9b2430,0xfe9b2490}==poses[3],
                'All six separate skeleton composites actually draw')
        wanted=set(struct.unpack_from('<6I',guest,0xf7a00+ids[victim-1]*32))
        require(wanted<=poses[victim],
                'Own headed/headless/collapse victim phases actually draw')
    else:
        bases={p&~2047 for p in orb_frames}
        require(len(bases)==1 and bases<={0xfffb1800,0xfffb2000} and
                {next(iter(bases))+i*256 for i in range(8)}==orb_frames,
                'All eight actual own facing-specific single-frame orb sprites draw')
        require({0xfe8402c0,0xfe840340,0xfe8403c0,0xfe840440,0xfe8404c0,0xfe840540,
                 0xfe8405c0,0xfe840640,0xfe8406c0,0xfe840740,0xfe8407a0,
                 0xfe83d500,0xfe83d560,0xfe83d5a0,0xfe83d600,0xfe83d660,0xfe83d6a0,0xfe83d700,0xfe83d760}<=poses[own],
                'All Sonya kiss and concurrent outro phases actually draw')
        require({0xfe9b0ae0,0xfe9b0b20,0xfe9b0b60,0xfe9b0ba0,0xfe9b0be0,0xfe9b0c20,0xfe9b0c60,
                 0xfe9b0ca0,0xfe9b0ce0,0xfe9b0d40,0xfe9b0da0,0xfe9b0e00,0xfe9b0e60,0xfe9b0ec0,0xfe9b0f20}<=poses[victim],
                'All fifteen independent burning-victim composites actually draw')
    return {'draws':dict(draws),'poses':{s:[f'{p:08X}' for p in sorted(v)] for s,v in poses.items()},
            'single_frames':[f'{p:08X}' for p in sorted(orb_frames)]}


def retirement(groups,begin,guest,ids,side):
    states=groups['FLOOR_STATE'];retired=groups['FLOOR_RETIRED']
    require(len(retired)==1 and len(states)==961 and [r['frame'] for r in states]==list(range(begin['origin'],begin['origin']+961)),
            'Every native actor state retained, no missing retirement interval')
    teardown=retired[0]['frame']
    require(teardown==min(r['frame'] for r in states if r['p1']==r['p2']==0) and
            retired[0]['mode']==3 and retired[0]['winner']==side and retired[0]['victim_health']==0,
            'Actual native retirement of both physical fighters after own fatality win')
    before=[r for r in states if r['frame']<teardown]
    first=states[0]
    require(first[f'p{side}']==begin['actor'] and first[f'main{side}']==begin['main'] and
            all(r['p1']==first['p1'] and r['p2']==first['p2'] and r['roster1']==ids[0] and r['roster2']==ids[1] for r in before),
            'Own physical fighter/victim pointers and IDs persist until actual native retirement')
    require(all(r['p1']==r['p2']==0 for r in states if r['frame']>=teardown),
            'Retired physical actors remain released throughout recorded transition')
    off=(0xff82bbb0-0xff800000)//8
    require(struct.unpack_from('<7H',guest,off)==(0x5600,0x0780,0x0220,0x0106,0x0780,0x0df0,0x0106),
            'Original CLR A0 and both absolute native pointer stores unchanged')
    stores=groups['FLOOR_POINTER_STORE']
    require(len(stores)==4 and all(r['frame']==teardown and r['mask']==65535 and r['value']==0 for r in stores),
            'Exactly four complete original halfword retirement stores')
    tracking={0x01060220:first['p1'],0x01060df0:first['p2']}
    expected=((0x01060220,0x01060220,0xff82bbf0),(0x01060220,0x01060230,0xff82bbf0),
              (0x01060df0,0x01060df0,0xff82bc20),(0x01060df0,0x01060e00,0xff82bc20))
    for s,(field,at,pc) in zip(stores,expected):
        require((s['field'],s['at'],s['pc'])==(field,at,pc) and s['before']==tracking[field],
                'Actual original store PC/physical field and previous pointer halves')
        tracking[field]&=~(65535<<(at-field))
    require(all(v==0 for v in tracking.values()),'Both exact native physical pointers fully cleared')
    return teardown


def check_palette_record(q,actual,guest,ids,side):
    """Expected RGB from original native palette tables, not sampled colors."""
    victim=3-side;hero=ids[side-1];identity=ids[victim-1]
    if hero==17 and identity<=11:
        phases=struct.unpack_from('<6I',guest,0xf7a00+identity*32)
        if q['pose'] not in phases[1:]:return None
        at=(0xff90c900-0xff800000)//8+identity*8+(4 if q['body']&64 else 0)
        ptr=struct.unpack_from('<I',guest,at)[0];off=(ptr-0xff800000)//8
        count=struct.unpack_from('<H',guest,off)[0]
        label='original_native_primary_alternate_headless_palette'
    elif hero==18 and 0xfe9b0ae0<=q['pose']<=0xfe9b0f20:
        off=0xf5900;ptr=0xff800000+off*8
        count=struct.unpack_from('<H',guest,off)[0];label='own_32_color_fire_palette'
        require(count==32,'Actual fire palette is32 colors, not old64-color flash alias')
    else:return None
    require(32<=count<=256,'Actual bounded original palette count')
    raw=struct.unpack_from('<'+str(count)+'H',guest,off+2)
    expected=np.array([sum(((((c>>shift)&31)<<3)|(((c>>shift)&31)>>2))<<dest
                          for shift,dest in ((10,16),(5,8),(0,0))) for c in raw],dtype=np.uint32)
    bank=q['bank']&0x7f00
    require(len(actual)==32768 and np.array_equal(actual[bank:bank+count],expected),
            'Every expected original native palette RGB value reaches the actual scanout bank')
    return dict(source=f'{ptr:08X}',count=count,bank=bank,slot=victim,
                kind=label,alternate=bool(q['body']&64))


def palettes(folder,groups,guest,ids,side):
    victim=3-side;by_frame={}
    for q in groups['FLOOR_QUEUE']:
        if q['slot']==victim:by_frame[q['frame']]=q
    records=[];own_records=[]
    own_by_frame={q['frame']:q for q in groups['FLOOR_QUEUE'] if q['slot']==side}
    for display in groups['FLOOR_DISPLAY']:
        q=by_frame.get(display['frame']-1)
        if not q:continue
        actual=np.fromfile(folder/display['palette_file'],dtype='<u4')
        result=check_palette_record(q,actual,guest,ids,side)
        if result:records.append(dict(frame=display['frame'],pose=f'{q["pose"]:08X}',**result))
    for display in groups['FLOOR_DISPLAY']:
        q=own_by_frame.get(display['frame']-1)
        if not q:continue
        actual=np.fromfile(folder/display['palette_file'],dtype='<u4')
        result=check_owned_body_palette(q,actual,guest,ids,side)
        own_records.append(dict(frame=display['frame'],pose=f'{q["pose"]:08X}',**result))
    applicable=ids[side-1]==18 or ids[3-side-1]<=11
    require(not applicable or len(records)>40,'Positive native palette coverage, not an empty palette check')
    require(len(own_records)>100,'Positive full-bright own normal/alternate fatality body coverage')
    return dict(records=records,checked_palette_entries=sum(r['count'] for r in records),
                own_fighter_records=own_records,own_fighter_palette_entries=sum(r['count'] for r in own_records),
                own_alternate_samples=sum(r['alternate'] for r in own_records),
                applicable=applicable,own_normal_alternate_palette_acceptance=True,
                all_original_donor_art_fidelity=False)


def check_owned_body_palette(q,actual,guest,ids,side):
    """The finisher's own body keeps its actual normal/alternate native colours."""
    hero=ids[side-1]
    require(q['slot']==side and q['id']==q['roster']==hero and hero in(17,18),
            'Actual own normal/alternate palette belongs to declared finisher')
    alternate=bool(q['body']&64)
    off=(0xf1500 if hero==17 else 0xf1600)if alternate else(0xfda00 if hero==17 else 0xfdb00)
    count=struct.unpack_from('<H',guest,off)[0]
    require(count==65,'Original transparent plus 64 native fighter colours')
    raw=struct.unpack_from('<65H',guest,off+2)
    expected=np.array([sum(((((c>>shift)&31)<<3)|(((c>>shift)&31)>>2))<<dest
                          for shift,dest in ((10,16),(5,8),(0,0)))for c in raw],dtype=np.uint32)
    bank=q['bank']&0x7f00
    require(len(actual)==32768 and np.array_equal(actual[bank:bank+65],expected),
            'Own normal/alternate fighter palette dimmed or recoloured')
    return dict(source=f'{0xff800000+off*8:08X}',count=65,bank=bank,slot=side,alternate=alternate,
                kind='own_full_bright_normal_alternate_fighter_palette')


def verify(folder,ids):
    inputs={};matched(folder,inputs)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    require(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation',log,re.I),'No game/observer error')
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    side=launch['human_slot'];require(side in (1,2),'Explicit actual physical winner slot')
    damage=json.loads((folder/'native_damage_verification.json').read_text(encoding='utf-8-sig'))
    require(launch['passed'] and damage['passed'] and damage['complete_native_rounds']==2 and
            damage['native_writer_pc']=='FF836700','Real two-round native wins and input activation')
    wrapper_name='mk2ks_finish_display_v680_v7.lua'
    wrapper=(folder/'input_sources'/wrapper_name).read_text()
    require(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',wrapper),'Read-only observer')
    groups,_,_,_,_=raster.data(folder)
    require(len(groups['FLOOR_BEGIN'])==1 and len(groups['FLOOR_RESULT'])==1,'One bounded native fatality')
    begin=groups['FLOOR_BEGIN'][0];result=groups['FLOOR_RESULT'][0]
    require(begin['human_slot']==side and begin['id']==ids[side-1] and begin['entry']==(0xfffaae00 if ids[side-1]==17 else 0xfffab200)
            and begin['frame']==begin['origin']==result['origin'],'Own actual native action starts window')
    guest_path=ROOT/'audit_v790_kano_friendship_p1/guest_maincpu.bin'
    guest=guest_path.read_bytes();guest_hash=hashlib.sha256(guest).hexdigest().upper()
    require(guest_hash=='9F55AA553617BD761BD3F5DD6D9701439DD98BA69527544DBB4DD744DC14CA12',
            'Exact whole current guest ROM, including patched single-frame tables')
    inputs[str(guest_path)]=guest_hash
    checkpoint=ROOT/'audit_v796_current_audio_babality_checkpoint/verification.json'
    proof=json.loads(checkpoint.read_text())
    require(proof['candidate']==NAME and proof['executable_sha256']==launch['executable_sha256']
            and proof['checked_inputs'].get(str(guest_path))==guest_hash,
            'Borrowed initial guest dump is pinned to this exact current executable')
    inputs[str(checkpoint)]=hashlib.sha256(checkpoint.read_bytes()).hexdigest().upper()
    cache=composites(groups,(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),
                     (ROOT/'mk2/mk2-maincpu.bin').read_bytes(),ids,guest,side)
    colors=palettes(folder,groups,guest,ids,side)
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
    teardown=retirement(groups,begin,guest,ids,side)
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
    return dict(passed=True,ids=ids,human_slot=side,cache=cache,palette=colors,replayed=drawn,held_transition_scanout=held,
                visible_poses={s:[f'{p:08X}' for p in sorted(v)] for s,v in visible.items()},
                native_teardown_frame=teardown,post_transition_replayed_samples=len(after),
                child_update_records=len(groups['FLOOR_CHILD_UPDATE']),
                child_publication_discovery=groups['FLOOR_CHILD_INSTRUCTION'],inputHashes=inputs,
                scope='Actual physical-slot fatality composite/sample paths; held transitions only direct scanout; not all victims/slots/audio/finishers/art acceptance',
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
