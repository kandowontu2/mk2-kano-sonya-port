"""Identical physical controller, higher field ceiling, existing wall cap."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_hk_retreat_preparation'
out=sync.ROOT/'audit_current_sonya_p2_campaign_render_skip_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="if frame>=40000 then log('HOST_BOUND','maximum_fields=40000 full_campaign_acceptance=false')"
assert source.count(marker)==1
source=source.replace(marker,"if frame>=60000 then log('HOST_BOUND','maximum_fields=60000 full_campaign_acceptance=false')")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_hk_retreat_runtime','audit_current_sonya_p2_campaign_render_skip_runtime')
assert runner.count("'-frameskip','0'")==1
runner=runner.replace("'-frameskip','0'","'-frameskip','10'").replace("'-str','900'","'-str','1250'")
(out/'run.ps1').write_text(runner)
print('Same controller;frameskip10;60k field ceiling/existing90sec/320MiB/10MiB/no media')
