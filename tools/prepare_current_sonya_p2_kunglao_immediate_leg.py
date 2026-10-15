"""Physical simultaneous Down/LP/Block, no three-field setup delay."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_leg_attack_guard_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_immediate_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=3 and age<7 then press('Low Punch');press('Block')end"
assert source.count(old)==1
source=source.replace(old,"if age<4 then press('Low Punch');press('Block')end")
old="kg_leg=frame;kg_retry=frame;press('Down')"
assert source.count(old)==1
source=source.replace(old,"kg_leg=frame;kg_retry=frame;press('Down');press('Low Punch');press('Block')")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_leg_attack_guard_runtime','audit_current_sonya_p2_kunglao_immediate_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Immediate physical leg chord only;90sec/320MiB/10MiB/no media')
