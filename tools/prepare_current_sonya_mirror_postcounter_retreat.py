"""Keep productive kick timing; retreat during post-hit recovery window."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_neutral_recovery_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_postcounter_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then')
end=source.index('   elseif leg_tactic and other.roster==0 then',start)
branch=source[start:end]
old="     if age>=10 and (ready or not safe) then press('Down');press('Block')end"
assert branch.count(old)==1
branch=branch.replace(old,"     if age>=10 then\n      if ready then press(forward=='Right' and 'Left' or 'Right')\n      elseif not safe then press('Down');press('Block')end\n     end")
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_neutral_recovery_runtime','audit_current_sonya_mirror_postcounter_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000fields; mirror-only postcounter physical retreat; no media')
