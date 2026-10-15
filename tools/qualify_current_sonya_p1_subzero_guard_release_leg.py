"""Report actual command/entry/outcome separately; never certify a planned hit."""
import json
from pathlib import Path
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load,check
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_subzero_guard_release_leg_runtime'
out=sync.ROOT/'audit_current_sonya_p1_subzero_guard_release_leg_checked'
assert not out.exists()
terminal=json.loads((base/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['limitReason'] in (None,'wall_limit')
assert not (base/'stderr.log').read_text().strip()
rows=load(base/'run.log')
stages=check(rows,1,18,list(range(13))+[14,15,16])
assert all(r['human']=='18:18' and r['writes']=='0' and r['assistance']=='none' for r in rows['FIGHT'])
plans=rows.get('SONYA_SETTLED_LEG_PLAN',[])
legs=[r for r in rows.get('SPECIAL',[]) if r['move']=='leg' and r['stage']=='11']
assert all(r['id']=='18' and r['roster']=='18' and r['actor']==r['a8'] and r['main']==r['a13'] for r in legs)
wins=[r for r in rows['WIN'] if r['stage']=='11' and r['slot']=='1']
report=dict(visitedStages=stages,physicalLegPlans=len(plans),nativeOwnedLegEntries=len(legs),
    firstPlan=plans[0] if plans else None,firstLegEntry=legs[0] if legs else None,
    ownSubZeroRoundWins=wins,stage12Reached=12 in stages,terminal=terminal,
    logSHA256=sync.sha(base/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
