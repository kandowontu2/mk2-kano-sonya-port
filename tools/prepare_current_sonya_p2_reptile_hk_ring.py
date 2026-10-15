"""Reuse current successful Sonya SubZero/Cage physical HK/ring policy."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_liukang_leg_spacing_preparation'
observer=sync.ROOT/'audit_current_sonya_p2_reptile_damage_trace_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_hk_ring_preparation'
assert not out.exists()
# Keep slim observer/damage tap, remove only failed Reptile leg-policy extension.
source=(observer/'campaign.lua').read_text()
old='other.roster==0 or (side==2 and (other.roster==1 or other.roster==9))'
assert source.count(old)==1
source=source.replace(old,'other.roster==0 or (side==2 and other.roster==1)')
old="(other.roster==8 or other.roster==2 or other.roster==0) then"
assert source.count(old)==1
source=source.replace(old,"(other.roster==8 or other.roster==2 or other.roster==0 or other.roster==9) then")
old='(other.roster==2 or other.roster==0) and 100 or 90'
assert source.count(old)==1
source=source.replace(old,'(other.roster==2 or other.roster==0 or other.roster==9) and 100 or 90')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(observer/'run.ps1').read_text().replace(observer.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(observer/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_damage_trace_runtime','audit_current_sonya_p2_reptile_hk_ring_runtime')
(out/'run.ps1').write_text(runner)
print('Reptile9 uses qualified physical HK/ring branch;90sec/320MiB/10MiB/no media')
