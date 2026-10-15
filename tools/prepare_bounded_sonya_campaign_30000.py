"""Same natural campaign inputs; later finite observation horizon."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_extended_sonya_campaign_preparation'
out=sync.ROOT/'audit_bounded_sonya_campaign_30000_preparation'
assert not out.exists()
out.mkdir()
source=(old/'extended.lua').read_text()
assert source.count('18000')==2
lua=out/'extended.lua'
lua.write_text(source.replace('18000','30000'))
runner=(old/'run_sonya_p1.ps1').read_text()
runner=runner.replace(old.name+'/extended.lua',out.name+'/extended.lua').replace(sync.sha(old/'extended.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_extended_sonya_campaign_p1_runtime','audit_bounded_sonya_campaign_30000_p1_runtime')
assert "'-str','300'" in runner
runner=runner.replace("'-str','300'","'-str','600'")
(out/'run_sonya_p1.ps1').write_text(runner)
