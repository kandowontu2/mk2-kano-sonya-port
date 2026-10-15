"""Retain actual launch release; defer physical kick until closer/lower flight."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_subzero_release_jump_preparation'
out=sync.ROOT/'audit_current_sonya_p2_subzero_late_kick_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if frame%6<3 then press('High Kick')end"
start=source.index('   elseif leg_tactic and other.roster==8 then\n')
end=source.index("   elseif (leg_tactic or strategy=='lowkick'",start)
branch=source[start:end]
assert branch.count(old)==1
branch=branch.replace(old,"if gap<115 and height<90 and frame%6<3 then press('High Kick')end")
source=source[:start]+branch+source[end:]
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_subzero_release_jump_runtime','audit_current_sonya_p2_subzero_late_kick_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared9000fields same launch/flight kick gap<115 height<90; no media')
