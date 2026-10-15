"""Extend productive Kitana match counter to observe native next stage."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kitana_standing_counter_preparation'
out=sync.ROOT/'audit_current_kano_standing_counter_long_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=18000')==source.count('maximum_fields=18000')==1
source=source.replace('frame>=18000','frame>=21000').replace('maximum_fields=18000','maximum_fields=21000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kitana_standing_counter_runtime','audit_current_kano_standing_counter_long_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared21000fields; same physical controller,90sec/320MiB,no media')
