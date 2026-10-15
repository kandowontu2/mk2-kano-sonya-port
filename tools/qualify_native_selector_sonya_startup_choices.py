"""Complete actual current Sonya AI/RNG/branch stream in original guard route.

Whole original true18 choice contract with only actual source-proven schedule
context changed. Do not infer missing moves, whole visual/audio coverage,
every arena, or complete startup/physical-control-port acceptance.
"""
import inspect
import json
import re
import struct
import traceback
from pathlib import Path
import capture_native_selector_sonya_startup_choices as capture
import verify_current_existing_cpu_leg_choices_v6274 as original

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_startup_choices_checked'
PREFIX='MK2_SONYA_STARTUP_CHOICE_'


def rows(text,tag):
    records=[]
    for line in text.splitlines():
        if line.startswith(PREFIX+tag+' '):
            fields=re.findall(r'(\w+)=([^\s]+)',line)
            need(len(fields)==len(dict(fields)),'Unique actual source-native Sonya AI record fields')
            records.append(dict(fields))
    return records


def binding(schedule):
    source=inspect.getsource(original.choice_gate)
    before="n(r,'schedule')==0xfffa3180"
    need(source.count(before)==1,'Only original fixed schedule context differs; all RNG/PC/owner/branch rules unchanged')
    source=source.replace(before,"n(r,'schedule')==actual_schedule",1)
    scope=dict(original.choice_gate.__globals__,actual_schedule=schedule)
    exec(compile(source,__file__+'::whole_original_true18_AI_gate_actual_source_schedule','exec'),scope)
    return scope['choice_gate']


def gate(text,guest,schedule):
    code=rows(text,'CODE');events=rows(text,'EVENT');terminal=rows(text,'RESULT')
    need(len(code)==2 and {(int(r['start'],16),int(r['stop'],16))for r in code}==
         {(0xfffbc200,0xfffbc350),(0xff80ec20,0xff80ed40)},
         'Both complete independently observed true Sonya router and original RNG code')
    for r in code:
        lo,hi=((int(r[k],16)-0xff800000)//8 for k in ('start','stop'))
        words=[int(w,16)for w in r['words'].split(',')]
        need(struct.pack('<'+'H'*len(words),*words)==guest[lo:hi] and
             r['writes']=='0'and r['assistance']=='none','Whole actual source-native router/RNG code words')
    choices=binding(schedule)(events)
    need(len(terminal)==1 and int(terminal[0]['choices'])==len(choices)and
         int(terminal[0]['frame'])==3618 and terminal[0]['writes']=='0'and terminal[0]['assistance']=='none',
         'Every native contiguous choice serial through actual terminal, no omitted choices')
    return dict(actualNativeChoices=choices,completeActualChoiceEvents=len(events),
        movesActuallyObserved=sorted({r['move']for r in choices}),
        entireOriginalConditionalRNGRegisterOwnershipContractRetained=True)


def execute(state):
    need(not OUT.exists(),'Fresh actual source-choice qualification')
    path=capture.OUT/'report.json';report=json.loads(path.read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(report['passed']and held['process'].poll()==report['nativeExit']==0 and
         held['identity']==report['actualNativeIdentity']and held['identity']['ParentProcessId']==38752 and
         not capture.previous.transport.previous.original.previous.choices.current.prior.identity.census(),
         'Original new actual native exact terminal0 handle and fresh census, not timeout restart')
    pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Whole immutable actual source/native input inventory')
    folder,text,_=capture.RAM_CASES[capture.KEY]
    physical=capture.previous.physical.gate(text,state['guest']);schedule=physical['schedule']
    positive=gate(text,state['guest'],schedule);faults=[]
    def alter(key,value,kind=None):
        line=next(l for l in text.splitlines()if l.startswith(PREFIX+'EVENT ')and
            (kind is None or dict(re.findall(r'(\w+)=([^\s]+)',l))['kind']==kind))
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Effective actual CPU choice record mutation')
        return text.replace(line,changed,1)
    trials=[('proxy_id',alter('id','17')),('wrong_owner',alter('owner','01000000')),
        ('wrong_main',alter('main','01000000',kind='first_result')),
        ('source_opcode',alter('opcode','FFFF')),('read_mask',alter('mask','FFFE')),
        ('source_pc',alter('pc','00000000')),('threshold250',alter('a0','000000FB',kind='first_call')),
        ('threshold400',alter('a0','00000191',kind='second_call')),
        ('result_range',alter('a0','000003E8',kind='first_result')),
        ('status_carry',alter('status','FFFFFFFF',kind='first_result')),
        ('actual_native_schedule',alter('schedule','FFFA3180')),
        ('missing_entry',text.replace(next(l+'\n'for l in text.splitlines()if l.startswith(PREFIX+'EVENT ')),'',1))]
    for label,bad in trials:
        try:gate(bad,state['guest'],schedule)
        except(ValueError,AssertionError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual true Sonya source-choice fault admitted: '+label)
    need(gate(text,state['guest'],schedule)==positive,'Complete original actual RNG/branch positive restored')
    for p in (Path(__file__),Path(original.__file__),Path(capture.__file__),path,
              ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua',capture.LUA):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed or pinned source/receipt mutation');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every whole original current source/evidence hash after choice faults')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        completeCurrentNativeSonyaAI=positive,wholeNativeStateHealth=physical,
        effectiveSourceChoiceFaultsRejected=faults,inputHashes=pins,
        requirements=report['requirements'],remainingGroups=report['remainingGroups'],
        actualCurrentSourceNativeSonyaChoiceStreamAccepted=True,
        allSonyaMoveBranchesObserved=set(positive['movesActuallyObserved'])=={'ring','square','bicycle'},
        fullMovePhaseDisplayAudioAcceptance=False,allArenaCPUContextsAccepted=False,
        firstCompleteStartupParentContractAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS whole actual Sonya AI choice stream and12 effective source/owner/RNG/branch faults',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual source-choice qualifier rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
