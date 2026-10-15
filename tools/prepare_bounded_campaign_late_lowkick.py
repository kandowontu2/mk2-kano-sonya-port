"""Earlier physical policy unchanged; crouch low-kick experiment after stage4."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_sonya_campaign_30000_preparation'
out=sync.ROOT/'audit_bounded_campaign_late_lowkick_preparation'
assert not out.exists()
out.mkdir()
source=(old/'extended.lua').read_text()
marker='  if winner==0 and human.hp>0 and other.hp>0 then'
assert source.count(marker)==1
source=source.replace(marker,"  if stage>=4 then strategy='lowkick';leg_tactic=false end\n"+marker)
lua=out/'campaign.lua'
lua.write_text(source)
runner=(old/'run_sonya_p1.ps1').read_text()
runner=runner.replace(old.name+'/extended.lua',out.name+'/campaign.lua').replace(sync.sha(old/'extended.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_sonya_campaign_30000_p1_runtime','audit_bounded_campaign_late_lowkick_p1_runtime')
(out/'run_sonya_p1.ps1').write_text(runner)
