"""Finite earned Liu clear on the preserved, later-corrupting original run.

All later146 cache writes remain bound and rejected as campaign acceptance.
Keep every target record, native winner witness, owned move and HP store.
"""
import collections
import hashlib
import inspect
import json
import re
from pathlib import Path
import check_native_scorpion_guard_earned_clear as original
import qualify_native_subzero_guard_pressure_earned_clear_phase_bound as phase_model
import qualify_native_liu_early_leg_preceding_campaign as prefix
import run_native_sonya_liu_early_leg_campaign as capture
import seal_native_sonya_shang_cache_failure as preservation

ROOT, need, sha = capture.ROOT,capture.need,capture.sha
OUT = ROOT/'audit_native_liu_early_leg_earned_clear_checked'
START,NEXT = 391498,394481
OBSERVED = dict(STATE=34,FIGHT=1,STAGE=1,RANGE_FIELD=1962,INPUT=3302,RANGE_DECISION=1962,
                RANGE_ACTION=326,LIVE=72,HEALTH=358,RANGE_CPU_ACTION=116,SPECIAL=14,WIN=2)
ABSENT = ('LOSS','SELECT','SELECT_ID','SELECT_EXIT','GUARD_ACTION')
COUNTS = dict(OBSERVED,**{tag:0 for tag in ABSENT})
once = original.native_health.once


def contexts(rows):
    body=inspect.getsource(phase_model.contexts)
    for before,after in (
        ("state['stage']=='11'","state['stage']=='12'"),
        ("state['roster']=='18,8'","state['roster']=='18,1'"),
        ("dict(RANGE_ACTION=82,RANGE_CPU_ACTION=60,GUARD_ACTION=72)","dict(RANGE_ACTION=2,RANGE_CPU_ACTION=1)"),
        ("dict(modes)=={'7':202,'5':12}","dict(modes)=={'7':3}"),
        ('Every214 non-input callback','Every3 non-input callback')):
        body=once(body,before,after)
    scope=dict(vars(phase_model),__file__=__file__)
    exec(compile(body,__file__+'::whole_actual_refill_phase_context_contract','exec'),scope)
    return scope['contexts'](rows)


def contract():
    body=inspect.getsource(original.fields).replace("'9'","'12'")
    for before,after in (
        ("q['cpu']=='10:10'","q['cpu']=='1:1'"),
        ("q['cpu_id']==q['cpu_roster']=='10'","q['cpu_id']==q['cpu_roster']=='1'"),
        ('identity=18 if side==1 else 10','identity=18 if side==1 else 1'),
        ('len(guard_by)==13127','len(guard_by)==1962'),
        ("q['scope']=='physical_attempt_not_assumed_activation'","q['scope']=='physical_input_not_assumed_activation'"),
        ("""    need([int(q['frame']) for q in own]==[266291,267912] and
         [q['health'] for q in own]==['48,0','46,0'] and
         all(int(q['frame'])>int(rows['LOSS'][-1]['frame']) for q in own),""",
         """    need([int(q['frame']) for q in own]==[392352,393931] and
         [q['health'] for q in own]==['84,0','27,0'] and not rows['LOSS'],"""),
        ("""    return dict(actualOwnedLegEntries=35,actualScorpionRoundWinnerCalls=14,ownSuccessfulRoundFrames=[266291,267912],
        ownSuccessfulRoundHP=['48,0','46,0'],actualPaidScorpionContinues=6,completeGuardFields=13127,
        completePhysicalDecisionFields=13127,completeScorpionInputEdges=21545,wholeNativeHealthPrefix=health)""",
         """    return dict(actualOwnedLegEntries=14,actualLiuRoundWinnerCalls=2,
        ownSuccessfulRoundFrames=[392352,393931],ownSuccessfulRoundHP=['84,0','27,0'],
        actualPaidLiuContinues=0,completeRangeFields=1962,completePhysicalDecisionFields=1962,
        completeLiuInputEdges=3302,wholeNativeHealthPrefix=health)""")):
        body=once(body,before,after)
    body=body.replace("'GUARD_FIELD'","'RANGE_FIELD'").replace("'GUARD_DECISION'","'RANGE_DECISION'")
    scope=dict(vars(original),__file__=__file__,START=START,NEXT=NEXT,COUNTS=COUNTS)
    exec(compile(body,__file__+'::whole_original_native_owner_winner_HP_contract','exec'),scope)
    return scope['fields']


def fields(rows,hp_gate):
    result=contract()(rows,hp_gate)
    callback_context,phase_counts,phase_modes=contexts(rows)
    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION'):
        role='cpu' if tag=='RANGE_CPU_ACTION' else 'human';identity='1' if role=='cpu' else '18'
        for index,q in enumerate(rows[tag]):
            context=callback_context[(tag,index)]
            need(q['actor']==q['owner']==q['a8']==context[role+'_actor']==context[role+'_owner'] and
                 q['main']==q['a13']==context[role+'_main'] and q['id']==q['roster']==identity and
                 q['mask']=='FFFF' and int(q['at'],16)==int(q['main'],16)+0x1f0 and
                 all(0<=int(h)<=161 for h in q['health'].split(',')),
                 'Every native action store retains actual actor/Main/address/register ownership, including refill phases')
    need(len(rows['STAGE'])==1 and rows['STAGE'][0]['frame']==str(START) and
         rows['STAGE'][0]['stage']=='12' and rows['STAGE'][0]['schedule']=='FFFA3000' and
         len(rows['FIGHT'])==1 and rows['FIGHT'][0]['frame']==str(START) and
         rows['FIGHT'][0]['human']=='18:18' and rows['FIGHT'][0]['cpu']=='1:1' and
         rows['FIGHT'][0]['stage']=='12' and rows['FIGHT'][0]['schedule']=='FFFA3000' and
         rows['FIGHT'][0]['selection']=='88' and rows['FIGHT'][0]['actors']=='01034E90,010350A0' and
         not any(q['button'] in ('Coin','Start') for q in rows['INPUT']),
         'One actual true-character match, no invented loss/continue, no artificial selector admission')
    return dict(result,nonInputPhaseActionCallbacks=phase_counts,nonInputPhaseSceneModes=phase_modes,
                actualPhaseCallbackMainEnvelopeFields=97)


def run():
    need(not OUT.exists(), 'Fresh finite earned-clear receipt on original terminal run')
    paths=[prefix.OUT/'report.json',preservation.OUT/'report.json',preservation.RETIRED/'report.json',
           capture.SOURCE/'report.json',original.native_health.reset.INIT/'native_reset_kernel_report.json',
           capture.OUT/'guest_memory_proof.json',capture.OUT/'native_terminal.json']
    earlier,failed,retired,source,kernel,guest,terminal=[json.loads(p.read_text()) for p in paths]
    identity=terminal['identity']
    need(earlier['passed'] and earlier['accepted']['completedOpponents']==12 and
         failed['preservationPassed'] and not failed['passed'] and failed['actualGlobalStores']==146 and
         failed['actualCorruptingNativeFrame']==480976 and retired['passed'] and source['passed'] and
         kernel['passed'] and guest['everyActualByteComparedInRAM'] and guest['bytes']==1048576 and
         guest['sha256']==earlier['currentWholeGuestSHA256']==kernel['proof']['wholeGuestSHA256'] and
         identity==earlier['actualLiveNativeIdentity']==failed['actualNativeIdentity'] and
         identity['ProcessId']==10800 and identity['ParentProcessId']==33348 and
         identity['createdUnix']==1791711060.8420143 and terminal['nativeExit']==0 and
         not prefix.original.census.census(),
         'Same preserved terminal guest; later real corruption remains FAILED, not a whole campaign pass')
    pins={}
    for proof in (earlier,failed,retired,source,kernel):
        need(not proof['fullPortAcceptance'],'All original scopes remain finite')
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h),'Frozen complete inputs unchanged: '+p);pins[p]=h
    lines=prefix.original.reader.complete_lines(capture.OUT/'run.log.gz')
    parse=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in lines if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    next_stage=[q for q in parse('STAGE') if q['stage']=='14']
    need(len(next_stage)==1 and next_stage[0]['frame']==str(NEXT) and next_stage[0]['schedule']=='FFFA3000' and
         any(int(q['frame'])>=NEXT+120 and q['stage']=='14' and q['human']=='18:18' and q['cpu']=='6:6' for q in parse('LIVE')),
         'Actual following Shang6 admission and owned fields; absent secret stage13 is not claimed completed')
    prefix_fn,compare=prefix.validators()
    need(compare(prefix_fn(lines),prefix_fn(prefix.original.reader.complete_lines(prefix.OLD/'run.log.gz')))==earlier['accepted'],
         'Entire actual earlier twelve conserved again')
    rows={tag:[] for tag in COUNTS};target=[]
    for line in lines:
        if not line.startswith('MK2_NAT_CAMPAIGN_'):continue
        q=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if START<=int(q['frame'])<NEXT:
            tag=line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_')
            need(tag in OBSERVED,'Every observed category retained, zero categories not invented')
            rows[tag].append(q);target.append(line)
    whole_hp=[q for q in parse('HEALTH') if int(q['frame'])<NEXT]
    need(len(whole_hp)==40752,'Every native HP store through this earned clear, including all refills')
    factory=inspect.getsource(original.native_health.contract)
    factory=once(factory,'need(len(starts)==221,','need(len(starts)==224,')
    factory=once(factory,"return scope['fields']","return scope['health_history']")
    scope=dict(vars(original.native_health),__file__=__file__)
    exec(compile(factory,__file__+'::whole224_native_refills_each_physical_slot','exec'),scope)
    hp_gate=scope['contract'](kernel['proof']);positive=fields(rows,lambda:hp_gate(whole_hp));faults=[]
    trials=[('LIVE',0,'human','1:1'),('LIVE',71,'cpu','18:1'),('RANGE_FIELD',0,'cpu_roster','18'),
            ('RANGE_FIELD',1961,'human_owner','01000000'),('SPECIAL',0,'pc','FFF00000'),
            ('SPECIAL',13,'a8','01000000'),('SPECIAL',0,'roster','1'),('WIN',0,'slot','2'),
            ('WIN',1,'health','0,0'),('WIN',0,'frame','391500'),('RANGE_DECISION',0,'scope','forced_activation'),
            ('FIGHT',0,'cpu','18:18'),('STAGE',0,'schedule','00000000')]
    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION'):
        index=next(i for i,q in enumerate(rows[tag]) if q['frame'] not in {f['frame'] for f in rows['RANGE_FIELD']})
        for i in (0,index):
            for key,value in (('owner','01000000'),('a13','01000000'),('at','01000000'),('mask','00FF')):
                trials.append((tag,i,key,value))
    scene=next(i for i,q in enumerate(rows['STATE']) if q['frame']=='392558')
    for key,value in (('mode','2'),('roster','1,1'),('states','0,0'),('actors','01000000,01000000')):
        trials.append(('STATE',scene,key,value))
    for tag,index,key,value in trials:
        bad=dict(rows);bad[tag]=list(rows[tag]);bad[tag][index]=dict(bad[tag][index],**{key:value})
        try:fields(bad,lambda:hp_gate(whole_hp))
        except (ValueError,KeyError,IndexError) as error:faults.append(dict(tag=tag,row=index,field=key,rejectedBy=str(error)))
        else:raise ValueError('False finite native evidence admitted')
    for tag in OBSERVED:
        for label,bad in (('missing',dict(rows,**{tag:rows[tag][1:]})),
                          ('changed',dict(rows,**{tag:[dict(rows[tag][0],writes='1'),*rows[tag][1:]]}))):
            try:fields(bad,lambda:hp_gate(whole_hp))
            except ValueError as error:faults.append(dict(tag=tag,field=label,rejectedBy=str(error)))
            else:raise ValueError('Altered actual category admitted')
    for tag in ABSENT:
        try:fields(dict(rows,**{tag:[dict(rows['STATE'][0])]}),lambda:hp_gate(whole_hp))
        except ValueError as error:faults.append(dict(tag=tag,field='invented',rejectedBy=str(error)))
        else:raise ValueError('Invented continuation/callback admitted')
    for pc in ('FF9DECE0','FF9DED10','FF9DEF40','FF9DEF70','FF825930','FF825960','FF836700'):
        i=next(i for i,q in enumerate(whole_hp) if q['pc']==pc);bad=list(whole_hp);bad[i]=dict(bad[i],after='65534')
        try:hp_gate(bad)
        except ValueError as error:faults.append(dict(tag='WHOLE_HEALTH',row=i,field='after',rejectedBy=str(error)))
        else:raise ValueError('Invalid native HP ledger admitted')
    need(fields(rows,lambda:hp_gate(whole_hp))==positive,'Full positive restored after every fault')
    for p in (*paths,Path(__file__).resolve(),Path(original.__file__),Path(original.native_health.__file__),
              Path(phase_model.__file__),Path(prefix.__file__),capture.OUT/'run.log.gz'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Entire original frozen evidence unchanged after gate')
    report=dict(passed=True,finiteNativeSonyaLiuClearAccepted=True,actualTerminalNativeIdentity=identity,
        accepted=positive,completeOriginalWindowInventory=OBSERVED,explicitAbsentCategories=list(ABSENT),
        completeTargetRows=len(target),completeTargetSHA256=hashlib.sha256(''.join(target).encode()).hexdigest().upper(),
        completePrecedingEarnedFights=12,actualObservedNextStage=next_stage[0],semanticFaultsRejected=faults,
        laterConfirmedCacheCorruptionPreserved=True,laterCampaignGameplayAccepted=False,secretStage13Accepted=False,
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],inputHashes=pins,
        fullPortAcceptance=False,newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteNativeSonyaLiuClearAccepted=True,accepted=positive,
                         completeTargetRows=len(target),semanticFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual finite checker outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
