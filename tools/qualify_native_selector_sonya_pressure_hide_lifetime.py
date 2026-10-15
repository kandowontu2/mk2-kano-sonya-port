"""Actual native hide/FIFO/front-buffer lifetime; no detached corpse assumed.

Original snapshot3107 shows the physical Kano3106 pass. Bind complete late
physical composites to real FIFO/DMA, require no later Kano sources, and track
actual low-pen overwrites with the unchanged original renderer equations.
"""
import hashlib
import json
import traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
import qualify_native_selector_sonya_pressure_renderer_faults_bound as faults
import qualify_native_selector_walkin_knife_display_ram as raster

ROOT,need,sha=faults.ROOT,faults.need,faults.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_hide_lifetime_checked'


def ownership(groups,state):
    queues=[r for r in groups['FLOOR_QUEUE']if r['frame']>=3039]
    inventory={(r['frame'],r['cursor']):r for r in groups['FLOOR_ALL_QUEUE']}
    need(len(inventory)==len(groups['FLOOR_ALL_QUEUE']), 'Every actual native FIFO publication independently unique')
    parts=defaultdict(list)
    for r in groups['FLOOR_QUEUE_PART']:parts[r['frame'],r['cursor']].append(r)
    identities={1:(0x01034e90,0x0106a370,17),2:(0x010350a0,0x0106bf30,18)}
    need(len({(r['frame'],r['cursor'])for r in queues})==len(queues), 'All actual late physical publications unique')
    for q in queues:
        actor,main,identity=identities[q['slot']]
        need((q['actor'],q['main'],q['owner'],q['parent'],q['id'],q['roster'],q['kind'])==
             (actor,main,actor,actor,identity,identity,0),'Entire late actual physical actor/Main/roster ownership')
        inv=inventory[q['frame'],q['cursor']]
        need(all(inv[k]==q[k]for k in ('actor','source','pose','cache','id','body','facing','bank')),
             'Physical publication agrees with independently inventoried native actor, never palette ownership')
        composition=raster.group(q,state['payload'],state['guest']);actual=parts[q['frame'],q['cursor']]
        need(q['multipart']==1 and len(composition)==len(actual)and
             all(all(p[k]==v for k,v in expected.items())for p,expected in zip(actual,composition)),
             'All actual late native packed-source composites and cache components exact')
        need(q['pc']==0xff804420 and q['row']==q['cache']+112*q['part']and q['part']in range(len(composition)),
             'Exact native cache iterator and FIFO publication source PC')
        p=composition[q['part']]
        need(q['source']==p['source']and(q['size']&65535,q['size']>>16)==(p['width'],p['height'])and
             q['command']>>16==p['command']|0x8002,'Whole actual published native source/size/command tuple')
    last=[q for q in queues if q['slot']==1 and q['frame']==3106]
    need(len(last)==2 and all(q['pose']==0xff00f860 for q in last)and
         max(q['frame']for q in queues if q['slot']==1)==3106,
         'Exactly both original physical Kano components last published3106, no detached actor assumption')
    sources={q['source']for q in last}
    need(all(not(0x10000000<=r['source']<0x1a000000)or
             (r['actor']==0x010350a0 and r['id']==18)for r in groups['FLOOR_ALL_QUEUE']if r['frame']>=3107),
         'Every later imported native publication is actual Sonya, no reappearing Kano or detached imported corpse')
    need(all(d['source']not in sources for d in groups['FLOOR_DMA']if d['frame']>=3107),
         'No later native body or black-shadow copy of either physical Kano death component')
    by_cursor=defaultdict(list)
    for q in groups['FLOOR_QUEUE']:by_cursor[q['cursor']].append(q)
    regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    qmap={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
    draws=0
    for d in groups['FLOOR_DMA']:
        if d['frame']<3039:continue
        published=[q for q in by_cursor[regs[d['event']]['b14']+192]if q['frame']<=d['frame']]
        q=published[-1]if published else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        need((d['event']in dispatch)==owned and d['slot']==(q['slot']if owned else 0),
             'Every late DMA classified by exact executing native FIFO cursor, including same-palette effects')
        if owned:
            r=dispatch[d['event']]
            need(qmap[r['queue_frame'],r['cursor']]==q and
                 (r['actor'],r['main'],r['slot'])==(q['actor'],q['main'],q['slot'])and
                 (d['source'],d['width'],d['height'],d['command'],d['palette'],d['x'],d['y'])==
                 (q['source'],q['size']&65535,q['size']>>16,q['command']>>16,q['bank']&0x7f00,q['xy']&1023,q['xy']>>16&511),
                 'Whole late owned physical FIFO tuple reaches native DMA unchanged')
            draws+=1
    return dict(actualLatePhysicalFIFOComponents=len(queues),actualLateOwnedDMADraws=draws,
                lastKanoPublicationField=3106,lastKanoPose=0xff00f860,lastKanoSources=sorted(sources))


class WriteTrackedWords(np.ndarray):
    def __array_finalize__(self,other):
        if other is not None:
            for k in ('written','labels','pen_write','label'):setattr(self,k,getattr(other,k,None))
    def __setitem__(self,key,value):
        super().__setitem__(key,value)
        if self.pen_write:
            self.written[key]=True;self.labels[key]=self.label


def tracked(context,sources):
    Base=context['renderer'].__globals__['Replay']
    class Tracking(Base):
        def apply(self,kind,d):
            if kind!='FLOOR_PRE_FRAME':
                self.words.pen_write=kind!='FLOOR_CPU'or bool(d['video_bank'])
                self.words.label=(d['slot']if d['command']&15==2 else 3 if d['source']in sources else 0)if kind=='FLOOR_DMA'else 0
            super().apply(kind,d)
            if kind=='FLOOR_PRE_FRAME':
                self.words=self.words.view(WriteTrackedWords)
                self.words.written=np.zeros((512,512),dtype=bool)
                self.words.labels=np.zeros((512,512),dtype=np.uint8)
                self.words.pen_write=True;self.words.label=0
    need(Tracking.dma is Base.dma and Tracking.cpu is Base.cpu and Tracking.scaled_dma is Base.scaled_dma,
         'Original whole DMA/CPU/scaling methods unchanged; observe host-array pen stores only')
    return Tracking


def execute(state):
    need(not OUT.exists(),'Fresh original native hide/visual-lifetime evidence')
    parent_path=faults.OUT/'report.json';parent=json.loads(parent_path.read_text())
    capture=faults.serialized.body.original.previous.capture
    held=capture.NATIVE_HANDLES[capture.KEY];folder,text,_=capture.RAM_CASES[capture.KEY]
    need(parent['passed']and held['process'].poll()==parent['nativeExit']==0 and
         held['identity']==parent['actualNativeIdentity']and held['identity']['ProcessId']==47004,
         'Original47004 terminal handle, never repeat gameplay for this lifetime check')
    pins=dict(parent['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'Every whole original source/evidence input intact')
    context=faults.scope['CONTEXT'];groups=context['groups'];display=capture.DISPLAY
    semantics=ownership(groups,state);sources=set(semantics['lastKanoSources'])
    geometry_path=ROOT/'audit_native_selector_sonya_cpu_pressure_round_shadow_scope_checked/report.json'
    geometry=json.loads(geometry_path.read_text())
    need(geometry['passed']and geometry['nativeFinishBlowStockInstructions']['FF804190']=='BTST   5h,A7'and
         geometry['nativeFinishBlowStockInstructions']['FF8041A0']=='JRNE   FF8045A0h',
         'Independently source-verified native hidden-body bit and original skip branch')
    physical=faults.serialized.body.original.previous.capture.reference.base.choices.native_state.original.pair.rows(text,'FIELD')
    need({r['frame']for r in physical if r['vbody']&32}==set(range(3107,3176)),
         'Exactly69 original live callbacks hide the owned physical Kano through stock bit5')
    Driver=tracked(context,sources);replay=Driver(folder,groups,context['buffers'],context['owners'])
    records=[];mask=None;last_clean=None
    helper=faults.serialized.body.original
    for f in range(3107,3618):
        if f not in context['latches']:continue
        for kind,d in helper.window(context,f):
            if kind!='FLOOR_FLIP':replay.apply(kind,d)
            else:flip=d
        latch=context['latches'][f];actual=display['buffers'][latch['file']]
        need(replay.words.tobytes()==actual, 'Every tracked complete native pass still equals all512x512 original VRAM words')
        snap=context['snaps'][f];field=context['displays'][f]
        proof=context['renderer'].__globals__['check_latch'](display['rgb'][snap['file']],actual,
            display['buffers'][field['palette_file']],flip['value'],flip['control'],flip['tap'])
        row,col=proof['row'],proof['column'];crop=lambda a:a[row:row+254,col:col+400]
        labels=crop(replay.words.labels);written=crop(replay.words.written)
        if f==3107:
            mask=(labels==1)|(labels==3)
            need(mask.any(), 'Last visible physical Kano body/possible shadow belongs to the actual3106 source pass')
        else:need(not np.any((labels==1)|(labels==3)), 'No post-hide source copy writes a Kano body or shadow')
        records.append(dict(frame=f,mode=next(r['mode']for r in groups['FLOOR_STATE']if r['frame']==f),
            oldKanoMaskPixels=int(mask.sum()),lowPenOverwritesOnOldKanoMask=int(written[mask].sum()),
            newKanoBodyOrShadowPixels=int(np.count_nonzero((labels==1)|(labels==3))),
            completeCurrentPixels=proof['pixels']))
        if f in (3108,3109,3536,3599,3617):
            need(written[mask].all(), 'Native background/next-scene lower-pen writes erase every old visible Kano pixel at required cleanup/continue boundaries')
        last_clean=f
    # Held fade callbacks occur only after the visible body lifetime. They are
    # fully bound separately; do not invent a DMA window during a native hold.
    held_frames=[r['snapshot']for r in groups['FLOOR_HELD']if r['snapshot']>=3107]
    need(held_frames==list(range(3482,3536))and len(records)+len(held_frames)==511,
         'Entire post-hide callback inventory:457 actual flip passes and54 genuine later held fade fields')
    faults_rejected=[]
    def reject(label,changed):
        try:ownership(changed,state)
        except (ValueError,AssertionError)as error:faults_rejected.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual effective visual-lifetime counterexample accepted: '+label)
    index=next(i for i,q in enumerate(groups['FLOOR_QUEUE'])if q['frame']==3106 and q['slot']==1)
    for key in ('actor','main','owner','id','source','bank'):
        queues=list(groups['FLOOR_QUEUE']);q=dict(queues[index]);q[key]^=1;queues[index]=q
        reject('actual_last_physical_Kano_'+key,dict(groups,FLOOR_QUEUE=queues))
    original=next(q for q in groups['FLOOR_ALL_QUEUE']if q['frame']==3106 and q['actor']==0x01034e90)
    for label,actor in (('resurrected_hidden_physical_body',0x01034e90),('fabricated_detached_imported_corpse',0x01031d10)):
        ghost=dict(original,frame=3107,actor=actor)
        reject(label,dict(groups,FLOOR_ALL_QUEUE=list(groups['FLOOR_ALL_QUEUE'])+[ghost]))
    restored=ownership(groups,state);need(restored==semantics, 'Whole untouched actual late physical ownership restored')
    for p in (Path(__file__),parent_path,geometry_path,Path(raster.__file__)):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace executed source/evidence');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()), 'Every complete source/capture pin after whole lifetime checks')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualLatePhysicalSourceFIFOAndDMA=semantics,records=records,heldPostHideFrames=held_frames,
        actualSourceHideFields=list(range(3107,3176)),lastPhysicalKanoVisibleSnapshot=3107,
        firstPostHideErasedSnapshot=3108,noDetachedImportedCorpseObserved=True,
        previousSeparateCorpseInterpretationCorrected=True,effectiveLifetimeFaultsRejected=faults_rejected,
        stockBloodTaskOwnershipIndividuallyAccepted=False,allFinisherEffectsOwnershipAccepted=False,
        finiteActualPressureNativeHideLifetimeAccepted=True,fullPortAcceptance=False,publicPlayableChanged=False,
        inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS real physical Kano hide/FIFO/next-field cleanup; no detached corpse fabricated',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual native hide/FIFO/pen-overwrite rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
