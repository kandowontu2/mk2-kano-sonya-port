"""Passive native HP parser/fallback path during bounded failed attempts."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_uppercut_spacing_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_hp_dispatch_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source+='''
local hp_dispatch_count=0
for _,address in ipairs({0xffffc800,0xfffaa400,0xff8775d0,0xff877420,0xff8771f0,0xff861d70,0xff861350,0xff861500})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'read-only native HP dispatch '..address,function()
  if not sz_leg or frame-sz_leg>14 or hp_dispatch_count>=200 then return end
  if cpu.PC.value~=address+16 then return end
  local own,other=sample(side),sample(opponent)
  if not own or not other or other.roster~=8 then return end
  hp_dispatch_count=hp_dispatch_count+1
  log('SUBZERO_HP_DISPATCH',string.format('start=%d age=%d entry=%08X pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X actor=%08X main=%08X action=%d flags=%04X body=%04X',sz_leg,frame-sz_leg,address,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,own.actor,own.main,own.action,own.flags,own.body))
 end)
end
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_uppercut_spacing_runtime','audit_current_sonya_subzero_hp_dispatch_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared passive eight-entry HP parser trace, max200 records, same9000fields/no media')
