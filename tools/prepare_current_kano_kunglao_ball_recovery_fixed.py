"""Correct physical-controller native action constant; executed original retained."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kunglao_guarded_ball_preparation'
out=sync.ROOT/'audit_current_kano_kunglao_ball_recovery_fixed_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
before='human.action~=531 and frame-kb_release>=12'
assert source.count(before)==1
native=(sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
assert 'ball_movi(1, 0x020b);' in native
source=source.replace(before,'human.action~=523 and frame-kb_release>=12')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kunglao_guarded_ball_runtime','audit_current_kano_kunglao_ball_recovery_fixed_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000fields; only physical recovery exclusion531to523,no media')
