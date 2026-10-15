-- Corrected whole5955: retain physical controller and passive observer.
-- The failure-only890s deadline is exactly the actual5942 inline callback.
dofile('mk2ks_current_subzero_pit_driver_v5940.lua')
dofile('mk2ks_current_pit_queue_rng_v5954.lua')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if emu.time()>=890 then
  print(string.format('MK2_TOMB_SOURCE_HOST_DEADLINE frame=%d writes=0 assistance=none',frame))
  manager.machine:exit()
 end
end)
