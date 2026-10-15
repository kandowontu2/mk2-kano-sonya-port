"""Restore productive current defensive-leg route, initialized selector and mirror guard."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_mirror_guard_preparation'
out=sync.ROOT/'audit_current_sonya_defensive_routes_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster))'
assert source.count(old)==1
source=source.replace(old,'css=frame;selections=selections+1;plan={}')
needle='  local age=frame-css\n'
assert source.count(needle)==1
source=source.replace(needle,needle+"  if age==56 then plan=route(p:read_u16(slots[side].roster));log('SELECT_INITIALIZED','target='..identity..' initial='..p:read_u16(slots[side].roster))end\n")
source=source.replace('frame>=30000','frame>=18000').replace('maximum_fields=30000','maximum_fields=18000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace("$env:MK2KS_CAMPAIGN_STRATEGY='leg'","$env:MK2KS_CAMPAIGN_STRATEGY='defensive_leg'")
for side in (1,2):
 text=runner.replace('audit_current_sonya_p2_mirror_guard_runtime',f'audit_current_sonya_defensive_routes_p{side}_runtime')
 text=text.replace("$env:MK2KS_CAMPAIGN_SIDE='2'",f"$env:MK2KS_CAMPAIGN_SIDE='{side}'")
 (out/f'run_p{side}.ps1').write_text(text)
print('Prepared native defensive-leg both slots/post-init selections/mirror guard;18000fields each')
