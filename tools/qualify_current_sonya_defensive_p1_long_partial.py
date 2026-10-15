"""Classify host-capped actual run; ignore only unterminated final text record."""
import json
import re
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_defensive_p1_long_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']!=0 and terminal['limitReason']=='wall_limit' and terminal['elapsedSeconds']<92
 assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
 assert not (folder/'stderr.log').read_text().strip()
 rows={};unterminated=0
 with (folder/'run.log').open() as stream:
  for line in stream:
   assert '[LUA ERROR]' not in line
   if not line.endswith('\n'):unterminated+=1;continue
   if line.startswith('MK2_NAT_CAMPAIGN_'):
    rows.setdefault(line.split()[0][17:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
 assert unterminated<=1 and not rows.get('RESULT')
 old=chronology.load(sync.ROOT/'audit_current_sonya_defensive_routes_p1_runtime/run.log')
 for tag in set(rows)|set(old):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<18000]==[r for r in rows.get(tag,[]) if int(r['frame'])<18000]
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 assert all(r['human']=='18:18' for r in rows['LIVE']+rows['FIGHT'])
 assert [r['stage'] for r in rows['STAGE']]==['0','1','2','3','4']
 wins=[r for r in rows['WIN'] if r['slot']=='1' and r['stage']=='4']
 assert wins and all(r['id']=='18' and r['pc']=='FF8296B0' and int(r['health'].split(',')[0])>int(r['health'].split(',')[1]) for r in wins)
 out=sync.ROOT/'audit_current_sonya_defensive_p1_long_partial_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passedObservationChecks':True,'completedRunAccepted':False,'classification':'native process stopped by host wall cap','lastCompleteFrame':max(int(r['frame']) for group in rows.values() for r in group),'unterminatedFinalRecordsExcluded':unterminated,'exact18000FieldPrefix':True,'actualKungLaoRoundWins':wins,'stages':[0,1,2,3,4],'logSHA256':sync.sha(folder/'run.log'),'fullPortAccepted':False},indent=2))
 print('PASS partial capped-run evidence/exactprefix/realIDs; no completed campaign acceptance')
