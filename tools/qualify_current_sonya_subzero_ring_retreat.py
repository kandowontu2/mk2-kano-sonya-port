"""Actual native KO after earned uppercut damage and physical ring follow-up."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

def gate(rows):
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 assert all(r['human']=='18:18' for r in rows['FIGHT'])
 wins=[r for r in rows['WIN'] if r['stage']=='1' and r['slot']=='2']
 assert len(wins)==1 and wins[0]['pc']=='FF8296B0' and wins[0]['id']=='18' and wins[0]['health']=='0,81'
 entries=rows['SUBZERO_RING_ENTRY'];assert len(entries)==5
 assert all(r['id']==r['roster']=='18' and r['pc']=='FFFFB410' and 0<int(r['cpu_hp'])<=41 for r in entries)
 damage=[r for r in rows['HEALTH'] if r['slot']=='1' and r['pc']=='FF836700' and 7142<int(r['frame'])<int(wins[0]['frame'])]
 assert [(r['before'],r['after']) for r in damage]==[('41','35'),('35','13'),('13','0')]
 assert int(wins[0]['frame'])-int(damage[-1]['frame'])==3
 return {'nativeSubzeroRoundWin':wins[0],'ringEntries':5,'nativeDamageSequence':[6,22,13],'subzeroMatchClear':False}

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_ring_retreat_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log');result=gate(rows)
 old=chronology.load(sync.ROOT/'audit_current_sonya_subzero_ring_finish_runtime/run.log')
 for tag in set(old)|set(rows):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<7143]==[r for r in rows.get(tag,[]) if int(r['frame'])<7143]
 bad=copy.deepcopy(rows);next(r for r in bad['WIN'] if r['stage']=='1')['id']='1'
 try:gate(bad)
 except AssertionError:pass
 else:raise AssertionError('Proxy winner accepted')
 out=sync.ROOT/'audit_current_sonya_subzero_ring_retreat_checked';assert not out.exists();out.mkdir()
 result.update(passed=True,proxyFaultRejected=True,earnedUppercutPrefixExact=True,logSHA256=sync.sha(folder/'run.log'),fullPortAccepted=False)
 (out/'report.json').write_text(json.dumps(result,indent=2))
 print('PASS native Sonya KO win81HP, real-ID ring follow-up after exact earned damage prefix')
