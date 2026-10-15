-- Whole original earned cross campaign; passive full enabled Pit audio.
dofile('mk2ks_current_cross_tomb_provenance_v5834.lua')
dofile('mk2ks_current_pit_winner_mix_observer_v5891.lua')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if emu.time()>=890 then
  print(string.format('MK2_TOMB_SOURCE_HOST_DEADLINE frame=%d writes=0 assistance=none',frame))
  manager.machine:exit()
 end
end)
