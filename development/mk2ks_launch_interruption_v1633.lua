-- Cold native P2 square-wave fixture. Physical opponent uppercut only.
-- Baseline v1620 starts the command at1571 and launch at1579. P1's
-- native task runs earlier than P2's: press HP two fields after that
-- observed launch, after the actual native crouch task is ready.
-- All health, position, roster, task and sample state remains read-only.
dofile('mk2ks_launch_channels_v1483.lua')
local frame,entry,tap=0,nil,nil
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local move=assert(os.getenv('MK2KS_HUMAN_SPECIAL_MOVE'))
assert(side==2 and move=='square','This fixture is specifically P2 square wave')
local hpframe=assert(tonumber(os.getenv('MK2KS_INTERRUPTION_HP_FRAME')))
assert(hpframe>=1580 and hpframe<=1590,'Physical uppercut timing bounds')
local high=manager.machine.ioport.ports[':IN0'].fields
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local cpu=manager.machine.devices[':maincpu']
  tap=cpu.spaces.program:install_write_tap(0x01d01030,0x01d0103f,'actual Sonya launch timing',function(at,data,mask)
   if at==0x01d01030 and mask==0xffff and data==0x6b00 then
    entry=entry or frame
    print(string.format('MK2_LAUNCH_INTERRUPTION_ENTRY frame=%d side=%d command=%04X writes=0',frame,side,data))
   end
  end)
 end
 if frame>=1573 and frame<hpframe+9 then
  high['P1 Down']:set_value(1)
  print(string.format('MK2_LAUNCH_INTERRUPTION_INPUT frame=%d slot=1 button=Down writes=0',frame))
 end
 if frame>=hpframe and frame<hpframe+5 then
  high['P1 High Punch']:set_value(1)
  print(string.format('MK2_LAUNCH_INTERRUPTION_INPUT frame=%d slot=1 button=High_Punch writes=0',frame))
 end
end)
emu.register_stop(function()if tap then tap:remove()end end)
