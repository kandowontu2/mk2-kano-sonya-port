"""Actual counter activation and native-earned progress, not intent."""
import json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology
from qualify_current_sonya_reptile_uppercut_campaign import gate

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_runtime'
    out=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_reptile_crouch_counter_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log');stages,wins=gate(rows)
    previous=chronology.load(sync.ROOT/'audit_current_sonya_p2_leg_campaign_runtime/run.log')
    cutoff=int(rows['STAGE'][1]['frame'])
    for tag in ('LIVE','WIN','SPECIAL','HP_STORE','SELECT_ID','LOSS','INPUT_DIGEST'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in previous.get(tag,[]) if int(r['frame'])<cutoff]
    attempts=rows.get('COUNTER_ATTEMPT',[])
    activations=rows.get('COUNTER_ACTIVATION',[])
    assert all(r['native_action']=='770' and r['cpu_id']=='9' and int(r['gap'])<95 and int(r['hp'])>0 for r in attempts)
    assert all(r['native_action']=='263' and r['id']=='18' and r['owner']==r['actor'] and r['stage']=='1' and int(r['hp'])>0 for r in activations)
    report=dict(passed=True,sourceSync=source,terminal=terminal,stages=stages,
                earnedReptileRoundWins=sum(r['stage']=='1' for r in wins),
                actualCrouchPunchAttempts=len(attempts),actualUppercutActivations=len(activations),
                unchangedBarakaPhase=True,result=rows['RESULT'][0],
                logSHA256=sync.sha(folder/'run.log'),fullCampaignAcceptance=False,fullPortAcceptance=False,
                scope='Actual current Sonya18 physical crouch-state770-gated HP attempts versus native Reptile9, passive uppercut263 transitions and earned health-qualified wins. No assumed activation/contact/win, full campaign/endings/visual/audio/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','stages','earnedReptileRoundWins','actualCrouchPunchAttempts','actualUppercutActivations')}))

if __name__=='__main__':main()
