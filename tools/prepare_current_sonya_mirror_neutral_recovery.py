"""Avoid prebuffered crouch-block while busy and opponent in stance; retain HK timing."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_standing_counter_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_neutral_recovery_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then')
end=source.index('   elseif leg_tactic and other.roster==0 then',start)
branch=source[start:end]
before="if age>=10 then press('Down');press('Block')end"
assert branch.count(before)==1
branch=branch.replace(before,"if age>=10 and (ready or not safe) then press('Down');press('Block')end")
before="    else\n     ms_start=nil;press('Down');press('Block')\n    end"
assert branch.count(before)==1
branch=branch.replace(before,"    elseif not ready and safe then\n     ms_start=nil -- Release recovery inputs; no standing pose is assumed.\n    else\n     ms_start=nil;press('Down');press('Block')\n    end")
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_standing_counter_runtime','audit_current_sonya_mirror_neutral_recovery_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000fields; mirror-only recovery-input release,no media')
