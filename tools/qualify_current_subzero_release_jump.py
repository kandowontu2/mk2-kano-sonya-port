"""Finite native chronology and launch timing, no assumed attack or victory."""
import collections
import inspect
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_p2_subzero_release_jump_runtime'
out=sync.ROOT/'audit_current_subzero_release_jump_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
rows=chronology.load(folder/'run.log')
assert rows['RESULT'][0]['frame']=='9000'
code=inspect.getsource(chronology.check)
old='health[side - 1] > 0 and health[2 - side] == 0'
assert code.count(old)==1
ns={};exec(compile(code.replace(old,'health[side - 1] > health[2 - side] >= 0'),'native_winner_gate','exec'),ns)
stages=ns['check'](rows,2,18,list(range(13))+[14,15,16])
prior=chronology.load(sync.ROOT/'audit_current_sonya_p2_mirror_guard_runtime/run.log')
cutoff=int(prior['STAGE'][1]['frame'])
assert rows['STAGE'][1]==prior['STAGE'][1]
for tag in set(rows)|set(prior):
 if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
 assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in prior.get(tag,[]) if int(r['frame'])<cutoff]
timing=rows['AIR_TIMING']
assert timing and all(r['owner']==r['actor'] and int(r['id'])==(8 if r['slot']=='1' else 18) for r in timing)
own=[r for r in timing if r['slot']=='2' and r['mode']=='2']
air=[r for r in own if int(r['floor'])-int(r['y'])>8]
actions=dict(collections.Counter(r['action'] for r in air))
wins=[r for r in rows.get('WIN',[]) if r['stage']=='1' and r['slot']=='2']
report={'passedObservationChecks':True,'completedRunAccepted':True,'terminal':terminal,
 'stages':stages,'openingMirrorPrefixExact':True,'pairedTimingRecords':len(timing),
 'humanAirborneFields':len(air),'humanAirborneActions':actions,
 'subZeroRoundWins':len(wins),'logSHA256':sync.sha(folder/'run.log'),
 'fullCampaignAccepted':False,'fullPortAccepted':False}
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k] for k in ('stages','humanAirborneFields','humanAirborneActions','subZeroRoundWins')}))
