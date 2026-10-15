"""Wall-capped finite native prefix/chronology; no strategy completion claim."""
import json,re
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load,check
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p1_kintaro_late_kick_runtime'
out=root/'audit_current_kano_p1_kintaro_late_kick_partial_checked';assert not out.exists()
old=root/'audit_current_kano_p1_subzero_guard_ready_v2_runtime/run.log';new=case/'run.log'
def prefix(path):return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and int(re.search(r'\bframe=(\d+)',s)[1])<=104638]
assert prefix(old)==prefix(new)
rows=load(new);stages=check(rows,1,17,list(range(13))+[14,15,16]);assert stages[-1]==15
assert all(r['human']=='17:17' and r['human_slot']=='1' for r in rows['FIGHT'])
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'));assert terminal['limitReason']=='wall_limit'
report=dict(nativeAndPhysicalPrefixPreservedThrough=104638,visitedStages=stages,
    lastObservedFrame=max(int(r['frame']) for values in rows.values() for r in values),
    ownKintaroRounds=[r for r in rows['WIN'] if r['stage']=='15' and r['slot']=='1'],
    terminal=terminal,logSHA256=sync.sha(new),strategyOutcomeCensored=True,fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
