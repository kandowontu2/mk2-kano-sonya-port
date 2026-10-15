"""Confirm neutral observer and bounded naturally reached victim checkpoint."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kitana_victim_visual_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_kitana_victim_visual_preparation/campaign.lua')
rows=chronology.load(folder/'run.log');old=chronology.load(sync.ROOT/'audit_current_kano_kitana_confirmed_jump_runtime/run.log')
for tag in set(rows)|set(old):
    if tag=='VICTIM_IMAGE':continue
    assert rows.get(tag,[])==old.get(tag,[]),tag
assert len(rows['VICTIM_IMAGE'])==1
images=list(folder.rglob('*.png'));assert len(images)==1 and images[0].stat().st_size<=60*1024
out=sync.ROOT/'audit_current_kano_kitana_victim_visual_checked'
assert not out.exists();out.mkdir()
report=dict(passedObserverNeutrality=True,nativeCheckpoint=rows['VICTIM_IMAGE'][0],
 imageSHA256=sync.sha(images[0]),bytes=images[0].stat().st_size,
 visualReview='Reviewed actual PNG: own Kano elevated in coherent victim pose, stock Kitana kneeling with arm extended, correct KANO/KITANA lifebars and name shadow, native arena/FIGHT overlay, no selection photos/cursor remnants. Single naturally reached checkpoint only.',
 fullCampaignClear=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
