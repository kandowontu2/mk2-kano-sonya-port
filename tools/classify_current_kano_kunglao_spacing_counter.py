"""Observation only: full continue gate failed at bounded pending-loss tail."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kunglao_spacing_counter_runtime'
out=sync.ROOT/'audit_current_kano_kunglao_spacing_counter_classified'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_kano_standing_counter_long_runtime/run.log')
for tag in set(rows)|set(old):
    if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL','KUNGLAO_ACTION_CHANGE','KUNGLAO_DAMAGE_DETAIL'):continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<18097]==[r for r in old.get(tag,[]) if int(r['frame'])<18097],tag
stages=chronology.check(rows,1,17,list(range(17)))
assert rows['RESULT'][0]['frame']=='24000'
assert len(rows['SELECT'])==len(rows['LOSS'])==3
for loss,selection in zip(rows['LOSS'][:-1],rows['SELECT'][1:]):
    assert selection['continue']==loss['frame']
assert int(rows['LOSS'][-1]['frame'])>int(rows['SELECT'][-1]['frame'])
tail=rows['STATE'][-1]
assert tail['mode']=='3' and tail['states']=='2,0' and tail['roster']=='17,0'
assert all(r['human']=='17:17' for r in rows['LIVE'])
assert all(r['ids']=='17,0' for r in rows['KUNGLAO_ACTION_CHANGE']+rows['KUNGLAO_DAMAGE_DETAIL'])
starts=[];previous=None
for r in rows['KUNGLAO_ACTION_CHANGE']:
    current=(r['p1_main'],r['actions'].split(',')[0])
    if current[1]=='259' and current!=previous:starts.append(r)
    previous=current
damage=rows['KUNGLAO_DAMAGE_DETAIL']
contacts=[r for r in damage if r['victim_slot']=='2' and r['actions'].split(',')[0]=='259' and r['a8']==r['p1_actor'] and r['a13']==r['p1_main']]
wins=[r for r in rows['WIN'] if r['stage']=='4' and r['slot']=='1']
incoming={}
for r in damage:
    if r['victim_slot']=='1':
        action=r['actions'].split(',')[1]
        entry=incoming.setdefault(action,dict(callbacks=0,damage=0))
        entry['callbacks']+=1;entry['damage']+=int(r['before'])-int(r['after'])
report=dict(observationCompleted=True,originalWholeContinueGatePassed=False,reason='Final native loss23784 still pending paid selection at host bound24000; no claim of completed last continue.',priorProductiveRouteExact=True,observedStages=stages,pendingLoss=rows['LOSS'][-1],terminalState=tail,nativeStandingKickStarts=len(starts),nativeOwnKickContacts=contacts,totalOutgoingNativeDamage=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),incomingByCpuActionAtCallback=incoming,ownKungLaoRoundWins=wins,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),strategyMatchClear=False,gameDefectEstablished=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(observationCompleted=True,originalWholeContinueGatePassed=False,standingKicks=len(starts),ownContacts=len(contacts),outgoing=report['totalOutgoingNativeDamage'],incomingByCpuAction=incoming,ownRounds=len(wins))))
