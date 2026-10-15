"""Accepted native challenger join and selector audio cleanup, stock/added controls."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync


def gate(rows,identity):
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 trigger=rows['JOIN_TRIGGER'];selection=rows['JOIN_SELECTION'];done=rows['JOIN_COMPLETE']
 assert len(trigger)==len(selection)==len(done)==1
 assert int(trigger[0]['id'])==int(trigger[0]['roster'])==identity and trigger[0]['state']=='0'
 assert not rows.get('LOSS')
 assert [(r['button'],int(r['age'])) for r in rows['JOIN_INPUT']]==[('Coin_1',n) for n in list(range(1,5))+list(range(41,45))]+[('Start_1',n) for n in range(64,68)]
 start=int(selection[0]['age'])
 assert int(done[0]['frame'])-int(selection[0]['frame'])==160
 states=[r for r in rows['JOIN_PLAYER_STATE'] if int(r['age'])>=start]
 assert [int(r['age']) for r in states]==list(range(start,start+161))
 assert all(r['mode']=='4' and r['p1']=='3' for r in states)
 assert all(r['p2']=='3' for r in states[1:])
 for side in (1,2):
  owners=[r for r in rows['JOIN_OWNER'] if int(r['age'])>=start and int(r['slot'])==side]
  assert len(owners)==161 and all(r['actor']==r['main']=='00000000' and r['id']=='0' for r in owners)
 for channel in range(10,19):
  fields=[r for r in rows['JOIN_CHANNEL'] if int(r['age'])>=start and int(r['channel'])==channel]
  assert [int(r['age']) for r in fields]==list(range(start,start+161))
  assert all(int(r['length'])==0 or int(r['sample']) in (-1,4294967295) for r in fields)
  assert len({r['pos'] for r in fields})==1
 return {'initialCpuID':identity,'acceptedNativeP1Join':True,'bothPlayersSelecting':True,
         'selectionFields':161,'battleFinishAudioCleanup':True,'gameLossNotUsed':True}


if __name__=='__main__':
 sync.verify()
 out=sync.ROOT/'audit_current_native_challenger_two_coins_checked';assert not out.exists()
 cases=[]
 for label,identity in [('added',18),('stock',3)]:
  folder=sync.ROOT/f'audit_current_native_challenger_two_coins_{label}_runtime'
  terminal=json.loads((folder/'terminal.json').read_text())
  assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
  rows=chronology.load(folder/'run.log')
  result=gate(rows,identity)
  bad=copy.deepcopy(rows)
  start=int(rows['JOIN_SELECTION'][0]['age'])
  next(r for r in bad['JOIN_PLAYER_STATE'] if int(r['age'])>=start)['p1']='0'
  try:gate(bad,identity)
  except AssertionError:pass
  else:raise AssertionError('Unaccepted join accepted')
  result.update(control=label,logSHA256=sync.sha(folder/'run.log'),terminalSHA256=sync.sha(folder/'terminal.json'),falseJoinFaultRejected=True)
  cases.append(result)
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,
  'coinageSettingsChanged':False,'bothAddedCharactersAsJoinedPlayersCovered':False,
  'heardAudioQualityVerified':False,'fullPortAccepted':False},indent=2))
 print('PASS native two-credit challenger join, stock and added CPU, both selector states/audio cleanup')
