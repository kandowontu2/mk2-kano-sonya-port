"""Current recorded Ring contacts and complete later Ring phase contracts.

Use the unchanged original release/flight/impact/guard/damage/recovery model
for the two lifetimes with independently observed entry-boundary actors.
The first recording starts at its source entry, after the preceding all-mode
callback: do not invent that missing callback or claim the whole startup gate.
No game replay, state mutation or visual inference of damage/Block is used.
"""
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import native_repeated_cpu_ring_contract_v2970 as ring
import qualify_native_selector_cpu_rings_snapshot as renderer
import qualify_native_selector_cpu_rings_snapshot_transport as transport

capture=renderer.capture
ROOT,need,sha=renderer.ROOT,renderer.need,renderer.sha
OUT=ROOT/'audit_native_selector_cpu_rings_snapshot_mechanics_checked'


def later_contract(text,guest,serial):
    def overlap_rows(log,tag):
        records=ring.stream.overlap.rows(log,tag)
        if tag in ('EVENT','CHILD','HEALTH','CHILD_FIELD','RETIRE'):
            records=[r for r in records if r.get('child_serial',r.get('serial'))==serial]
        return records
    birth=ring.one(overlap_rows(text,'CHILD'),'One independently recorded later Ring birth')
    end=ring.one(overlap_rows(text,'RETIRE'),'One independently recorded later Ring retirement')['frame']
    def guard_rows(log,tag):
        records=ring.original.rows(log,tag)
        if tag in ('GUARD','TESTED','BLOCK'):
            records=[r for r in records if birth['frame']<=r['frame']<=end]
        return records
    overlap=SimpleNamespace(**dict(vars(ring.stream.overlap),rows=overlap_rows))
    stream=SimpleNamespace(**dict(vars(ring.stream),overlap=overlap))
    original=SimpleNamespace(**dict(vars(ring.original),rows=guard_rows))
    scope=dict(ring.verify.__globals__,stream=stream,original=original)
    # Entire original function, with only serial-specific record routing.
    source=inspect.getsource(ring.verify)
    exec(compile(source,__file__+'::unchanged_original_later_Ring_'+str(serial),'exec'),scope)
    return scope['verify'](text,guest,'kano')


def contacts(text,guest):
    ring.original.source(text,guest)
    born=ring.stream.overlap.rows(text,'CHILD')
    need(len(born)==3 and [r['serial']for r in born]==[1,2,3],
         'Every original Ring child, no omitted or invented contact')
    independent=renderer.rows(text,'MK2_STARTUP_PROJECTILE_HEALTH')
    need(len(independent)==3,'Complete independent source-owned three-contact inventory')
    accepted=[]
    for child,h in zip(born,independent,strict=True):
        actor,main,parent=child['a8'],child['a13'],child['shot_owner']
        native=ring.one([r for r in ring.stream.overlap.rows(text,'HEALTH')
            if r['a8']==actor and r['a13']==main and r['serial']==child['serial']],
            'One separate native health tap per actual Ring child lifetime')
        hit=native['frame']
        expected=(1841,2196,3051)[child['serial']-1]
        need(hit==expected and native['slot']==1 and native['at']==0x010602f0 and
             native['pc']==0xff836700 and native['mask']==65535 and
             native['main_owner']==actor and native['shot_owner']==parent and native['id']==18,
             'Original actual projectile health address/source/owner/mask')
        for key in ('frame','slot','before','after','at','mask','a8','a13','pc','a10'):
            actual=int(h[key],16 if key in ('at','mask','a8','a13','pc','a10')else 10)
            need(actual==native[key],'Both independent full native health operands agree: '+key)
        need(int(h['owner'],16)==actor and int(h['parent'],16)==parent and h['id']=='18' and
             h['roster']=='17,18' and h['states']=='1,0' and h['writes']=='0' and h['assistance']=='none',
             'Independent true native child/parent/roster ownership, not a proxy')
        guards=[r for r in ring.original.rows(text,'GUARD')if r['frame']==hit and r['actor']==actor]
        tests=[r for r in ring.original.rows(text,'TESTED')if r['frame']==hit and r['actor']==actor]
        g=ring.one(guards,'One actual victim Main guard read')
        t=ring.one(tests,'One actual tested victim guard word')
        need((g['main'],g['owner'],g['parent'],g['victim'],g['vmain'],g['vowner'],g['vid'])==
             (main,actor,parent,0x01034e90,0x0106a370,0x01034e90,17) and
             (t['main'],t['vmain'],t['loaded_main'],t['owner'],t['parent'])==
             (main,0x0106a370,0x0106a370,actor,parent) and
             t['tested_flags']==t['vflags']==g['vflags']==1,
             'Actual guard word and loaded Main belong to true human Kano')
        blocks=[r for r in ring.original.rows(text,'BLOCK')if r['frame']==hit and r['actor']==actor]
        physical=ring.one([r for r in blocks if r['decision']==2],'One physical active-low Block read')
        decision=ring.one([r for r in blocks if r['decision']in (0,1)],'One executed native block branch')
        blocked=decision['decision']==1
        need((physical['entry'],physical['pc'],physical['main'],physical['owner'],physical['process_slot'])==
             (0xff832040,0xff832050,0x0106a370,0x01034e90,1) and
             physical['controls']==decision['controls'] and bool(physical['controls']&0x20)==(not blocked) and
             decision['entry']in ((0xff837b90,0xff837bd0)if blocked else(0xff837ae0,)) and
             decision['pc']==decision['entry']+16 and decision['main']==main and
             decision['owner']==actor and decision['parent']==parent,
             'Source-bound actual physical blocked/full-hit branch, never held-input inference')
        damage=6 if blocked else 22
        need(native['before']-native['after']==native['a10']==damage and
             blocked==(child['serial']==1),'Actual six chip / two twenty-two damage contacts')
        accepted.append(dict(serial=child['serial'],contact=hit,blocked=blocked,damage=damage,
            child=actor,main=main,parent=parent,independentHealthOperandsExact=True,
            actualPhysicalBlockDecisionVerified=True))
    return accepted


def execute(state):
    need(not OUT.exists(),'Fresh additive current Ring mechanics evidence')
    path=transport.OUT/'report.json';receipt=json.loads(path.read_text())
    held=capture.NATIVE_HANDLES[capture.KEY];folder,text,_=capture.RAM_CASES[capture.KEY]
    need(receipt['passed']and held['process'].poll()==receipt['nativeExit']==0 and
         held['identity']==receipt['actualNativeIdentity'],'Same retained actual terminal0 native game')
    pins=dict(receipt['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Complete immutable current input pins')
    def gate(value):
        return dict(contacts=contacts(value,state['guest']),
            laterCompletePhaseContracts=[later_contract(value,state['guest'],n)for n in (2,3)])
    positive=gate(text);faults=[]
    def change(tag,key,value,**where):
        line=next(l for l in text.splitlines()if l.startswith(tag+' ')and
            all(dict(re.findall(r'(\w+)=([^\s]+)',l)).get(k)==str(v)for k,v in where.items()))
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Effective actual Ring counterexample')
        return text.replace(line,changed,1)
    trials=[]
    for frame,wrong in ((1841,'00000016'),(2196,'00000006'),(3051,'00000006')):
        trials.extend([
            ('independent_damage_'+str(frame),change('MK2_STARTUP_PROJECTILE_HEALTH','a10',wrong,frame=frame)),
            ('native_damage_'+str(frame),change('MK2_CPU_OVERLAP_HEALTH','a10',wrong,frame=frame)),
            ('physical_block_'+str(frame),change('MK2_RING_PAIR_BLOCK','controls','FFFFFFFF',frame=frame,decision=2)),
            ('tested_victim_main_'+str(frame),change('MK2_RING_PAIR_TESTED','loaded_main','01000000',frame=frame))])
    for birth in (2190,3042):
        trials.append(('later_flight_pose_'+str(birth),change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=birth+3)))
        trials.append(('independent_later_parent_'+str(birth),change('MK2_CPU_OVERLAP_CHILD','shot_owner','01000000',frame=birth)))
    for label,bad in trials:
        try:gate(bad)
        except(ValueError,AssertionError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective observed Ring mechanics fault admitted: '+label)
    need(gate(text)==positive,'Complete untouched current mechanics positive restored')
    for p in (Path(__file__),Path(ring.__file__),Path(ring.original.__file__),Path(renderer.__file__),path):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No changed executed source/evidence');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Entire current source inventory after mechanics faults')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        completeCurrentContactsAndLaterPhases=positive,effectiveMechanicsFaultsRejected=faults,
        firstPreEntryAllModeCallbackRecorded=False,firstCompleteStartupParentContractAccepted=False,
        requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],inputHashes=pins,
        allArenaCPUContextsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS three current native Ring contact branches and two complete later phase contracts',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual current Ring mechanics failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
