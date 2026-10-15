"""Record capped observations honestly; never qualify truncated campaigns."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
out=sync.ROOT/'audit_bounded_campaign_policy_limits_observed'
assert not out.exists()
results={}
for policy in ('late_lowkick','settled_lowkick'):
    folder=sync.ROOT/f'audit_bounded_campaign_{policy}_p1_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['limitReason']=='wall_limit' and terminal['exitCode']!=0
    assert terminal['peakWorkingSetBytes']<320*1024*1024
    rows=(folder/'run.log').read_text().splitlines()
    live=[r for r in rows if r.startswith('MK2_NAT_CAMPAIGN_LIVE ')]
    assert live and all('human=18:18 ' in r for r in live)
    crouch=[r for r in live if re.search(r'actions=282,',r)]
    results[policy]=dict(terminal=terminal,completed=False,qualifiedCampaign=False,
        sampledNativeCrouchKickFields=len(crouch),sampledCrouchRecords=crouch,
        logSHA256=sync.sha(folder/'run.log'))
assert results['settled_lowkick']['sampledNativeCrouchKickFields']>0
report=dict(results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Two host-capped physical-policy experiments. Settled policy produced sampled native crouch kick; neither completed or qualifies campaign progress. No gameplay bug conclusion from defeat or host limit.',fullGoalComplete=False)
out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(recorded=True,qualifiedCampaigns=0,settledPolicyNativeCrouchKick=True)))
