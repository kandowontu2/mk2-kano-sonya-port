"""Same actual CPU Sonya trials: selected complete legs and whole owned render trace.

The attempted two-uninterrupted-pair gates remain REJECTED. Independently
qualify each actual completed original leg, every real native owned body and
shadow through the observed KO field, plus complete real HP/store histories.
Interrupted mixed moves and full KO/round continuation remain unaccepted.
"""
import copy
import hashlib
import inspect
import json
import re
import struct
from collections import defaultdict
from pathlib import Path
import capture_native_kano_laser_cpu_leg_repeat_p2 as capture
import native_extended_cpu_pair_contract_v2939 as pair

ROOT,need,sha,once,base=capture.ROOT,capture.need,capture.sha,capture.once,capture.base
OUT=ROOT/'audit_native_kano_laser_cpu_leg_owned_trace_checked'


def whole_health_factory():
    original=capture.previous.complete_health
    source=inspect.getsource(original.whole_health)
    source=once(source,'p=prior.cpu.original','p=pair')
    source=once(source,"assert set(posts)=={(f,s)for f in range(first,last+1)for s in(1,2)},'Both complete draw-time physical slots'",
                "assert set(posts)=={(f,s)for f in range(first,last)for s in(1,2)},'Every actual post field before source-defined lost-pair KO exit; no invented terminal post'")
    source=once(source,'for frame in range(first,last+1):','for frame in range(first,last):')
    scope=dict(original.whole_health.__globals__,pair=pair)
    exec(compile(source,__file__+'::whole_original_both_slot_HP_replay_real_KO_post_boundary','exec'),scope)
    return scope['whole_health']


def physical(text,guest):
    fields=pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
    need(by and len(fields)==len(by),'Unique real native pre-fields')
    first,last=min(by),max(by)
    need(set(by)==set(range(first,last+1)),'Every native live callback through observed KO')
    origin=by[first]
    for r in fields:
        need(all(r[k]==origin[k]for k in ('actor','main','vactor','vmain','owner','vowner','id','vid','roster','vroster','stage','schedule')) and
             r['actor']==r['owner'] and r['vactor']==r['vowner'] and
             (r['id'],r['vid'],r['state'],r['vstate'],r['mode'],r['cpu_slot'],r['human_slot'])==(18,18,0,1,2,2,1) and
             r['floor']==r['vfloor']==r['stage_floor']-135 and r['writes']==0 and r['assistance']=='none',
             'Every actual true Sonya CPU/human owner, role, identity and native floor anchor')
    complete=pair.rows(text,'COMPLETE')
    need(len(complete)==1,'Exactly one actual complete uninterrupted leg per rejected repeated trial')
    leg=pair.verify_pair(text,'sonya',complete[0]['cycle'],guest)
    need(leg['passed'],str(leg['errors']))
    need(leg['held_fields']==46 and leg['damage']==35 and leg['target']=='sonya','Entire original selected native leg contract')
    terminals=pair.rows(text,'RESULT')
    failed=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_HSPECIAL_FAILED ')]
    phase=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_HPHASE_RESULT ')]
    need(len(terminals)==len(failed)==len(phase)==1 and terminals[0]['frame']==int(phase[0]['frame'])==last+1 and
         int(failed[0]['frame'])==last and failed[0]['reason']=='lost_owned_pair_at_field_done' and
         by[last]['vhp']==0 and terminals[0]['complete_count']==1 and terminals[0]['cycles']==3,
         'Exact source-defined observer KO exit, not idle timeout, game completion or two-pair acceptance')
    health=whole_health_factory()(text,guest)
    stores=pair.rows(text,'HEALTH')
    need(stores[-1]['after']==0 and stores[-1]['frame']<last and stores[-1]['slot']==1 and
         stores[-1]['a8']==origin['vactor'] and stores[-1]['a13']==origin['vmain'] and
         all(r['frame']<last for r in stores),'Final actual victim-thread native KO store precedes last pre-callback; no missing terminal HP execution')
    health.update(lastActuallyRecordedPost=last-1,lastPreHPZero=True,terminalPostInvented=False,
                  fullKOTransitionAccepted=False)
    flags=pair.flag_rows(text)
    # Both physical targets can be written by the opposite real Main during a
    # native hit/grab. Validate target ownership, actual current instruction
    # words, continuous before/after stores, and every corresponding callback.
    relevant=[r for r in flags if first<=r['frame']<last]
    owners={1:(origin['vactor'],origin['vmain']),2:(origin['actor'],origin['main'])}
    for slot in (1,2):
        prefix='v'if slot==1 else''
        actor,main=owners[slot]
        for kind,offset in (('body',0x160),('flags',0x210),('action',0x1f0)):
            ledger=[r for r in relevant if r['slot']==slot and r['kind']==kind]
            current=by[first][prefix+kind];cursor=0
            for frame in range(first,last):
                need(by[frame][prefix+kind]==current,'Every physical native '+kind+' callback agrees with complete store history')
                while cursor<len(ledger)and ledger[cursor]['frame']==frame:
                    r=ledger[cursor];at=(r['pc']-32-0xff800000)//8
                    need(r['before']==current and (r['actor'],r['main'],r['id'],r['state'])==(actor,main,18,1 if slot==1 else 0) and
                         r['at']==(actor if kind=='body'else main)+offset and
                         0<=at<=len(guest)-4 and struct.unpack_from('<HH',guest,at)==(r['op0'],r['op1']) and
                         (r['cpu_slot'],r['human_slot'],r['writes'],r['assistance'])==(2,1,0,'none'),
                         'Every actual both-slot store operand/address/owner and independently derived current instruction')
                    current=r['after'];cursor+=1
            need(cursor==len(ledger)and by[last][prefix+kind]==current,'Every physical terminal native '+kind+' store replayed')
    need(len(relevant)==len(flags),'No earlier/later unvalidated native flag stores')
    return dict(selectedOriginalLeg=leg,wholeNativeHealthHistory=health,wholeNativeFlagStores=len(flags),
                expectedNativeBodyShadowFrames=sorted(by),owners=owners,ids={1:18,2:18},floors={1:origin['vfloor'],2:origin['floor']},
                allRecordedPreFields=len(fields),twoUninterruptedPairsAccepted=False,mixedFollowupsAccepted=False,fullKOTransitionAccepted=False)


def binding(guest):
    source=inspect.getsource(base.shadow.check)
    first=source.index(' # The older physical/ownership/health checker')
    last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
    source=once(source,source[first:last],
                " state=physical(b['cpuLog'],guest)\n entry_frames={r['frame']for r in pair.rows(b['cpuLog'],'ENTRY')}\n")
    before=""" fields=rows['MK2_HPHASE_POST_FIELD'];by={(num(t,'frame'),num(t,'slot')):t for t in fields};frames={f for f,s in by}
 first=min(frames);owners={s:(num(by[first,s],'actor'),num(by[first,s],'main'))for s in(1,2)};ids={side:identity,3-side:4};floors={s:num(by[first,s],'floor')for s in(1,2)}"""
    after=""" fields=rows['MK2_HPHASE_POST_FIELD']
 frames=set(state['expectedNativeBodyShadowFrames'])
 # Exact expected native body-call keys derive from real complete pre-fields.
 # This is NOT a fabricated terminal POST_FIELD: every actual post/HP field
 # is independently replayed above, with the missing KO post left explicit.
 by={(f,s):None for f in frames for s in(1,2)}
 owners=state['owners'];ids=state['ids'];floors=state['floors']"""
    source=once(source,before,after)
    cached={}
    def same_physical_log(text,current_guest):
        need(current_guest==guest,'Immutable independently derived current guest')
        digest=hashlib.sha256(text.encode()).hexdigest()
        if digest not in cached:cached[digest]=physical(text,current_guest)
        # Body-only counterexamples keep their entire CPU log byte-identical.
        # Any physical mutation still invokes the complete uncached gate below.
        return copy.deepcopy(cached[digest])
    scope=dict(vars(base.shadow),physical=same_physical_log,pair=pair)
    exec(compile(source,__file__+'::whole_original_owned_body_shadow_all_actual_fields_including_KO_draw','exec'),scope)
    return scope['check']


def load(actual,key):
    folder,text,images=actual.RAM_CASES[key]
    report=json.loads((folder/'result.json').read_text())
    need(not report['passed'] and report['nativeExit']==0 and not report['nativeTerminal']['hostDecodeErrors'],
         'Preserve actual whole repeated-trial rejection')
    rows=defaultdict(list)
    for line in text.splitlines():
        if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return dict(move='leg',side=2,folder=folder,report_path=folder/'result.json',report=report,rows=rows,
                streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()),human='sonya',cpuLog=text)


def mutate_line(text,prefix,key,value,predicate=lambda r:True):
    for line in text.splitlines():
        if not line.startswith(prefix+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if key in row and predicate(row):
            need(row[key]!=str(value),'Counterexample changes an actual native observation')
            changed=re.sub(r'(?<!\w)'+key+r'=[^\s]+',key+'='+str(value),line,count=1)
            return text.replace(line,changed,1)
    raise ValueError('Missing actual counterexample target '+prefix+' '+key)


def run(actual,guarded):
    need(not OUT.exists() and not base.identity.census(),'Same native terminals only; no replay')
    check=binding(actual.guest);cases=[];faults=[];pins={}
    for owner,key in ((actual,actual.KEY),(guarded,guarded.KEY)):
        b=load(owner,key)
        need(all(sha(p)==h for p,h in b['report']['inputHashes'].items()),'All actually executed inputs immutable')
        case=check(b,actual.guest,actual.payload,actual.gfx32)
        # Preserve the whole original eleven body/stream/shadow faults.
        fault_view=dict(b,report=dict(b['report'],sourceBoundBodyShadowSemantics=case))
        values=base.shadow_faults(fault_view,actual.guest,actual.payload,actual.gfx32,check)
        faults.extend(dict(case=key,**v)for v in values)
        text=b['cpuLog'];leg=case['state']['selectedOriginalLeg'];cycle=leg['cycle']
        remove=lambda prefix,predicate:text.replace(next(line+'\n'for line in text.splitlines()if line.startswith(prefix+' ')and predicate(dict(re.findall(r'(\w+)=([^\s]+)',line)))),'',1)
        trials=[
            ('selected_native_step_missing',remove('MK2_CPU_PAIR_EVENT',lambda r:r['cycle']==str(cycle)and r['kind']=='step')),
            ('selected_native_action_missing',remove('MK2_CPU_PAIR_ENTRY',lambda r:r['cycle']==str(cycle))),
            ('selected_victim_ready_missing',remove('MK2_CPU_PAIR_VICTIM_REGAIN',lambda r:r['cycle']==str(cycle))),
            ('selected_victim_ready_busy',mutate_line(text,'MK2_CPU_PAIR_VICTIM_REGAIN','vflags','00000015',lambda r:r['cycle']==str(cycle))),
            ('selected_held_pose_wrong',mutate_line(text,'MK2_CPU_PAIR_FIELD','vpose','00000000',lambda r:r['cycle']==str(cycle)and r['vaction']==str(pair.SPECS['sonya']['victim_state']))),
            ('whole_pre_floor_wrong',mutate_line(text,'MK2_CPU_PAIR_FIELD','floor','999')),
            ('whole_native_health_before_wrong',mutate_line(text,'MK2_CPU_PAIR_HEALTH','before','160')),
            ('current_CPU_store_word_wrong',mutate_line(text,'MK2_CPU_PAIR_FLAG','op0','FFFF',lambda r:r['slot']=='2')),
            ('current_human_store_word_wrong',mutate_line(text,'MK2_CPU_PAIR_FLAG','op0','FFFF',lambda r:r['slot']=='1')),
            ('last_actual_post_field_missing',remove('MK2_HPHASE_POST_FIELD',lambda r:int(r['frame'])==case['state']['wholeNativeHealthHistory']['lastActuallyRecordedPost']))]
        for label,changed in trials:
            need(changed!=text,'Actual physical field mutation')
            try:physical(changed,actual.guest)
            except(ValueError,AssertionError)as error:faults.append(dict(case=key,fault=label,rejectedBy=str(error)))
            else:raise ValueError('Actual physical/health/store corruption accepted: '+label)
        need(check(b,actual.guest,actual.payload,actual.gfx32)==case,'All positive gates restored after faults')
        cases.append(dict(key=key,finiteQualification=case,wholeRepeatedTrialStillRejected=True))
        pins.update(b['report']['inputHashes'])
        for p in b['folder'].rglob('*'):
            if p.is_file():pins[str(p.resolve())]=sha(p)
    for p in (Path(__file__),Path(pair.__file__),Path(base.shadow.__file__),Path(capture.__file__),
              Path(capture.previous.complete_health.__file__),actual.OUT/'failure.json',guarded.OUT/'failure.json'):
        pins[str(p.resolve())]=sha(p)
    need(len(faults)==42 and all(sha(p)==h for p,h in pins.items()),'All 42 real faults and conserved actual evidence')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=actual.native.NAME,cases=cases,inputHashes=pins,
        actualFaultsRejected=faults,actualSelectedCompleteLegs=2,wholeRepeatedTrialsStillRejected=True,
        everyActualOwnedBodyShadowCallSourceBound=True,wholeNativeHealthAndBothSlotFlagsVerified=True,
        terminalPostInvented=False,mixedFollowupsAccepted=False,fullKOTransitionAccepted=False,allCPUContextsAccepted=False,
        allArenasAccepted=False,fullVisualTimelineAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active',scope=__doc__))
    print(json.dumps(dict(passed=True,actualSelectedCompleteLegs=2,actualFaultsRejected=len(faults),wholeRepeatedTrialsStillRejected=True)),flush=True)


def execute(actual,guarded):
    try:run(actual,guarded)
    except Exception as error:
        import traceback
        need(not OUT.exists(),'Immutable actual owned-trace qualification failure')
        OUT.mkdir();base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                                  fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
