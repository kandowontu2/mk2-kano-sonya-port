"""Bind eight inspected samples to unchanged earned native finisher traces."""
import json
from pathlib import Path
from PIL import Image
import verify_native_source_sync as sync
out=sync.ROOT/'audit_bounded_secondary_visual_samples_checked'
assert not out.exists()
results={}
for fighter in ('kano','sonya'):
    folder=sync.ROOT/f'audit_bounded_secondary_visual_{fighter}_p1_runtime'
    baseline=sync.ROOT/f'audit_bounded_secondary_finisher_{fighter}_p1_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='bounded_four_png'
    lines=(folder/'run.log').read_text().splitlines()
    old=(baseline/'run.log').read_text().splitlines()
    prefix='MK2_STOCK_HEAD_V921_'
    actual=[r for r in lines if r.startswith(prefix) and not r.startswith(prefix+'VISUAL_SAVED ')]
    assert actual==[r for r in old if r.startswith(prefix)]
    receipts=[r for r in lines if r.startswith(prefix+'VISUAL_SAVED ')]
    assert len(receipts)==4
    images={}
    for stage in ('startup','active','late','post_wrap'):
        path=folder/'snap'/f'secondary_{stage}.png'
        with Image.open(path) as img:assert img.size==(400,254)
        images[stage]=dict(SHA256=sync.sha(path),bytes=path.stat().st_size)
    assert len(list((folder/'snap').rglob('*.png')))==4
    results[fighter]=dict(terminal=terminal,images=images,savedReceipts=receipts,
        logSHA256=sync.sha(folder/'run.log'),baselineLogSHA256=sync.sha(baseline/'run.log'),
        manualReview='Correct performer/victim names and bodies, own laser/orb effects and own winner pose, no selection portraits observed. Post-wrap debris remains visible; no later scene clearing claim. Finite screenshots, not full animation/geometry/palette/shadow/audio acceptance.')
report=dict(finiteSampleReviewPassed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    totalPNGBytes=sum(i['bytes'] for r in results.values() for i in r['images'].values()),
    scope='Eight manually inspected P1 secondary finisher samples against Kitana; exact original native scalar trace retained. No P2/all-victim/full-animation/final effects retirement/next-scene/audio or full-port acceptance.',fullGoalComplete=False)
out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(samples=8,totalPNGBytes=report['totalPNGBytes'],fullGoalComplete=False)))
