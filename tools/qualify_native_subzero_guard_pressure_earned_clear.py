"""Whole actual SubZero clear, prior eleven fights and native HP history.

Retain the original owned-leg/winner/paid-continue/native-health contract.
Only observed opponent, fields, inventory and actual successful rounds change.
Include every target category and its actual ownership; never accept art/audio
or the rest of the tower from this finite native gameplay gate.
"""
import collections
import hashlib
import inspect
import json
import re
from pathlib import Path
import check_native_scorpion_guard_earned_clear as original
import qualify_native_subzero_ring_preceding_campaign as prefix
import run_native_sonya_subzero_guard_pressure_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT/'audit_native_subzero_guard_pressure_earned_clear_checked'
START, NEXT = 304271, 391498
COUNTS = dict(STATE=1195,FIGHT=25,STAGE=1,RANGE_FIELD=50593,INPUT=82473,
              RANGE_DECISION=50593,RANGE_ACTION=10311,GUARD_ACTION=5889,
              RANGE_CPU_ACTION=3206,LIVE=1775,SPECIAL=392,HEALTH=9489,
              WIN=54,LOSS=23,SELECT=23,SELECT_ID=46,SELECT_EXIT=23)
OWN_FRAMES = [306368,312584,334660,366801,377168,388387,390990]
OWN_HP = ['20,0','15,0','9,0','12,0','34,0','33,0','9,0']


def contract():
    body = inspect.getsource(original.fields).replace("'9'","'11'")
    once = original.native_health.once
    for before,after in (("q['cpu']=='10:10'","q['cpu']=='8:8'"),
                         ("q['cpu_id']==q['cpu_roster']=='10'","q['cpu_id']==q['cpu_roster']=='8'"),
                         ('identity=18 if side==1 else 10','identity=18 if side==1 else 8'),
                         ('len(guard_by)==13127','len(guard_by)==50593')):
        body=once(body,before,after)
    body=body.replace("'GUARD_FIELD'","'RANGE_FIELD'").replace("'GUARD_DECISION'","'RANGE_DECISION'")
    body=once(body,"q['scope']=='physical_attempt_not_assumed_activation'",
                   "q['scope']=='physical_input_not_assumed_activation'")
    body=once(body,
        """    need([int(q['frame']) for q in own]==[266291,267912] and
         [q['health'] for q in own]==['48,0','46,0'] and
         all(int(q['frame'])>int(rows['LOSS'][-1]['frame']) for q in own),""",
        """    need([int(q['frame']) for q in own]==OWN_FRAMES and
         [q['health'] for q in own]==OWN_HP and
         int(rows['LOSS'][-1]['frame'])==386484 and
         [int(q['frame']) for q in own if int(q['frame'])>386484]==[388387,390990],""")
    body=once(body,
        """    return dict(actualOwnedLegEntries=35,actualScorpionRoundWinnerCalls=14,ownSuccessfulRoundFrames=[266291,267912],
        ownSuccessfulRoundHP=['48,0','46,0'],actualPaidScorpionContinues=6,completeGuardFields=13127,
        completePhysicalDecisionFields=13127,completeScorpionInputEdges=21545,wholeNativeHealthPrefix=health)""",
        """    return dict(actualOwnedLegEntries=392,actualSubZeroRoundWinnerCalls=54,
        ownSuccessfulRoundFrames=[388387,390990],ownSuccessfulRoundHP=['33,0','9,0'],
        earlierSingleWonRoundsNotCreditedAsMatch=5,allActualOwnRoundFrames=OWN_FRAMES,
        allActualOwnRoundHP=OWN_HP,actualPaidSubZeroContinues=23,completeRangeFields=50593,
        completePhysicalDecisionFields=50593,completeSubZeroInputEdges=82473,
        wholeNativeHealthPrefix=health)""")
    scope=dict(vars(original),__file__=__file__,START=START,NEXT=NEXT,COUNTS=COUNTS,
               OWN_FRAMES=OWN_FRAMES,OWN_HP=OWN_HP)
    exec(compile(body,__file__+'::whole_original_owned_native_fields_contract','exec'),scope)
    return scope['fields']


def fields(rows, health_gate):
    positive=contract()(rows,health_gate)
    need(set(rows)==set(COUNTS), 'All seventeen observed target categories retained')
    field_by={int(row['frame']):row for row in rows['RANGE_FIELD']}
    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION','GUARD_ACTION'):
        side='cpu' if tag=='RANGE_CPU_ACTION' else 'human'
        expected='8' if side=='cpu' else '18'
        for row in rows[tag]:
            context=field_by[int(row['frame'])]
            need(row['actor']==row['owner']==row['a8']==context[side+'_actor']==context[side+'_owner'] and
                 row['main']==row['a13']==context[side+'_main'] and
                 row['id']==row['roster']==expected and row['mask']=='FFFF' and
                 int(row['at'],16)==int(row['main'],16)+0x1f0 and
                 all(0<=int(h)<=161 for h in row['health'].split(',')),
                 'Every actual human/CPU action store has its same native actor/Main/address/register ownership')
    need(len(rows['STAGE'])==1 and rows['STAGE'][0]['frame']==str(START) and
         rows['STAGE'][0]['stage']=='11' and rows['STAGE'][0]['schedule']=='FFFA3000',
         'Exact actual native target admission')
    for row in rows['FIGHT']:
        need(row['stage']=='11' and row['schedule']=='FFFA3000' and
             row['human']=='18:18' and row['cpu']=='8:8' and
             len(set(row['actors'].split(',')))==2 and
             all(0x01000000<=int(actor,16)<0x01100000 for actor in row['actors'].split(',')),
             'Every actual fight admission is true Sonya/SubZero, never a name-only proxy')
    exits={row['number']:row for row in rows['SELECT_EXIT']}
    need(len(exits)==23 and all(str(int(loss['number'])+1) in exits and
         int(exits[str(int(loss['number'])+1)]['frame'])==int(loss['frame'])+518 for loss in rows['LOSS']),
         'Every paid continue completes its actual native selector exit before returning to combat')
    return positive


def run():
    need(not OUT.exists(), 'Fresh finite actual SubZero clear receipt')
    preceding_path=ROOT/'audit_native_subzero_guard_pressure_preceding_campaign_checked/report.json'
    kernel_path=original.native_health.reset.INIT/'native_reset_kernel_report.json'
    source_path=capture.SOURCE/'report.json'
    proof_path=capture.OUT/'guest_memory_proof.json'
    identity_path=capture.OUT/'native_identity.json'
    pins_path=capture.OUT/'input_hashes_before.json'
    preceding,kernel,source,proof,identity,pins=[json.loads(path.read_text()) for path in
        (preceding_path,kernel_path,source_path,proof_path,identity_path,pins_path)]
    need(preceding['passed'] and preceding['finiteCurrentFirstElevenEarnedFightsByExactConservationAccepted'] and
         preceding['actualLiveNativeIdentity']==identity and source['passed'] and kernel['passed'] and
         proof['everyActualByteComparedInRAM'] and proof['bytes']==1048576 and
         proof['sha256']==preceding['currentWholeGuestSHA256']==kernel['proof']['wholeGuestSHA256'] and
         identity['ProcessId']==7268 and identity['ParentProcessId']==21628 and
         identity['createdUnix']==1791708051.8534794 and identity in prefix.census.census(),
         'Same exact native birth/path/command/parent and whole current guest/native reset/damage/refill kernels')
    for receipt in (preceding,kernel,source):
        for path,digest in receipt['inputHashes'].items():
            need(sha(path)==digest and (path not in pins or pins[path]==digest), 'Every frozen prerequisite unchanged')
            pins[path]=digest
    need(all(sha(path)==digest for path,digest in pins.items()), 'All executed sources still frozen')
    lines=prefix.reader.complete_lines(capture.OUT/'run.log.gz')
    need(not any(line.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ')) for line in lines),
         'Entire same native stream free of observed cache overrun')
    parse=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in lines
                      if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    next_stage=[row for row in parse('STAGE') if row['stage']=='12']
    need(len(next_stage)==1 and next_stage[0]['frame']==str(NEXT) and next_stage[0]['schedule']=='FFFA3000' and
         any(int(row['frame'])>=NEXT+120 and row['stage']=='12' and row['human']=='18:18' and row['cpu']=='1:1'
             for row in parse('LIVE')), 'Actual subsequent native Liu Kang admission and later own fields')
    old_prefix=prefix.prefix(prefix.reader.complete_lines(prefix.OLD/'run.log.gz'))
    current_prefix=prefix.prefix(lines)
    need(prefix.compare(current_prefix,old_prefix)==preceding['accepted'], 'Whole eleven preceding fights conserved again')
    rows={tag:[] for tag in COUNTS}
    target_lines=[]
    for line in lines:
        if not line.startswith('MK2_NAT_CAMPAIGN_'): continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if START<=int(row['frame'])<NEXT:
            tag=line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_')
            need(tag in rows, 'No actual target category omitted or silently discarded')
            rows[tag].append(row);target_lines.append(line)
    whole_hp=[row for row in parse('HEALTH') if int(row['frame'])<NEXT]
    need(len(whole_hp)==40394, 'Every actual native HP store through successful clear retained')
    factory=inspect.getsource(original.native_health.contract)
    factory=original.native_health.once(factory,'need(len(starts)==221,','need(len(starts)==222,')
    factory=original.native_health.once(factory,"return scope['fields']","return scope['health_history']")
    scope=dict(vars(original.native_health),__file__=__file__)
    exec(compile(factory,__file__+'::whole_original_complete_222_native_refills_per_slot','exec'),scope)
    hp_gate=scope['contract'](kernel['proof'])
    positive=fields(rows,lambda:hp_gate(whole_hp))
    faults=[]
    trials=[('LIVE',0,'human','1:1'),('LIVE',1774,'cpu','8:1'),('RANGE_FIELD',0,'cpu_roster','18'),
            ('RANGE_FIELD',50592,'human_owner','01000000'),('SPECIAL',0,'pc','FFF00000'),
            ('SPECIAL',391,'a8','01000000'),('SPECIAL',0,'roster','1'),
            ('WIN',next(i for i,q in enumerate(rows['WIN']) if q['frame']=='388387'),'slot','2'),
            ('WIN',next(i for i,q in enumerate(rows['WIN']) if q['frame']=='390990'),'health','0,0'),
            ('WIN',next(i for i,q in enumerate(rows['WIN']) if q['frame']=='388387'),'frame','377168'),
            ('SELECT',0,'target','1'),('SELECT_ID',45,'state','1'),
            ('RANGE_DECISION',0,'scope','forced_activation'),('FIGHT',0,'cpu','1:1'),
            ('STAGE',0,'schedule','00000000'),('SELECT_EXIT',0,'frame','308264')]
    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION','GUARD_ACTION'):
        for key,value in (('owner','01000000'),('a13','01000000'),('at','01000000'),('mask','00FF')):
            trials.append((tag,0,key,value))
    for tag,index,key,value in trials:
        bad=dict(rows);bad[tag]=list(rows[tag]);bad[tag][index]=dict(bad[tag][index],**{key:value})
        try: fields(bad,lambda:hp_gate(whole_hp))
        except (ValueError,KeyError,IndexError) as error: faults.append(dict(tag=tag,row=index,field=key,rejectedBy=str(error)))
        else: raise ValueError('False native target evidence admitted')
    for tag in COUNTS:
        bad=dict(rows);bad[tag]=rows[tag][1:]
        try: fields(bad,lambda:hp_gate(whole_hp))
        except ValueError as error: faults.append(dict(tag=tag,row=0,field='missing',rejectedBy=str(error)))
        else: raise ValueError('Omitted native target category admitted')
    for pc in ('FF9DECE0','FF9DED10','FF9DEF40','FF9DEF70','FF825930','FF825960','FF836700'):
        index=next(i for i,row in enumerate(whole_hp) if row['pc']==pc)
        bad=list(whole_hp);bad[index]=dict(bad[index],after='65534')
        try: hp_gate(bad)
        except ValueError as error: faults.append(dict(tag='WHOLE_HEALTH',row=index,field='after',rejectedBy=str(error)))
        else: raise ValueError('Invalid native HP history admitted')
    need(fields(rows,lambda:hp_gate(whole_hp))==positive and identity in prefix.census.census(),
         'Whole positive restored after all faults; same native still live, never replayed for timeout')
    for path in (preceding_path,kernel_path,source_path,proof_path,identity_path,pins_path,
                 Path(__file__).resolve(),Path(original.__file__),Path(original.native_health.__file__),Path(prefix.__file__),Path(capture.__file__)):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(path)==digest for path,digest in pins.items()), 'All frozen inputs unchanged after complete gate')
    report=dict(passed=True,finiteNativeSonyaSubZeroClearAccepted=True,actualLiveNativeIdentity=identity,
        accepted=positive,actualObservedNextStage=next_stage[0],completeOriginalWindowInventory=COUNTS,
        completeTargetRows=len(target_lines),completeTargetSHA256=hashlib.sha256(''.join(target_lines).encode()).hexdigest().upper(),
        completePrecedingEarnedFights=11,semanticFaultsRejected=faults,wholeCurrentGuestSHA256=proof['sha256'],
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False,originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],inputHashes=pins,
        newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteNativeSonyaSubZeroClearAccepted=True,accepted=positive,
                         completeTargetRows=len(target_lines),semanticFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(), 'Retain actual original finite qualification failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
