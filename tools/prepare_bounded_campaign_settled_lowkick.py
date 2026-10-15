"""Correct only physical lowkick crouch timing; retain failed immediate policy."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_campaign_late_lowkick_preparation'
out=sync.ROOT/'audit_bounded_campaign_settled_lowkick_preparation'
assert not out.exists()
out.mkdir()
source=(old/'campaign.lua').read_text()
for before,after in [
 ('if close_start and frame-close_start<12 then',"if close_start and frame-close_start<(strategy=='lowkick'and 20 or 12) then"),
 ("press('Down');if age<4 then press('Low Kick')end","press('Down');if age>=12 and age<18 then press('Low Kick')end"),
 ("elseif strategy=='lowkick'then press('Down');press('Low Kick')","elseif strategy=='lowkick'then press('Down')"),
 ('30000','24000')]:
    assert before in source
    source=source.replace(before,after)
lua=out/'campaign.lua'
lua.write_text(source)
runner=(old/'run_sonya_p1.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_campaign_late_lowkick_p1_runtime','audit_bounded_campaign_settled_lowkick_p1_runtime')
(out/'run_sonya_p1.ps1').write_text(runner)
