"""Actual ungated source-executed Ring guard/branch/damage contexts.

Do not fabricate the absent legacy MK2_RING_PAIR schema or its control-port
sample. The independently recorded executing native entries/registers and
two health taps prove the actual chip/full-hit decisions. This is not the
whole older phase/startup/physical-port model, nor full-port acceptance.
"""
import inspect
import json
import re
import struct
import traceback
from pathlib import Path
import qualify_native_selector_cpu_rings_snapshot_mechanics as previous
import qualify_native_selector_cpu_rings_snapshot as renderer
import qualify_native_selector_cpu_rings_snapshot_transport as transport

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
capture,ring=previous.capture,previous.ring
OUT=ROOT/'audit_native_selector_cpu_rings_native_branches_checked'


def source_gate(text,guest):
    # Complete actually observed code inventory; no manufactured CODE records.
    actual=ring.original.original.rows(text,'CODE')
    expected={(0xff83ed80,0xff83f060),(0xff837d40,0xff837dc0),(0xff861350,0xff861700),
              (0xfffc3800,0xfffc5800),(0xfffc6000,0xfffc8000)}
    need(len(actual)==5 and {(r['start'],r['stop'])for r in actual}==expected,
         'All five original actually captured overlap source windows')
    for r in actual:
        lo,hi=((r[k]-0xff800000)//8 for k in ('start','stop'))
        values=[int(v,16)for v in r['words'].split(',')]
        need(struct.pack('<'+'H'*len(values),*values)==guest[lo:hi],
             'Every independent observed code word equals actual current cold guest')
    base=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for start,stop in ((0xff837900,0xff837dd0),(0xff832040,0xff8321a0)):
        lo,hi=((v-0xff800000)//8 for v in (start,stop))
        need(guest[lo:hi]==base[lo:hi],'Complete original guard/physical Block branch source unchanged')
    # Preserve every authored instruction expectation from the original Ring
    # source model. Only its nine-record legacy inventory boundary is replaced
    # by the explicit actual five-record gate above, not silently waived.
    source=inspect.getsource(ring.original.source)
    begin=source.index('    windows=');end=source.index('    def check(',begin)
    source=source[:begin]+source[end:]
    scope=dict(ring.original.source.__globals__)
    exec(compile(source,__file__+'::original_authored_source_checks_actual_inventory','exec'),scope)
    scope['source'](text,guest)


def gate(text,guest):
    source_gate(text,guest)
    events=renderer.rows(text,'MK2_STARTUP_PROJECTILE_EVENT')
    ordered=renderer.rows(text,'MK2_STARTUP_PROJECTILE_CODE')
    for r in ordered:
        lo,hi=((int(r[k],16)-0xff800000)//8 for k in ('start','stop'))
        words=[int(w,16)for w in r['words'].split(',')]
        need(struct.pack('<'+'H'*len(words),*words)==guest[lo:hi],'Whole ungated constructor/child/removal source')
    for r in events:
        entry=int(r['entry'],16)
        need(int(r['pc'],16)==entry+16 and int(r['mask'],16)==65535 and
             int(r['opcode'],16)==struct.unpack_from('<H',guest,(entry-0xff800000)//8)[0] and
             r['writes']=='0'and r['assistance']=='none',
             'Every actual independently executed event opcode, read mask and PC source-bound')
    born=ring.stream.overlap.rows(text,'CHILD');health=renderer.rows(text,'MK2_STARTUP_PROJECTILE_HEALTH')
    need(len(born)==len(health)==3 and [r['serial']for r in born]==[1,2,3],
         'Complete independent three-Ring child and damage inventory')
    result=[]
    for serial,(child,h)in enumerate(zip(born,health,strict=True),1):
        actor,main,parent=child['a8'],child['a13'],child['shot_owner'];hit=int(h['frame'])
        need(hit==(1841,2196,3051)[serial-1],'Original actually observed contact field')
        local=[r for r in events if int(r['frame'])==hit and int(r['a8'],16)==actor]
        def one(kind):return ring.one([r for r in local if r['kind']==kind],'One executing '+kind+' per actual contact')
        guard,tested,physical=one('guard'),one('tested'),one('physical_block')
        decision=ring.one([r for r in local if r['kind']in ('blocked','blocked_direct','unblocked')],
                          'One actually executed source block/full-hit decision')
        for r in (guard,tested,decision):
            need(int(r['a13'],16)==main and int(r['owner'],16)==actor and int(r['parent'],16)==parent and
                 r['id']=='18'and r['roster']=='17,18'and r['states']=='1,0'and r['mode']=='2',
                 'Every executing guard/decision belongs to this true native child/Main/parent')
        need(int(guard['entry'],16)==0xff837d40 and int(guard['a0'],16)==0x01034e90 and
             int(guard['victim'],16)==0x0106a370 and int(tested['entry'],16)==0xff837d90 and
             int(tested['a0'],16)==0x0106a370 and int(tested['a4'],16)==1,
             'Actual victim object, loaded victim Main and tested guard register')
        need(int(physical['entry'],16)==0xff832040 and int(physical['a13'],16)==0x0106a370 and
             int(physical['owner'],16)==0x01034e90 and physical['process_slot']=='1',
             'Native physical Block function actually executes with true human Kano Main')
        blocked=decision['kind']!='unblocked';damage=6 if blocked else 22
        need(int(decision['entry'],16)==({'blocked':0xff837b90,'blocked_direct':0xff837bd0,
             'unblocked':0xff837ae0}[decision['kind']]) and
             int(decision['a0'],16)==(0x20 if blocked else 0) and blocked==(serial==1),
             'Source-executed native decision and actual returned Block bit agree, not HP inference')
        native=ring.one([r for r in ring.stream.overlap.rows(text,'HEALTH')if r['serial']==serial and
             r['a8']==actor and r['a13']==main],'One separate native health context for this child')
        for key in ('frame','slot','before','after','at','mask','a8','a13','pc','a10'):
            need(int(h[key],16 if key in ('at','mask','a8','a13','pc','a10')else 10)==native[key],
                 'Both independently captured full native damage operands agree: '+key)
        need(native['before']-native['after']==native['a10']==damage and native['slot']==1 and
             native['at']==0x010602f0 and native['pc']==0xff836700 and native['mask']==65535 and
             native['main_owner']==actor and native['shot_owner']==parent and native['id']==18 and
             int(h['owner'],16)==actor and int(h['parent'],16)==parent and h['id']=='18' and
             h['writes']=='0'and h['assistance']=='none' and
             [int(r['sequence'])for r in (guard,tested,physical,decision)]==
             sorted(int(r['sequence'])for r in (guard,tested,physical,decision)) and
             int(decision['sequence'])<int(h['sequence']),
             'Actual executed decision precedes correctly owned native six/22 damage stores')
        result.append(dict(serial=serial,contact=hit,blocked=blocked,damage=damage,child=actor,main=main,
            actualDecisionEntry=decision['entry'],actualReturnedBlockBit=int(decision['a0'],16),
            exactNativeHealthBefore=native['before'],exactNativeHealthAfter=native['after'],
            originalPhysicalBlockFunctionEntered=True,actualControlPortByteRecorded=False,
            exactIndependentExecutingSourceAndHealth=True))
    return result


def execute(state):
    need(not OUT.exists(),'Fresh source-native branch qualification; original failure preserved')
    failed=previous.OUT/'failure.json';need(not json.loads(failed.read_text())['passed'],'Keep original actual mechanics rejection')
    path=transport.OUT/'report.json';receipt=json.loads(path.read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(receipt['passed']and held['process'].poll()==0 and held['identity']==receipt['actualNativeIdentity'],
         'Same original native terminal0, no replay or substituted branch data')
    pins=dict(receipt['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Entire original byte inventory intact')
    _,text,_=capture.RAM_CASES[capture.KEY];positive=gate(text,state['guest']);faults=[]
    def change(tag,key,value,**where):
        line=next(l for l in text.splitlines()if l.startswith(tag+' ')and
             all(dict(re.findall(r'(\w+)=([^\s]+)',l)).get(k)==str(v)for k,v in where.items()))
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Effective actual source-native branch corruption')
        return text.replace(line,changed,1)
    trials=[]
    for frame,kind,wrong in ((1841,'blocked_direct','00000016'),(2196,'unblocked','00000006'),(3051,'unblocked','00000006')):
        for key,value,event in (('opcode','FFFF',kind),('a0','00000021',kind),('owner','01000000',kind),
                                ('a0','01000000','tested'),('a4','00000000','tested'),('a13','01000000','physical_block')):
            trials.append((f'{frame}_{event}_{key}',change('MK2_STARTUP_PROJECTILE_EVENT',key,value,frame=frame,kind=event)))
        trials.append((f'{frame}_independent_damage',change('MK2_STARTUP_PROJECTILE_HEALTH','a10',wrong,frame=frame)))
        trials.append((f'{frame}_native_damage',change('MK2_CPU_OVERLAP_HEALTH','a10',wrong,frame=frame)))
    for label,bad in trials:
        try:gate(bad,state['guest'])
        except(ValueError,AssertionError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual source-native branch fault admitted: '+label)
    need(gate(text,state['guest'])==positive,'Complete untouched branch/damage positive restored')
    for p in (Path(__file__),Path(previous.__file__),Path(ring.__file__),Path(ring.original.__file__),
              ROOT/'mk2/mk2-maincpu.bin',failed,path):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed-source/evidence mutation');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Whole input inventory after twenty-four effective faults')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualNativeBranchContacts=positive,effectiveSourceBranchFaultsRejected=faults,inputHashes=pins,
        requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],
        threeSourceExecutedBlockHitContactsAccepted=True,originalLegacyMechanicsRejectionPreserved=True,
        completeLegacyPhysicalControlPortContractAccepted=False,firstCompleteStartupParentContractAccepted=False,
        wholeOriginalPhaseContractAccepted=False,allArenaCPUContextsAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS actual source-native Ring blocked6/full22/full22 decisions and24 effective faults',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual new source-native branch failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
