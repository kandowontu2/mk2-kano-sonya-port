"""Bounded screenshots tied to unchanged earned-win scalar trace."""
import json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_sonya_winner_visual_screen_runtime'
    out=sync.ROOT/'audit_current_sonya_winner_visual_screen_checked'
    assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_winner_visual_screen_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    rows=chronology.load(folder/'run.log')
    old=chronology.load(sync.ROOT/'audit_current_sonya_native_winner_runtime/run.log')
    for tag,records in rows.items():
        if tag in ('VISUAL_SAVED','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
        assert records==[r for r in old.get(tag,[]) if int(r['frame'])<5400]
    assert all(r['writes']=='0' and r['assistance']=='none' for records in rows.values() for r in records)
    assert rows['RESULT'][0]['frame']=='5400'
    wins=[r for r in rows['WIN'] if r['slot']=='2']
    assert len(wins)==1 and wins[0]['frame']=='4944' and wins[0]['health']=='0,135' and wins[0]['id']=='18'
    assert [r['frame'] for r in rows['VISUAL_SAVED']]==['4979','5020']
    by={int(r['frame']):r for r in rows['WINNER_POSE']}
    assert by[4979]['pose']=='FF032460' and by[5020]['pose']=='FF0325C0'
    assert all(by[f]['id']=='18' and by[f]['owner']==by[f]['actor'] for f in (4979,5020))
    images=list(folder.rglob('*.png'))
    assert {p.name for p in images}=={'winner_4979.png','winner_5020.png'} and len(images)==2
    total=sum(p.stat().st_size for p in images);assert total<=512*1024
    assert not any(p.suffix.lower() in ('.bin','.wav') for p in folder.rglob('*'))
    report=dict(passed=True,sourceSync=source,terminal=terminal,totalPNGBytes=total,
                screenshots=[dict(name=p.name,sha256=sync.sha(p),bytes=p.stat().st_size) for p in images],
                scalarPrefixUnchanged=True,earnedNativeWinFrame=4944,
                continuousRasterAccepted=False,fullPortAcceptance=False,
                scope='Two bounded current Sonya P2 earned-win checkpoints, intermediate and held final pose; unchanged scalar prefix and native win at actual CPU health0. Not continuous pixels, all winner configurations, audio, endings or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,totalPNGBytes=total,fullPortAcceptance=False)))

if __name__=='__main__':main()
