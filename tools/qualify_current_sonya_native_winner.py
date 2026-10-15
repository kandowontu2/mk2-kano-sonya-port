"""Earned-win pose progression, not a claim of late table lookup or pixels."""
import json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_sonya_native_winner_runtime'
    out=sync.ROOT/'audit_current_sonya_native_winner_checked'
    assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_native_winner_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log')
    assert all(r['writes']=='0' and r['assistance']=='none' for records in rows.values() for r in records)
    assert chronology.check(rows,2,18,list(range(13))+[14,15,16])==[0,1]
    assert rows['RESULT'][0]['frame']=='7000'
    wins=[r for r in rows['WIN'] if r['slot']=='2']
    assert [int(r['frame']) for r in wins]==[4944,6094]
    poses=rows['WINNER_POSE']
    assert len(poses)==560
    assert all(r['id']=='18' and r['roster']=='18' and r['owner']==r['actor'] and int(r['hp'])>0 and r['cpu_hp']=='0' for r in poses)
    by={int(r['frame']):r for r in poses}
    assert len(by)==len(poses)
    groups=['FF032360','FF0323C0','FF032400','FF032460','FF0324C0','FF032500','FF032560']
    proofs=[]
    for start in (4961,6094):
        for index,group in enumerate(groups):
            assert all(by[start+index*6+j]['pose']==group for j in range(6))
        hold=start+42
        end=hold
        while end in by:
            assert by[end]['pose']=='FF0325C0'
            end+=1
        assert end-hold>=60
        proofs.append(dict(start=start,finalPoseStart=hold,lastObserved=end-1))
    old=chronology.load(sync.ROOT/'audit_current_sonya_p2_leg_campaign_runtime/run.log')
    for tag,records in rows.items():
        if tag in ('WINNER_POSE','WINNER_TABLE','RESULT','HOST_BOUND'):continue
        assert records==[r for r in old.get(tag,[]) if int(r['frame'])<7000]
    table=rows['WINNER_TABLE']
    assert [(r['at'],r['data']) for r in table]==[('FFFF3640','54D0'),('FFFF3650','FFA1')]
    assert all(r['frame']=='1173' for r in table)
    report=dict(passed=True,sourceSync=source,terminal=terminal,earnedWinPoses=proofs,
                baselineScalarTraceUnchanged=True,setupTablePointer='FFA154D0',
                lateWinnerTableLookupVerified=False,fullPortAcceptance=False,
                logSHA256=sync.sha(folder/'run.log'),
                scope='Two earned current Sonya P2 round wins: seven changing own pose groups at six fields each and eighth held pose, continuous real Sonya ownership. Table read observed only during setup. No full pixels/audio/all winners/endings/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,twoEarnedSonyaVictorySequences=True,fullPortAcceptance=False)))

if __name__=='__main__':main()
