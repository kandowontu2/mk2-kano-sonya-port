"""Classify executed physical command failure without claiming game completion."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_uppercut_edges_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log')
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 old=chronology.load(sync.ROOT/'audit_current_sonya_subzero_historical_uppercut_runtime/run.log')
 for tag in set(old)|set(rows):
  if tag in ('SUBZERO_COMMAND_FIELD','SUBZERO_UPPERCUT_ENTRY','RESULT','HOST_BOUND','INPUT_DIGEST','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<9000]==[r for r in rows.get(tag,[]) if int(r['frame'])<9000]
 fields=rows['SUBZERO_COMMAND_FIELD'];first=fields[0]['start']
 window=[r for r in fields if r['start']==first]
 assert [int(r['age']) for r in window]==list(range(15))
 assert all(r['id']==r['roster']=='18' and r['owner']==r['actor'] for r in window)
 assert window[1]['action']=='770'
 throw=next(r for r in window if r['cpu_action']=='1287')
 hp=next(r for r in window if int(r['in0'],16)&0x1000==0)
 assert int(throw['frame'])<int(hp['frame']) and hp['cpu_action']=='1287'
 assert not rows.get('SUBZERO_UPPERCUT_ENTRY')
 out=sync.ROOT/'audit_current_sonya_subzero_throw_before_punch_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'classification':'physical command interrupted by native CPU throw before HP edge in first complete window','firstCommandFrame':int(first),'crouchAge':1,'throwAge':int(throw['age']),'hpEdgeAge':int(hp['age']),'ordinaryScalarPrefixUnchanged':True,'logSHA256':sync.sha(folder/'run.log'),'allAttemptsHaveSameCause':False,'characterDefectEstablished':False,'campaignCompleted':False,'fullPortAccepted':False},indent=2))
 print('PASS first complete attempt: native crouch, CPU throw age6, HP edge age7; unchanged scalar prefix')
