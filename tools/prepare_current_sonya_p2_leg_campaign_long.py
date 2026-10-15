"""Longer finite cold campaign; keep original physical policy and host limits."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_p2_delayed_campaign_preparation'
runner_base=sync.ROOT/'audit_current_sonya_p2_leg_campaign_preparation/run.ps1'
out=sync.ROOT/'audit_current_sonya_p2_leg_campaign_long_preparation'
assert not out.exists()
source=(old/'campaign.lua').read_text()
assert source.count('frame>=12000')==1 and source.count('maximum_fields=12000')==1
source=source.replace('frame>=12000','frame>=30000').replace('maximum_fields=12000','maximum_fields=30000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=runner_base.read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_leg_campaign_runtime','audit_current_sonya_p2_leg_campaign_long_runtime')
runner=runner.replace("'-str','400'","'-str','700'")
(out/'run.ps1').write_text(runner)
print('Prepared30000field cold campaign,90sec/320MiB/10MiB caps unchanged')
