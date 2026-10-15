"""Separate approach threshold from upper reach; only physical CPU5 response."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_crouch_upper_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_crouch_spacing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='if gap>70 and height<=8 and other.flags&0x10==0 then'
new='if gap>100 and height<=8 and other.flags&0x10==0 then'
assert source.count(old)==1
source=source.replace(old,new)
assert source.replace(new,old)==(base/'campaign.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_crouch_upper_runtime','audit_current_kano_p2_mileena_crouch_spacing_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only approach threshold70->100;upper reach75 unchanged;90sec/320MiB/10MiB/no media')
