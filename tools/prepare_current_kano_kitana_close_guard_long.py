"""Extend productive physical controller only, retain90second resource bounds."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kitana_close_guard_preparation'
out=sync.ROOT/'audit_current_kano_kitana_close_guard_long_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=18000')==1 and source.count('maximum_fields=18000')==1
source=source.replace('frame>=18000','frame>=21000').replace('maximum_fields=18000','maximum_fields=21000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kitana_close_guard_runtime','audit_current_kano_kitana_close_guard_long_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared21000field productivecontroller continuation,90sec/320MiB/no media')
