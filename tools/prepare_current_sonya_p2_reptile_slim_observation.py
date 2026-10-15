"""Observation-only log reduction, identical physical controller."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_leg_spacing_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_slim_observation_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='if mask==0xffff and first_live then'
assert source.count(old)==1
source=source.replace(old,'if mask==0xffff and first_live and (frame<6684 or p:read_u16(at)~=(data&0xffff)) then')
old='if live_fields<300 or frame%30==0 then'
assert source.count(old)==1
source=source.replace(old,'if live_fields<300 or (frame<6684 and frame%30==0) or frame%120==0 then')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_leg_spacing_runtime','audit_current_sonya_p2_reptile_slim_observation_runtime')
(out/'run.ps1').write_text(runner)
print('Observer-only HP no-op filter/LIVE120 after6683; physical controller unchanged;90sec/320MiB/10MiB/no media')
