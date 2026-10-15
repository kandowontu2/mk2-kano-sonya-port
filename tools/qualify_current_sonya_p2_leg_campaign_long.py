"""Long cold campaign and native paid-continue evidence; not a tower clear."""
import json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_current_sonya_p2_leg_campaign_long_checked';assert not out.exists()
    folder=sync.ROOT/'audit_current_sonya_p2_leg_campaign_long_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    lua=sync.ROOT/'audit_current_sonya_p2_leg_campaign_long_preparation/campaign.lua'
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['observerSha256']==sync.sha(lua)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log')
    for records in rows.values():
        assert all(r['human_slot']=='2' and r['fighter']=='sonya' and r['writes']=='0' and r['assistance']=='none' for r in records)
    stages=chronology.check(rows,2,18,list(range(13))+[14,15,16]);assert stages==[0,1]
    result=rows['RESULT'][0];assert len(rows['RESULT'])==1 and result['frame']=='30000'
    assert result['ending']==result['ending_completed']=='-1'
    assert result['selections']=='11' and result['losses']=='10'
    assert len(rows['SELECT'])==11 and len(rows['LOSS'])==10
    assert all(r['target']=='18' for r in rows['SELECT'])
    assert all(r['roster']=='18' for r in rows['SELECT_ID'])
    assert all(r['human']=='18:18' for r in rows['LIVE'])
    assert {r['pc'] for r in rows['HEALTH']}<=set(('FF836700','FF825930','FF825960','FF9DECE0','FF9DED10','FF9DEF40','FF9DEF70'))
    short=chronology.load(sync.ROOT/'audit_current_sonya_p2_leg_campaign_runtime/run.log')
    # Compare the entire shared pre-terminal trace, not just the input checksum.
    def prefix(r):return {tag:[x for x in values if int(x['frame'])<12000] for tag,values in r.items() if tag not in ('HOST_BOUND','RESULT','INPUT_DIGEST_FINAL')}
    assert prefix(rows)==prefix(short)
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,observedStages=stages,
        actualSelections=11,actualPaidContinueLosses=10,allLiveHumanIDs18=True,
        completeShared12000FieldPrefixEqual=True,allHealthWritersNative=True,
        logSHA256=sync.sha(folder/'run.log'),fullCampaignAcceptance=False,fullPortAcceptance=False,
        scope='30000-field cold physical Sonya P2 leg campaign: native two-win stage0 advance, ten losses/paid continues and eleven actual Sonya selections with native health writers. Stalled by losing to Kung Lao, not a qualified boss/ending clear; no full raster/audio acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualPaidContinues=10,fullCampaignAcceptance=False)))

if __name__=='__main__':main()
