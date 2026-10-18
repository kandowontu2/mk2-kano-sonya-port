"""Save-only earned-intro provenance; no state-load or campaign-clear proof."""
import csv
import json
from inspect_normal_runtime import BASE, PORT, sha
from refresh_special_videos import command


def main():
    name='stock_wolf_2219_kano_earned_kintaro_checkpoint_v3'
    run=BASE/name
    command(PORT/'audit_campaign_run.py',name)
    receipt=json.loads((run/'execution.json').read_text())
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    assert '--campaign-boss-checkpoint' in receipt['testArguments']
    assert len(audit['naturallyDefeatedOpponents'])==14
    assert audit['maxMapPosition']==15
    events=list(csv.DictReader((run/'boss_checkpoint.csv').open()))
    assert len(events)==2 and [r['event'] for r in events]==['save_requested','file_observed']
    assert all((r['mode'],r['map'],r['p1selected'],r['p2selected'])==('7','15','17','12') for r in events)
    assert int(events[1]['field'])-int(events[0]['field'])>=4
    reference=BASE/'stock_wolf_2219_kano_kintaro_varied_finish_uppercut13/campaign.csv'
    count=0
    with reference.open() as old,(run/'campaign.csv').open() as new:
        previous=iter(csv.DictReader(old))
        for row in csv.DictReader(new):
            assert row==next(previous), 'Changed earned route before saved intro'
            count+=1
    state=run/'earned_kintaro_intro.sta'
    assert 1024<state.stat().st_size<16*1024*1024
    report=dict(scope='Unedited save-only first earned Kintaro intro, local planning only',
        naturallyDefeatedHumanOpponents=14,identicalReferenceRows=count,events=events,
        checkpointBytes=state.stat().st_size,stateLoaded=False,loadVerificationPassed=False,
        campaignClear=False,fullPortVerified=False,pins={str(p):sha(p) for p in
            (state,reference,run/'campaign.csv',run/'autoboot.lua',run/'execution.json',run/'boss_checkpoint.csv')})
    (run/'EARNED_CHECKPOINT_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Verified14 earned human matches,',count,'identical rows,',state.stat().st_size,'checkpoint bytes; load unverified')


if __name__=='__main__':main()
