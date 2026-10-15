"""Earned native finite ladder chronology and actual continued Sonya IDs."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

def gate(rows,side):
 assert all(r['writes']=='0' and r['assistance']=='none' and int(r['human_slot'])==side for group in rows.values() for r in group)
 assert rows['BOOT'][0]['strategy']=='defensive_leg' and rows['BOOT'][0]['boot']=='600'
 assert rows['RESULT'][0]['frame']=='18000'
 assert all(r['human']=='18:18' for r in rows['LIVE']+rows['FIGHT'])
 assert all(r['roster']=='18' for r in rows['SELECT_ID'])
 assert all(r['target']=='18' for r in rows['SELECT_INITIALIZED'])
 stages=rows['STAGE'];actual=[int(r['stage']) for r in stages]
 assert actual==list(range(len(actual)))
 wins=[r for r in rows['WIN'] if int(r['slot'])==side]
 for win in wins:
  health=list(map(int,win['health'].split(',')))
  assert win['id']=='18' and win['pc']=='FF8296B0' and health[side-1]>health[2-side]>=0
 for previous,current in zip(stages,stages[1:]):
  earned={int(r['frame']) for r in wins if r['stage']==previous['stage'] and int(previous['frame'])<=int(r['frame'])<int(current['frame'])}
  assert len(earned)>=2
 return {'side':side,'earnedStages':actual,'earnedOwnRoundWins':len(wins),'paidLosses':len(rows.get('LOSS',[])),'fullCampaignClear':False}

if __name__=='__main__':
 sync.verify();cases=[]
 for side in (1,2):
  folder=sync.ROOT/f'audit_current_sonya_defensive_routes_p{side}_runtime'
  terminal=json.loads((folder/'terminal.json').read_text())
  assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
  assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
  rows=chronology.load(folder/'run.log');case=gate(rows,side)
  bad=copy.deepcopy(rows);bad['FIGHT'][0]['human']='18:1'
  try:gate(bad,side)
  except AssertionError:pass
  else:raise AssertionError('Proxy accepted')
  case.update(logSHA256=sync.sha(folder/'run.log'),proxyFaultRejected=True);cases.append(case)
 out=sync.ROOT/'audit_current_sonya_defensive_routes_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,'fullPortAccepted':False,'gameSourceChanged':False},indent=2))
 print(json.dumps(cases))
