"""Physical retreat resumes when HK command ends, rather than four fields later."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_hk_throw_onset_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_hk_early_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='(not sh_start or frame-sh_start>=10)'
assert source.count(old)==1
source=source.replace(old,'(not sh_start or frame-sh_start>=(other.roster==9 and 6 or 10))')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_hk_throw_onset_runtime','audit_current_sonya_p2_reptile_hk_early_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('Reptile-only HK retreat delay10->6;90sec/320MiB/10MiB/no media')
