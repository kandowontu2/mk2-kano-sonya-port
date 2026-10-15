"""Only CPU2 retreat threshold changes; retain all existing passive probes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_cage_contact_trace_preparation'
out=sync.ROOT/'audit_current_sonya_p2_cage_early_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='if height<=8 and gap<90 and (not sh_start'
assert source.count(marker)==1
source=source.replace(marker,'if height<=8 and gap<(other.roster==2 and 100 or 90) and (not sh_start')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_cage_contact_trace_runtime','audit_current_sonya_p2_cage_early_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('CPU2 physical back threshold100 only;30k/90sec/320MiB/10MiB/no media')
