"""Extend only the observation bound, not gameplay or assistance."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_campaign_progress_core_preparation'
out=sync.ROOT/'audit_bounded_extended_sonya_campaign_preparation'
assert not out.exists()
out.mkdir()
source=(old/'core.lua').read_text()
assert source.count('12000')==2
lua=out/'extended.lua'
lua.write_text(source.replace('12000','18000'))
runner=(old/'run_sonya_p1.ps1').read_text()
runner=runner.replace(old.name+'/core.lua',out.name+'/extended.lua').replace(sync.sha(old/'core.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_campaign_progress_core_sonya_p1_runtime','audit_bounded_extended_sonya_campaign_p1_runtime')
(out/'run_sonya_p1.ps1').write_text(runner)
