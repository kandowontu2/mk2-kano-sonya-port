"""Correlate physical jump plans with already recorded exact action changes."""
import json
from collections import Counter
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_mirror_jump_action_trace_runtime'
rows=chronology.load(folder/'run.log')
events=[r for r in rows['MIRROR_ACTION_CHANGE'] if r['slot']=='1']
requests=rows['MIRROR_JUMPKICK_ATTEMPT']
assert requests
plans=Counter(r['human_action'] for r in requests)
links=[]
for request in requests:
    start=int(request['frame'])
    subsequent=[r for r in events if start<=int(r['frame'])<=start+16]
    links.append(dict(frame=start,plannedAction=int(request['human_action']),gap=int(request['gap']),
                      observedActions=[int(r['action']) for r in subsequent],
                      jumpTransitionObserved=any(r['action'] in ('512','779') for r in subsequent)))
assert any(r['plannedAction'] in (1792,1793,769) for r in links)
report=dict(physicalJumpRequests=len(links),requestActionCounts=dict(plans),
 observedJumpWindows=sum(r['jumpTransitionObserved'] for r in links),windows=links,
 controllerProblem='Request timer advances regardless of native jump acceptance. Some requests begin in block/crouch-transition states. Retry delay plus renewed Block can prevent the intended jump from starting.',
 nextAction='Gate jump plans on actual grounded neutral stance; release Block/Down before Up and only advance retry bookkeeping after observing a native jump.',
 semanticsScope='1283 and1286 are native hurt/victim continuations in preserved prior tests, not normal attacks.273 remains unidentified. Time-window correlation is not proof of causal acceptance or exact hit attribution.',
 fullPortAccepted=False,logSHA256=sync.sha(folder/'run.log'))
out=sync.ROOT/'audit_current_mirror_jump_requests'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='windows'},indent=2))
