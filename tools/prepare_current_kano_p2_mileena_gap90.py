"""One physical spacing adjustment based on observed native throw-start gaps."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_throw_trace_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_gap90_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='elseif other.roster==5 and gap<70 and height<=8 then'
new='elseif other.roster==5 and gap<90 and height<=8 then'
assert source.count(old)==1
source=source.replace(old,new)
assert source.replace(new,old)==(base/'campaign.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_throw_trace_runtime','audit_current_kano_p2_mileena_gap90_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only physical retreat gap70->90; passive throw trace retained;90sec/320MiB/10MiB/no media')
