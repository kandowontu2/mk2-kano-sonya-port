"""Unchanged earned scene records and exact bounded image count, not auto visual approval."""
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_stock_pit_sonya_impact_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_stock_pit_sonya_impact_preparation/stage.lua')
rows=base.load(folder/'run.log');old=base.load(sync.ROOT/'audit_current_stock_pit_initialized_selector_sonya_p1_kitana_runtime/run.log')
for tag in set(rows)|set(old):
    if tag=='IMPACT_IMAGE':continue
    assert rows.get(tag,[])==old.get(tag,[]),tag
images=list(folder.rglob('*.png'));assert len(images)==1 and images[0].stat().st_size<=60*1024
assert len(rows['IMPACT_IMAGE'])==1 and rows['IMPACT_IMAGE'][0]['age']=='260'
out=sync.ROOT/'audit_current_stock_pit_sonya_impact_checked'
assert not out.exists();out.mkdir()
report=dict(passedUnchangedScene=True,image=str(images[0]),bytes=images[0].stat().st_size,imageSHA256=sync.sha(images[0]),visualReviewPending=True,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
