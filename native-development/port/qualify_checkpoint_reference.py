"""Planning continuation fidelity, explicitly NOT continuous campaign evidence."""
import csv
import json
from inspect_normal_runtime import BASE, PORT, sha
from refresh_special_videos import FLAGS
import subprocess
import sys


def main():
    run=BASE/'stock_wolf_2219_kano_checkpoint_reference'
    reference=BASE/'stock_wolf_2219_kano_kintaro_varied_finish_uppercut13/campaign.csv'
    receipt=json.loads((run/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut'] and receipt['planningStateLoadUsed']
    log=(run/'mame.log').read_text()
    assert 'Fatal error:' not in log and '[LUA ERROR]' not in log
    count=0
    with reference.open() as old,(run/'campaign.csv').open() as new:
        original=iter(csv.DictReader(old));prior=next(original)
        for row in csv.DictReader(new):
            while int(prior['frame'])<int(row['frame']):prior=next(original)
            keys=[k for k in row if k!='combat' or row['mode']=='2']
            assert all(row[k]==prior[k] for k in keys),row['frame']
            count+=1
    assert count==15657 and row['frame']=='161302'
    rejected=subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),run.name],
        capture_output=True,text=True,creationflags=FLAGS)
    assert rejected.returncode!=0 and 'Loaded-state planning is not campaign acceptance' in rejected.stderr
    assert not (run/'CAMPAIGN_AUDIT.json').exists()
    report=dict(scope='Planning-only continuation matches native reference; NOT a campaign clear',
        nativeStateRowsMatched=count,combatCounterMatchedDuringCombat=True,
        noncombatLuaCombatAgeExcluded=True,continuousCampaignAuditorRejected=True,
        finalField=161302,newWinClaimed=False,fullPortVerified=False,pins={str(p):sha(p) for p in
            (run/'execution.json',run/'autoboot.lua',run/'campaign.csv',reference)})
    (run/'PLANNING_REFERENCE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Verified15657 native-reference rows; continuous campaign auditor correctly rejects planning run')


if __name__=='__main__':main()
