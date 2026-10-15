"""Finite continuation of actual earned KO policy; preserve failure frontier."""
import json
import check_campaign_stage_chronology as chronology
import qualify_current_sonya_subzero_ring_retreat as short
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_ring_retreat_long_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log');old=chronology.load(sync.ROOT/'audit_current_sonya_subzero_ring_retreat_runtime/run.log')
 prefix={tag:[r for r in records if int(r['frame'])<9000] for tag,records in rows.items()}
 short.gate(prefix)
 for tag in set(old)|set(rows):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<9000]==prefix.get(tag,[])
 assert rows['RESULT'][0]['frame']=='18000'
 assert all(r['human']=='18:18' for r in rows['FIGHT'])
 assert [r['stage'] for r in rows['STAGE']]==['0','1']
 wins=[r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1']
 assert wins and all(r['id']=='18' and r['pc']=='FF8296B0' for r in wins)
 out=sync.ROOT/'audit_current_sonya_subzero_ring_retreat_long_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'exact9000FieldPrefix':True,'earnedSubzeroRoundWins':wins,'subzeroMatchClear':False,'trueIDContinuesObserved':True,'logSHA256':sync.sha(folder/'run.log'),'fullPortAccepted':False},indent=2))
 print('PASS exact productive prefix and real-ID continues;18000fields did not clear SubZero')
