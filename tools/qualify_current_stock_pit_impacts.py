"""Two reviewed late stock-victim Pit frames; no all-frame/heard-mix claims."""
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync
sync.verify()
cases=[];total=0
for name in ('kunglao','jax_sonya_p2'):
    folder=sync.ROOT/('audit_current_stock_pit_impact_'+name+'_runtime')
    prior=sync.ROOT/('audit_current_native_pit_stock_'+name+'_runtime')
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/('audit_current_stock_pit_impact_preparation/'+name+'.lua'))
    assert not (folder/'stderr.log').read_text().strip()
    rows=base.load(folder/'run.log');old=base.load(prior/'run.log')
    for tag in set(rows)|set(old):
        if tag in ('IMPACT_IMAGE','VISUAL_SAVED'):continue
        assert rows.get(tag,[])==old.get(tag,[])
    assert len(rows['IMPACT_IMAGE'])==1 and rows['IMPACT_IMAGE'][0]['age']=='260'
    images=list(folder.rglob('*.png'));assert len(images)==1 and images[0].name=='stock_pit_impact_260.png'
    image=images[0];size=image.stat().st_size;assert size<=60*1024;total+=size
    cases.append(dict(case=name,unchangedNativeSceneRecords=True,reviewedImage=str(image),imageSHA256=sync.sha(image),age=260))
assert total<=120*1024
out=sync.ROOT/'audit_current_stock_pit_impacts_checked'
assert not out.exists();out.mkdir()
report=dict(passedFiniteImpactVisualReview=True,cases=cases,totalImageBytes=total,
            allFramesReviewed=False,heardMixAccepted=False,allStockVictimsAccepted=False,
            fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
