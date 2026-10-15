"""Natural longer campaign, retain capped/complete distinction explicitly."""
import copy,json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def gate(rows):
    assert all(r['writes']=='0' and r['assistance']=='none' and r['human_slot']=='2' and r['fighter']=='sonya' for records in rows.values() for r in records)
    stages=chronology.check(rows,2,18,list(range(13))+[14,15,16])
    assert stages[:2]==[0,1] and all(r['human']=='18:18' for r in rows['LIVE'])
    attempts=rows.get('COUNTER_ATTEMPT',[]);activations=rows.get('COUNTER_ACTIVATION',[])
    assert len(attempts)>=21 and len(activations)>=14
    assert all(r['native_action']=='770' and r['cpu_id']=='9' and int(r['gap'])<95 and int(r['hp'])>0 for r in attempts)
    assert all(r['native_action']=='263' and r['id']=='18' and r['owner']==r['actor'] and int(r['hp'])>0 for r in activations)
    return stages,[r for r in rows['WIN'] if r['slot']=='2']

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_long_runtime'
    out=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_long_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    complete=terminal['exitCode']==0 and terminal['limitReason'] is None
    assert complete or (terminal['limitReason']=='wall_limit' and terminal['exitCode']!=0)
    assert terminal['elapsedSeconds']<=(90 if complete else 92)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_reptile_crouch_counter_long_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log');stages,wins=gate(rows)
    if complete:
        assert len(rows['RESULT'])==1 and rows['RESULT'][0]['frame']=='20000'
        assert rows['HOST_BOUND'][0]['maximum_fields']=='20000'
    else:
        assert not rows.get('RESULT')
    previous=chronology.load(sync.ROOT/'audit_current_sonya_reptile_crouch_counter_runtime/run.log')
    for tag in set(rows)|set(previous):
        if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<12000]==[r for r in previous.get(tag,[]) if int(r['frame'])<12000]
    bad=copy.deepcopy(rows);bad['LIVE'][0]['human']='18:1'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Proxy Sonya accepted')
    report=dict(passedObservationChecks=True,completedRunAccepted=complete,sourceSync=source,terminal=terminal,
                stages=stages,earnedReptileRoundWins=sum(r['stage']=='1' for r in wins),
                actualCrouchPunchAttempts=len(rows.get('COUNTER_ATTEMPT',[])),
                actualUppercutActivations=len(rows.get('COUNTER_ACTIVATION',[])),
                original12000FieldPrefixUnchanged=True,proxyIdentityRejected=True,
                lastObservedField=max(int(r['frame']) for records in rows.values() for r in records),
                logSHA256=sync.sha(folder/'run.log'),fullCampaignAcceptance=False,fullPortAcceptance=False,
                scope='Same current cold physical counter policy for up to20000fields, genuine native victories/IDs and exact prior12000field prefix. Wall-capped runs never accepted as completed. No full campaign/ending/art/audio/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passedObservationChecks','completedRunAccepted','stages','earnedReptileRoundWins','actualUppercutActivations')}))

if __name__=='__main__':main()
