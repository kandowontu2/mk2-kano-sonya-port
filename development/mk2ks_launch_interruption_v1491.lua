-- Same cold genuine match; additional physical opponent uppercut only.
-- No guest memory or sample/save-item writes, no forced health or position.
dofile('mk2ks_launch_channels_v1483.lua')
local frame,entry,tap=0,nil,nil
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local high=manager.machine.ioport.ports[':IN0'].fields
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local cpu=manager.machine.devices[':maincpu']
  tap=cpu.spaces.program:install_write_tap(0x01d01030,0x01d0103f,'actual Sonya launch timing',function(at,data,mask)
   if mask==0xffff and(data==0x6b00 or data==0x6b01)then
    entry=entry or frame
    print(string.format('MK2_LAUNCH_INTERRUPTION_ENTRY frame=%d side=%d command=%04X writes=0',frame,side,data))
   end
  end)
 end
 -- Crouch after the cold fixture's real command begins, before launch.
 -- This is physical input timing, not game-state assignment.
 if frame>=1573 and not entry then
  high['P'..(3-side)..' Down']:set_value(1)
  print(string.format('MK2_LAUNCH_INTERRUPTION_INPUT frame=%d slot=%d button=Down writes=0',frame,3-side))
 end
 if entry then
  local age=frame-entry
  if age>=1 and age<9 then
   high['P'..(3-side)..' Down']:set_value(1)
   print(string.format('MK2_LAUNCH_INTERRUPTION_INPUT frame=%d slot=%d button=Down writes=0',frame,3-side))
  end
  if age>=1 and age<6 then
   high['P'..(3-side)..' High Punch']:set_value(1)
   print(string.format('MK2_LAUNCH_INTERRUPTION_INPUT frame=%d slot=%d button=High_Punch writes=0',frame,3-side))
  end
 end
end)
emu.register_stop(function()if tap then tap:remove()end end)
