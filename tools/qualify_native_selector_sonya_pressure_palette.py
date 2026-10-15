"""Whole observed native palette-cache arithmetic, not visible-owner counting.

Source-derived resets, allocation pointer stores, reference increments/releases
and free timestamps predict every cache word and every frame snapshot. Bind
all112426 live FIFO palette inputs in original callback order. Owner assignments
are inventoried but do not claim every possible hidden owner is understood.
"""
import collections
import json
import subprocess
import traceback
from pathlib import Path
import bind_native_selector_sonya_pressure_palette as binding
import inspect_native_selector_sonya_pressure_palette as observed

ROOT,need,sha=binding.ROOT,binding.need,binding.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_palette_arithmetic_checked'
CONTEXT=None
SOURCE=None
BASE=0x0105bb30


def source_gate(guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    ranges=((0xff80cb50,0xff80dad0),(0xff814df0,0xff814eb0))
    for lo,hi in ranges:
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:z]==stock[a:z], 'Entire original native palette arithmetic/reset source unchanged')
    expected={
        0xff80cd70:'CLR    A1',0xff80cd80:'MOVE   A1,*A0+,0',
        0xff80d490:'MOVE   A0,*A1,1',0xff80d500:'MOVE   *A1(20H),A2,0',
        0xff80d520:'INC    A2',0xff80d530:'MOVE   A2,*A1(20H),0',
        0xff80d680:'MOVE   *A1(20H),A0,0',0xff80d6a0:'DEC    A0',
        0xff80d6b0:'JRNN   FF80D6F0H',0xff80d6f0:'MOVE   A0,*A1(20H),0',
        0xff80d720:'MOVE   @105D090H,A0,0',0xff80d750:'MOVE   A0,*A1(30H),0',
        0xff814e10:'CLR    A0',0xff814e80:'MOVE   A0,*A1+,1'}
    asm={}
    for lo,hi in ranges:
        result=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(ROOT/'mk2/mk2-maincpu.bin'),
            '-arch','tms34010','-basepc',hex(lo),'-skip',str((lo-0xff800000)//8),
            '-count',str(hi-lo),'-norawbytes'],capture_output=True,text=True,check=True)
        for line in result.stdout.splitlines():
            at,text=line.split(':',1);asm[int(at,16)]=text.strip().upper()
    need(all(asm.get(at)==text for at,text in expected.items()), 'Exact unchanged native cache operands independently disassembled')
    return dict(ranges=ranges,instructions={f'{at:08X}':text for at,text in expected.items()})


def gate(events,guest):
    need(SOURCE is not None, 'Independent unchanged source model initialized')
    for lo,hi in SOURCE['ranges']:
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:z]==SOURCE['stock'][a:z], 'Whole original palette source retained')
    state=None;expected_sequence=1;frames=[];stores=collections.Counter()
    increments=releases=reset_removed=queues=owner_stores=0
    blood_inputs=0;blood_counts=[];per_index=collections.defaultdict(collections.Counter)
    last_snapshot=None
    for r in events:
        tag=r['tag']
        if tag!='MK2_EFFECT_QUEUE':
            need(r['sequence']==expected_sequence, 'Every original palette callback contiguous and ordered')
            expected_sequence+=1
        if tag=='MK2_PAL_CACHE':
            need(len(r['entries'])==60 and all(len(t)==3 for t in r['entries']), 'Entire native sixty-slot cache snapshot')
            if r['phase']=='initial':
                need(state is None and r['sequence']==1 and r['frame']==0, 'Actual initial cache before all recorded writes')
                state=[list(t) for t in r['entries']]
                need(all(t==[0,0,0] for t in state), 'Actual cold cache starts with no outstanding palette references')
            else:
                need(state is not None and [tuple(t) for t in state]==r['entries'],
                     'Source-predicted whole cache equals every actual native snapshot')
                if r['phase']=='frame_done':frames.append(r['frame'])
                else:need(r['phase']=='terminal', 'Only actual terminal or frame snapshot')
            last_snapshot=r
        elif tag=='MK2_PAL_WRITE':
            need(state is not None, 'No cache store precedes actual cold baseline')
            i,off=r['index'],r['offset']
            need(0<=i<60 and off in (0,16,32,48) and r['at']==BASE+i*64+off and r['mask']==65535,
                 'Exact source-defined native cache index/address/full halfword mask')
            src,refs,stamp=state[i];word=(src&65535,src>>16,refs,stamp)[off//16]
            need(r['before']==word and r['source']==src and r['refs']==refs and r['stamp']==stamp,
                 'Whole actual pre-store cache fields match source-predicted history')
            pc=r['pc'];value=None;kind=None
            if pc==0xff814e90:
                need(r['a0']==0 and r['at'] in (r['a1'],r['a1']+16), 'Original boot clear register and two-halfword address')
                value=0;kind='boot_clear'
            elif pc==0xff80cd90:
                need(r['a0']==r['at'] and r['a1']==0, 'Original complete-cache reset operands')
                value=0;kind='cache_reset'
            elif pc==0xff80d4a0:
                need(off in (0,16) and r['a1']==BASE+i*64 and refs==0,
                     'Native allocation pointer only replaces an unused cache slot')
                value=(r['a0']>>off)&65535;kind='allocation_pointer'
            elif pc==0xff80d550:
                need(off==32 and r['a1']==BASE+i*64 and refs<65535 and
                     r['a0']==(i|(i<<8)) and r['a3']==i<<8 and r['a2']==refs+1,
                     'Native acquisition source operands and encoded bank derive exact increment')
                value=refs+1;kind='acquire';increments+=1;per_index[i]['acquires']+=1
            elif pc==0xff80d710:
                need(off==32 and r['a1']==BASE+i*64 and refs>0 and r['a0']==refs-1,
                     'Native release subtracts exactly one existing reference, no underflow')
                value=refs-1;kind='release';releases+=1;per_index[i]['releases']+=1
            elif pc==0xff80d770:
                need(off==48 and r['a1']==BASE+i*64 and refs==0 and r['a0']<=65535,
                     'Native zero-reference release records its actual timestamp operand')
                value=r['a0'];kind='free_timestamp'
            else:
                raise ValueError(f'Unmodeled actual native palette-cache store PC {pc:08X}')
            need(r['data']==value and r['after']==value,
                 'Source arithmetic predicts entire actual written palette word')
            if off in (0,16):
                state[i][0]=(src&~(65535<<off))|(value<<off)
            elif off==32:
                if kind in ('boot_clear','cache_reset'):
                    reset_removed+=refs;per_index[i]['resetRemoved']+=refs
                state[i][1]=value
            else:state[i][2]=value
            stores[kind]+=1
        elif tag=='MK2_EFFECT_QUEUE':
            i=(r['bank']&0x7f00)>>8
            need(state is not None and 0<=i<60 and
                 r['palette_source']==state[i][0] and r['refs']==state[i][1] and r['refs']>0,
                 'Every actual FIFO palette source/reference derives from whole recorded cache arithmetic')
            queues+=1
            if r['palette_source']==0xffaf2a40:
                blood_inputs+=1;blood_counts.append(r['refs'])
        elif tag=='MK2_PAL_OWNER':
            need(r['mask']==65535 and r['after']==r['data'], 'Whole native palette owner bank store')
            owner_stores+=1
        elif tag=='MK2_PAL_RESULT':
            need(r['terminalFrame']==r['frame']==3618, 'Actual terminal cache result callback')
        else:raise ValueError('Unexpected actual palette tag '+tag)
    need(frames==list(range(1,3619)) and last_snapshot['phase']=='terminal',
         'All3618 original startup/select/live/KO/reset/held/continue cache snapshots')
    need(queues==112426 and blood_inputs==1089, 'Every whole original FIFO and stock blood input checked')
    need(sum(t[1] for t in state)==increments-releases-reset_removed,
         'Whole native palette reference conservation including source-defined cache resets')
    return dict(nativeCacheStores=sum(stores.values()),sourceOperationCounts=dict(stores),
        referenceAcquires=increments,referenceReleases=releases,referencesDiscardedByNativeReset=reset_removed,
        terminalReferences=sum(t[1] for t in state),terminalCache=[tuple(t) for t in state],
        actualFrameCacheSnapshots=len(frames),allNativeFIFOInputs=queues,stockBloodInputs=blood_inputs,
        actualBloodReferenceRange=[min(blood_counts),max(blood_counts)],nativeOwnerBankStores=owner_stores,
        perNativeCacheSlot={str(i):dict(counts) for i,counts in sorted(per_index.items())},
        entireObservedCacheArithmeticAccepted=True,allHiddenPaletteOwnersIndividuallyAccepted=False,
        everyNativeAllocationSearchBranchAccepted=False,freeTimestampGlobalProducerIndividuallyAccepted=False)


def execute(state,events=None):
    global CONTEXT,SOURCE
    need(not OUT.exists(), 'Fresh immutable actual palette arithmetic proof')
    capture=binding.capture;handle=capture.NATIVE_HANDLES[capture.KEY]
    proof=json.loads((binding.OUT/'report.json').read_text())
    need(proof['passed'] and handle['process'].poll()==0 and handle['identity']==proof['actualNativeIdentity'],
         'Same terminal actual35924 game and accepted whole comparison')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'All whole earlier source/native pins intact')
    guest=state['guest'];source=source_gate(guest)
    SOURCE=dict(source,stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes())
    CONTEXT=observed.parse() if events is None else events
    result=gate(CONTEXT,guest);faults=[]
    def reject(label,changed,source_bytes=guest):
        try:gate(changed,source_bytes)
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective native palette counterexample accepted: '+label)
    wi=next(i for i,r in enumerate(CONTEXT) if r['tag']=='MK2_PAL_WRITE' and r['pc']==0xff80d550)
    row=CONTEXT[wi]
    for key in ('before','data','mask','after','source','refs','stamp','pc','a0','a1','a2','a3','index','offset','at'):
        changed=list(CONTEXT);changed[wi]=dict(row,**{key:row[key]^1})
        reject('native_acquire_'+key,changed)
    ri=next(i for i,r in enumerate(CONTEXT) if r['tag']=='MK2_PAL_WRITE' and r['pc']==0xff80d710)
    changed=list(CONTEXT);changed[ri]=dict(changed[ri],a0=changed[ri]['a0']^1)
    reject('native_release_operand',changed)
    ai=next(i for i,r in enumerate(CONTEXT) if r['tag']=='MK2_PAL_WRITE' and r['pc']==0xff80d4a0)
    changed=list(CONTEXT);changed[ai]=dict(changed[ai],a0=changed[ai]['a0']^1)
    reject('native_palette_source_operand',changed)
    si=next(i for i,r in enumerate(CONTEXT) if r['tag']=='MK2_PAL_CACHE' and r['phase']=='frame_done')
    entries=list(CONTEXT[si]['entries']);entries[0]=(entries[0][0]^1,*entries[0][1:])
    changed=list(CONTEXT);changed[si]=dict(changed[si],entries=entries)
    reject('native_whole_cache_snapshot',changed)
    qi=next(i for i,r in enumerate(CONTEXT) if r['tag']=='MK2_EFFECT_QUEUE' and r['palette_source']==0xffaf2a40)
    for key in ('refs','palette_source','bank'):
        changed=list(CONTEXT);changed[qi]=dict(changed[qi],**{key:changed[qi][key]^(256 if key=='bank' else 1)})
        reject('actual_blood_input_'+key,changed)
    changed=list(CONTEXT);del changed[wi]
    reject('missing_actual_palette_store',changed)
    bad=bytearray(guest);bad[(0xff80d520-0xff800000)//8]^=1
    reject('native_reference_increment_instruction',CONTEXT,bad)
    need(len(faults)==23 and gate(CONTEXT,guest)==result, 'All23 effective cache faults reject and entire original positive restored')
    for p in (Path(__file__),Path(observed.__file__),binding.OUT/'report.json',ROOT/'mame-mkp/unidasm.exe'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h, 'No original source or native record edited');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()), 'Whole source/current native evidence inventory unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        arithmetic=result,sourceOperands=source,effectiveFaultsRejected=faults,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        paletteReferenceArithmeticAccepted=True,allHiddenPaletteOwnersAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,
        newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    return value


def safe_execute(state,events=None):
    try:return execute(state,events)
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual native arithmetic rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
