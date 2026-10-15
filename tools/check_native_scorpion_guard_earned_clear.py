"""Same actual live run: true Sonya beats true Scorpion by native round wins.

Entire earlier nine-fight prefix conserved; complete source-native HP ledger,
every Scorpion guard/decision/activation/continue/winner field retained.
No artwork/audio/ending/full-campaign acceptance from this finite gate.
"""
import gzip
import hashlib
import inspect
import json
import re
from pathlib import Path
import capture_native_paired_stumble_scorpion_guard as current
import check_native_scorpion_guard_first_five_prefix as prefix_model
import qualify_native_sonya_first_nine_ladder_fights as native_health

ROOT, need, sha = current.ROOT, current.need, current.sha
OUT = ROOT / 'audit_native_scorpion_guard_earned_clear_checked'
START, NEXT = 244878, 268421
COUNTS = dict(LIVE=470, WIN=14, LOSS=6, HEALTH=2491, SPECIAL=35,
              GUARD_FIELD=13127, GUARD_DECISION=13127, SELECT=6, SELECT_ID=12, INPUT=21545, STATE=325)


def fields(rows, whole_health):
    need({tag:len(values) for tag,values in rows.items()}==COUNTS, 'Entire actual Scorpion-window inventory retained')
    for values in rows.values():
        need(all(q['human_slot']=='1' and q['fighter']=='sonya' and q['writes']=='0' and q['assistance']=='none' and
                 START<=int(q['frame'])<NEXT for q in values), 'Every field is actual unassisted Sonya P1 in exact native fight window')
    for q in rows['LIVE']:
        need(q['stage']=='9' and q['schedule']=='FFFA3000' and q['human']=='18:18' and q['cpu']=='10:10' and
             q['human_actor']!=q['cpu_actor'] and q['human_main']!=q['cpu_main'] and
             all(0x01000000<=int(q[k],16)<0x01100000 for k in ('human_actor','cpu_actor','human_main','cpu_main')) and
             all(0<=int(h)<=161 for h in q['health'].split(',')), 'All live native identities, Main/actor contexts and HP are genuine')
    guard_by = {int(q['frame']):q for q in rows['GUARD_FIELD']}
    need(len(guard_by)==13127, 'Every actual guard field unique')
    for q in rows['GUARD_FIELD']:
        need(q['stage']=='9' and q['human_id']==q['human_roster']=='18' and q['cpu_id']==q['cpu_roster']=='10' and
             q['human_owner']==q['human_actor'] and q['cpu_owner']==q['cpu_actor'] and
             q['human_actor']!=q['cpu_actor'] and q['human_main']!=q['cpu_main'] and
             all(0x01000000<=int(q[k],16)<0x01100000 for k in ('human_actor','cpu_actor','human_main','cpu_main')),
             'All ordinary guard fields preserve actual two owned character bodies')
    need([q['frame'] for q in rows['GUARD_DECISION']]==[q['frame'] for q in rows['GUARD_FIELD']] and
         all(q['scope']=='physical_attempt_not_assumed_activation' for q in rows['GUARD_DECISION']),
         'Every physical decision has its original native field; decisions do not fabricate activation')
    for q in rows['SPECIAL']:
        context=guard_by[int(q['frame'])]
        need(q['move']=='leg' and q['entry']=='FFF80800' and q['at']=='FFF80810' and q['pc']=='FFF80830' and
             q['id']==q['roster']=='18' and q['stage']=='9' and
             q['actor']==q['a8']==context['human_actor'] and q['main']==q['a13']==context['human_main'],
             'Every one of35 actual native leg entries owned by true Sonya, not intended inputs or another task')
    for q in rows['WIN']:
        side=int(q['slot']); identity=18 if side==1 else 10
        hp=list(map(int,q['health'].split(',')))
        witness=[s for s in rows['STATE'] if int(s['frame'])==int(q['frame'])+1]
        need(side in (1,2) and int(q['id'])==identity and q['stage']=='9' and q['pc']=='FF8296B0' and
             q['entry']==f'{0xfffef800+identity*32:08X}' and hp[side-1]>hp[2-side] and
             witness and witness[0]['winner']==q['slot'] and witness[0]['health']==q['health'] and
             witness[0]['mode'] in ('5','11'), 'Every native winner has exact ID/entry/instruction, earned HP and next-field actual scene witness')
    own=[q for q in rows['WIN'] if q['slot']=='1']
    need([int(q['frame']) for q in own]==[266291,267912] and
         [q['health'] for q in own]==['48,0','46,0'] and
         all(int(q['frame'])>int(rows['LOSS'][-1]['frame']) for q in own),
         'Two real own round victories after most recent paid loss in same successful match')
    inputs={(q['button'],int(q['frame'])) for q in rows['INPUT']}
    for q in rows['LOSS']:
        f=int(q['frame']);number=str(int(q['number'])+1)
        selected=[s for s in rows['SELECT'] if s['number']==number]
        confirmed=[s for s in rows['SELECT_ID'] if s['number']==number]
        need(len(selected)==1 and int(selected[0]['frame'])==f+314 and selected[0]['target']=='18' and
             selected[0]['schedule']=='FFFA3000' and len(confirmed)==2 and
             all(s['roster']=='18' and s['state']=='3' for s in confirmed), 'Each of six genuine losses has exact physical continue and two true Sonya confirmations')
        for button,age in [*[('Coin',a) for a in (*range(20,25),*range(270,275))],*[('Start',a) for a in range(310,315)]]:
            need((button,f+age) in inputs, 'Every source-defined Coin/Start field retained, no free continuation')
    health=whole_health()
    return dict(actualOwnedLegEntries=35,actualScorpionRoundWinnerCalls=14,ownSuccessfulRoundFrames=[266291,267912],
        ownSuccessfulRoundHP=['48,0','46,0'],actualPaidScorpionContinues=6,completeGuardFields=13127,
        completePhysicalDecisionFields=13127,completeScorpionInputEdges=21545,wholeNativeHealthPrefix=health)


def run():
    need(not OUT.exists(), 'Fresh finite actual Scorpion progression receipt')
    nine_path=ROOT/'audit_native_sonya_first_nine_ladder_fights_checked/report.json'
    kernel_path=native_health.reset.INIT/'native_reset_kernel_report.json'
    source_path=current.SOURCE/'report.json'
    nine,kernel,source=[json.loads(p.read_text()) for p in (nine_path,kernel_path,source_path)]
    proof_path=current.OUT/'guest_memory_proof.json';proof=json.loads(proof_path.read_text())
    identity_path=current.OUT/'native_identity.json';identity=json.loads(identity_path.read_text())
    pins_path=current.OUT/'input_hashes_before.json';pins=json.loads(pins_path.read_text())
    need(nine['passed'] and nine['finiteFirstNineLadderProgressionAccepted'] and kernel['passed'] and source['passed'] and
         source['physicalBranchPriorityChanges']==1 and source['timingChanges']==0 and
         proof['everyActualByteComparedInRAM'] and proof['sha256']==nine['currentWholeGuestSHA256']==kernel['proof']['wholeGuestSHA256'] and
         all(sha(p)==h for report in (nine,kernel,source) for p,h in report['inputHashes'].items()) and
         all(sha(p)==h for p,h in pins.items()) and identity in prefix_model.progress.census.census(),
         'Same actual live native identity, entire initialized guest and all original current sources still bound')
    lines=prefix_model.complete_lines(current.OUT/'run.log.gz')
    need(not any(l.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ')) for l in lines), 'No observed cache failure in whole actual stream')
    def parse(tag):
        return [dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in lines if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    stages=parse('STAGE'); next_stage=[q for q in stages if q['stage']=='10']
    need(len(next_stage)==1 and int(next_stage[0]['frame'])==NEXT and next_stage[0]['schedule']=='FFFA3000' and
         any(int(q['frame'])>=NEXT+120 and q['stage']=='10' and q['human']=='18:18' and q['cpu']=='5:5' for q in parse('LIVE')),
         'Actual native Mileena admission and later true owned fight fields, not an inferred stage advance')
    tags=tuple('MK2_NAT_CAMPAIGN_'+t+' ' for t in prefix_model.TAGS)
    preceding=lambda seq:[l for l in seq if l.startswith(tags) and int(re.search(r'\bframe=(\d+)\b',l)[1])<START]
    earlier=preceding(lines); oracle=preceding(prefix_model.complete_lines(prefix_model.OLD/'run.log.gz'))
    need(earlier==oracle, 'Entire original verified nine-fight input/state/health/schedule/winner prefix conserved before Scorpion')
    whole_hp=[q for q in parse('HEALTH') if int(q['frame'])<NEXT]
    need(len(whole_hp)==26851, 'Entire independently inventoried current HP prefix, no stores dropped')
    factory=inspect.getsource(native_health.contract)
    factory=native_health.once(factory,'need(len(starts)==221,','need(len(starts)==146,')
    factory=native_health.once(factory,"return scope['fields']","return scope['health_history']")
    scope=dict(vars(native_health),__file__=__file__)
    exec(compile(factory,__file__+'::whole_original_checked_native_HP_history_146_actual_refills_per_slot','exec'),scope)
    hp_gate=scope['contract'](kernel['proof'])
    rows={tag:[q for q in parse(tag) if START<=int(q['frame'])<NEXT] for tag in COUNTS}
    positive=fields(rows,lambda:hp_gate(whole_hp))
    trials=[('LIVE',0,'human','1:1'),('LIVE',469,'cpu','10:1'),('GUARD_FIELD',0,'cpu_roster','18'),
        ('GUARD_FIELD',13126,'human_owner','01000000'),('SPECIAL',0,'pc','FFF00000'),('SPECIAL',34,'a8','01000000'),
        ('SPECIAL',0,'roster','1'),('WIN',12,'slot','2'),('WIN',13,'health','0,0'),('WIN',12,'frame','264000'),
        ('SELECT',0,'target','1'),('SELECT_ID',11,'state','1'),('GUARD_DECISION',0,'scope','forced_activation')]
    faults=[]
    for tag,index,key,value in trials:
        bad=dict(rows);bad[tag]=list(rows[tag]);bad[tag][index]=dict(bad[tag][index],**{key:value})
        try:fields(bad,lambda:hp_gate(whole_hp))
        except (ValueError,KeyError,IndexError) as error:faults.append(dict(tag=tag,row=index,field=key,rejectedBy=str(error)))
        else:raise ValueError('False actual Scorpion evidence admitted')
    for tag in COUNTS:
        bad=dict(rows);bad[tag]=rows[tag][1:]
        try:fields(bad,lambda:hp_gate(whole_hp))
        except ValueError as error:faults.append(dict(tag=tag,row=0,field='missing',rejectedBy=str(error)))
        else:raise ValueError('Omitted actual Scorpion evidence admitted')
    for pc in ('FF9DECE0','FF9DED10','FF9DEF40','FF9DEF70','FF825930','FF825960','FF836700'):
        i=next(i for i,q in enumerate(whole_hp) if q['pc']==pc)
        bad=list(whole_hp);bad[i]=dict(bad[i],after='65534')
        try:hp_gate(bad)
        except ValueError as error:faults.append(dict(tag='WHOLE_HEALTH',row=i,field='after',rejectedBy=str(error)))
        else:raise ValueError('Invalid actual current native health history admitted')
    need(fields(rows,lambda:hp_gate(whole_hp))==positive and identity in prefix_model.progress.census.census(), 'Whole actual positive and same original live handle restored after fault suite')
    for p in (nine_path,kernel_path,source_path,proof_path,identity_path,pins_path,Path(__file__).resolve(),
              Path(prefix_model.__file__).resolve(),Path(native_health.__file__).resolve()):pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'All actual inputs unchanged after complete finite gate')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,finiteNativeSonyaScorpionClearAccepted=True,
        actualLiveNativeIdentity=identity,accepted=positive,actualObservedNextStage=next_stage[0],completeOriginalWindowInventory=COUNTS,
        completePrecedingVerifiedNineFightRows=len(earlier),completeEarlierPrefixSHA256=hashlib.sha256(''.join(earlier).encode()).hexdigest().upper(),
        semanticFaultsRejected=faults,wholeCurrentGuestSHA256=proof['sha256'],
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,fullPortAcceptance=False,
        originalNaturalIntegrationRequirements=nine['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=nine['originalRemainingWorkGroups'],
        inputHashes=pins,newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteNativeSonyaScorpionClearAccepted=True,actualNativePID=identity['ProcessId'],
        accepted=positive,semanticFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual original Scorpion gate outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
