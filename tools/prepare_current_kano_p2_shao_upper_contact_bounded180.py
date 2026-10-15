"""Reach the previously unobserved Shao contact probe with the same resource caps."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_crouch_upper_contact_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_upper_contact_bounded180_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace('audit_current_kano_p2_shao_crouch_upper_contact_runtime','audit_current_kano_p2_shao_upper_contact_bounded180_runtime')
assert runner.count('TotalSeconds -gt 90')==1
runner=runner.replace('TotalSeconds -gt 90','TotalSeconds -gt 180')
(out/'run.ps1').write_text(runner)
print('Shao actualupper/nativeHP contact probe:180sec/320MiB/10MiB/no media/no guestwrites')
