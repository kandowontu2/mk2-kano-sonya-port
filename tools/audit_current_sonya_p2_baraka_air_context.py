"""Distinguish actual airborne observations from voluntary jump activations."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
case=sync.ROOT/'audit_current_sonya_p2_baraka_ready_backjump_runtime'
out=sync.ROOT/'audit_current_sonya_p2_baraka_air_context_checked'
assert not out.exists()
rows=load(case/'run.log')
air=rows['BARAKA_ACTUAL_AIR'];throws=rows['BARAKA_THROW_START']
assert all(r['id']=='18' and int(r['height'])>8 for r in air)
linked=[]
for r in air:
    matches=[t for t in throws if t['human_actor']==r['actor'] and t['human_main']==r['main'] and 0<int(r['frame'])-int(t['frame'])<=12]
    if matches:
        assert len(matches)==1
        linked.append(dict(airFrame=int(r['frame']),throwFrame=int(matches[0]['frame']),action=int(r['action']),actor=r['actor'],main=r['main']))
assert linked and all(r['action']==0 for r in linked)
actions=dict(Counter(int(r['action']) for r in air))
# A clear counterexample prevents using all 68 rising-height observations as jumps.
faultRejected=len(linked)>0
assert faultRejected
report=dict(passedFiniteChecks=True,actualAirborneTransitions=len(air),sampledActions=actions,postThrowAirborneTransitions=len(linked),pairedContexts=linked,allAirborneMeansVoluntaryJumpFaultRejected=faultRejected,voluntaryJumpActivationCountProven=False,controllerSucceeded=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pairedContexts'}))
