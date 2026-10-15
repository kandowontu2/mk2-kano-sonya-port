"""Extend the observed natural controller tactic; keep all host limits."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_preparation'
out=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_long_preparation';assert not out.exists()
source=(old/'campaign.lua').read_text()
assert source.count('frame>=12000')==1
source=source.replace('frame>=12000','frame>=20000').replace('maximum_fields=12000','maximum_fields=20000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text().replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_reptile_crouch_counter_runtime','audit_current_sonya_reptile_crouch_counter_long_runtime').replace("'-str','400'","'-str','700'")
(out/'run.ps1').write_text(runner)
print('Prepared20000fields, same physical policy, no media, unchanged90sec/320MiB/10MiB caps')
