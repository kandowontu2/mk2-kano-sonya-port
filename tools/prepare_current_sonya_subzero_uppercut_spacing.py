"""Start crouch/HP before entering the observed CPU throw proximity."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_early_uppercut_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_uppercut_spacing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   elseif leg_tactic and other.roster==8 then')
end=source.index('   elseif (leg_tactic or strategy==',start)
branch=source[start:end]
assert branch.count('gap<63')==1 and branch.count('gap>58')==1
branch=branch.replace('gap<63','gap<90').replace('gap>58','gap>85')
source=source[:start]+branch+source[end:]
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_early_uppercut_runtime','audit_current_sonya_subzero_uppercut_spacing_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared physical uppercut preparation at gap<90 instead of63; same9000field cap')
