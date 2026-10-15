"""Finite genuine Sonya ladder progression on the repaired current guest.

Complete original physical inputs, selection, actor/roster, native winners,
state witnesses and health-store chains. Baraka losses and whole campaign
remain unaccepted. No artwork, sound or new replay is inferred.
"""
import gzip
import hashlib
import json
import re
from pathlib import Path
import retire_native_kung_lao_guard_losing_baraka as preserved

ROOT,need,sha=preserved.ROOT,preserved.need,preserved.sha
FOLDER=preserved.capture.OUT
OUT=ROOT/'audit_native_sonya_first_six_ladder_fights_checked'
COUNTS=dict(LIVE=5877,STAGE=7,SELECT_ID=148,WIN=171,LOSS=73,HEALTH=30685,ROM=6,
    STATE=3833,SELECT=74,INPUT=267581,SPECIAL=797,CPU_ID=0)
OPPONENTS=(17,11,7,4,0,18,3)


def health_history(stores):
    complete=0;damage=0;noops=0
    for slot in ('1','2'):
        chain=[q for q in stores if q['slot']==slot]
        start_pc,step_pc,reset_pc,address=('FF9DECE0','FF9DEF40','FF825930','010602F0') if slot=='1' else (
            'FF9DED10','FF9DEF70','FF825960','01060EC0')
        need(all(a['after']==b['before'] for a,b in zip(chain,chain[1:])), 'Entire continuous native health-store history explains every next previous value')
        starts=[(i,q) for i,q in enumerate(chain) if q['pc']==start_pc]
        need(len(starts)==171, 'Every actual inter-round/next-match native refill retained')
        consumed=set()
        for index,start in starts:
            need(start['before']=='161' and start['after']=='65535', 'Original exact full-word native fill sentinel')
            frame=int(start['frame']);consumed.add(index);before=65535
            for age,value in enumerate([*range(4,161,2),161]):
                need(index+age+1<len(chain), 'Complete observed 81-store refill, never a truncated prefix')
                q=chain[index+age+1]
                need(q['pc']==step_pc and int(q['frame'])==frame+age and int(q['before'])==before and int(q['after'])==value and
                     q['a8']==start['a8'] and q['a13']==start['a13'], 'Each native refill step, exact field, previous value, actor and task')
                consumed.add(index+age+1);before=value
            complete+=1
        for index,q in enumerate(chain):
            need(q['at']==address and q['pc'] in (start_pc,step_pc,reset_pc,'FF836700') and
                 (index in consumed or 0<=int(q['before'])<=161 and 0<=int(q['after'])<=161),
                 'Every native slot/writer accounted; invalid HP only in complete original refill')
            need(all(0x01000000<=int(q[k],16)<0x01100000 for k in ('a8','a13')), 'Actual native health-writer actor/task context in RAM')
            if q['pc']=='FF836700':
                need(0<=int(q['after'])<=int(q['before'])<=161, 'Native damage primitive never increases HP')
                if q['after']==q['before']:noops+=1
                else:damage+=1
            elif q['pc']==reset_pc:need(q['after']=='161','Native next-round reset restores full HP')
    return dict(actualHealthStores=len(stores),completeNativeRefillSequences=complete,
        actualNativeDamageDecrements=damage,nativeSameValueStoresNotCreditedAsDamage=noops,
        wholeObservedHPHistoryExplained=True)


def fields(rows):
    need({tag:len(values) for tag,values in rows.items()}==COUNTS, 'Complete exact original native field/input inventory retained')
    for values in rows.values():
        for q in values:
            need(q['human_slot']=='1' and q['fighter']=='sonya' and q['writes']=='0' and q['assistance']=='none', 'Every recorded native field/input remains genuine unassisted Sonya P1')
    rom=rows['ROM'];need(len({q['order'] for q in rom})==6,'All six actual native schedule rows')
    chosen=next(q for q in rom if q['list']=='FFFA3000')
    need(tuple(map(int,chosen['ids'].split(',')))[:7]==OPPONENTS and chosen['table']=='FFFA2C00', 'Actual native cold schedule binds all entered opponents, no proxy IDs')
    live=rows['LIVE'];stages=rows['STAGE'];wins=rows['WIN'];losses=rows['LOSS'];states=rows['STATE']
    need([int(q['stage']) for q in stages]==list(range(7)), 'Cold earned sequential ladder progression0..6')
    need([int(q['frame']) for q in live]==sorted({int(q['frame']) for q in live}), 'Every observed LIVE callback unique and chronologically ordered')
    for q in live:
        stage=int(q['stage']);expected=OPPONENTS[stage]
        need(q['human']=='18:18' and q['cpu']==f'{expected}:{expected}' and q['schedule']=='FFFA3000', 'All live native roster/actor identities true and scheduled')
        need(q['human_actor']!=q['cpu_actor'] and q['human_main']!=q['cpu_main'] and
             all(0x01000000<=int(q[k],16)<0x01100000 for k in ('human_actor','human_main','cpu_actor','cpu_main')),
             'All real published fighter actor/Main contexts valid and distinct')
        need(all(0<=int(h)<=161 for h in q['health'].split(',')), 'All live combat HP fields valid, not native fill sentinels')
    for q in wins:
        side=int(q['slot']);stage=int(q['stage']);expected=18 if side==1 else OPPONENTS[stage]
        need(side in (1,2) and int(q['id'])==expected and q['entry']==f'{0xfffef800+expected*32:08X}' and q['pc']=='FF8296B0',
             'Every actual native winner dispatch preserves actual winning fighter ID and instruction')
        hp=list(map(int,q['health'].split(',')))
        need(hp[side-1]>hp[2-side], 'Native winner health agrees with victory, including ordinary timeout wins')
        witness=[s for s in states if int(s['frame'])==int(q['frame'])+1]
        need(witness and witness[0]['winner']==str(side) and witness[0]['health']==q['health'] and witness[0]['mode'] in ('5','11'),
             'Every original winner call followed by the actual native winner scene, not assumed activation')
    for previous,current in zip(stages,stages[1:]):
        stage=previous['stage'];end=int(current['frame'])
        after=max([int(q['frame']) for q in losses if q['stage']==stage and int(q['frame'])<end]+[int(previous['frame'])])
        earned=[q for q in wins if q['stage']==stage and q['slot']=='1' and after<int(q['frame'])<end]
        need(len(earned)>=2 and current['schedule']=='FFFA3000' and any(q['stage']==current['stage'] and int(q['frame'])>=end for q in live),
             'Every advancement follows two own wins in the same successful attempt, not accumulated failed rounds')
    selections=rows['SELECT'];confirmed=rows['SELECT_ID'];inputs=rows['INPUT']
    need([int(q['number']) for q in selections]==list(range(1,75)), 'All genuine sequential cold/paid selections')
    for q in selections:
        need(q['target']=='18' and q['schedule']=='FFFA3000', 'Physical native selection target true Sonya, schedule unchanged')
        selected=[s for s in confirmed if s['number']==q['number']]
        need(len(selected)==2 and all(s['roster']=='18' and s['state']=='3' for s in selected), 'Both actual native confirmation fields retain true Sonya')
    for q in losses:
        frame=int(q['frame']);number=str(int(q['number'])+1)
        need(any(s['number']==number and int(s['frame'])==frame+360 for s in selections), 'Every earned loss followed by actual360-field physical continue selection')
        for button,age in (('Coin_1',116),('1_Player_Start',156)):
            need(any(s['button']==button and int(s['frame'])==frame+age for s in inputs), 'Actual paid coin/start edges recorded for every native continue')
    need(sum(q['stage']=='6' for q in losses)>=47 and not any(q['stage']=='6' and q['slot']=='1' for q in wins), 'Failed Baraka policy never relabelled as earned seventh victory')
    health=health_history(rows['HEALTH'])
    return dict(verifiedCompletedOpponentIDs=list(OPPONENTS[:6]),verifiedCompletedOpponentNames=['Kano','Jax','Raiden','Kitana','Kung Lao','Sonya'],
        reachedStage=6,failedOpponent='Baraka',fullTowerAccepted=False,liveFields=len(live),nativeWinnerCalls=len(wins),
        physicalInputEdges=len(inputs),physicalPaidLosses=len(losses),nativeHealth=health)


def run():
    need(not OUT.exists(),'Fresh exact first-six-fight finite verification')
    saved=json.loads((preserved.OUT/'report.json').read_text());retired=json.loads((preserved.RETIRED/'report.json').read_text())
    proof=json.loads((FOLDER/'guest_memory_proof.json').read_text());result=json.loads((FOLDER/'result.json').read_text())
    source_kernel=ROOT/'audit_native_sonya_first_four_ladder_refills_initializer/report.json'
    kernel=json.loads(source_kernel.read_text())
    need(saved['preservationPassed'] and not saved['passed'] and retired['passed'] and
         all(sha(p)==h for report in (saved,retired) for p,h in report['inputHashes'].items()) and
         proof['everyActualByteComparedInRAM'] and proof['bytes']==1048576 and
         proof['sha256']==kernel['wholeExpectedGuestSHA256']==result['guestSHA256'] and
         not result['passed'] and not result['nativeCacheOverrunObserved'] and not (FOLDER/'stderr.log').read_text().strip(),
         'Whole current actual native guest, source-native refill kernel, exact retired failed transport and all frozen inputs')
    text=gzip.open(FOLDER/'run.log.gz','rt',encoding='utf-8').read()
    need(not re.search(r'MK2_CURRENT_CAMPAIGN_CACHE_FAILURE |MK2_MILEENA_CAMPAIGN_OVERRUN |MK2_NAT_CAMPAIGN_ENDING_COMPLETED |MK2_POSTENDING_COMPLETE |LUA ERROR|stack traceback',text),
         'No observed corruption; missing ending/join remain unaccepted')
    rows={tag:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')] for tag in COUNTS}
    positive=fields(rows);faults=[]
    trials=[]
    for stage in range(7):
        indices=[i for i,q in enumerate(rows['LIVE']) if q['stage']==str(stage)]
        for index in (indices[0],indices[len(indices)//2],indices[-1]):
            for field,value in (('human','1:1'),('cpu','18:1'),('human_main','00000000')):trials.append(('LIVE',index,field,value))
    trials += [('STAGE',i,'schedule','00000000') for i in range(7)]
    trials += [('WIN',i,'slot','2') for i,q in enumerate(rows['WIN']) if q['slot']=='1']
    for pc in ('FF9DECE0','FF9DED10','FF9DEF40','FF9DEF70'):
        index=next(i for i,q in enumerate(rows['HEALTH']) if q['pc']==pc)
        trials.append(('HEALTH',index,'after','65534' if pc in ('FF9DECE0','FF9DED10') else '5'))
    trials += [('HEALTH',0,'pc','FF838860'),('SELECT_ID',0,'roster','1'),('SELECT_ID',147,'state','1')]
    for tag,index,key,value in trials:
        bad=dict(rows);bad[tag]=list(rows[tag]);bad[tag][index]=dict(bad[tag][index],**{key:value})
        try: fields(bad)
        except (ValueError,IndexError,StopIteration) as error:faults.append(dict(tag=tag,row=index,field=key,rejectedBy=str(error)))
        else:raise ValueError('False native ladder evidence admitted')
    for tag,index in (('LIVE',0),('STAGE',3),('WIN',0),('HEALTH',0),('SELECT_ID',0),('INPUT',0)):
        bad=dict(rows);bad[tag]=rows[tag][:index]+rows[tag][index+1:]
        try:fields(bad)
        except ValueError as error:faults.append(dict(tag=tag,row=index,field='missing',rejectedBy=str(error)))
        else:raise ValueError('Omitted actual native evidence admitted')
    need(fields(rows)==positive,'Whole original positive native chronology unchanged after all faults')
    OUT.mkdir()
    pins=dict(saved['inputHashes'])
    for p in (preserved.OUT/'report.json',preserved.RETIRED/'report.json',source_kernel,Path(__file__).resolve()):pins[str(p)]=sha(p)
    (OUT/'report.json').write_text(json.dumps(dict(passed=True,finiteFirstSixLadderProgressionAccepted=True,
        actualNativeGame=preserved.GAME,actualRAMParent=preserved.PARENT,accepted=positive,semanticFaultsRejected=faults,
        currentWholeGuestSHA256=proof['sha256'],completeChronologySHA256=hashlib.sha256(text.encode()).hexdigest().upper(),
        completeOriginalInventory=COUNTS,originalFailedCampaignTransportPreserved=True,
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,KanoCampaignAccepted=False,
        artAccepted=False,audioAccepted=False,allFinishersAccepted=False,fullPortAcceptance=False,
        originalNaturalIntegrationRequirements=saved['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=saved['originalRemainingWorkGroups'],
        inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteFirstSixLadderProgressionAccepted=True,accepted=positive,
        semanticFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual original qualification outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
