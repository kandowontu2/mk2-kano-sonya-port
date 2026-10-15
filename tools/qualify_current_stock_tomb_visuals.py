"""Exact earned-controller equivalence plus four individually reviewed images."""
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync
sync.verify()
results=[]
total=0
for case in ('kunglao','jax_sonya_p2'):
    folder=sync.ROOT/('audit_current_stock_tomb_visual_'+case+'_runtime')
    prior=sync.ROOT/('audit_current_native_tomb_stock_'+case+'_runtime')
    checked=json.loads((sync.ROOT/('audit_current_native_tomb_stock_'+case+'_checked/report.json')).read_text())
    assert checked['passedNativeStockVictimTomb'] and checked['logSHA256']==sync.sha(prior/'run.log')
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/('audit_current_stock_tomb_visual_preparation/'+case+'.lua'))
    assert not (folder/'stderr.log').read_text().strip()
    rows=base.load(folder/'run.log');old=base.load(prior/'run.log')
    for tag in set(rows)|set(old):
        if tag=='VISUAL_SAVED':continue
        assert rows.get(tag,[])==old.get(tag,[])
    assert [r['age'] for r in rows['VISUAL_SAVED']]==['120','600']
    images=sorted(folder.rglob('*.png'))
    assert len(images)==2 and {p.name for p in images}=={'stock_tomb_120.png','stock_tomb_600.png'}
    size=sum(p.stat().st_size for p in images);assert size<=120*1024;total+=size
    results.append(dict(case=case,actualControllerAndSceneRecordsUnchanged=True,
                        reviewedImages=[dict(path=str(p),SHA256=sync.sha(p)) for p in images],
                        ceilingSpikesStockVictimReviewed=True,ownWinnerPoseAndNameReviewed=True,
                        nativeContinueDoorsReviewed=True,noSelectorPortraitLeftoversObserved=True))
assert total<=240*1024
out=sync.ROOT/'audit_current_stock_tomb_visuals_checked'
assert not out.exists();out.mkdir()
report=dict(passedFiniteVisualReview=True,cases=results,images=4,totalImageBytes=total,
            audioAccepted=False,allFramesReviewed=False,allStockVictimsAccepted=False,
            fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(passed=True,images=4,totalImageBytes=total,fullPortAccepted=False)))
