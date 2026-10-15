"""Check native low-health ring activation/earned context without win claim."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_ring_finish_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log');old=chronology.load(sync.ROOT/'audit_current_sonya_subzero_range_long_runtime/run.log')
 threshold=next(r for r in old['HEALTH'] if r['slot']=='1' and r['pc']=='FF836700' and r['after']=='41')
 cutoff=int(threshold['frame'])+1
 for tag in set(old)|set(rows):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 rings=rows['SUBZERO_RING_ENTRY'];assert rings
 assert all(r['id']==r['roster']=='18' and r['pc']=='FFFFB410' and 0<int(r['cpu_hp'])<=41 for r in rings)
 wins=[r for r in rows['WIN'] if r['stage']=='1']
 assert wins[0]['slot']=='1' and wins[0]['health']=='7,0'
 assert all(r['human']=='18:18' for r in rows['FIGHT'])
 out=sync.ROOT/'audit_current_sonya_subzero_ring_finish_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'actualNativeRingEntries':len(rings),'physicalPolicyStartsAfterEarnedCPUHealth41':True,'exactPrefixUntilLowHealth':True,'firstRoundCPUHealthAtLoss':7,'subzeroMatchClear':False,'logSHA256':sync.sha(folder/'run.log'),'fullPortAccepted':False},indent=2))
 print('PASS native low-health rings/unchanged earned prefix; first round loss with CPU7HP')
