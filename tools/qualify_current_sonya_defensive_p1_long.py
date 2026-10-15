"""Original finite true-ID/earned-stage gates plus exact long-run prefix."""
import copy
import inspect
import json
import check_campaign_stage_chronology as chronology
import qualify_current_sonya_defensive_routes as base
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_defensive_p1_long_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
 rows=chronology.load(folder/'run.log');old=chronology.load(sync.ROOT/'audit_current_sonya_defensive_routes_p1_runtime/run.log')
 for tag in set(old)|set(rows):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<18000]==[r for r in rows.get(tag,[]) if int(r['frame'])<18000]
 code=inspect.getsource(base.gate);assert code.count("'18000'")==1
 context={};exec(compile(code.replace("'18000'","'30000'"),__file__+'::extended gate','exec'),context)
 result=context['gate'](rows,1)
 bad=copy.deepcopy(rows);bad['FIGHT'][0]['human']='18:1'
 try:context['gate'](bad,1)
 except AssertionError:pass
 else:raise AssertionError('Proxy accepted')
 result.update(passed=True,exact18000FieldPrefix=True,proxyFaultRejected=True,logSHA256=sync.sha(folder/'run.log'),fullPortAccepted=False)
 out=sync.ROOT/'audit_current_sonya_defensive_p1_long_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result))
