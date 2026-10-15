-- Unchanged cold real-input move scenario plus read-only native sound timing.
dofile('mk2ks_human_special_matrix_v3.lua')
local cpu=manager.machine.devices[':maincpu']
local frame,tap=0,nil
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  tap=cpu.spaces.program:install_write_tap(0x01d01030,0x01d0103f,'actual special native sound time',function(at,data,mask)
   if at==0x01d01030 and mask==0xffff then
    print(string.format('MK2_HAUDIO_SOUND frame=%d seconds=%.12f word=%04X mask=%04X pc=%08X writes=0 assistance=none',frame,emu.time(),data,mask,cpu.state.PC.value))
   end
  end)
 end
end)
emu.register_stop(function()
 print(string.format('MK2_HAUDIO_RESULT frame=%d seconds=%.12f writes=0 assistance=none',frame,emu.time()))
 if tap then tap:remove()end
end)
