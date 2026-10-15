-- Read-only timing wrapper for the original donor DCS oracle.
-- The underlying diagnostic writes only the requested hardware sound bytes.
dofile('mk3_isolated_sound_probe.lua')
local frame,tap=0,nil
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local p=manager.machine.devices[':maincpu'].spaces.program
  tap=p:install_write_tap(0x01680000,0x0168001f,'original DCS exact time',function(at,data,mask)
   if frame>=1199 and frame<=1202 then
    print(string.format('MK3_FRIEND_ISOLATED_TIME frame=%d seconds=%.12f address=%08X data=%04X mask=%04X',frame,emu.time(),at,data&0xffff,mask&0xffff))
   end
  end)
 end
end)
emu.register_stop(function()if tap then tap:remove()end end)
