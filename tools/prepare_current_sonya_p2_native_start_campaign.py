"""Normal boot600 coin/start, native schedule selection, existing physical leg."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_delayed_campaign_preparation'
out=sync.ROOT/'audit_current_sonya_p2_native_start_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=12000')==1
source=source.replace('frame>=12000','frame>=30000').replace('maximum_fields=12000','maximum_fields=30000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace("MK2KS_CAMPAIGN_STRATEGY='zoning'","MK2KS_CAMPAIGN_STRATEGY='leg'").replace("MK2KS_TEST_BOOT_FRAME='700'","MK2KS_TEST_BOOT_FRAME='600'")
runner=runner.replace('audit_current_sonya_p2_delayed_campaign_runtime','audit_current_sonya_p2_native_start_runtime').replace("'-str','400'","'-str','900'")
(out/'run.ps1').write_text(runner)
print('Prepared30k native normal-start P2 campaign; no forced schedule/state/health, no media,90sec/320MiB caps')
