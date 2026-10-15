"""Reuse proven native-readiness guarded leg policy for Sub-Zero only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_mirror_guard_preparation'
out=sync.ROOT/'audit_current_sonya_p2_subzero_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='if leg_tactic and other.roster==18 then'
assert source.count(old)==1
source=source.replace(old,'if leg_tactic and (other.roster==18 or other.roster==8) then')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_mirror_guard_runtime','audit_current_sonya_p2_subzero_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared30k SubZero guarded readiness/leg only, mirror inputs unchanged/no media')
