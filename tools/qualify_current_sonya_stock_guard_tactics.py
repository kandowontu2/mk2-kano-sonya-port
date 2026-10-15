"""Finite historical-policy trials, not full restoration/clear acceptance."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

def gate(rows,side):
 assert all(r['writes']=='0' and r['assistance']=='none' and int(r['human_slot'])==side for group in rows.values() for r in group)
 assert rows['RESULT'][0]['frame']=='18000'
 assert all(r['human']=='18:18' for r in rows['LIVE']+rows['FIGHT'])
 stages=[int(r['stage']) for r in rows['STAGE']];assert stages==[0,1]
 wins=[r for r in rows['WIN'] if int(r['slot'])==side]
 for win in wins:
  hp=list(map(int,win['health'].split(',')))
  assert win['pc']=='FF8296B0' and win['id']=='18' and hp[side-1]>hp[2-side]>=0
 assert len([r for r in wins if r['stage']=='0'])>=2
 assert not [r for r in wins if r['stage']=='1']
 return {'side':side,'stages':stages,'secondOpponentID':int(next(r for r in rows['FIGHT'] if r['stage']=='1')['cpu'].split(':')[0]),'secondOpponentOwnRoundWins':0}

if __name__=='__main__':
 sync.verify();cases=[]
 for side in (1,2):
  folder=sync.ROOT/f'audit_current_sonya_stock_guard_tactics_p{side}_runtime'
  terminal=json.loads((folder/'terminal.json').read_text())
  assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
  rows=chronology.load(folder/'run.log');case=gate(rows,side)
  bad=copy.deepcopy(rows);bad['FIGHT'][0]['human']='18:1'
  try:gate(bad,side)
  except AssertionError:pass
  else:raise AssertionError('Proxy accepted')
  case.update(logSHA256=sync.sha(folder/'run.log'),proxyFaultRejected=True);cases.append(case)
 out=sync.ROOT/'audit_current_sonya_stock_guard_tactics_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'classification':'finite controller failures at second opponent','cases':cases,'fullPortAccepted':False},indent=2))
 print('PASS finite two-slot true-ID evidence; stock guard controllers failed second opponents')
