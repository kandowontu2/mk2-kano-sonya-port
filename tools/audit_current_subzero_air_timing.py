"""Inspect bounded continuous action evidence; no exact collision causality claim."""
import collections
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

sync.verify()
folder=sync.ROOT/'audit_current_sonya_p2_subzero_air_timing_runtime'
out=sync.ROOT/'audit_current_subzero_air_timing_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
rows=chronology.load(folder/'run.log')
assert rows['RESULT'][0]['frame']=='9000'
previous=chronology.load(sync.ROOT/'audit_current_sonya_p2_subzero_air_runtime/run.log')
for tag in set(rows)|set(previous):
 if tag in ('AIR_TIMING','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
 assert rows.get(tag,[])==[r for r in previous.get(tag,[]) if int(r['frame'])<9000]
timing=rows['AIR_TIMING']
assert timing and all(r['writes']=='0' and r['assistance']=='none' for r in timing)
assert all(r['owner']==r['actor'] and int(r['id'])==(8 if r['slot']=='1' else 18) for r in timing)
own=[r for r in timing if r['slot']=='2' and r['mode']=='2']
cpu=[r for r in timing if r['slot']=='1' and r['mode']=='2']
assert own and cpu
air=[r for r in own if int(r['floor'])-int(r['y'])>8]
transitions=[]
last=None
for r in own:
 key=(r['actor'],r['action'])
 if key!=last:
  transitions.append({k:r[k] for k in ('frame','age','action','x','y','floor','hp')})
 last=key
report={'passedObservationChecks':True,'scalarBaselineExact':True,'terminal':terminal,
 'logSHA256':sync.sha(folder/'run.log'),'pairedRecords':len(timing),
 'humanAirborneFields':len(air),'humanAirborneActions':dict(collections.Counter(r['action'] for r in air)),
 'humanActions':dict(collections.Counter(r['action'] for r in own)),
 'cpuActions':dict(collections.Counter(r['action'] for r in cpu)),
 'humanActionTransitions':transitions,'exactHitRecoveryAttribution':False,'fullPortAccepted':False}
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k] for k in ('pairedRecords','humanAirborneFields','humanAirborneActions','humanActions','cpuActions')}))
