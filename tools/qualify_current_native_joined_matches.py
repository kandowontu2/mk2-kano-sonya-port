"""Check genuine paid challenger joins through both real-ID match arrangements."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync


def gate(rows, targets):
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 assert not rows.get('LOSS')
 assert len(rows['JOIN_TRIGGER'])==len(rows['JOIN_SELECTION'])==1
 assert rows['JOIN_TRIGGER'][0]['id']==rows['JOIN_TRIGGER'][0]['roster']=='18'
 assert rows['JOIN_TRIGGER'][0]['state']=='0'
 assert [(r['button'],int(r['age'])) for r in rows['JOIN_INPUT']]==[('Coin_1',n) for n in list(range(1,5))+list(range(41,45))]+[('Start_1',n) for n in range(64,68)]
 start=int(rows['JOIN_SELECTION'][0]['age'])
 selecting=[r for r in rows['JOIN_PLAYER_STATE'] if int(r['age'])>=start and r['mode']=='4']
 assert len(selecting)>140 and all(r['p1']=='3' for r in selecting)
 assert all(r['p2']=='3' for r in selecting[1:])
 routes=rows['JOINED_ROUTE'];selected=rows['JOINED_SELECTED']
 assert len(routes)==len(selected)==2
 for side,target in enumerate(targets,1):
  route=next(r for r in routes if int(r['slot'])==side)
  choice=next(r for r in selected if int(r['slot'])==side)
  assert int(route['target'])==int(choice['target'])==int(choice['actual'])==target
  fields=[r for r in rows['JOINED_MATCH_PAIR'] if int(r['slot'])==side]
  assert [int(r['age']) for r in fields]==list(range(161))
  assert all(int(r['id'])==int(r['roster'])==target and r['state']=='1' and r['owner']==r['actor'] for r in fields)
  assert len({(r['actor'],r['main']) for r in fields})==1
  assert all(0x01000000<=int(r['actor'],16)<0x01100000 and 0x01000000<=int(r['main'],16)<0x01100000 for r in fields)
 assert len(rows['JOINED_MATCH_COMPLETE'])==1 and rows['JOINED_MATCH_COMPLETE'][0]['fields']=='161'
 return {'targets':targets,'acceptedPaidChallengerJoin':True,'actualSelectedIDs':True,'stableJoinedMatchFieldsPerSlot':161}


if __name__=='__main__':
 sync.verify()
 out=sync.ROOT/'audit_current_native_joined_matches_checked';assert not out.exists()
 cases=[]
 for targets in ([17,18],[18,17]):
  folder=sync.ROOT/f'audit_current_native_joined_{targets[0]}_{targets[1]}_runtime'
  terminal=json.loads((folder/'terminal.json').read_text())
  assert terminal['exitCode']==0 and terminal['limitReason'] is None
  assert not (folder/'stderr.log').read_text().strip()
  assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
  rows=chronology.load(folder/'run.log');case=gate(rows,targets)
  for key,field,value in [('JOINED_MATCH_PAIR','id','1'),('JOINED_MATCH_PAIR','owner','00000000'),('JOINED_SELECTED','actual','1')]:
   bad=copy.deepcopy(rows);bad[key][0][field]=value
   try:gate(bad,targets)
   except AssertionError:pass
   else:raise AssertionError(f'Accepted injected {key}/{field} fault')
  case.update(logSHA256=sync.sha(folder/'run.log'),terminalSHA256=sync.sha(folder/'terminal.json'),proxyOwnerSelectionFaultsRejected=True)
  cases.append(case)
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,'fullPortAccepted':False,'joinedCombatMovesVerified':False,'gameSourceChanged':False},indent=2))
 print('PASS both paid joined-match arrangements, initialized selections and real-ID actor ownership')
