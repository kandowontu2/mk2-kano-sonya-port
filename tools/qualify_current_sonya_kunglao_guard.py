"""Finite guarded Kung Lao trial, with unchanged earned earlier ladder prefix."""
import copy
import json
import check_campaign_stage_chronology as chronology
import qualify_current_sonya_defensive_routes as base
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_kunglao_guard_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
 rows=chronology.load(folder/'run.log');old=chronology.load(sync.ROOT/'audit_current_sonya_defensive_routes_p1_runtime/run.log')
 cutoff=int(next(r for r in old['FIGHT'] if r['stage']=='4')['frame'])
 for tag in set(old)|set(rows):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]
 result=base.gate(rows,1)
 bad=copy.deepcopy(rows);bad['FIGHT'][0]['human']='18:1'
 try:base.gate(bad,1)
 except AssertionError:pass
 else:raise AssertionError('Proxy accepted')
 result.update(passedObservationChecks=True,unchangedEarnedPrefixThrough=cutoff-1,kungLaoRoundWins=[r for r in rows['WIN'] if r['stage']=='4' and r['slot']=='1'],fullPortAccepted=False,proxyFaultRejected=True,logSHA256=sync.sha(folder/'run.log'))
 out=sync.ROOT/'audit_current_sonya_kunglao_guard_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result))
