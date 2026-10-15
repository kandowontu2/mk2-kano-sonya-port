"""Qualify observed progress in truncated run, never completed-run acceptance."""
import json
from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_bounded_kano_campaign_18000_p1_runtime'
out=sync.ROOT/'audit_bounded_kano_campaign_18000_limit_observed'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['limitReason']=='wall_limit' and terminal['exitCode']!=0
assert terminal['peakWorkingSetBytes']<=320*1024**2
assert not (case/'stderr.log').read_text().strip()
text=(case/'run.log').read_text()
rows=[(line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),fields(line)) for line in text.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_')]
assert rows and all(r['writes']=='0' and r['assistance']=='none' for _,r in rows)
stages=[int(r['stage']) for t,r in rows if t=='STAGE']
assert stages==list(range(max(stages)+1))
wins=[r for t,r in rows if t=='WIN' and r['slot']=='1']
assert all(r['id']=='17' and r['pc']=='FF8296B0' and int(r['health'].split(',')[0])>0 and r['health'].split(',')[1]=='0' for r in wins)
for stage in stages[1:]:
    arrival=int(next(r['frame'] for t,r in rows if t=='STAGE' and int(r['stage'])==stage))
    assert len({r['frame'] for r in wins if int(r['stage'])==stage-1 and int(r['frame'])<arrival})>=2
live=[r for t,r in rows if t=='LIVE']
assert live and all(r['human']=='17:17' for r in live)
assert not any(t=='RESULT' for t,_ in rows)
prefix='MK2_NAT_CAMPAIGN_'
def early(value): return [line for line in value.splitlines() if line.startswith(prefix) and int(fields(line)['frame'])<12000]
baseline=(sync.ROOT/'audit_bounded_campaign_progress_core_kano_p1_runtime/run.log').read_text()
assert early(text)==early(baseline)
out.mkdir()
(out/'report.json').write_text(json.dumps({'observedProgressQualified':True,'completedRun':False,'fullCampaignClear':False,'releaseAcceptance':False,'observedStages':stages,'qualifiedOwnRoundWins':len(wins),'lastObservedFrame':max(int(r['frame']) for _,r in rows),'earlyPrefixUnchanged':True,'logSha256':sync.sha(case/'run.log'),'terminal':terminal},indent=2))
print('Observed natural stages '+str(stages)+'; wall-capped incomplete, NOT campaign acceptance')
