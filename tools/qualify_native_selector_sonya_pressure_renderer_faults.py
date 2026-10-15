"""Effective actual pressure CPU/DMA/pass faults, original equations unchanged.

Use the very same original Replay class and actual event windows for negative
controls. Never mutate native guest state or original captured buffers. All
1746 original whole-pass positives are restored after the counterexamples.
"""
import hashlib
import json
import traceback
from bisect import bisect_left,bisect_right
from collections import ChainMap
from pathlib import Path
import numpy as np
import qualify_native_selector_sonya_pressure_snapshot_replay as previous
import seal_native_selector_sonya_pressure_snapshot_provenance as parent

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_renderer_faults_checked'
CONTEXT=None


def prepare(text,display):
    groups,buffers,_,_,owners=previous.original.data(text,display)
    renderer=previous.original.bindings(text,display)
    events=sorted(((kind,r)for kind in ('FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU','FLOOR_FLIP')
                   for r in groups[kind]),key=lambda e:e[1]['event'])
    keys=[r['event']for _,r in events]
    need(len(keys)==len(set(keys)), 'Entire original event inventory has unique native ordering')
    return dict(groups=groups,buffers=buffers,owners=owners,renderer=renderer,
        events=events,eventKeys=keys,latches={r['snapshot']:r for r in groups['FLOOR_LATCH']},
        pre={r['frame']:r for r in groups['FLOOR_PRE_FRAME']},
        snaps={r['frame']:r for r in groups['FLOOR_SNAP']},
        displays={r['frame']:r for r in groups['FLOOR_DISPLAY']})


def window(context,frame):
    latch=context['latches'][frame];anchor=context['pre'][frame-1]
    need(anchor['event']<latch['event']and anchor['phase']=='before_first_frame_dma'and
         latch['snapshot']==latch['flip_frame']==frame,
         'Exact actual independent BEFORE-DMA through current native flip, no target-seeded pass')
    a=bisect_left(context['eventKeys'],anchor['event']);b=bisect_right(context['eventKeys'],latch['event'])
    events=context['events'][a:b]
    need(events[0][0]=='FLOOR_PRE_FRAME'and events[-1][0]=='FLOOR_FLIP'and
         events[0][1]==anchor and events[-1][1]['event']==latch['event'],
         'All actual commands in this original native pass, exact anchor and flip')
    return events


def one_pass(folder,context,frame,display,event_changes=None):
    # The same original equations and cached packed-stream decoder used by the
    # full1746-pass oracle; only RAM bindings differ in the negative controls.
    scope=context['renderer'].__globals__
    original_class=scope['Replay']
    rebound=previous.original.bindings('',display).__globals__['Replay']
    need(rebound.begin.__code__ == original_class.begin.__code__ and
         rebound.apply.__code__ == original_class.apply.__code__ and
         rebound.scaled_dma is original_class.scaled_dma,
         'Whole original native begin/apply/scaling bytecode retained in fault RAM namespace')
    replay=rebound(folder,context['groups'],context['buffers'],context['owners'])
    events=window(context,frame);flip=None
    for kind,record in events:
        d=(event_changes or {}).get(record['event'],record)
        if kind=='FLOOR_FLIP':flip=d
        else:replay.apply(kind,d)
    need(flip is not None, 'Actual final native flip present')
    latch=context['latches'][frame]
    actual=np.frombuffer(display['buffers'][latch['file']],dtype='<u2').reshape(512,512)
    need(np.array_equal(replay.words,actual), 'Entire512x512 independently replayed VRAM words exact')
    snap=context['snaps'][frame];field=context['displays'][frame]
    result=scope['check_latch'](display['rgb'][snap['file']],replay.words.tobytes(),
        display['buffers'][field['palette_file']],flip['value'],flip['control'],flip['tap'])
    return dict(frame=frame,event=flip['event'],commands=len(events),pixels=result['pixels'],
        wordsSHA256=hashlib.sha256(replay.words.tobytes()).hexdigest().upper())


def execute(state):
    global CONTEXT
    need(not OUT.exists(),'Fresh immutable actual complete pressure renderer counterexamples')
    receipt=json.loads(parent.OUT.read_text());pins=dict(receipt['inputHashes'])
    capture=previous.capture;held=capture.NATIVE_HANDLES[capture.KEY];folder,text,_=capture.RAM_CASES[capture.KEY]
    need(receipt['passed']and held['process'].poll()==receipt['nativeExit']==0 and
         held['identity']==receipt['actualNativeIdentity']and held['identity']['ProcessId']==47004 and
         not capture.reference.base.choices.current.prior.identity.census(),
         'Same original47004 terminal handle and empty native census, no new match')
    need(all(sha(p)==h for p,h in pins.items()),'Whole original source/native/capture evidence unchanged')
    baseline=json.loads((previous.OUT/'report.json').read_text())
    display=capture.DISPLAY;CONTEXT=prepare(text,display)
    frames=(1818,2324,2611,2942,3039,3107,3176,3599,3617)
    need(set(frames)<=set(CONTEXT['latches']), 'Actual native flips for all named KO/reset/hidden/continue test fields')
    positive={f:one_pass(folder,CONTEXT,f,display)for f in frames}
    faults=[]
    def reject(label,frame,action):
        try:action()
        except (ValueError,AssertionError)as error:faults.append(dict(kind=label,frame=frame,rejectedBy=str(error)))
        else:raise ValueError('Actual effective renderer counterexample admitted: '+label)
        need(one_pass(folder,CONTEXT,frame,display)==positive.get(frame,one_pass(folder,CONTEXT,frame,display)),
             'Whole untouched actual native pass restored after every negative control')
    for f in frames:
        file=CONTEXT['latches'][f]['file'];raw=bytearray(display['buffers'][file]);raw[-1]^=1
        changed=dict(display,buffers=ChainMap({file:bytes(raw)},display['buffers']))
        reject('actual_full_target_VRAM_word_%d'%f,f,lambda:one_pass(folder,CONTEXT,f,changed))
    f=1818;events=window(CONTEXT,f);anchor=events[0][1]
    raw=bytearray(display['buffers'][anchor['file']]);raw[-1]^=1
    changed=dict(display,buffers=ChainMap({anchor['file']:bytes(raw)},display['buffers']))
    reject('actual_hidden_prepass_word',f,lambda:one_pass(folder,CONTEXT,f,changed))
    flip=events[-1][1];changed_flip=dict(flip,value=flip['value']^16)
    reject('actual_native_flip_row',f,lambda:one_pass(folder,CONTEXT,f,display,{flip['event']:changed_flip}))
    body=next(r for kind,r in reversed(events)if kind=='FLOOR_DMA'and r['slot']==2 and r['command']&15==2 and r['width']and r['height'])
    for label,key,value in (('actual_native_body_palette','palette',body['palette']^0x100),
                            ('actual_native_body_X','x',body['x']^1),
                            ('actual_native_body_clip','right',0)):
        mutated=dict(body);mutated[key]=value
        reject(label,f,lambda:one_pass(folder,CONTEXT,f,display,{body['event']:mutated}))
    # Find an actually consumed native CPU store, not any unanchored inventory
    # record or a fabricated write. The original pre-write assertion must fail.
    cpu_case=next((frame,r)for frame in sorted(CONTEXT['latches'])for kind,r in window(CONTEXT,frame)
                  if kind=='FLOOR_CPU'and r['mask'])
    cpu_frame,cpu=cpu_case;positive[cpu_frame]=one_pass(folder,CONTEXT,cpu_frame,display)
    part=0 if cpu['mask']&255 else 1;before='before%d'%part
    mutated=dict(cpu);mutated[before]^=1
    reject('actual_consumed_CPU_prewrite_word',cpu_frame,
           lambda:one_pass(folder,CONTEXT,cpu_frame,display,{cpu['event']:mutated}))
    need(len(faults)==15, 'All nine full targets, anchor/flip/body palette/X/clip and real CPU store faults effective')
    restored=CONTEXT['renderer'](folder)
    need(restored==baseline['completeActualPassReplay'],
         'Every original whole1746-pass positive restored byte-for-byte after actual renderer faults')
    for p in (Path(__file__),parent.OUT,previous.OUT/'report.json',Path(previous.__file__)):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed source or positive result edited');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All whole source/native pins intact after original full restored positive')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualIndependentPassPositives=list(positive.values()),effectiveRendererFaultsRejected=faults,
        actualConsumedCPUStore=dict(frame=cpu_frame,event=cpu['event'],at=cpu['at'],pc=cpu['pc'],mask=cpu['mask']),
        originalWhole1746PassPositiveRestored=True,wholeExactPassVRAMWords=baseline['wholeExactPassVRAMWords'],
        finiteActualPressureRendererFaultSuiteAccepted=True,unsavedInterPassErasureAccepted=False,
        corpseEffectOwnershipAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        inputHashes=pins,requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS whole restored pressure rendering and15 actual native pass faults',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual pressure renderer counterexample failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
