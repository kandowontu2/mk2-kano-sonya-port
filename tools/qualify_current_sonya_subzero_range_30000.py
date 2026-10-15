"""Verify unchanged long-run prefix and actual native campaign frontier."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_range_30000_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024
 rows=chronology.load(folder/'run.log');old=chronology.load(sync.ROOT/'audit_current_sonya_subzero_range_long_runtime/run.log')
 for tag in set(old)|set(rows):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<18000]==[r for r in rows.get(tag,[]) if int(r['frame'])<18000]
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 assert rows['RESULT'][0]['frame']=='30000' and [r['stage'] for r in rows['STAGE']]==['0','1']
 assert all(r['human']=='18:18' for r in rows['FIGHT'])
 wins=[r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1']
 assert wins and all(r['pc']=='FF8296B0' and r['id']=='18' and int(r['health'].split(',')[1])>int(r['health'].split(',')[0]) for r in wins)
 out=sync.ROOT/'audit_current_sonya_subzero_range_30000_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'fields':30000,'exactPrefixThrough17999':True,'earnedSubzeroRoundWins':wins,'subzeroMatchClear':False,'realIDAllObservedFights':True,'logSHA256':sync.sha(folder/'run.log'),'fullPortAccepted':False},indent=2))
 print('PASS30000fields/exact18000prefix/real IDs; earned SubZero rounds='+str(len(wins))+'; no match clear')
