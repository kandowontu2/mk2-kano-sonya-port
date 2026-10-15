"""All actual stock blood reference owners, including unpublished objects.

Use native interleaved log order, exact pool epochs, acquisition registers,
bank assignments, Main owner snapshots and native releases. Never equate
palette references to visible sprites or infer unobserved owners from colors.
"""
import bisect
import collections
import gzip
import json
import re
import subprocess
import traceback
from pathlib import Path
import qualify_native_selector_sonya_pressure_palette_router as arithmetic
import qualify_native_selector_sonya_pressure_blood_slots as stock

ROOT,need,sha=arithmetic.ROOT,arithmetic.need,arithmetic.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_blood_all_owners_checked'
CONTEXT=None


def source_gate(guest):
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=0xff83b2c0,0xff83b3f0
    a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
    need(guest[a:z]==original[a:z], 'Whole original palette construction/actual A8 bank assignment unchanged')
    result=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(ROOT/'mk2/mk2-maincpu.bin'),
        '-arch','tms34010','-basepc',hex(lo),'-skip',str(a),'-count',str(hi-lo),'-norawbytes'],
        capture_output=True,text=True,check=True)
    asm={int(line.split(':',1)[0],16):line.split(':',1)[1].strip().upper() for line in result.stdout.splitlines()}
    need(asm[0xff83b2c0]=='MOVE   A0,A8' and asm[0xff83b2f0]=='CALLA  FF80CF60H' and
         asm[0xff83b320]=='MOVE   A0,*A8(140H),0', 'Source-defined actual palette owner is acquired object A8')
    return lo,hi,original


def ordered_record(events):
    capture=arithmetic.previous.binding.capture
    folder=capture.RAM_CASES[capture.KEY][0]
    pal={r['sequence']:r for r in events if r['tag'].startswith('MK2_PAL_')}
    queues=iter(r for r in events if r['tag']=='MK2_EFFECT_QUEUE')
    original_heads=iter(stock.SCOPE['CONTEXT']['HEAD'])
    result=[];queue_count=0;head_count=0
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as stream:
        for ordinal,line in enumerate(stream):
            if line.startswith('MK2_EFFECT_HEAD '):
                row=dict(re.findall(r'(\w+)=([^\s]+)',line))
                decoded={k:(v if k=='assistance' else int(v,16 if k in stock.original.HEX else 10)) for k,v in row.items()}
                need(decoded==next(original_heads), 'Every native pool halfword/context identical to source-qualified companion')
                result.append((ordinal,'HEAD',decoded));head_count+=1
            elif line.startswith('MK2_PAL_'):
                row=dict(re.findall(r'(\w+)=([^\s]+)',line));r=pal[int(row['sequence'])]
                result.append((ordinal,r['tag'],r))
            elif line.startswith('MK2_EFFECT_QUEUE '):
                row=dict(re.findall(r'(\w+)=([^\s]+)',line));r=next(queues)
                need(int(row['sequence'])==r['sequence'], 'Every FIFO remains in actual native callback order')
                result.append((ordinal,r['tag'],r));queue_count+=1
    need(next(original_heads,None) is None and next(queues,None) is None and
         head_count==4418 and queue_count==112426, 'No whole pool/FIFO callbacks omitted')
    return result


def gate(ordered,guest):
    source_gate(guest)
    heads=[r for _,tag,r in ordered if tag=='HEAD']
    stock.original.pools(dict(HEAD=heads))
    pop={};alive={};complete=[];pending=None;blood_queues=0
    task_rows=stock.SCOPE['CONTEXT']['TASK']
    # Main snapshots are byte/event-identical in this actual capture binding.
    task_by_main=collections.defaultdict(list)
    for t in task_rows:task_by_main[t['main']].append(t)
    source=0xffaf2a40
    for ordinal,tag,r in ordered:
        if tag=='HEAD' and r['head']==0x01060130:
            if r['pc']==0xff809150 and r['at']==0x01060140:
                pop[r['target']]=(ordinal,r)
            elif r['pc']==0xff8097d0 and r['at']==0x01060130:
                need(r['target'] not in alive, 'Every actual stock blood reference released before object returns to free pool')
                pop.pop(r['target'],None)
        elif tag=='MK2_PAL_WRITE' and r['offset']==32 and r['source']==source:
            actor=r['actor'];main=r['main']
            if r['pc']==0xff80d550:
                need(pending is None and actor in pop and actor not in alive,
                     'One actual new stock blood reference within its unique native object epoch')
                born,b=pop[actor]
                need(born<ordinal and b['main']==main and r['after']==len(alive)+1,
                     'Actual acquisition Main and whole reference count equal all owned live blood epochs')
                record=dict(actor=actor,main=main,bank=r['index']|(r['index']<<8),
                    bornFrame=b['frame'],bornNativeSequence=b['sequence'],acquireFrame=r['frame'],
                    acquirePaletteSequence=r['sequence'],acquireOrdinal=ordinal,
                    nativeBankAssigned=False,draws=0)
                alive[actor]=record;pending=record
            elif r['pc']==0xff80d710:
                need(actor in alive and pending is None and alive[actor]['main']==main and
                     r['refs']==len(alive) and r['after']==len(alive)-1,
                     'Actual owning blood actor/Main releases exactly its outstanding native reference')
                record=alive.pop(actor)
                need(record['nativeBankAssigned'], 'Actual stock blood bank assignment observed before release')
                record.update(releaseFrame=r['frame'],releasePaletteSequence=r['sequence'],releaseOrdinal=ordinal)
                actual=[t for t in task_by_main[main] if record['acquireFrame']<=t['frame']<r['frame']]
                need(actual and all(t['owner']==actor for t in actual),
                     'Every actual live Main owner field belongs to this visible or unpublished blood object')
                record['actualMainOwnerSnapshots']=len(actual);complete.append(record)
            elif r['pc'] in (0xff80cd90,0xff814e90):
                need(not alive, 'No outstanding stock blood owner discarded by native cache reset')
            else:raise ValueError('Unexpected actual stock blood reference operation')
        elif tag=='MK2_PAL_OWNER' and pending is not None:
            need(r['pc']==0xff83b340 and r['actor']==pending['actor'] and r['main']==pending['main'] and
                 r['after']==pending['bank'] and r['before']==0 and r['mask']==65535,
                 'Exact source-defined native blood bank assigned to acquired actor, including invisible owner')
            pending['nativeBankAssigned']=True;pending=None
        elif tag=='MK2_EFFECT_QUEUE' and r['palette_source']==source:
            need(r['actor'] in alive and alive[r['actor']]['nativeBankAssigned'] and
                 r['bank']==alive[r['actor']]['bank']&0x7f00 and r['refs']==len(alive),
                 'Every blood publication count equals all actual owners, not just visible bodies')
            alive[r['actor']]['draws']+=1;blood_queues+=1
    need(not alive and pending is None and len(complete)==32 and blood_queues==1089,
         'All32 actual stock blood references assigned and released; no owner leaks or orphan drawing')
    drawn=[e for e in complete if e['draws']];unpublished=[e for e in complete if not e['draws']]
    need(len(drawn)==17 and len(unpublished)==15 and sum(e['draws'] for e in complete)==1089,
         'Actual seventeen published plus fifteen unpublished blood epochs explain the complete cache counts')
    return dict(actualStockBloodOwnerEpochs=32,publishedOwnerEpochs=17,unpublishedOwnerEpochs=15,
        nativeBloodPublications=1089,allReferenceAcquiresReleased=True,
        everyNativeBloodCountExplainedByActualOwnerEpochs=True,actualOwnerEpochs=complete,
        allOtherHiddenPaletteOwnersAccepted=False,allFinisherEffectsAccepted=False)


def execute(state,events):
    global CONTEXT
    need(not OUT.exists(), 'Fresh immutable whole actual blood-owner evidence')
    capture=arithmetic.previous.binding.capture;handle=capture.NATIVE_HANDLES[capture.KEY]
    proof=json.loads((arithmetic.OUT/'report.json').read_text())
    need(proof['passed'] and handle['process'].poll()==0 and handle['identity']==proof['actualNativeIdentity'],
         'Same actual35924 terminal handle and complete arithmetic acceptance')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'Whole current source/native pins intact')
    CONTEXT=ordered_record(events);result=gate(CONTEXT,state['guest']);faults=[]
    def reject(label,changed):
        try:gate(changed,state['guest'])
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective stock blood owner fault accepted: '+label)
    ai=next(i for i,(_,tag,r) in enumerate(CONTEXT) if tag=='MK2_PAL_WRITE' and
            r['offset']==32 and r['source']==0xffaf2a40 and r['pc']==0xff80d550)
    for key in ('actor','main','after','index'):
        changed=list(CONTEXT);at,tag,row=changed[ai];changed[ai]=(at,tag,dict(row,**{key:row[key]^1}))
        reject('actual_blood_acquire_'+key,changed)
    oi=next(i for i,(_,tag,r) in enumerate(CONTEXT) if tag=='MK2_PAL_OWNER' and r['sequence']==CONTEXT[ai][2]['sequence']+1)
    for key in ('actor','main','after','pc'):
        changed=list(CONTEXT);at,tag,row=changed[oi];changed[oi]=(at,tag,dict(row,**{key:row[key]^1}))
        reject('actual_blood_owner_bank_'+key,changed)
    ri=next(i for i,(_,tag,r) in enumerate(CONTEXT) if tag=='MK2_PAL_WRITE' and
            r['offset']==32 and r['source']==0xffaf2a40 and r['pc']==0xff80d710)
    for key in ('actor','main','refs','after'):
        changed=list(CONTEXT);at,tag,row=changed[ri];changed[ri]=(at,tag,dict(row,**{key:row[key]^1}))
        reject('actual_blood_release_'+key,changed)
    changed=list(CONTEXT);del changed[oi];reject('missing_actual_owner_bank',changed)
    changed=list(CONTEXT);del changed[ri];reject('missing_actual_blood_release',changed)
    need(len(faults)==14 and gate(CONTEXT,state['guest'])==result,
         'All14 effective owner faults reject and entire actual positive restored')
    for p in (Path(__file__),arithmetic.OUT/'report.json',stock.OUT/'report.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h, 'No whole earlier evidence rewritten');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()), 'Whole current source/native inventory unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        stockBlood=result,effectiveFaultsRejected=faults,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        allStockBloodReferenceOwnersAccepted=True,allHiddenPaletteOwnersAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,
        newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');return value


def safe_execute(state,events):
    try:return execute(state,events)
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual stock blood owner failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
