"""Finite cold campaign progression comparison, never a full-clear claim."""
import json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_current_sonya_p2_campaign_tactics_checked';assert not out.exists()
    lua=sync.ROOT/'audit_current_sonya_p2_delayed_campaign_preparation/campaign.lua'
    cases={}
    for tactic in ('delayed','leg'):
        folder=sync.ROOT/f'audit_current_sonya_p2_{tactic}_campaign_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['observerSha256']==sync.sha(lua)
        assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90
        assert terminal['logBytes']<=10*1024*1024
        assert not (folder/'stderr.log').read_text().strip()
        assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
        rows=chronology.load(folder/'run.log')
        for records in rows.values():
            assert all(r['writes']=='0' and r['assistance']=='none' and r['human_slot']=='2' and r['fighter']=='sonya' for r in records)
        stages=chronology.check(rows,2,18,list(range(13))+[14,15,16])
        assert stages==([0] if tactic=='delayed' else [0,1])
        assert all(r['human']=='18:18' for r in rows['LIVE'])
        assert rows['BOOT'][0]['boot']=='700'
        assert rows['BOOT'][0]['strategy']==('zoning' if tactic=='delayed' else 'leg')
        assert len(rows['HOST_BOUND'])==1 and rows['HOST_BOUND'][0]['maximum_fields']=='12000'
        assert len(rows['RESULT'])==1 and rows['RESULT'][0]['frame']=='12000'
        wins=[r for r in rows['WIN'] if r['slot']=='2']
        if tactic=='leg':
            assert len(wins)==2 and all(r['stage']=='0' for r in wins)
            assert any(r['move']=='leg' and r['id']=='18' and r['roster']=='18' for r in rows['SPECIAL'])
        else: assert not wins
        cases[tactic]=dict(stages=stages,earnedHumanRoundWins=len(wins),
            result=rows['RESULT'][0],terminal=terminal,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,cases=cases,sourceSync=source_sync,fullCampaignAcceptance=False,
        fullPortAcceptance=False,scope='Cold Sonya P2, ordinary boot700 selection and controls: zoning lost stage0; existing physical leg tactic earned two native FF8296B0 wins with actual CPU health0 and true Sonya18, advancing to stage1. No boss/ending, full art/audio or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualSonyaP2LadderAdvance=True,fullCampaignAcceptance=False)))

if __name__=='__main__':main()
