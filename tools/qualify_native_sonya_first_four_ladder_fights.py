"""Finite earned Sonya ladder progression; failed fifth fight stays false.

All received native LIVE fields, selections, health-store observations and
winner reads are checked. No artwork/audio/ending/full-port acceptance.
"""
import copy
import gzip
import hashlib
import json
import re
from pathlib import Path
import retire_native_raiden_guard_losing_kung_lao as preserved

ROOT, need, sha = preserved.ROOT, preserved.need, preserved.sha
FOLDER = preserved.capture.OUT
OUT = ROOT / 'audit_native_sonya_first_four_ladder_fights_checked'


def fields(rows):
    live, stages, selected, wins, losses, health, rom = [rows[tag] for tag in
        ('LIVE','STAGE','SELECT_ID','WIN','LOSS','HEALTH','ROM')]
    need(len(live)==7116 and len(stages)==5 and [int(q['stage']) for q in stages]==list(range(5)),
         'Entire original LIVE and stage inventory, not a convenient subset')
    actual_schedule=next(q for q in rom if q['list']=='FFFA3000')
    expected_cpu=[int(q) for q in actual_schedule['ids'].split(',')]
    need(expected_cpu[:5]==[17,11,7,4,0] and len(expected_cpu)==17,
         'Actual native cold-boot schedule retains true Kano/Jax/Raiden/Kitana/Kung Lao IDs')
    for collection in rows.values():
        for q in collection:
            need(q['human_slot']=='1' and q['fighter']=='sonya' and q['writes']=='0' and q['assistance']=='none',
                 'Every actual native field unassisted true human Sonya P1')
    need([int(q['frame']) for q in live]==sorted({int(q['frame']) for q in live}), 'Complete ordered unique LIVE callbacks')
    for q in live:
        stage=int(q['stage']); expected=expected_cpu[stage]
        need(q['human']=='18:18' and q['cpu']==f'{expected}:{expected}' and q['schedule']=='FFFA3000',
             'Every native actor/roster identity follows actual schedule, never a stock proxy')
        need(all(0x01000000<=int(q[k],16)<0x01100000 for k in ('human_actor','human_main','cpu_actor','cpu_main')) and
             q['human_actor']!=q['cpu_actor'] and q['human_main']!=q['cpu_main'], 'Every current actor/Main context in native RAM')
        need(len(q['health'].split(','))==2 and all(0<=int(h)<=161 for h in q['health'].split(',')), 'All actual fighter HP fields bounded')
    for q in stages:
        stage=int(q['stage']); frame=int(q['frame'])
        need(q['schedule']=='FFFA3000' and any(int(v['stage'])==stage and int(v['frame'])>=frame for v in live),
             'Each entered stage has resumed true native fighter fields')
        if stage:
            prior=stages[stage-1]
            earned=[w for w in wins if w['slot']=='1' and int(w['stage'])==stage-1 and int(prior['frame'])<int(w['frame'])<frame]
            need(len(earned)>=2, 'Earned own native round winner entries precede every ladder advancement')
    for q in selected:
        need(q['roster']=='18' and q['state']=='3', 'All physical paid reselections retain true Sonya')
    for q in wins:
        expected=18 if q['slot']=='1' else expected_cpu[int(q['stage'])]
        need(q['slot'] in ('1','2') and int(q['id'])==expected and q['entry']==f'{0xfffef800+expected*32:08X}' and
             q['pc']=='FF8296B0', 'All actual native winner dispatch identities and instructions match')
    for q in health:
        need(q['slot'] in ('1','2') and 0<=int(q['before'])<=161 and 0<=int(q['after'])<=161,
             'All observed original native health stores bounded; observers never return replacement data')
    for q in losses:
        frame=int(q['frame'])
        need(any(s['number']==str(int(q['number'])+1) and frame<int(s['frame'])<=frame+500 for s in selected),
             'Every earned paid loss has actual subsequent physical native Sonya reselection')
    need(sum(q['stage']=='4' for q in losses)==88 and not any(q['slot']=='1' and q['stage']=='4' for q in wins),
         'Unsuccessful fifth-fight policy preserved, never qualified as completed tower')
    return dict(nativeLiveFields=len(live),nativeWinnerReads=len(wins),nativeHealthStores=len(health),
        physicalSelectionFields=len(selected),actualPaidLosses=len(losses),reachedStage=4,
        firstFourOpponentIDs=expected_cpu[:4],firstFourOpponentNames=['Kano','Jax','Raiden','Kitana'],
        fifthOpponentID=0,fifthOpponentName='Kung Lao',fifthFightAccepted=False)


def run():
    need(not OUT.exists(), 'Fresh finite progression qualification')
    retained=json.loads((preserved.OUT/'report.json').read_text())
    retired=json.loads((preserved.RETIRED/'report.json').read_text())
    proof=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    metadata=json.loads((FOLDER/'result.json').read_text())
    need(retained['preservationPassed'] and not retained['passed'] and retired['passed'] and
         all(sha(p)==h for report in (retained,retired) for p,h in report['inputHashes'].items()) and
         proof['everyActualByteComparedInRAM'] and proof['bytes']==1048576 and
         proof['sha256']==metadata['guestSHA256']=='8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479' and
         not metadata['passed'] and not metadata['nativeCacheOverrunObserved'] and not (FOLDER/'stderr.log').read_text().strip(),
         'Same terminal failed transport, frozen inputs, entire verified actual repaired native guest')
    text=gzip.open(FOLDER/'run.log.gz','rt',encoding='utf-8').read()
    parse=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    rows={tag:parse(tag) for tag in ('LIVE','STAGE','SELECT_ID','WIN','LOSS','HEALTH','ROM')}
    need(not any(tag in text for tag in ('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ',
        'MK2_NAT_CAMPAIGN_ENDING_COMPLETED ','MK2_POSTENDING_COMPLETE ','LUA ERROR','stack traceback')), 'No observed corruption/ending/join in finite failed trial')
    accepted=fields(rows)
    faults=[]
    cases=[]
    for stage in range(5):
        indices=[i for i,q in enumerate(rows['LIVE']) if q['stage']==str(stage)]
        for index in (indices[0],indices[len(indices)//2],indices[-1]):
            for key,value in (('human','1:1'),('cpu','18:1'),('writes','1'),('assistance','memory'),('human_actor','00000000')):
                cases.append(('LIVE',index,key,value))
    cases += [('STAGE',i,'stage','6') for i in range(5)]
    cases += [('SELECT_ID',i,'roster','1') for i in (0,len(rows['SELECT_ID'])//2,len(rows['SELECT_ID'])-1)]
    cases += [('WIN',i,'entry','FFFEF800') for i,q in enumerate(rows['WIN']) if q['slot']=='1']
    cases += [('ROM',0,'ids',rows['ROM'][0]['ids'].replace('17,11,7','1,11,7'))]
    for tag,index,key,value in cases:
        bad=copy.deepcopy(rows);bad[tag][index][key]=value
        try: fields(bad)
        except (ValueError,StopIteration,IndexError) as error:
            faults.append(dict(tag=tag,row=index,field=key,rejectedBy=str(error)))
        else: raise ValueError('False native progression field admitted')
    for tag,index in [('LIVE',0),('STAGE',2),('SELECT_ID',0)]:
        bad=copy.deepcopy(rows);bad[tag].pop(index)
        try: fields(bad)
        except ValueError as error: faults.append(dict(tag=tag,row=index,field='missing',rejectedBy=str(error)))
        else: raise ValueError('Omitted original native evidence admitted')
    OUT.mkdir()
    pins=dict(retained['inputHashes'])
    for p in (Path(__file__).resolve(),preserved.OUT/'report.json',preserved.RETIRED/'report.json'):
        pins[str(p)]=sha(p)
    (OUT/'report.json').write_text(json.dumps(dict(passed=True,finiteFirstFourLadderProgressionAccepted=True,
        actualNativeGame=preserved.GAME,actualRAMParent=preserved.PARENT,accepted=accepted,
        semanticFaultsRejected=faults,originalCampaignTransportPassed=False,
        currentWholeGuestSHA256=proof['sha256'],completeChronologySHA256=hashlib.sha256(text.encode()).hexdigest().upper(),
        artAccepted=False,audioAccepted=False,allFinishersAccepted=False,fullTowerAccepted=False,endingAccepted=False,
        freshJoinAccepted=False,KanoCampaignAccepted=False,fullPortAcceptance=False,
        originalNaturalIntegrationRequirements=retained['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=retained['originalRemainingWorkGroups'],inputHashes=pins,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteFirstFourLadderProgressionAccepted=True,accepted=accepted,
        semanticFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)


if __name__ == '__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(), 'Never overwrite an original qualification outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
