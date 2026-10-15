-- A real P1 forward jump kick interrupts cold native P2 square wave.
-- No guest positions, health, task state, identities or sample items written.
dofile('mk2ks_launch_channels_v1483.lua')
local frame=0
assert(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')=='2' and os.getenv('MK2KS_HUMAN_SPECIAL_MOVE')=='square')
local high=manager.machine.ioport.ports[':IN0'].fields
local function press(button)
 high['P1 '..button]:set_value(1)
 print(string.format('MK2_LAUNCH_INTERRUPTION_INPUT frame=%d slot=1 button=%s writes=0',frame,button:gsub(' ','_')))
end
emu.register_frame(function()
 frame=frame+1
 if frame>=1573 and frame<1576 then press('Up');press('Right')end
 if frame>=1581 and frame<1585 then press('High Kick')end
end)
