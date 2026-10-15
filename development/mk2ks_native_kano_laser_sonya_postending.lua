-- Entire established physical Sonya tower/ending/fresh Kano join unchanged.
-- One passive stop protects the diagnostic from a confirmed cache overrun;
-- it never alters inputs, actors, health, CPU, schedule, RNG or sound state.
dofile('mk2ks_native_sonya_p1_postending_kano.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local observed,pending,stores=0,false,0
local tap=p:install_write_tap(0x01060000,0x01061fff,'terminal on real native cache global overrun',function(at,data,mask)
 if cpu.PC.value~=0xff838860 then return end
 stores=stores+1;pending=true
 if stores<=180 then
  print(string.format('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE observer_callback=%d seconds=%.12f pc=%08X at=%08X data=%04X mask=%04X a8=%08X a13=%08X writes=0 assistance=none',
   observed,emu.time(),cpu.PC.value,at,data&0xffff,mask,cpu.A8.value,cpu.A13.value))
 end
end)
emu.register_frame_done(function()
 observed=observed+1
 if pending then
  print(string.format('MK2_CURRENT_CAMPAIGN_CACHE_STOP observer_callback=%d seconds=%.12f global_cache_stores=%d acceptance=false writes=0 assistance=none',observed,emu.time(),stores))
  manager.machine:exit()
 end
end)
emu.register_stop(function()
 print(string.format('MK2_CURRENT_CAMPAIGN_CACHE_RESULT observer_callback=%d global_cache_stores=%d writes=0 assistance=none',observed,stores))
 tap:remove()
end)
