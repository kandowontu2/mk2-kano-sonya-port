"""All actual blood Main fields, full companion FIFO/DMA/audio, effective faults.

No new native game. Keep whole original descriptor/projection/pool/drawing
contract and source-derived168-slot partition. Strengthen ownership to every
observed Main field in each blood lifetime, not only matching owner rows.
"""
import hashlib
import json
import traceback
from pathlib import Path
import qualify_native_selector_sonya_pressure_blood_slots as previous
import qualify_native_selector_sonya_pressure_renderer_faults_bound as companion

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_blood_bound_checked'


def gate(groups,guest):
    result=previous.gate(groups,guest)
    observed=0
    for e in result['actualBloodAllocationEpochs']:
        actual=[t for t in groups['TASK']if t['main']==e['main']and
                e['bornSequence']<t['sequence']<e['retiredSequence']]
        need(len(actual)==e['taskFields']and all(t['owner']==e['actor']for t in actual),
             'Every actual blood Main field retains exact allocated actor through its whole lifetime')
        observed+=len(actual)
    result['everyActualBloodMainOwnerField']=observed
    return result


def companions(groups,capture):
    original=companion.scope['CONTEXT']['groups']
    begin=groups['BEGIN'][0]['frame']
    oldq=[q for q in original['FLOOR_ALL_QUEUE']if q['frame']>=begin]
    newq=groups['QUEUE']
    fields=('frame','actor','cursor','source','cache','pose','id','body','facing','pc')
    need(len(oldq)==len(newq)and all(all(a[k]==b[k]for k in fields)and
         a['bank']&0x7f00==b['bank']for a,b in zip(oldq,newq)),
         'Every original actual companion FIFO and new native publication tuple identical')
    oldd=[d for d in original['FLOOR_DMA']if d['frame']>=begin]
    newd=groups['DMA']
    fields=('frame','source','command','x','y','width','height','scaleX','scaleY','left','right','top','bottom','skip','pc')
    registers={r['event']:r for r in original['FLOOR_DMA_REGS']}
    need(len(oldd)==len(newd)and all(all(a[k]==b[k]for k in fields)and
         a['palette']==b['bank']and registers[a['event']]['b14']+192==b['cursor']
         for a,b in zip(oldd,newd)),
         'Every whole actual companion DMA operation/cursor identical, including scenery/effects/shadows')
    old=capture.reference.AUDIO[capture.reference.KEY];new=capture.AUDIO[capture.KEY]
    for kind in ('pcmChunks','dacChunks','pcmHeaders','dacHeaders'):
        need(new[kind]==old[kind],'Entire original and new actual sound bytes/headers identical: '+kind)
    need(new['rom']==old['rom'],'Both complete actual sound-ROM endpoints identical')
    return dict(actualCompanionNative=47004,newActualNative=45272,
        wholeNativeFIFOComparisons=len(newq),wholeNativeDMAComparisons=len(newd),
        entireActualPCMandDACCallbacks=len(new['pcmChunks']),
        entirePCMBytes=sum(map(len,new['pcmChunks'])),
        actualWholePCM_SHA256=hashlib.sha256(b''.join(new['pcmChunks'])).hexdigest().upper(),
        currentNewVRAMPixelsIndependentlyCaptured=False,
        earlierActualSnapshotAndSourceAudioEvidenceRemainsSeparate=True)


def execute(state):
    need(not OUT.exists(),'Fresh actual blood effective fault and companion binding evidence')
    original=previous.original;capture=original.capture
    parent_path=previous.OUT/'report.json';proof=json.loads(parent_path.read_text())
    handle=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed']and handle['process'].poll()==0 and handle['identity']==proof['actualNativeIdentity'],
         'Same actual45272 terminal handle, never replay for faults')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All whole actual source/native pins intact')
    groups=previous.SCOPE['CONTEXT'];guest=state['guest']
    result=gate(groups,guest);binding=companions(groups,capture)
    faults=[]
    def reject(label,changed,source=guest):
        try:gate(changed,source)
        except (ValueError,AssertionError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective actual blood counterexample accepted: '+label)
    index=next(i for i,q in enumerate(groups['QUEUE'])if q['palette_source']==0xffaf2a40)
    q=groups['QUEUE'][index]
    for key,value in (('actor',q['actor']^0x210),('cache',q['cache']^16),
                      ('source',q['source']^1),('size',q['size']^1),
                      ('command',q['command']^0x10000),('xy',q['xy']^1),
                      ('palette_source',q['palette_source']^16),('refs',q['refs']^1),
                      ('pose',1),('id',17),('body',q['body']^2),('bank',q['bank']^256)):
        values=list(groups['QUEUE']);values[index]=dict(q,**{key:value})
        reject('actual_blood_publication_'+key,dict(groups,QUEUE=values))
    e=result['actualBloodAllocationEpochs'][0]
    ti=next(i for i,t in enumerate(groups['TASK'])if t['main']==e['main']and
            e['bornSequence']<t['sequence']<e['retiredSequence'])
    for key,value in (('owner',e['actor']^0x210),('main',e['main']^16),('next',groups['TASK'][ti]['next']^16)):
        tasks=list(groups['TASK']);tasks[ti]=dict(tasks[ti],**{key:value})
        reject('actual_blood_Main_'+key,dict(groups,TASK=tasks))
    heads=list(groups['HEAD']);hi=next(i for i,h in enumerate(heads)if h['sequence']==e['bornSequence']-1)
    heads[hi]=dict(heads[hi],value=heads[hi]['value']^1)
    reject('actual_native_pop_halfword',dict(groups,HEAD=heads))
    heads=list(groups['HEAD']);hi=next(i for i,h in enumerate(heads)if h['sequence']==e['retiredSequence'])
    heads[hi]=dict(heads[hi],target=heads[hi]['target']^0x210)
    reject('actual_native_return_object',dict(groups,HEAD=heads))
    di=next(i for i,d in enumerate(groups['DMA'])if d['sequence']>q['sequence']and
            d['cursor']==q['cursor']and d['source']==q['source']and d['command']&15==2)
    draws=list(groups['DMA']);draws[di]=dict(draws[di],x=draws[di]['x']^1)
    reject('actual_native_blood_DMA_x',dict(groups,DMA=draws))
    lists=list(groups['LISTS']);lists[0]=dict(lists[0],mainFree=lists[0]['mainFree'][:-1])
    reject('missing_native_free_Main',dict(groups,LISTS=lists))
    ghost=dict(q,frame=e['retiredFrame'],sequence=e['retiredSequence']+1,cursor=q['cursor']^16)
    reject('republished_retired_stock_blood',dict(groups,QUEUE=groups['QUEUE']+[ghost]))
    for label,at in (('stock_blood_descriptor',q['cache']),('native_pool_pop_instruction',0xff809120)):
        bad=bytearray(guest);bad[(at-0xff800000)//8]^=1
        reject(label,groups,bad)
    need(len(faults)==22,'All22 effective actual source/ownership/lifecycle/drawing counterexamples rejected')
    need(gate(groups,guest)==result and companions(groups,capture)==binding,
         'Entire original blood source/ownership and every companion operation/byte restored')
    for p in (Path(__file__),Path(previous.__file__),parent_path,
              companion.OUT/'report.json',capture.snapshot.OUT/'failure.json',
              ROOT/'audit_native_selector_sonya_pressure_stock_clear_sealed.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed predecessor or actual failure edited');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Whole source/current native evidence inventory intact')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        actualEffectCallbacks=proof['actualEffectCallbacks'],stockBlood=result,
        fullActualCompanionBinding=binding,effectiveBloodFaultsRejected=faults,
        finiteStockBloodPoolAndTaskOwnershipAccepted=True,bloodFaultSuiteAccepted=True,
        allFinisherEffectsOwnershipAccepted=False,individualBloodAudioProducerAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS actual whole blood Main/pool/descriptor/drawing and22 faults; companion native tuples/audio exact',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual effective blood-fault rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
