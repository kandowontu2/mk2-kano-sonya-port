"""Whole actual stock blood FIFO, source projection and pool/task lifetimes.

Classify from native palette allocator pointers, never color rectangles.
Bind every such publication to original descriptors, actual pool pop/return,
owning Main snapshots and FIFO-to-DMA dispatch. No full effects/port claim.
"""
import bisect
import json
import re
import struct
import traceback
from collections import defaultdict
from pathlib import Path
import capture_native_selector_sonya_pressure_effects as capture
import inspect_native_smoke_callers as disasm

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_blood_checked'
HEX=set('head at before value mask merged target targetNext a2 actor main pc returnPC type owner resume cursor source cache pose body facing bank palette_source size xy command world camera display activeStop freeStop mainStop mainFreeStop next attached parent action p1 p2'.split())
LISTS={'active','free','mains','mainFree'}
CONTEXT=None


def parse(text):
    groups=defaultdict(list);ordered=[]
    for line in text.splitlines():
        if not line.startswith('MK2_EFFECT_'):continue
        tag=line.split(' ',1)[0][11:]
        pairs=re.findall(r'(\w+)=([^\s]+)',line);r=dict(pairs)
        need(len(r)==len(pairs),'Unique complete native effect metadata fields')
        need(r['writes']=='0'and r['assistance']=='none','Passive actual effect observation')
        for key,value in list(r.items()):
            if key=='assistance':continue
            if key in LISTS:r[key]=[]if value=='-'else[int(a,16)for a in value.split(',')]
            else:r[key]=int(value,16 if key in HEX else 10)
        groups[tag].append(r);ordered.append((tag,r))
    need([r['sequence']for _,r in ordered]==list(range(1,len(ordered)+1)),
         'Every actual effect callback in complete contiguous native order')
    return groups,ordered


def source_gate(guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff8090c0,0xff809280),(0xff8096c0,0xff809800),
                  (0xff804000,0xff804430),(0xff80dcc0,0xff80e440),
                  (0xffaf2a40,0xffaf2b40)):
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:z]==stock[a:z],'Whole original native pool/scheduler/projection/blood palette source')
    asm={int(s.split(':',1)[0],16):s.split(':',1)[1].strip().upper()for s in disasm.disassemble()}
    expected={0xff809120:'MOVE   A2,@1060130H,1',0xff8097a0:'MOVE   A0,@1060130H,1',
        0xff80df60:'MOVI   A8H,A3',0xff80dff0:'MOVE   A1,@1068E50H,1',
        0xff80e030:'ADDI   6F0H,A1',0xff80e050:'MOVE   A1,*A2,1',
        0xff80e060:'DSJS   A3,FF80E020H',0xff80e070:'MOVE   A0,*A2,1',
        0xff80dce0:'ADDI   100H,A1',0xff80dd00:'MMTM   A1,A7-A12',
        0xff80e3d0:'MMTM   A2,A7-A12'}
    need(all(asm.get(a)==v for a,v in expected.items()),'Exact original pool operands and169-slot scheduler construction')
    return stock,expected


def pools(groups):
    object_heads=[r for r in groups['HEAD']if r['head']==0x01060130 and r['pc']in(0xff809150,0xff8097d0)]
    births=defaultdict(list);returns=defaultdict(list)
    need(len(object_heads)%2==0,'Every original pool operation includes both halfwords')
    for a,b in zip(object_heads[::2],object_heads[1::2]):
        need(a['at']==0x01060130 and b['at']==0x01060140 and
             b['sequence']==a['sequence']+1 and b['before']==a['merged'] and
             all(a[k]==b[k]for k in('target','targetNext','a2','actor','main','pc','type','owner','resume')),
             'Whole actual low/high native pool operation and context continuity')
        for r in (a,b):
            shift=r['at']-r['head']
            need(r['mask']==65535 and r['merged']==
                 ((r['before']&~(r['mask']<<shift))|((r['value']&r['mask'])<<shift))&0xffffffff,
                 'Exact masked native pool store arithmetic')
        if a['pc']==0xff809150:
            need(a['before']==a['target']and b['merged']==a['targetNext']==a['a2'],
                 'Source-defined native pop removes exact object from free head')
            births[a['target']].append(b)
        else:
            need(b['merged']==a['target']and a['targetNext']==a['before']==a['a2'],
                 'Source-defined native return inserts exact object before prior free head')
            returns[a['target']].append(a)
    return births,returns


def task_lists(groups):
    snapshots=groups['LISTS'];tasks=defaultdict(list)
    for t in groups['TASK']:tasks[t['frame']].append(t)
    need([r['frame']for r in snapshots]==list(range(1818,3618)),
         'All1800 actual live/KO/reset/held/continue task-list snapshots')
    expected={0x01068ea0+i*0x6f0 for i in range(169)}
    for r in snapshots:
        need(all(r[k]==1 for k in ('activeOK','freeOK','mainOK','mainFreeOK')),
             'Every original object/process list traverses without invalid pointers or cycles')
        active,free=r['mains'],r['mainFree']
        need(len(set(active))==len(active)and len(set(free))==len(free)and
             not(set(active)&set(free))and set(active)|set(free)==expected and
             r['mainStop']==r['mainFreeStop']==0,
             'Entire source-defined169 Main records partition into native active/free lists')
        actual=tasks[r['frame']]
        need([t['main']for t in actual]==active and
             [t['next']for t in actual]==active[1:]+([0]if active else[]),
             'Every independently recorded active Main next link matches full native list')
    return tasks


def signed(n):return (n&65535)-65536 if n&32768 else n&65535


def gate(groups,guest):
    stock,instructions=source_gate(guest)
    births,returns=pools(groups);task_lists(groups)
    queues=groups['QUEUE'];keys={(q['frame'],q['cursor']):q for q in queues}
    need(len(keys)==len(queues),'Every entire native FIFO publication unique')
    # All queue reads of a bank in one native publication pass observe the
    # same allocator record. A changed source pointer cannot silently exclude
    # one publication from the original stock-blood classification.
    palette={}
    for q in queues:
        key=q['frame'],q['bank'];v=q['palette_source'],q['refs']
        need(key not in palette or palette[key]==v,'All independent same-pass native palette allocator reads agree')
        palette[key]=v
    blood=[q for q in queues if q['palette_source']==0xffaf2a40]
    need(blood,'Actual native stock blood observed from allocator source, not pixel color')
    by_owner=defaultdict(list)
    for t in groups['TASK']:by_owner[t['owner']].append(t)
    epochs={};sources=set()
    for q in blood:
        need(q['id']==0 and not(q['body']&2)and q['refs']>0 and q['pose']==0,
             'Original allocated single-sprite stock blood, no imported fighter/corpse alias')
        at=(q['cache']-0xff800000)//8
        need(0<=at<=len(stock)-14 and guest[at:at+14]==stock[at:at+14],
             'Every whole original stock blood descriptor unchanged')
        w,h,dx,dy,source,format_word=struct.unpack_from('<4hIH',stock,at)
        cmd=q['command']>>16
        need(w>0 and h>0 and q['size']==w|(h<<16)and q['source']==source and
             cmd==q['facing']and cmd&15==2 and cmd&0x7000==format_word&0x7000,
             'Entire native stock descriptor dimensions/source/pixel command')
        x,y=signed(q['world']),signed(q['world']>>16)
        if not(q['body']&1):x-=signed(q['camera']);y-=signed(q['camera']>>16)
        if cmd&16:x+=w-1
        if cmd&32:y+=h-1
        x+=signed(q['display']);y+=signed(q['display']>>16)
        need(q['xy']==(x&65535)|((y&65535)<<16),
             'Unchanged single-sprite world/camera/flip/display projection, no multipart displacement')
        candidates=births[q['actor']];index=bisect.bisect_left([b['sequence']for b in candidates],q['sequence'])-1
        need(index>=0,'Every blood publication has actual preceding native pool allocation')
        birth=candidates[index]
        stop=next((r for r in returns[q['actor']]if r['sequence']>birth['sequence']),None)
        need(stop is not None and birth['sequence']<q['sequence']<stop['sequence'],
             'Every blood publication occurs before its actual pool return, even within same field')
        key=q['actor'],birth['sequence']
        if key not in epochs:
            own=[t for t in by_owner[q['actor']]if birth['sequence']<t['sequence']<stop['sequence']]
            need(own and all(t['main']==birth['main']for t in own)and
                 stop['actor']==stop['owner']==q['actor']and stop['main']==birth['main'],
                 'Actual allocated blood owns the original native Main and returns under that Main')
            epochs[key]=dict(actor=q['actor'],main=birth['main'],birth=birth,retirement=stop,
                taskFields=len(own),publications=[],descriptors=set())
        epochs[key]['publications'].append(q)
        epochs[key]['descriptors'].add(q['cache']);sources.add(q['source'])
    by_cursor=defaultdict(list)
    for q in queues:by_cursor[q['cursor']].append(q)
    qseq={q['sequence']:q for q in blood};draws=[]
    for d in groups['DMA']:
        candidates=by_cursor[d['cursor']]
        index=bisect.bisect_left([q['sequence']for q in candidates],d['sequence'])-1
        if index<0:continue
        q=candidates[index]
        if q['sequence']not in qseq or q['source']!=d['source']or d['command']&15!=2:continue
        need((d['bank'],d['command'],d['width'],d['height'],d['x'],d['y'])==
             (q['bank'],q['command']>>16,q['size']&65535,q['size']>>16,q['xy']&1023,q['xy']>>16&511),
             'Every actual stock blood FIFO tuple reaches native DMA unchanged')
        draws.append(dict(frame=d['frame'],queueSequence=q['sequence'],dmaSequence=d['sequence'],actor=q['actor']))
    need({r['queueSequence']for r in draws}==set(qseq),
         'Every stock blood publication actually consumed by native drawing')
    records=[]
    for (actor,start),e in epochs.items():
        stop=e['retirement'];next_pop=next((b['sequence']for b in births[actor]if b['sequence']>start),float('inf'))
        need(all(not(stop['sequence']<q['sequence']<next_pop and q['actor']==actor and q['cache']in e['descriptors'])for q in queues),
             'No retired stock blood artwork republished before actual address reuse')
        records.append(dict(actor=actor,main=e['main'],bornFrame=e['birth']['frame'],bornSequence=start,
            retiredFrame=stop['frame'],retiredSequence=stop['sequence'],taskFields=e['taskFields'],
            publicationFields=[q['frame']for q in e['publications']],descriptors=sorted(e['descriptors'])))
    return dict(nativeBloodPublications=len(blood),actualNativeBloodDraws=len(draws),
        actualBloodAllocationEpochs=records,sourceBoundStockBloodGraphics=sorted(sources),
        nativeTaskSnapshots=1800,wholeMainSlotsPerSnapshot=169,
        stockSourceInstructions={f'{a:08X}':v for a,v in instructions.items()})


def execute(state):
    global CONTEXT
    need(not OUT.exists(),'Fresh actual whole stock blood source/lifetime evidence')
    parent_path=capture.OUT/'report.json';proof=json.loads(parent_path.read_text())
    handle=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed']and handle['process'].poll()==0 and proof['actualNativeIdentity']==handle['identity'],
         'Same actual45272 terminal handle, no replay for blood qualification')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every whole current source/native pin intact')
    text=capture.RAM_CASES[capture.KEY][1];groups,ordered=parse(text);CONTEXT=groups
    result=gate(groups,state['guest'])
    for p in (Path(__file__),Path(disasm.__file__),ROOT/'mame-mkp/unidasm.exe',ROOT/'mk2/mk2-maincpu.bin',parent_path):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed source or previous evidence changed');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All whole source/native evidence pins intact')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        actualEffectCallbacks=len(ordered),stockBlood=result,finiteStockBloodPoolAndTaskOwnershipAccepted=True,
        bloodFaultSuiteAccepted=False,fullEffectRasterAndAudioAccepted=False,allFinisherEffectsOwnershipAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS actual whole stock blood source/projection/pool/Main lifetime',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual whole native blood rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
