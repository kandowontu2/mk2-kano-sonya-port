"""Real earned Kano wins and uninterrupted own pose progression."""
import copy
import json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def gate(rows):
    assert chronology.check(rows,1,17,list(range(13))+[14,15,16])==[0]
    wins=[r for r in rows['WIN'] if r['slot']=='1']
    assert [(r['frame'],r['health']) for r in wins]==[('8755','7,0'),('9968','39,0')]
    poses=rows['WINNER_POSE'];assert len(poses)==563
    assert all(r['id']=='17' and r['roster']=='17' and r['owner']==r['actor'] and int(r['hp'])>0 and r['cpu_hp']=='0' for r in poses)
    by={int(r['frame']):r for r in poses};assert len(by)==len(poses)
    groups=['FF012200','FF012260','FF0122C0','FF012320','FF0123C0','FF012440','FF0124C0']
    proofs=[]
    for start in (8764,9968):
        actor,main=by[start]['actor'],by[start]['main']
        for index,group in enumerate(groups):
            assert all(by[start+index*6+j]['pose']==group for j in range(6))
        hold=start+42;end=hold
        while end in by:
            assert by[end]['pose']=='FF012560'
            end+=1
        assert end-hold>=60
        assert all(by[f]['actor']==actor and by[f]['main']==main for f in range(start,end))
        proofs.append(dict(start=start,finalPoseStart=hold,lastObserved=end-1))
    return proofs

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_kano_native_winner_runtime'
    out=sync.ROOT/'audit_current_kano_native_winner_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_native_winner_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log')
    assert all(r['writes']=='0' and r['assistance']=='none' for records in rows.values() for r in records)
    assert rows['RESULT'][0]['frame']=='10200'
    old=chronology.load(sync.ROOT/'audit_bounded_compact_kano_campaign_p1_runtime/run.log')
    for tag,records in rows.items():
        if tag in ('WINNER_POSE','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
        assert [r for r in records if int(r['frame'])<10200]==[r for r in old.get(tag,[]) if int(r['frame'])<10200]
    proofs=gate(rows)
    bad=copy.deepcopy(rows);bad['WINNER_POSE'][0]['id']='1'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Proxy Liu Kang winner accepted')
    bad=copy.deepcopy(rows);next(r for r in bad['WINNER_POSE'] if r['frame']=='8782')['pose']='FF012560'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Skipped Kano victory pose accepted')
    report=dict(passed=True,sourceSync=source,terminal=terminal,earnedWinPoses=proofs,
                baselineScalarPrefixUnchanged=True,proxyIdentityRejected=True,skippedPoseRejected=True,
                logSHA256=sync.sha(folder/'run.log'),fullPortAcceptance=False,
                scope='Two current Kano P1 earned wins against real CPU Kano: seven own victory pose groups at six fields each and eighth held pose, continuous actor/Main identity ownership. No complete pixel/audio, other winner contexts, bosses/endings or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,twoEarnedKanoVictorySequences=True,fullPortAcceptance=False)))

if __name__=='__main__':main()
