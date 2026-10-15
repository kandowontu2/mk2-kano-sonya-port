-- Whole original earned mirror Tomb; ordinary delayed command, no held Down.
dofile('mk2ks_current_random_tomb_provenance_v5800.lua')
dofile('mk2ks_current_tomb_winner_mix_observer_v5779.lua')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if emu.time()>=890 then
  print(string.format('MK2_TOMB_SOURCE_HOST_DEADLINE frame=%d writes=0 assistance=none',frame))
  manager.machine:exit()
 end
end)
