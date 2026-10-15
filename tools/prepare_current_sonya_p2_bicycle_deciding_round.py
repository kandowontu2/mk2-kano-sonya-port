"""Same physical inputs, extend field ceiling only within existing wall cap."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_bicycle_ready_escape_preparation'
out=sync.ROOT/'audit_current_sonya_p2_bicycle_deciding_round_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="if frame>=60000 then log('HOST_BOUND','maximum_fields=60000 full_campaign_acceptance=false')"
assert source.count(marker)==1
source=source.replace(marker,"if frame>=70000 then log('HOST_BOUND','maximum_fields=70000 full_campaign_acceptance=false')")
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_bicycle_ready_escape_runtime','audit_current_sonya_p2_bicycle_deciding_round_runtime').replace("'-str','1250'","'-str','1500'")
(out/'run.ps1').write_text(runner)
print('Same controller;70k ceiling/existing90sec/320MiB/10MiB/no media')
