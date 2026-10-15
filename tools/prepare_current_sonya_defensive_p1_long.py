"""Extend actual productive five-stage route; retain exact physical policy."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_defensive_routes_preparation'
out=sync.ROOT/'audit_current_sonya_defensive_p1_long_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=18000')==1
source=source.replace('frame>=18000','frame>=30000').replace('maximum_fields=18000','maximum_fields=30000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_p1.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_defensive_routes_p1_runtime','audit_current_sonya_defensive_p1_long_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared SonyaP1 productive route extension30000fields, unchanged native inputs/resource caps')
