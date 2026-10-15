"""Exact accepted ordinary/scene input equivalence; raster review separate."""
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync
sync.verify()
prior_report=json.loads((sync.ROOT/'audit_current_stock_tomb_other_sides_checked/report.json').read_text())
assert prior_report['passedFiniteStockTombRoles']
out=sync.ROOT/'audit_current_stock_tomb_other_sides_visuals_checked'
assert not out.exists()
results=[];total=0
for proof in prior_report['cases']:
    case=proof['case']
    folder=sync.ROOT/('audit_current_stock_tomb_other_sides_visual_'+case+'_runtime')
    prior=sync.ROOT/('audit_current_stock_tomb_'+case+'_runtime')
    assert proof['logSHA256']==sync.sha(prior/'run.log')
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/('audit_current_stock_tomb_other_sides_visual_preparation/'+case+'.lua'))
    assert not (folder/'stderr.log').read_text().strip()
    rows,old=base.load(folder/'run.log'),base.load(prior/'run.log')
    for tag in set(rows)|set(old):
        if tag=='VISUAL_SAVED':continue
        assert rows.get(tag,[])==old.get(tag,[]),tag
    assert len(rows['VISUAL_SAVED'])==1 and rows['VISUAL_SAVED'][0]['age']=='120'
    images=list(folder.rglob('*.png'))
    assert len(images)==1 and images[0].name=='stock_tomb_120.png'
    size=images[0].stat().st_size;assert size<=60*1024;total+=size
    results.append(dict(case=case,actualControllerAndSceneRecordsUnchanged=True,image=str(images[0]),imageSHA256=sync.sha(images[0]),imageBytes=size,terminal=terminal))
assert total<=120*1024
out.mkdir();(out/'report.json').write_text(json.dumps(dict(passedObserverNeutrality=True,cases=results,images=2,totalImageBytes=total,visualReviewPending=True,allFramesReviewed=False,fullPortAccepted=False),indent=2))
print(json.dumps(dict(passed=True,images=2,totalImageBytes=total)))
