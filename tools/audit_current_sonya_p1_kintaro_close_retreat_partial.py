"""Wall cap before changed strategy: qualify observed prefix, never claim a tested boss tactic."""
import json,re
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load,check
sync.verify()
root=sync.ROOT
case=root/'audit_current_sonya_p1_kintaro_close_retreat_runtime'
baseline=root/'audit_current_sonya_p1_boss_light_runtime/run.log'
out=root/'audit_current_sonya_p1_kintaro_close_retreat_partial_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['limitReason']=='wall_limit'
assert not (case/'stderr.log').read_text().strip()
rows=load(case/'run.log')
last=max(int(r['frame']) for entries in rows.values() for r in entries)
assert last<107554
def prefix(path):
 return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and int(re.search(r'\bframe=(\d+)',s)[1])<=last]
assert prefix(baseline)==prefix(case/'run.log')
stages=check(rows,1,18,list(range(13))+[14,15,16])
assert 15 not in stages and all(r['human']=='18:18' and r['writes']=='0' and r['assistance']=='none' for r in rows['FIGHT'])
report=dict(changedKintaroStrategyExecuted=False,changedShaoRingControllerExecuted=False,
 strategyOutcome='unobserved: wall cap before changed stage15 branch',
 observedPrefixExactlyEquivalentThrough=last,matchingRecords=len(prefix(baseline)),visitedStages=stages,
 terminal=terminal,logSHA256=sync.sha(case/'run.log'),
 fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
