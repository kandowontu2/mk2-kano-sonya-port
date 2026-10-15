-- Read-only audio observation over genuine cold physical-input gameplay.
dofile('mk2ks_native_friendship_probe_v788.lua')
local frame,tap=0,nil
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local cpu=manager.machine.devices[':maincpu'];local p=cpu.spaces.program
  tap=p:install_write_tap(0x01d01030,0x01d0103f,'native Friendship sample dispatch',function(at,data,mask)
   local command=data&0xffff
   if at==0x01d01030 and mask==0xffff and command>=0xfff7 and command<=0xfffe then
    print(string.format('MK2_FRIEND_VOICE frame=%d writes=0 assistance=none seconds=%.12f command=%04X',frame,emu.time(),command))
   end
   if at~=0x01d01030 or mask~=0xffff or not(command>=0x6aa0 and command<=0x6ab4)then return end
   local actor,main=cpu.state.A8.value,cpu.state.A13.value
   local pool={};for voice=0,4 do pool[#pool+1]=tostring(p:read_u16(main+0x180+voice*16))end
   print(string.format('MK2_FRIEND_AUDIO frame=%d writes=0 assistance=none seconds=%.12f command=%04X actor=%08X main=%08X id=%d pose=%08X a9=%08X timers=%s',frame,emu.time(),command,actor,main,p:read_u16(actor+0x1f0),p:read_u32(actor+0x1d0),cpu.state.A9.value,table.concat(pool,',')))
  end)
 end
end)
emu.register_stop(function()if tap then tap:remove()end end)
