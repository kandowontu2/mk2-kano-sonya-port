"""Only actual CPU2 Cage gets immediate physical HK; native combat unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_campaign_slim_health_preparation'
out=sync.ROOT/'audit_current_kano_p2_cage_early_hk_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=2 and age<6 then press('High Kick')end"
new="if age>=(other.roster==2 and 0 or 2) and age<(other.roster==2 and 4 or 6) then press('High Kick')end"
assert source.count(old)==1
source=source.replace(old,new)
oldstart='kp_start=frame;kp_retry=frame'
assert source.count(oldstart)==1
source=source.replace(oldstart,oldstart+";if other.roster==2 then press('High Kick')end")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_campaign_slim_health_runtime','audit_current_kano_p2_cage_early_hk_runtime')
(out/'run.ps1').write_text(runner)
print('CPU2 Cage-only physical HK age0..3 including initial trigger;90sec/320MiB/10MiB/no media')
