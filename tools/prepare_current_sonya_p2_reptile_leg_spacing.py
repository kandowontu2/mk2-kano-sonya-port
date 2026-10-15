"""Extend qualified physical leg spacing to Reptile9, preserve earlier route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_liukang_leg_spacing_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_leg_spacing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='other.roster==0 or (side==2 and other.roster==1)'
assert source.count(old)==1
source=source.replace(old,'other.roster==0 or (side==2 and (other.roster==1 or other.roster==9))')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_liukang_leg_spacing_runtime','audit_current_sonya_p2_reptile_leg_spacing_runtime')
(out/'run.ps1').write_text(runner)
print('Reptile9 physical leg spacing only;90sec/320MiB/10MiB/no media')
