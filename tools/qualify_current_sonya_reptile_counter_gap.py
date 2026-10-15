"""Keep earned chronology and actual uppercut evidence, not a success quota."""
import copy,inspect,json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology
import qualify_current_sonya_reptile_crouch_counter_long as base

def main():
    source=sync.verify();folder=sync.ROOT/'audit_current_sonya_reptile_counter_gap_runtime'
    out=sync.ROOT/'audit_current_sonya_reptile_counter_gap_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_reptile_counter_gap_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    code=inspect.getsource(base.gate).replace('assert len(attempts)>=21 and len(activations)>=14','assert attempts and activations')
    context=dict(vars(base));exec(compile(code,__file__,'exec'),context)
    rows=chronology.load(folder/'run.log');stages,wins=context['gate'](rows)
    assert rows['RESULT'][0]['frame']=='20000' and rows['HOST_BOUND'][0]['maximum_fields']=='20000'
    previous=chronology.load(sync.ROOT/'audit_current_sonya_reptile_crouch_counter_runtime/run.log')
    cutoff=int(rows['STAGE'][1]['frame'])
    for tag in ('LIVE','WIN','SPECIAL','SELECT_ID','LOSS','INPUT_DIGEST'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in previous.get(tag,[]) if int(r['frame'])<cutoff]
    bad=copy.deepcopy(rows);bad['LIVE'][0]['human']='18:1'
    try:context['gate'](bad)
    except AssertionError:pass
    else:raise AssertionError('Proxy accepted')
    report=dict(passedObservationChecks=True,completedRunAccepted=True,sourceSync=source,terminal=terminal,stages=stages,
                earnedReptileRoundWins=sum(r['stage']=='1' for r in wins),actualCrouchPunchAttempts=len(rows['COUNTER_ATTEMPT']),
                actualUppercutActivations=len(rows['COUNTER_ACTIVATION']),unchangedBarakaPhase=True,proxyIdentityRejected=True,
                logSHA256=sync.sha(folder/'run.log'),fullCampaignAcceptance=False,fullPortAcceptance=False,
                scope='Physical crouch-counter approach gap85 removes previous95..105 no-attack controller dead zone. Native IDs, actual action263 and earned chronology checked; no assumed opponent clear or whole campaign/art/audio/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passedObservationChecks','stages','earnedReptileRoundWins','actualUppercutActivations')}))

if __name__=='__main__':main()
