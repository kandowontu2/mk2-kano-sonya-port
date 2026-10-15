"""Use actual vertical velocity to time physical HK on descent, no guest writes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_mirror_confirmed_jump_preparation'
out=sync.ROOT/'audit_current_mirror_descending_kick_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
first=source.index('   if leg_tactic and other.roster==18 then\n')
last=source.index('   elseif leg_tactic and other.roster==0 then',first)
branch=source[first:last]
old="if jumping and height>20 and frame%6<3 then press('High Kick')end"
assert branch.count(old)==1
branch=branch.replace(old,"if jumping and height>8 and height<70 and p:read_i32(human.actor+0x60)>0 and frame%6<3 then press('High Kick')end")
assert branch.count('gap>90')==2
branch=branch.replace('gap>90','gap>45')
branch=branch.replace('MIRROR_CONFIRMED_JUMP_ATTEMPT','MIRROR_DESCENDING_KICK_ATTEMPT')
source=source[:first]+branch+source[last:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_mirror_confirmed_jump_runtime','audit_current_mirror_descending_kick_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared21000field descending physical kick tactic,no media,90sec/320MiB')
