"""Qualify finite unchanged-policy extension, including its failure to clear."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_range_long_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
 rows=chronology.load(folder/'run.log')
 old=chronology.load(sync.ROOT/'audit_current_sonya_subzero_range_uppercut_runtime/run.log')
 for tag in set(old)|set(rows):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<9000]==[r for r in rows.get(tag,[]) if int(r['frame'])<9000]
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 assert rows['RESULT'][0]['frame']=='18000'
 assert [r['stage'] for r in rows['STAGE']]==['0','1']
 assert not [r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1']
 assert all(r['human']=='18:18' for r in rows['FIGHT'])
 out=sync.ROOT/'audit_current_sonya_subzero_range_long_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'classification':'finite controller failure to clear SubZero','exactOrdinaryPrefixThrough8999':True,'fields':18000,'subzeroOwnRoundWins':0,'trueIDPreservedOnContinues':True,'logSHA256':sync.sha(folder/'run.log'),'fullPortAccepted':False},indent=2))
 print('PASS unchanged-prefix/real-ID finite18000field evidence; SubZero clearance failed')
