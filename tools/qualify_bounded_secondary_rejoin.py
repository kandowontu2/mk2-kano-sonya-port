"""Earned finisher -> actual paid continue -> reselected match; finite rasters."""
import json,re
from pathlib import Path
from PIL import Image
import verify_native_source_sync as sync
out=sync.ROOT/'audit_bounded_secondary_rejoin_checked'
assert not out.exists()
results={}
def records(path):
    rows={};lines=[]
    for line in path.read_text().splitlines():
        assert '[LUA ERROR]' not in line and '_FAILED ' not in line
        if line.startswith('MK2_STOCK_HEAD_V921_'):
            rows.setdefault(line.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
            lines.append(line)
    return rows,lines
for fighter,identity,address,duration in [('kano','17','FFD86600',196),('sonya','18','FFD7B000',197)]:
    folder=sync.ROOT/f'audit_bounded_secondary_rejoin_delayed_{fighter}_p1_runtime'
    baseline=sync.ROOT/f'audit_bounded_secondary_finisher_{fighter}_p1_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='bounded_two_png'
    assert not (folder/'stderr.log').read_text().strip()
    rows,lines=records(folder/'run.log');old,oldlines=records(baseline/'run.log')
    action=rows['ACTION'][0];wrap=rows['WRAP'][0]
    assert len(rows['ACTION'])==len(rows['WRAP'])==1
    assert action['variant']=='2' and action['address']==address and action['damage']=='322'
    assert int(wrap['frame'])-int(action['frame'])==duration
    bound=int(wrap['frame'])+120
    def originalPrefix(lines):return [r for r in lines if int(re.search(r'frame=(\d+)',r)[1])<bound]
    assert originalPrefix(lines)==originalPrefix(oldlines)
    assert not rows.get('CACHE_OVERWRITE')
    request=rows['REJOIN_REQUEST'][0];css=rows['REJOIN_CSS'][0];live=rows['REJOIN_LIVE'][0];end=rows['REJOIN_TERMINAL'][0]
    assert int(wrap['frame'])<int(request['frame'])<int(css['frame'])<int(live['frame'])<int(end['frame'])
    assert live['own_id']==identity and live['victim_id']=='4'
    assert live['own_actor']==live['own_owner'] and live['victim_actor']==live['victim_owner']
    assert int(end['frame'])-int(live['frame'])==60
    req=int(request['frame'])
    paid=[r for r in rows['INPUT'] if r['slot']=='2' and int(r['frame'])>=req and r['button'] in ('Coin','Start')]
    assert len([r for r in paid if r['button']=='Coin'])==10
    assert [int(r['frame'])-req for r in paid if r['button']=='Start']==list(range(310,315))
    images={}
    for stage in ('selection','next_match'):
        path=folder/'snap'/f'rejoin_{stage}.png'
        with Image.open(path) as img:assert img.size==(400,254)
        images[stage]=dict(SHA256=sync.sha(path),bytes=path.stat().st_size)
    assert len(list((folder/'snap').rglob('*.png')))==2
    results[fighter]=dict(terminal=terminal,request=request,selection=css,newMatch=live,survivalFields=60,
        images=images,logSHA256=sync.sha(folder/'run.log'),baselineLogSHA256=sync.sha(baseline/'run.log'),
        manualReview='Native selection and next arena with correct Kano/Sonya versus Kitana bodies/names; no prior laser/orb/debris/selector overlays observed in next-match sample. Finite raster samples, not every transition field.')
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Two P1 secondary finishers, original earned native prefix unchanged, actual loser credit/Start/reselection and next match60fields; four inspected transition rasters. Not P2/all victims/full cleanup chronology/audio/campaign or full-port acceptance.',fullGoalComplete=False)
out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,rejoinedMatches=2,reviewedPNGs=4,fullGoalComplete=False)))
