"""Natural campaign: ordinary crouch+HP tactic against real Reptile9."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_p2_delayed_campaign_preparation'
out=sync.ROOT/'audit_current_sonya_reptile_uppercut_preparation';assert not out.exists()
source=(old/'campaign.lua').read_text()
needle='  if winner==0 and human.hp>0 and other.hp>0 then\n';assert source.count(needle)==1
source=source.replace(needle,needle+"   local strategy=other.roster==9 and 'uppercut' or strategy\n   local leg_tactic=strategy=='leg'or strategy=='defensive_leg'\n")
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(sync.ROOT/'audit_current_sonya_p2_leg_campaign_preparation/run.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_leg_campaign_runtime','audit_current_sonya_reptile_uppercut_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared12000field physical leg/uppercut tactic, unchanged native difficulty/RNG/resource caps')
