"""Validate bounded natural campaign observations without assuming a clear."""
import copy,json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def gate(rows):
    assert all(r['writes']=='0' and r['assistance']=='none' and r['human_slot']=='2' and r['fighter']=='sonya' for records in rows.values() for r in records)
    stages=chronology.check(rows,2,18,list(range(13))+[14,15,16])
    assert stages[:2]==[0,1]
    assert all(r['human']=='18:18' for r in rows['LIVE'])
    assert rows['BOOT'][0]['boot']=='700' and rows['BOOT'][0]['strategy']=='leg'
    assert rows['RESULT'][0]['frame']=='12000' and len(rows['RESULT'])==1
    assert rows['HOST_BOUND'][0]['maximum_fields']=='12000'
    wins=[r for r in rows['WIN'] if r['slot']=='2']
    return stages,wins

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_sonya_reptile_uppercut_runtime'
    out=sync.ROOT/'audit_current_sonya_reptile_uppercut_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_reptile_uppercut_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log');stages,wins=gate(rows)
    previous=chronology.load(sync.ROOT/'audit_current_sonya_p2_leg_campaign_runtime/run.log')
    cutoff=int(rows['STAGE'][1]['frame'])
    for tag in ('LIVE','WIN','SPECIAL','HP_STORE','SELECT_ID','LOSS','INPUT_DIGEST'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in previous.get(tag,[]) if int(r['frame'])<cutoff]
    stage1=[r for r in rows['LIVE'] if r['stage']=='1']
    assert stage1 and all(r['cpu'].split(':')==['9','9'] for r in stage1)
    bad=copy.deepcopy(rows);bad['LIVE'][0]['human']='18:1'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Proxy Sonya accepted')
    report=dict(passed=True,sourceSync=source,terminal=terminal,stages=stages,
                earnedHumanRoundWins=len(wins),earnedReptileRoundWins=sum(r['stage']=='1' for r in wins),
                unchangedBarakaPhase=True,proxyIdentityRejected=True,
                result=rows['RESULT'][0],logSHA256=sync.sha(folder/'run.log'),
                fullCampaignAcceptance=False,fullPortAcceptance=False,
                scope='Current cold Sonya P2 boot700: unchanged physical leg tactic against Baraka3; existing physical approach/crouch+HP uppercuts against native Reptile9 only. Native wins and actual health qualify advancement, not controller intent. No whole bosses/endings/art/audio/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,stages=stages,earnedReptileRoundWins=report['earnedReptileRoundWins'],fullCampaignAcceptance=False)))

if __name__=='__main__':main()
