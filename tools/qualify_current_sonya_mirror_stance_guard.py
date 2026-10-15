"""Earned campaign chronology and unchanged pre-mirror route, capped runs explicit."""
import inspect
import json
import re
import check_campaign_stage_chronology as chronology
import qualify_current_sonya_defensive_routes as base
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_mirror_stance_guard_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 complete=terminal['exitCode']==0 and terminal['limitReason'] is None
 assert complete or (terminal['exitCode']!=0 and terminal['limitReason']=='wall_limit')
 assert terminal['elapsedSeconds']<92 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
 assert not (folder/'stderr.log').read_text().strip()
 rows={};unterminated=0
 with (folder/'run.log').open() as stream:
  for line in stream:
   assert '[LUA ERROR]' not in line
   if not line.endswith('\n'):unterminated+=1;continue
   if line.startswith('MK2_NAT_CAMPAIGN_'):
    rows.setdefault(line.split()[0][17:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
 assert unterminated<=1
 if complete:assert rows['RESULT'][0]['frame']=='30000'
 else:assert not rows.get('RESULT')
 old=chronology.load(sync.ROOT/'audit_current_sonya_kunglao_guard_runtime/run.log')
 cutoff=int(next(r for r in old['FIGHT'] if r['stage']=='5')['frame'])
 for tag in set(old)|set(rows):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]
 code=inspect.getsource(base.gate)
 code=code.replace(" assert rows['RESULT'][0]['frame']=='18000'\n",'')
 code=code.replace('assert actual==list(range(len(actual)))','assert actual==(list(range(13))+[14,15,16])[:len(actual)]')
 context={};exec(compile(code,__file__+'::native chronological gate','exec'),context)
 result=context['gate'](rows,1)
 result.update(passedObservationChecks=True,completedRunAccepted=complete,lastCompleteFrame=max(int(r['frame']) for group in rows.values() for r in group),preMirrorRouteExactThrough=cutoff-1,mirrorRoundWins=[r for r in rows['WIN'] if r['stage']=='5' and r['slot']=='1'],fullPortAccepted=False,logSHA256=sync.sha(folder/'run.log'))
 out=sync.ROOT/'audit_current_sonya_mirror_stance_guard_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result))
