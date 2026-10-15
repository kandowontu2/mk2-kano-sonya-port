"""Bind eight manually inspected PNG samples to unchanged cross-grab gameplay."""
import json
from pathlib import Path
from PIL import Image
import verify_native_source_sync as sync
out=sync.ROOT/'audit_bounded_cross_grab_visual_review_checked';assert not out.exists();results={}
for move in ('choke','leg'):
    folder=sync.ROOT/f'audit_bounded_cross_grab_visual_{move}_p1_runtime'
    base=sync.ROOT/f'audit_bounded_current_cross_grab_{move}_p1_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='bounded_four_png'
    lines=(folder/'run.log').read_text().splitlines();old=(base/'run.log').read_text().splitlines()
    assert [r for r in lines if r.startswith('MK2_HSPECIAL_')]==[r for r in old if r.startswith('MK2_HSPECIAL_')]
    saved=[r for r in lines if r.startswith('MK2_HPHASE_VISUAL_SAVED ')];assert len(saved)==4
    pngs=sorted((folder/'snap').rglob('*.png'));assert len(pngs)==4
    images={}
    for path in pngs:
        with Image.open(path) as img:assert img.size==(400,254)
        images[path.name]=dict(SHA256=sync.sha(path),bytes=path.stat().st_size)
    results[move]=dict(terminal=terminal,images=images,savedReceipts=saved,logSHA256=sync.sha(folder/'run.log'),
        baselineLogSHA256=sync.sha(base/'run.log'),manualSampleReview='Expected character/victim pose, correct names, no selector overlays; no missing body or persistent grab pose observed in four samples.')
report=dict(finiteSamplesReviewed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Eight 400x254 P1 cross-grab PNG samples; selection/entry, two action phases and recovered marker. Presented snapshot may lag actor-state callback. Not whole animation, pixel-exact alignment, P2 visuals, all arenas/audio/CPU/finishers or whole port.',
    totalPNGBytes=sum(i['bytes'] for v in results.values() for i in v['images'].values()),fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(samples=8,totalPNGBytes=report['totalPNGBytes'],fullGoalComplete=False)))
