"""Exact current native Pit queue/body/full-scene saved-pass reconstruction.

No best-frame/page/pose searches. Art/audio/whole-port acceptance stays separate.
"""
import argparse
import hashlib
import json
import struct
import sys
import wave
import re
from collections import defaultdict
from pathlib import Path
import numpy as np
import inspect_natural_pit_saved_passes_v680_v1 as raster
import verify_cpu_pair_display_v635_v3 as composite
import verify_native_pit_scene_v680_v1 as scene
from verify_native_candidate_v680 import matched, matched_reference
from verify_pit_initial_cache_v680 import verify as initial_cache

CASES={'audit_v681_pit_initial_kano_p1':('kano',1,'audit_v672_current_pit_kano_p1'),
       'audit_v681_pit_initial_sonya_p2':('sonya',2,'audit_v672_current_pit_sonya_p2')}

def data(folder):
    groups,*rest=raster.data(folder)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    for row in scene.rows(log,'PIT_NATIVE'):
        groups['PIT_NATIVE'].append({k:int(v,16 if k in raster.base.HEX else 10)
                                     for k,v in row.items()if k not in ('fighter','assistance')})
    return (groups,*rest)


def body_queues(groups,payload,original,proof):
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
    scene.need(len(queues)==len(groups['FLOOR_QUEUE']),'Unambiguous original FIFO publications')
    parts=defaultdict(list)
    for p in groups['FLOOR_QUEUE_PART']:parts[p['frame'],p['cursor']].append(p)
    regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    scene.need(len(regs)==len(groups['FLOOR_DMA_REGS']) and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH']),
               'One original DMA/queue association per command')
    dmas={r['event']:r for r in groups['FLOOR_DMA']}
    scene.need(set(regs)==set(dmas) and set(dispatch)<=set(dmas),'Complete native DMA register coverage')
    by_cursor=defaultdict(list)
    for q in queues.values():by_cursor[q['cursor']].append(q)
    for published in by_cursor.values():published.sort(key=lambda q:q['frame'])
    first=0xff182000+(proof['actual_id']-17)*6*64
    poses=set();draws=0;translations=[]
    for dma in dmas.values():
        published=[q for q in by_cursor[regs[dma['event']]['b14']+192] if q['frame']<=dma['frame']]
        q=published[-1] if published else None
        owned=bool(q and dma['command']&15==2 and q['source']==dma['source'])
        scene.need((dma['event'] in dispatch)==owned and dma['slot']==(1 if owned else 0),
                   'Every DMA classified by actual original FIFO, never palette')
        if not owned:continue
        d=dispatch[dma['event']]
        q=queues[d['queue_frame'],d['cursor']]
        scene.need(q['slot']==d['slot']==1 and q['actor']==q['owner']==d['actor'] and q['main']==d['main'] and
                   q['cursor']==regs[dma['event']]['b14']+192 and
                   q['id']==q['roster']==proof['actual_id'] and q['bank']&0x7f00==dma['palette'],
                   'Actual constructed true-ID cinematic victim, Main+140h and native palette')
        expected=composite.group(q,payload,original);observed=parts[q['frame'],q['cursor']]
        scene.need(len(expected)==len(observed)==1 and
                   all(observed[0][key]==value for key,value in expected[0].items()),
                   'Actual own ROM body descriptor and exact native cache')
        part=expected[0]
        scene.need(q['pc']==0xff804420 and q['part']==0 and q['row']==q['cache'] and
                   q['source']==dma['source']==part['source'] and
                   q['size']&0xffff==dma['width']==part['width'] and q['size']>>16==dma['height']==part['height'] and
                   q['command']>>16==dma['command']==(part['command']|0x8002) and
                   q['xy']&1023==dma['x'] and(q['xy']>>16)&511==dma['y'],
                   'Original six-word publication reaches native DMA unchanged')
        scene.need(q['pose'] in {first+phase*64 for phase in range(6)},'Own fall/impact stream, no stock proxy')
        poses.add(q['pose']);draws+=1
        translations.append(dict(frame=dma['frame'],pose=q['pose'],x=dma['x']-(q['x']-part['dx']),
                                 y=(dma['y']-(q['y']-part['dy']))%256))
    scene.need(poses=={first+phase*64 for phase in range(6)},'Every own fall pose and impact actually queued')
    return dict(body_draws=draws,poses=[f'{p:08X}' for p in sorted(poses)],translations=translations)


def native_impact(groups,proof,original):
    args=groups['PIT_NATIVE'];impact=proof['pit_impact']
    shake=[r for r in args if r['entry']==0xff9e1290 and r['frame']==impact]
    scene.need(len(shake)==1 and shake[0]['frame']==impact and shake[0]['a11']==0x50005 and
               shake[0]['pc']==0xff9e12a0,'Original five-step, five-pixel impact shake entry')
    sounds=[r for r in args if r['entry']==0xffa12530 and r['frame']==impact]
    indices=[r['a0'] for r in sounds]
    victim=0xcc if proof['actual_id']==17 else 0xce
    scene.need(0xcf in indices and victim in indices,'Actual native impact effect and correct male/female voice group')
    for at,word in ((0xff85c560,0x09c0),(0xff85c570,0x00cf),(0xff85c5b0,0x09e1),
                    (0xff85c5c0,0xccce),(0xff85c5d0,0xcccc),(0xff85c610,0x09eb),
                    (0xff85c620,5),(0xff85c630,5),(0xff9e1390,0x07a6),(0xff9e13c0,0x4566),
                    (0xff9e13d0,0x0786),(0xff9e1400,0x09c0),(0xff9e1410,3),
                    (0xff9e1450,0x03ab),(0xff9e1460,0x3dca)):
        scene.need(struct.unpack_from('<H',original,(at-0xff800000)//8)[0]==word,'Original native impact/shake instruction')
    cameras=[(r['frame'],r['cameraY']) for r in groups['FLOOR_SNAP'] if impact-1<=r['frame']<=impact+20]
    scene.need(len(cameras)==22,'Every actual impact/shake camera field captured')
    changes=[(frame,value) for i,(frame,value) in enumerate(cameras) if i and value!=cameras[i-1][1]]
    scene.need(len(changes)==5 and [r[1] for r in changes]==[-5,0,-5,0,-5] and
               all(b[0]-a[0]==3 for a,b in zip(changes,changes[1:])) and
               impact<=changes[0][0]<=impact+1,'Exactly original alternating three-field camera cadence')
    return dict(native_sound_groups=indices,expected_victim_group=victim,
                shake_arguments='00050005',camera_changes=changes)


def audio_trace(folder,reference,groups):
    records=groups['FLOOR_AUDIO']
    scene.need(records,'Actual native sound-update callbacks retained')
    previous=None;total=0;peak=0
    with wave.open(str(reference/'native_audio.wav'),'rb') as wav:
        scene.need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(2,2,48000),
                   'Actual previous matched native stereo PCM reference')
        for row in records:
            scene.need(row['rate']==48000 and row['channels']==2,'Actual declared native mix rate/channels')
            raw=(folder/row['file']).read_bytes()
            scene.need(len(raw)==row['samples']*4,'Every complete native mixed-audio block retained')
            end=round(float(row['seconds'])*48000);first=end-row['samples']
            scene.need(first>=0 and end<=wav.getnframes() and(previous is None or first==previous),
                       'Actual emulator-time audio blocks are contiguous, no best-sample search')
            wav.setpos(first)
            scene.need(raw==wav.readframes(row['samples']),
                       'Every native mixed PCM sample exactly matches the unchanged real-input reference')
            samples=np.frombuffer(raw,dtype='<i2').astype(np.int32)
            peak=max(peak,int(np.max(np.abs(samples))) if len(samples) else 0)
            previous=end;total+=row['samples']
    scene.need(peak>0 and total>48000*7,'Complete non-silent native Pit/impact/post-impact mix interval')
    return dict(blocks=len(records),stereo_frames=total,peak=peak,exact_reference_PCM=True,
                scope='Exact synchronized native mix replay plus separate voice-group routing, not auditory/artistic or all-character audio acceptance')


def inspect(folder,fighter,side,reference):
    inputs={};matched(folder,inputs);matched_reference(reference,inputs)
    proof=scene.verify(folder,fighter,reference,side=side)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    ref=(reference/'run.log').read_text(encoding='utf-8-sig')
    for tag in ('INPUT','HEALTH','FIGHT','STATE','PIT_LOOKUP','PIT_EXIT'):
        prefix=lambda text:[r for r in scene.rows(text,tag)if int(r['frame'])<=proof['pit_exit']]
        scene.need(prefix(log)==prefix(ref),'Exact original campaign through first Pit native exit: '+tag)
    groups,_,_,_,_=data(folder)
    payload=(scene.ROOT/scene.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    original=(scene.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    cache=body_queues(groups,payload,original,proof)
    init=initial_cache(folder,proof)
    effect=native_impact(groups,proof,original)
    audio=audio_trace(folder,reference,groups)
    drawing=raster.inspect(folder)
    scene.need(drawing['frames']==331 and [r['frame'] for r in drawing['records']]==list(range(proof['pit_enter'],proof['pit_enter']+331)),
               'All consecutive declared Pit display fields, including impact/post-impact')
    scene.need(all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawing['records']),
               'Every exact retained prior native pass, VRAM word and displayed pixel matches')
    pixels=sum(r['display_pixels'] for r in drawing['records'])
    for path in folder.rglob('*'):
        if path.is_file():inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    for path in (reference/'run.log',reference/'result.json',reference/'native_audio.wav'):
        inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    return dict(passed=True,fighter=fighter,human_slot=side,native_state=proof,initial_cache=init,body=cache,impact=effect,
                rendered=drawing,audio=audio,exact_screen_pixels=pixels,inputHashes=inputs,
                fullPortAcceptance=False,artAcceptance=False,audioAcceptance=False,
                scope='two_current_Pit_native_queue_complete_saved_display_passes_and_shake_voice_group_routing_not_all_cinematics_art_correct_PCM_or_goal')


def report():
    cases={name:inspect(scene.ROOT/name,fighter,side,scene.ROOT/ref) for name,(fighter,side,ref) in CASES.items()}
    inputs={}
    for case in cases.values():inputs.update(case.pop('inputHashes'))
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(scene.ROOT/'tools') and path.suffix=='.py':
                inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    for name in ('mk2/mk2-maincpu.bin','diagnostic_v545_native_roll_edge_clearance/roms/mk2ks/mk2ks.mdata'):
        path=scene.ROOT/name;inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    return dict(passed=True,candidate=scene.NAME,cases=cases,inputHashes=inputs,fullPortAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    scene.need(not args.output.exists(),'Never overwrite evidence')
    proof=report();args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=True,rendered_frames=sum(c['rendered']['frames'] for c in proof['cases'].values()),
                         pixels=sum(c['exact_screen_pixels'] for c in proof['cases'].values())),indent=2))
