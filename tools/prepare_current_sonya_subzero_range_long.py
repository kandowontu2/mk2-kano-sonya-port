"""Extend existing physical range policy; no altered opponents or results."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_range_uppercut_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_range_long_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=9000')==1
source=source.replace('frame>=9000','frame>=18000').replace('maximum_fields=9000','maximum_fields=18000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_range_uppercut_runtime','audit_current_sonya_subzero_range_long_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18000fields unchanged physical range-aware uppercut policy')
