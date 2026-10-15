"""Exact sampled-frame pair geometry at air-kick transitions; no hitbox inference."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_p2_subzero_release_jump_runtime'
out=sync.ROOT/'audit_current_subzero_air_kick_range_checked'
assert not out.exists()
rows=chronology.load(folder/'run.log')
pairs={}
for r in rows['AIR_TIMING']:
 if r['mode']=='2':pairs.setdefault(int(r['frame']),{})[int(r['slot'])]=r
onsets=[]
prior=None
for frame,pair in sorted(pairs.items()):
 if set(pair)!={1,2}:continue
 h,c=pair[2],pair[1]
 assert h['id']=='18' and c['id']=='8' and h['owner']==h['actor'] and c['owner']==c['actor']
 if h['action']=='1025' and (prior is None or prior['action']!='1025'):
  onsets.append({'frame':frame,'gap':abs(int(h['x'])-int(c['x'])),
   'height':int(h['floor'])-int(h['y']),'cpuHeight':int(c['floor'])-int(c['y']),
   'cpuAction':int(c['action']),'ownHP':int(h['hp']),'cpuHP':int(c['hp'])})
 prior=h
assert onsets
report={'passedObservationChecks':True,'logSHA256':sync.sha(folder/'run.log'),
 'nativeAction1025Onsets':onsets,'onsetsBeyond115Pixels':sum(r['gap']>115 for r in onsets),
 'exactHitboxContactVerified':False,'fullPortAccepted':False,
 'nextTest':'Retain proven launch release; defer kick button until paired gap is below115 and actual flight height below90, so early distant kick cannot consume the attack window.'}
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
