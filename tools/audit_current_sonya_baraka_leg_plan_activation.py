"""Compare actual owned leg entries to physical plans; no causal bug claim."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;log=root/'audit_current_sonya_p2_baraka_own_ready_leg_runtime/run.log'
out=root/'audit_current_sonya_baraka_leg_plan_activation_checked';assert not out.exists()
rows=load(log);plans=rows['BARAKA_LEG_PLAN']
entries=[r for r in rows['SPECIAL'] if r['stage']=='6' and r['move']=='leg']
assert entries and all(r['id']==r['roster']=='18' and r['actor']==r['a8'] and r['main']==r['a13'] for r in entries)
matched=[]
for e in entries:
    prior=[p for p in plans if 0<=int(e['frame'])-int(p['frame'])<12]
    assert prior
    p=max(prior,key=lambda r:int(r['frame']))
    matched.append(dict(plan=int(p['frame']),entry=int(e['frame']),delay=int(e['frame'])-int(p['frame']),planAction=p['human_action']))
report=dict(physicalLegPlans=len(plans),actualOwnedLegEntries=len(entries),
    planActionCounts=dict(Counter(p['human_action'] for p in plans)),
    matchedEntryDelayFields=dict(Counter(p['delay'] for p in matched)),matchedEntries=matched,
    logSHA256=sync.sha(log),
    caveat='Unmatched plans are not proof of a character defect; timing/range/airborne victim/interruption remain possible. Settled-crouch causality is not proven by this comparison.',fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='matchedEntries'}))
