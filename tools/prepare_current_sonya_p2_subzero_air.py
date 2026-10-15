"""Actual flight feedback against Sub-Zero; retain earned mirror route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_mirror_guard_preparation'
out=sync.ROOT/'audit_current_sonya_p2_subzero_air_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('    -- Read-only feedback: jump from actual grounded state')
end=source.index('    previous_y=human.y',start)+len('    previous_y=human.y')
branch="   elseif leg_tactic and other.roster==8 then\n"+source[start:end]+'\n'
needle="   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(needle)==1
source=source.replace(needle,branch+needle)
source=source.replace('frame>=30000','frame>=16000').replace('maximum_fields=30000','maximum_fields=16000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_mirror_guard_runtime','audit_current_sonya_p2_subzero_air_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared16k actual-flight SubZero policy; unchanged mirror opening, no media')
