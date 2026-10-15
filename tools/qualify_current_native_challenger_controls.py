"""Stock versus added input observation; never label an unaccepted join a success."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_native_challenger_controls_checked';assert not out.exists()
cases=[]
for label,identity in [('added',18),('stock',3)]:
 folder=sync.ROOT/f'audit_current_native_challenger_{label}_control_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None
 rows=chronology.load(folder/'run.log')
 trigger=rows['JOIN_TRIGGER'];assert len(trigger)==1
 assert trigger[0]['live_age']=='180' and int(trigger[0]['id'])==int(trigger[0]['roster'])==identity and trigger[0]['state']=='0'
 inputs=rows['JOIN_INPUT']
 assert [(r['button'],int(r['age'])) for r in inputs]==[('Coin_1',n) for n in range(1,5)]+[('Start_1',n) for n in range(24,28)]
 states=rows['JOIN_PLAYER_STATE']
 assert not any(r['p1']=='3' for r in states)
 coin=[r for r in states if 2<=int(r['age'])<=4]
 start=[r for r in states if 25<=int(r['age'])<=27]
 assert len(coin)==len(start)==3
 assert all(int(r['in1'])&1==0 for r in coin) and all(int(r['in1'])&4==0 for r in start)
 selection=int(rows['JOIN_SELECTION'][0]['frame'])
 assert rows['LOSS'] and int(rows['LOSS'][-1]['frame'])<selection
 resumed=next(r for r in rows['SELECT'] if int(r['frame'])>=selection)
 assert resumed['continue']==rows['LOSS'][-1]['frame']
 cases.append({'control':label,'initialCpuID':identity,'coinAndStartBitsObservedActive':True,
               'newP1JoinProven':False,'P2PaidContinueObserved':True,'selectionFrame':selection,
               'logSHA256':sync.sha(folder/'run.log'),'terminalSHA256':sync.sha(folder/'terminal.json')})
out.mkdir();(out/'report.json').write_text(json.dumps({'passedObservationChecks':True,'cases':cases,
 'addedSpecificJoinDefectEstablished':False,'originalUnmodifiedMk2ComparisonDone':False,
 'nextAction':'Inspect actual native IN1 reader PC and start-acceptance path; inputs appear active for both stock and added CPU cases.',
 'fullPortAccepted':False},indent=2))
print(json.dumps({'passedObservationChecks':True,'cases':cases}))
