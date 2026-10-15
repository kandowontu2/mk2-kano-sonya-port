"""Physical crouch settlement before HP, initiated outside prior throw gap."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_crouch_dispatch_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_crouch_settle_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   elseif leg_tactic and other.roster==8 then')
end=source.index('   elseif (leg_tactic or strategy==',start)
branch=source[start:end]
for before,after in [('frame-sz_leg<12','frame-sz_leg<28'),("if age<9 then press('Down')end","if age<26 then press('Down')end"),("if age>=2 and age<5 then press('High Punch')end","if age>=13 and age<18 then press('High Punch')end"),('gap<90','gap<150'),('gap>85','gap>145')]:
 assert branch.count(before)==1
 branch=branch.replace(before,after)
source=source[:start]+branch+source[end:]
source=source.replace('frame-sz_leg>14','frame-sz_leg>30')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_crouch_dispatch_runtime','audit_current_sonya_subzero_crouch_settle_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared physical Down26/HP13..17, outside gap150; same9000fields/caps')
