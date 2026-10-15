"""Read-only main crouch/ordinary HP path, capped scalar observer."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_hp_dispatch_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_crouch_dispatch_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source+='''
local crouch_dispatch_count=0
for _,address in ipairs({0xff82f9f0,0xff82fa40,0xff82fd10,0xff82fe00,0xff82fef0,0xff8300c0,0xff832040,0xff836fe0})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'read-only main crouch '..address,function()
  if not sz_leg or frame-sz_leg>14 or crouch_dispatch_count>=200 then return end
  if cpu.PC.value~=address+16 then return end
  local own,other=sample(side),sample(opponent)
  if not own or not other or other.roster~=8 or cpu.A8.value~=own.actor then return end
  crouch_dispatch_count=crouch_dispatch_count+1
  log('SUBZERO_CROUCH_DISPATCH',string.format('start=%d age=%d entry=%08X pc=%08X a0=%08X a1=%08X a13=%08X actor=%08X main=%08X action=%d counter=%d main_slot=%d body=%04X',sz_leg,frame-sz_leg,address,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A13.value,own.actor,own.main,own.action,p:read_u16(own.main+0x220),p:read_u16(own.main+0x20),own.body))
 end)
end
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_hp_dispatch_runtime','audit_current_sonya_subzero_crouch_dispatch_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared native main crouch/HP/counter path, max200 added scalar records')
