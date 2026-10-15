"""Grounded physical pressure from native stage3, unchanged earlier route."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_kano_campaign_reactive_preparation'
out=sync.ROOT/'audit_bounded_kano_campaign_uppercut_preparation'
assert not out.exists()
out.mkdir()
base=old/'campaign.lua'
source=base.read_text()
for before,after in (("strategy~='reactive'","strategy~='uppercut'"),("strategy='reactive';log('POLICY'","strategy='uppercut';log('POLICY'"),('physical_policy=reactive_jumpkick','physical_policy=grounded_uppercut')):
    assert source.count(before)==1
    source=source.replace(before,after)
lua=out/'campaign.lua'
lua.write_text(source)
runner=(old/'run_kano_p1.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base),sync.sha(lua))
runner=runner.replace('audit_bounded_kano_campaign_reactive_p1_runtime','audit_bounded_kano_campaign_uppercut_p1_runtime')
(out/'run_kano_p1.ps1').write_text(runner)
print('Prepared native stage3 grounded uppercut-input experiment')
