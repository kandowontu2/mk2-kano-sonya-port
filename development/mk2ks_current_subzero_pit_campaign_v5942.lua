-- Whole normal paid stage progression, true current Kano/Sonya versus Sub-Zero8.
dofile('mk2ks_current_subzero_pit_driver_v5940.lua')
dofile('mk2ks_current_subzero_pit_audio_v5941.lua')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if emu.time()>=890 then
  print(string.format('MK2_TOMB_SOURCE_HOST_DEADLINE frame=%d writes=0 assistance=none',frame))
  manager.machine:exit()
 end
end)
