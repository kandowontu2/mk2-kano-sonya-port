-- Original true-ID earned matches and facing commands; passive audio only.
dofile('mk2ks_tomb_mirror_provenance_ram_v4341.lua')
dofile('mk2ks_current_tomb_source_audio_observer_v5750.lua')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if emu.time()>=890 then
  print(string.format('MK2_TOMB_SOURCE_HOST_DEADLINE frame=%d writes=0 assistance=none',frame))
  manager.machine:exit()
 end
end)
