"""Actual close-range leg command after native crouch preparation."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_range_uppercut_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_settled_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=13 and age<26 and gap<95 and age%6<3 then press('High Punch')end"
assert source.count(old)==1
source=source.replace(old,"if age>=13 and age<26 and gap<85 and age%6<3 then press('Low Punch');press('Block')end")
source+='''
taps[#taps+1]=p:install_read_tap(0xfff80800,0xfff8080f,'read-only own leg activation',function()
 if cpu.PC.value~=0xfff80810 then return end
 local own,other=sample(side),sample(opponent)
 if own and other and other.roster==8 and cpu.A8.value==own.actor then
  log('SUBZERO_LEG_ENTRY',string.format('actor=%08X main=%08X id=%d roster=%d gap=%d health=%d,%d pc=%08X',own.actor,own.main,own.id,own.roster,math.abs(own.x-other.x),own.hp,other.hp,cpu.PC.value))
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_range_uppercut_runtime','audit_current_sonya_subzero_settled_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared native crouch-settled LP+Block at gap<85; same9000field caps')
