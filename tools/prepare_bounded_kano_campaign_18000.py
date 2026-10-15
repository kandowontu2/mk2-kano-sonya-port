"""Extend unchanged cold physical campaign past earlier 12000-field bound."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_campaign_progress_core_preparation'
out=sync.ROOT/'audit_bounded_kano_campaign_18000_preparation'
assert not out.exists()
out.mkdir()
base=old/'core.lua'
source=base.read_text()
marker="if frame>=12000 then log('HOST_BOUND','maximum_fields=12000 full_campaign_acceptance=false')"
assert source.count(marker)==1
source=source.replace(marker,"if frame>=18000 then log('HOST_BOUND','maximum_fields=18000 full_campaign_acceptance=false')")
lua=out/'campaign.lua'
lua.write_text(source)
runner=(old/'run_kano_p1.ps1').read_text()
runner=runner.replace(old.name+'/core.lua',out.name+'/campaign.lua').replace(sync.sha(base),sync.sha(lua))
runner=runner.replace('audit_bounded_campaign_progress_core_kano_p1_runtime','audit_bounded_kano_campaign_18000_p1_runtime')
assert "'-str','300'" in runner
runner=runner.replace("'-str','300'","'-str','400'")
(out/'run_kano_p1.ps1').write_text(runner)
print('Prepared unchanged 18000-field Kano P1 policy, str400 avoids timed final snapshot')
