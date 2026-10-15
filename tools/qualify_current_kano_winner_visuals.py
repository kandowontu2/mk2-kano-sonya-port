"""Check exact preterminal trace and small earned-win screenshots."""
import json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_kano_winner_visual_runtime'
    out=sync.ROOT/'audit_current_kano_winner_visual_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_winner_visual_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    rows=chronology.load(folder/'run.log')
    old=chronology.load(sync.ROOT/'audit_current_kano_native_winner_runtime/run.log')
    for tag,records in rows.items():
        if tag in ('VISUAL_SAVED','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
        assert [r for r in records if int(r['frame'])<9100]==[r for r in old.get(tag,[]) if int(r['frame'])<9100]
    assert all(r['writes']=='0' and r['assistance']=='none' for records in rows.values() for r in records)
    assert rows['RESULT'][0]['frame']=='9100'
    wins=[r for r in rows['WIN'] if r['slot']=='1']
    assert len(wins)==1 and wins[0]['frame']=='8755' and wins[0]['health']=='7,0' and wins[0]['id']=='17'
    assert [r['frame'] for r in rows['VISUAL_SAVED']]==['8782','8823']
    by={int(r['frame']):r for r in rows['WINNER_POSE']}
    assert by[8782]['pose']=='FF012320' and by[8823]['pose']=='FF012560'
    assert all(by[f]['id']=='17' and by[f]['owner']==by[f]['actor'] for f in (8782,8823))
    images=list(folder.rglob('*.png'))
    assert len(images)==2 and {p.name for p in images}=={'winner_8782.png','winner_8823.png'}
    total=sum(p.stat().st_size for p in images);assert total<=512*1024
    assert not any(p.suffix.lower() in ('.bin','.wav') for p in folder.rglob('*'))
    report=dict(passed=True,sourceSync=source,terminal=terminal,totalPNGBytes=total,
                screenshots=[dict(name=p.name,sha256=sync.sha(p),bytes=p.stat().st_size) for p in images],
                scalarPreterminalPrefixUnchanged=True,earnedNativeWinFrame=8755,
                continuousRasterAccepted=False,fullPortAcceptance=False,
                scope='Two bounded current Kano P1 earned-win checkpoints, intermediate and held final pose; unchanged scalar prefix and native win at actual CPU health0. Not continuous raster, every winner context, audio, endings or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,totalPNGBytes=total,fullPortAcceptance=False)))

if __name__=='__main__':main()
