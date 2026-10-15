"""Whole late native source ownership plus measured erase-observation gap.

Never waive the failed full-pen erase assertion or claim detached corpse
ownership. Prove the actual physical FIFO/DMA lifetime and measure the exact
flip-to-prepass interval with the unchanged native CPU/DMA equations.
"""
import hashlib
import json
import traceback
from pathlib import Path
import numpy as np
import qualify_native_selector_sonya_pressure_hide_lifetime as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_hide_source_checked'
FAILURE=original.OUT/'failure.json'


def execute(state):
    need(not OUT.exists(),'Fresh actual native hide ownership and missing-transfer diagnosis')
    failed=json.loads(FAILURE.read_text())
    need(not failed['passed']and failed['error']==
         "ValueError('Native background/next-scene lower-pen writes erase every old visible Kano pixel at required cleanup/continue boundaries')",
         'Keep actual whole-pen erase check FAILED; no weaker replacement acceptance')
    parent_path=original.faults.OUT/'report.json';parent=json.loads(parent_path.read_text())
    capture=original.faults.serialized.body.original.previous.capture
    held=capture.NATIVE_HANDLES[capture.KEY];folder,text,_=capture.RAM_CASES[capture.KEY]
    need(parent['passed']and held['process'].poll()==parent['nativeExit']==0 and held['identity']==parent['actualNativeIdentity'],
         'Same actual47004 terminal handle; no new game for this source diagnosis')
    pins=dict(parent['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'Every whole source/evidence pin unchanged')
    context=original.faults.scope['CONTEXT'];groups=context['groups'];display=capture.DISPLAY
    semantics=original.ownership(groups,state)
    # Inspect every asserted writer on each late actual physical publication.
    # The snapshot3107 front buffer is generated from physical source field3106.
    latch=context['latches'][3107];pre=context['pre'][3106]
    events=original.faults.serialized.body.original.window(context,3107)
    owned_events={d['event']for d in groups['FLOOR_DMA']if d['slot']==1 and d['frame']==3106}
    need(owned_events and owned_events<={d['event']for _,d in events}and
         pre['event']<min(owned_events)<=max(owned_events)<latch['event'],
         'Actual complete Kano source3106 FIFO/DMA is between true BEFORE-DMA anchor and displayed3107 flip')
    # Both alternating display pages are observed; do not silently use a mask
    # from a different native page as a mandatory overwrite condition.
    Driver=original.tracked(context,set(semantics['lastKanoSources']))
    replay=Driver(folder,groups,context['buffers'],context['owners'])
    samples=[];previous_mask=None
    for frame in (3106,3107,3108,3109):
        for kind,d in original.faults.serialized.body.original.window(context,frame):
            if kind!='FLOOR_FLIP':replay.apply(kind,d)
            else:flip=d
        actual=display['buffers'][context['latches'][frame]['file']]
        need(replay.words.tobytes()==actual, 'Every probe keeps the whole original512x512 native pass positive')
        snap=context['snaps'][frame];field=context['displays'][frame]
        proof=context['renderer'].__globals__['check_latch'](display['rgb'][snap['file']],actual,
            display['buffers'][field['palette_file']],flip['value'],flip['control'],flip['tap'])
        row,column=proof['row'],proof['column'];crop=lambda a:a[row:row+254,column:column+400]
        mask=(crop(replay.words.labels)==1)|(crop(replay.words.labels)==3)
        samples.append(dict(frame=frame,frontRow=row,frontColumn=column,displayStart=flip['value'],
            actualNewKanoPixels=int(mask.sum()),previousScreenMaskPixels=int(previous_mask.sum())if previous_mask is not None else None,
            observedLowPenWritesOnPreviousScreenMask=int(crop(replay.words.written)[previous_mask].sum())if previous_mask is not None else None))
        if frame==3107:previous_mask=mask.copy()
    # Native CPU/DMA commands outside the saved display pass are independently
    # replayed from a prior observed flip, never seeded from the tested anchor.
    intervals=[]
    Base=context['renderer'].__globals__['Replay']
    helper=original.faults.serialized.body.original
    for frame in (3106,3107,3108):
        before=context['latches'][frame];after=context['pre'][frame]
        need(before['event']<after['event'], 'Actual previous displayed flip precedes next BEFORE-DMA anchor')
        seed=display['buffers'][before['file']];target=display['buffers'][after['file']]
        gap=Base(folder,groups,context['buffers'],context['owners'])
        gap.begin(before['epoch']);gap.words=np.frombuffer(seed,dtype='<u2').copy().reshape(512,512)
        gap.last_event=before['event'];count=0;prewrite_error=None
        for kind,d in context['events']:
            if not before['event']<d['event']<after['event']:continue
            need(kind in ('FLOOR_CPU','FLOOR_DMA'), 'Only actual native writes, no arbitrary source re-anchor inside interval')
            count+=1
            try:gap.apply(kind,d)
            except AssertionError as error:prewrite_error=str(error);break
        actual=np.frombuffer(target,dtype='<u2').reshape(512,512)
        different=np.argwhere(gap.words!=actual)
        intervals.append(dict(displayFrame=frame,priorFlipEvent=before['event'],nextPrepassEvent=after['event'],
            observedWriteCommands=count,nativePrewriteAssertionError=prewrite_error,
            unexplainedWholeVRAMWords=len(different),firstDifference=({
                'row':int(different[0,0]),'column':int(different[0,1]),
                'model':int(gap.words[tuple(different[0])]),'actual':int(actual[tuple(different[0])])}if len(different)else None)))
    video_source=ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/mame/midway/midtunit_v.cpp'
    code=video_source.read_text()
    need('TMS340X0_FROM_SHIFTREG_CB_MEMBER(midtunit_video_device::from_shiftreg)'in code and
         'memcpy(&m_local_videoram[address >> 3], shiftreg, 2 * 512 * sizeof(uint16_t));'in code,
         'Actual compiled device has a complete2048-byte native shift-register VRAM path outside program-space write taps')
    faults_rejected=[]
    def reject(label,changed):
        try:original.ownership(changed,state)
        except (ValueError,AssertionError)as error:faults_rejected.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual effective source-lifetime counterexample accepted: '+label)
    index=next(i for i,q in enumerate(groups['FLOOR_QUEUE'])if q['frame']==3106 and q['slot']==1)
    for key in ('actor','main','owner','id','source','bank'):
        queues=list(groups['FLOOR_QUEUE']);q=dict(queues[index]);q[key]^=1;queues[index]=q
        reject('actual_last_physical_Kano_'+key,dict(groups,FLOOR_QUEUE=queues))
    last=next(q for q in groups['FLOOR_ALL_QUEUE']if q['frame']==3106 and q['actor']==0x01034e90)
    for label,actor in (('resurrected_hidden_physical_body',0x01034e90),('fabricated_detached_imported_corpse',0x01031d10)):
        ghost=dict(last,frame=3107,actor=actor)
        reject(label,dict(groups,FLOOR_ALL_QUEUE=list(groups['FLOOR_ALL_QUEUE'])+[ghost]))
    need(original.ownership(groups,state)==semantics,'Entire actual late source ownership positive restored after eight faults')
    for p in (Path(__file__),Path(original.__file__),FAILURE,parent_path,video_source):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed source or actual erase rejection edited');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()), 'Whole source/native input inventory intact')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualLatePhysicalSourceFIFOAndDMA=semantics,actualHideBoundaryPasses=samples,actualFlipToPrepassIntervals=intervals,
        lastPhysicalKanoVisibleSnapshot=3107,lastPhysicalKanoPublicationField=3106,
        noPostHideKanoBodyOrShadowSourceCopies=True,noDetachedImportedCorpseObserved=True,
        previousSeparateCorpseInterpretationCorrected=True,effectiveLateSourceFaultsRejected=faults_rejected,
        finiteActualLatePhysicalSourceLifetimeAccepted=True,failedFullPenOverwriteCheckPreserved=True,
        completeNativeInterPassErasureAccepted=False,unobservedShiftRegisterTransferCaptureRequired=True,
        measuredGapProvedToBeShiftRegister=False,stockBloodTaskOwnershipIndividuallyAccepted=False,
        allFinisherEffectsOwnershipAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS actual late FIFO/DMA ownership; exact erase observation gaps reported, not waived',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual late-source and interval-diagnosis rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
