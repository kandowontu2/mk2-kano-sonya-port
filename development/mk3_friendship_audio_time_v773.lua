dofile('mk3_friendship_audio_reference_v770.lua')
local frame,tap=0,nil
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local cpu=manager.machine.devices[':maincpu'];local p=cpu.spaces.program
  tap=p:install_write_tap(0x01680000,0x0168001f,'original Friendship exact sound time',function(at,data,mask)
   if frame>4000 and at==0x01680000 and mask&255~=0 then
    print(string.format('MK3_FRIEND_AUDIO_TIME frame=%d seconds=%.12f byte=%02X pc=%08X',frame,emu.time(),data&255,cpu.state.PC.value))
   end
  end)
 end
end)
emu.register_stop(function()if tap then tap:remove()end end)
