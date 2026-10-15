"""Exact physical/gameplay prefix and terminal result, never combine attempts."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_bicycle_ready_escape.py').read_text().replace('audit_current_sonya_p2_bicycle_ready_escape','audit_current_sonya_p2_bicycle_deciding_round')
exec(compile(source,__file__+'::native_context','exec'))
reference=chronology.load(sync.ROOT/'audit_current_sonya_p2_bicycle_ready_escape_runtime/run.log')
last=max(int(r['frame']) for group in rows.values() for r in group)
cutoff=min(last,60000)
for tag in set(rows)|set(reference):
    if tag not in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in reference.get(tag,[]) if int(r['frame'])<cutoff],tag
baseline=(sync.ROOT/'audit_current_sonya_p2_bicycle_ready_escape_preparation/campaign.lua').read_text()
candidate=(sync.ROOT/'audit_current_sonya_p2_bicycle_deciding_round_preparation/campaign.lua').read_text()
assert candidate.replace("if frame>=70000 then log('HOST_BOUND','maximum_fields=70000 full_campaign_acceptance=false')","if frame>=60000 then log('HOST_BOUND','maximum_fields=60000 full_campaign_acceptance=false')")==baseline
attempt=[r for r in rows['WIN'] if r['stage']=='3' and int(r['frame'])>55928]
loss=[r for r in rows.get('LOSS',[]) if r['stage']=='3' and int(r['frame'])>55928]
(out/'deciding-round.json').write_text(json.dumps(dict(passed=True,controllerUnchanged=True,gameplayPrefixIdenticalBefore=cutoff,lastLoggedField=last,latestAttemptWins=attempt,latestLosses=loss,kungLaoMatchCleared=4 in stages,fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n');print('Exact prefix before '+str(cutoff))
