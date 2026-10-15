"""Reject interpreting an incorrectly PC-filtered observer as no activation."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
case=sync.ROOT/'audit_current_sonya_p2_baraka_crouch_lead_upper_runtime'
out=sync.ROOT/'audit_current_sonya_baraka_upper_observer_limit_checked'
assert not out.exists()
rows=load(case/'run.log')
upper=[r for r in rows['BARAKA_PRETHROW'] if r['action']=='263']
assert upper and not rows.get('BARAKA_NATIVE_UPPER')
assert all(r['pc']=='FF8B6C70' and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in upper)
report=dict(passedFiniteChecks=True,ownedPreThrowUpperStateSamples=len(upper),sampleFrames=[int(r['frame']) for r in upper],filteredUpperEntryRows=0,zeroFilteredRowsMeansNoUpperActivationFaultRejected=True,activationCountProven=False,actualUpperContactProven=False,controllerSucceeded=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
