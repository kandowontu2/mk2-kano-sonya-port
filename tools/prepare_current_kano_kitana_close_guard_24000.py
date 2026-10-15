"""Continue the productive controller, without increasing wall or memory caps."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kitana_close_guard_long_preparation'
out=sync.ROOT/'audit_current_kano_kitana_close_guard_24000_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=21000')==1 and source.count('maximum_fields=21000')==1
source=source.replace('frame>=21000','frame>=24000').replace('maximum_fields=21000','maximum_fields=24000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kitana_close_guard_long_runtime','audit_current_kano_kitana_close_guard_24000_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000fields, identicalcontroller,90sec/320MiB/no media')
