"""Record a physical controller experiment without assuming victory."""
import json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology


def main():
    source = sync.verify()
    folder = sync.ROOT / 'audit_current_sonya_p2_lao_throw_campaign_runtime'
    out = sync.ROOT / 'audit_current_sonya_p2_lao_throw_campaign_checked'
    assert not out.exists()
    terminal = json.loads((folder / 'terminal.json').read_text())
    assert terminal['exitCode'] != 0 and terminal['limitReason'] == 'wall_limit'
    assert terminal['peakWorkingSetBytes'] <= 320*1024*1024
    assert 90 <= terminal['elapsedSeconds'] <= 92 and terminal['logBytes'] <= 10*1024*1024
    assert terminal['observerSha256'] == sync.sha(sync.ROOT / 'audit_current_sonya_p2_lao_throw_campaign_preparation/campaign.lua')
    assert not (folder / 'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png', '.bin', '.wav') for p in folder.rglob('*'))
    rows = chronology.load(folder / 'run.log')
    assert all(r['writes']=='0' and r['assistance']=='none'
               and r['human_slot']=='2' and r['fighter']=='sonya'
               for records in rows.values() for r in records)
    stages = chronology.check(rows, 2, 18, list(range(13))+[14,15,16])
    assert all(r['human']=='18:18' for r in rows['LIVE'])
    assert rows['BOOT'][0]['boot']=='700' and rows['BOOT'][0]['strategy']=='leg'
    assert not rows.get('RESULT')
    assert len(rows['HOST_BOUND'])==1 and rows['HOST_BOUND'][0]['maximum_fields']=='20000'
    attempts = [r for r in rows['DECISION'] if r['move']=='throw']
    assert attempts and all(r['stage']=='1' for r in attempts)
    # The unchanged Cage phase must match the earlier physical leg test.
    previous = chronology.load(sync.ROOT / 'audit_current_sonya_p2_leg_campaign_runtime/run.log')
    cutoff = int(rows['STAGE'][1]['frame'])
    for tag in ('LIVE','WIN','SPECIAL','HP_STORE','SELECT_ID','LOSS'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff] == [r for r in previous.get(tag,[]) if int(r['frame'])<cutoff]
    wins = [r for r in rows['WIN'] if r['slot']=='2']
    report = dict(passed=True, sourceSync=source, terminal=terminal,
                  stages=stages, earnedHumanRoundWins=len(wins),
                  kungLaoThrowAttempts=len(attempts), completedRunAccepted=False,
                  lastObservedField=max(int(r['frame']) for records in rows.values() for r in records),
                  unchangedCagePhase=True, logSHA256=sync.sha(folder/'run.log'),
                  fullCampaignAcceptance=False, fullPortAcceptance=False,
                  scope='Current cold Sonya P2 boot700: physical leg policy except ordinary forward+LP throw attempts against native Kung Lao. Native wins/actual health determine advancement; no assumed successful throws or full clear.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True, stages=stages, earnedHumanRoundWins=len(wins), kungLaoThrowAttempts=len(attempts), fullCampaignAcceptance=False)))


if __name__=='__main__':
    main()
