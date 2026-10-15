"""Same actual reset capture; fix only the original control-reader binding.

Retain the failed prefix lookup and all original response/round/HP criteria.
Additionally replay both live native action/body/flag histories and require
the actual human's stock neutral-jump setter, not a lift or hurt response.
No gameplay replay, guest writes, build, ROM copy or raw-media output.
"""
import copy
import hashlib
import inspect
import json
import re
import struct
import traceback
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace
import native_kano_laser_post_reset_controls_contract as prior
import verify_native_kano_laser_cpu_leg_owned_trace as mutation

ROOT,need,once=prior.ROOT,prior.need,prior.once
base,sha=mutation.base,mutation.sha
OUT=ROOT/'audit_native_kano_laser_post_reset_controls_bound_checked'


def binding():
    original=prior.original_controls
    scope=dict(vars(original),rows=prior.rows)
    source=inspect.getsource(original.actual_controls)
    exec(compile(source,__file__+'::whole_unchanged_original_actual_controls_current_prefix','exec'),scope)
    bound=SimpleNamespace(actual_controls=scope['actual_controls'])
    scope=dict(vars(prior),original_controls=bound)
    exec(compile(inspect.getsource(prior.check),__file__+'::whole_unchanged_actual_round_response_gate','exec'),scope)
    return scope['check']


def provenance(text,guest,state):
    pair=mutation.pair
    fields=pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
    first,last=state['round']['actualNativeResume'],state['round']['last']
    selected=[r for r in fields if first<=r['frame']<=last]
    need(len(selected)==last-first+1 and set(r['frame']for r in selected)==set(range(first,last+1)),
         'Every actual next-round paired callback through observed terminal')
    origin=by[first];owners={1:(origin['vactor'],origin['vmain']),2:(origin['actor'],origin['main'])}
    flags=[r for r in pair.flag_rows(text)if first<=r['frame']<last]
    for r in selected:
        need(all(r[k]==origin[k]for k in ('actor','main','vactor','vmain','owner','vowner','id','vid','roster','vroster')) and
             (r['id'],r['vid'],r['state'],r['vstate'],r['mode'])==(18,18,0,1,2) and
             r['owner']==r['actor'] and r['vowner']==r['vactor'] and
             r['floor']==r['vfloor']==r['stage_floor']-135 and r['writes']==0 and r['assistance']=='none',
             'Every actual next-round true owned identity, physical role and floor')
    for slot in (1,2):
        prefix='v'if slot==1 else'';actor,main=owners[slot]
        for kind,offset in (('action',0x1f0),('flags',0x210),('body',0x160)):
            ledger=[r for r in flags if r['slot']==slot and r['kind']==kind]
            current=origin[prefix+kind];cursor=0
            for frame in range(first,last):
                need(by[frame][prefix+kind]==current,'Every post-reset pre-field matches complete native '+kind+' history')
                while cursor<len(ledger)and ledger[cursor]['frame']==frame:
                    r=ledger[cursor];at=(r['pc']-32-0xff800000)//8
                    need(r['before']==current and (r['actor'],r['main'],r['id'],r['state'])==(actor,main,18,1 if slot==1 else 0) and
                         r['at']==(actor if kind=='body'else main)+offset and 0<=at<=len(guest)-4 and
                         struct.unpack_from('<HH',guest,at)==(r['op0'],r['op1']) and
                         (r['cpu_slot'],r['human_slot'],r['writes'],r['assistance'])==(2,1,0,'none'),
                         'Every post-reset actual native store has continuous value/address/owner/current opcode provenance')
                    current=r['after'];cursor+=1
            need(cursor==len(ledger)and by[last][prefix+kind]==current,'All observed post-reset native stores replay to terminal')
    result=prior.rows(text,'RESULT')[0];jump=prior.rows(text,'JUMP')[0]
    jf=int(jump['frame']);start=int(jump['start']);actor,main=owners[1]
    setters=[r for r in flags if start<=r['frame']<jf and r['slot']==1 and r['kind']=='action'and r['after']==0x30b]
    need(len(setters)==1 and setters[0]['pc']==0xff82f730 and setters[0]['a8']==actor and setters[0]['a13']==main,
         'Actual human neutral jump executes its own native stock setter, never opponent lift')
    posts=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_HPHASE_POST_FIELD ')]
    q=next(r for r in posts if int(r['frame'])==jf-1 and r['slot']=='1')
    need(q['action']=='779'and int(q['y'])<int(q['floor'])and int(q['vy'],16)&0x80000000 and q['gravity']=='00008000',
         'Actual human jump response has native neutral-jump action/upward velocity/gravity')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=((p-0xff800000)//8 for p in (0xff82f700,0xff82f800))
    need(guest[lo:hi]==stock[lo:hi],'Whole native neutral-jump setter kernel unchanged from original ROM')
    return dict(passed=True,first=first,last=last,actualNativeFlagStores=len(flags),owners=owners,
                jumpNativeSetter=setters[0],actualJumpPostField=q,originalJumpKernelUnchanged=True)


def load(actual):
    folder,text,images=actual.RAM_CASES[actual.KEY]
    report=json.loads((folder/'result.json').read_text())
    need(not report['passed']and report['nativeExit']==0 and report['error']=="IndexError('list index out of range')"and
         not report['nativeTerminal']['hostDecodeErrors']and all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Original actual prefix-lookup failure and whole executed candidate/observers preserved')
    rows=defaultdict(list)
    for s in text.splitlines():
        if s.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):
            rows[s.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',s)))
    return dict(move='leg',side=2,folder=folder,report=report,rows=rows,streams=[],human='sonya',cpuLog=text),images


def run(actual):
    need(not OUT.exists()and not base.identity.census(),'Same terminal native job; no replay')
    b,images=load(actual);text=b['cpuLog'];check=binding()
    need(hashlib.sha256(actual.guest).hexdigest().upper()==b['report']['guestSHA256'],
         'Entire same independently reconstructed native guest retained in RAM')
    def complete(changed):
        state=check(dict(b,cpuLog=changed),actual.guest,actual.payload,actual.gfx32)
        return state,provenance(changed,actual.guest,state)
    positive,stores=complete(text)
    events=positive['actualControls'];first=positive['round']['actualNativeResume'];last=positive['round']['last']
    mutate=lambda tag,key,value,predicate=lambda r:True:mutation.mutate_line(text,tag,key,value,predicate)
    def remove(tag,predicate=lambda r:True):
        s=next(s for s in text.splitlines()if s.startswith(tag+' ')and predicate(dict(re.findall(r'(\w+)=([^\s]+)',s))))
        return text.replace(s+'\n','',1)
    event=lambda name:lambda r:int(r['frame'])==events[name]-1 and r['slot']=='1'
    trials=[]
    for name in ('walk','jump','punch','recover'):
        trials.append(('missing_actual_'+name,remove('MK2_POST_CTRL_'+name.upper())))
        trials.append(('wrong_actual_'+name+'_action',mutate('MK2_HPHASE_POST_FIELD','action','1283',event(name))))
    trials.extend([
        ('false_other_airborne_jump',mutate('MK2_HPHASE_POST_FIELD','action','1285',event('jump'))),
        ('jump_not_above_floor',mutate('MK2_HPHASE_POST_FIELD','y','81',event('jump'))),
        ('jump_native_setter_opword_wrong',mutate('MK2_CPU_PAIR_FLAG','op0','FFFF',lambda r:int(r['frame'])==stores['jumpNativeSetter']['frame']and r['slot']=='1'and r['kind']=='action')),
        ('jump_executed_by_opponent_Main',mutate('MK2_CPU_PAIR_FLAG','a13','01000000',lambda r:int(r['frame'])==stores['jumpNativeSetter']['frame']and r['slot']=='1'and r['kind']=='action')),
        ('missing_physical_Up_pulses','\n'.join(s for s in text.splitlines()if not(s.startswith('MK2_POST_CTRL_INPUT ')and 'button=Up' in s))+'\n'),
        ('missing_physical_High_Punch_pulses','\n'.join(s for s in text.splitlines()if not(s.startswith('MK2_POST_CTRL_INPUT ')and 'button=High_Punch' in s))+'\n'),
        ('missing_survival_Block',remove('MK2_POST_CTRL_INPUT',lambda r:r['button']=='Block'and int(r['frame'])==events['recover']+1)),
        ('post_reset_native_HP_store_missing',remove('MK2_CPU_ROUND_HEALTH',lambda r:int(r['frame'])>=first)),
        ('post_reset_native_owner_wrong',mutate('MK2_CPU_ROUND_FIELD','owner','01000000',lambda r:r['slot']=='1'and int(r['frame'])==first)),
        ('post_reset_independent_floor_wrong',mutate('MK2_CPU_PAIR_FIELD','stage_floor','999',lambda r:int(r['frame'])==first)),
        ('post_reset_actual_Main_wrong',mutate('MK2_CPU_PAIR_FIELD','vmain','01000000',lambda r:int(r['frame'])==first)),
        ('terminal_survival_time_wrong',mutate('MK2_POST_CTRL_RESULT','frame',str(last-1))),
        ('missing_actual_control_postfield',remove('MK2_HPHASE_POST_FIELD',event('jump'))),
    ])
    faults=[]
    for label,changed in trials:
        need(changed!=text,'Genuine change to one actual evidence record')
        try:complete(changed)
        except (ValueError,AssertionError,KeyError)as error:
            # Missing exact indexed response fields is an explicit missing-evidence rejection.
            need(not isinstance(error,KeyError)or label=='missing_actual_control_postfield','No parser exception counted as semantic success')
            faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual post-reset counterexample accepted: '+label)
    need(complete(text)==(positive,stores),'Whole original positive restores after every actual semantic fault')
    channels=base.channels_gate(text,last)
    pins=dict(b['report']['inputHashes'])
    for p in (Path(__file__),Path(prior.__file__),Path(prior.original_controls.__file__),Path(mutation.__file__),
              ROOT/'mk2/mk2-maincpu.bin',b['folder']/'result.json',b['folder']/'run.log.gz',actual.OUT/'failure.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every immutable executed input/evidence remains unchanged')
    report=dict(passed=True,candidate=b['report']['candidate'],actualControls=positive,nativeControlStoreProvenance=stores,
        actualSemanticFaultsRejected=faults,passiveSoundChannels=channels,originalPrefixFailurePreserved=True,
        gameplayReplayed=False,actualNativeRastersStillInRAM=len(images),fullPostResetRasterAcceptance=False,
        bodyShadowFaultsPending=True,fullAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False,
        inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();base.save(OUT/'report.json',report)
    print(json.dumps(dict(passed=True,controls=events,nativeStores=stores['actualNativeFlagStores'],faults=len(faults),
                         fullPortAcceptance=False)),flush=True)


def execute(actual):
    try:run(actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual successor failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
