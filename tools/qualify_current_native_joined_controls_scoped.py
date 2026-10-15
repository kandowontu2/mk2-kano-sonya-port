"""Joined real-ID physical movement/normal attacks through native round result."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync


def gate(rows,targets):
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 assert not rows.get('LOSS')
 assert len(rows['JOIN_TRIGGER'])==1 and rows['JOIN_TRIGGER'][0]['id']==rows['JOIN_TRIGGER'][0]['roster']=='18'
 assert [(r['button'],int(r['age'])) for r in rows['JOIN_INPUT']]==[('Coin_1',n) for n in list(range(1,5))+list(range(41,45))]+[('Start_1',n) for n in range(64,68)]
 assert len(rows['JOINED_SELECTED'])==2
 for side,target in enumerate(targets,1):
  selected=next(r for r in rows['JOINED_SELECTED'] if int(r['slot'])==side)
  assert int(selected['actual'])==int(selected['target'])==target
  fields=[r for r in rows['JOINED_MATCH_PAIR'] if int(r['slot'])==side]
  assert len(fields)>1000 and [int(r['age']) for r in fields]==list(range(len(fields)))
  assert all(int(r['id'])==int(r['roster'])==target and r['state']=='1' and r['owner']==r['actor'] for r in fields)
  assert len({(r['actor'],r['main']) for r in fields})==1
  assert {257,259}.issubset({int(r['action']) for r in fields})
  assert max(int(r['x']) for r in fields)-min(int(r['x']) for r in fields)>10
  inputs=[r for r in rows['JOINED_CONTROL'] if int(r['slot'])==side]
  assert {'High_Punch','High_Kick','Up'}.issubset({r['button'] for r in inputs})
 wins=rows['WIN'];assert len(wins)==1
 win=wins[0];assert win['pc']=='FF8296B0' and win['slot']=='2' and int(win['id'])==targets[1] and win['health']=='0,161'
 last=max(int(r['frame']) for r in rows['JOINED_MATCH_PAIR'])
 assert int(win['frame'])==last+1
 assert rows['JOINED_CONTROL_WINDOW_END'][0]['elapsed_fields']=='1600'
 return {'targets':targets,'pairedGameplayFields':len(fields),'actualPunchAndKickBothSlots':True,'actualMovementBothSlots':True,'nativeRoundWinnerID':targets[1],'jumpActivationProven':False}


if __name__=='__main__':
 sync.verify()
 out=sync.ROOT/'audit_current_native_joined_controls_scoped_checked';assert not out.exists()
 cases=[]
 for targets in ([17,18],[18,17]):
  folder=sync.ROOT/f'audit_current_native_joined_controls_scoped_{targets[0]}_{targets[1]}_runtime'
  terminal=json.loads((folder/'terminal.json').read_text())
  assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
  assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
  rows=chronology.load(folder/'run.log');case=gate(rows,targets)
  for key,field,value in [('JOINED_MATCH_PAIR','id','1'),('JOINED_MATCH_PAIR','owner','00000000'),('WIN','id','1')]:
   bad=copy.deepcopy(rows);bad[key][0][field]=value
   try:gate(bad,targets)
   except AssertionError:pass
   else:raise AssertionError('Injected proxy/owner/winner fault accepted')
  case.update(logSHA256=sync.sha(folder/'run.log'),terminalSHA256=sync.sha(folder/'terminal.json'),faultsRejected=True)
  cases.append(case)
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,'fullPortAccepted':False,'allJoinedMovesVerified':False,'gameSourceChanged':False},indent=2))
 print('PASS both joined arrangements: real actors, movement, punches, kicks, native KO winner')
