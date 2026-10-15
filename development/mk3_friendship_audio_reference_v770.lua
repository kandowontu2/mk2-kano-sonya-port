-- Original MK3 read-only sound observation atop the retained physical scene
-- reference. That scene uses opponent-health-only assistance, not port proof.
dofile('mk3_friendship_scene_reference_v758.lua')
local frame,cpu,p,taps=0,nil,nil,{}
local function log(tag,text)
 print(string.format('MK3_FRIEND_AUDIO_%s frame=%d %s',tag,frame,text))
end
emu.register_frame(function()
 frame=frame+1
 if frame~=1 then return end
 cpu=manager.machine.devices[':maincpu'];p=cpu.spaces.program
 for _,at in ipairs({0xffaa65a0,0xffaa6aa0,0xffaa6e00})do
  taps[#taps+1]=p:install_read_tap(at,at+15,'original Friendship audio selection',function(offset)
   if offset~=at then return end
   local actor=cpu.state.A8.value
   local id=actor>=0x01000000 and actor<0x01400000 and p:read_u16(actor+0x1f0)or-1
   if at~=0xffaa6e00 then
    log('CALLBACK',string.format('entry=%08X actor=%08X id=%d a13=%08X',at,actor,id,cpu.state.A13.value))
   else
    local table=cpu.state.A0.value
    if table>=0xffaa65d0 and table<=0xffaa65f0 or table>=0xffaa6ad0 and table<=0xffaa6b30 then
     log('TABLE',string.format('entry=%08X packed=%08X command=%04X actor=%08X id=%d',table,p:read_u32(table),p:read_u16(table+16),actor,id))
    end
   end
  end)
 end
 taps[#taps+1]=p:install_write_tap(0x01680000,0x0168001f,'actual original DCS bytes',function(at,data,mask)
  if at==0x01680000 and mask&255~=0 then log('BYTE',string.format('pc=%08X value=%02X mask=%04X',cpu.state.PC.value,data&255,mask))end
 end)
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
