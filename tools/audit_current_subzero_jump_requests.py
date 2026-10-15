"""Correlate requested jumps with actual action states, bounded existing evidence."""
import collections
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_p2_subzero_air_timing_runtime'
out=sync.ROOT/'audit_current_subzero_jump_requests_checked'
assert not out.exists()
rows=chronology.load(folder/'run.log')
own={int(r['frame']):r for r in rows['AIR_TIMING'] if r['slot']=='2' and r['mode']=='2'}
requests=[]
for r in rows['DECISION']:
 if r.get('move')!='jump':continue
 f=int(r['frame'])
 before=own.get(f-1)
 following=[own[t] for t in range(f,min(f+13,max(own)+1)) if t in own]
 if not before or len(following)!=13:continue
 assert before['id']=='18' and before['owner']==before['actor']
 requests.append({'frame':f,'beforeAction':int(before['action']),
  'beforeFlags':before['flags'],'beforeHeight':int(before['floor'])-int(before['y']),
  'followingActions':[int(a['action']) for a in following],
  'followingHeights':[int(a['floor'])-int(a['y']) for a in following]})
assert requests
counts=dict(collections.Counter(str(r['beforeAction']) for r in requests))
report={'passedObservationChecks':True,'logSHA256':sync.sha(folder/'run.log'),
 'complete13FieldJumpRequestWindows':len(requests),'beforeActionCounts':counts,
 'requests':requests,'exactCauseOfRejectedJumpProven':False,
 'nextTest':'Neutral release interval before Up; do not reapply Down/Block until launch window completes. Observe actual actions/height before assuming a jump.',
 'fullPortAccepted':False}
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'requestWindows':len(requests),'beforeActionCounts':counts}))
