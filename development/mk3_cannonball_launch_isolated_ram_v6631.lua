-- Donor hardware-only asset oracle, NOT a gameplay/activation acceptance test.
-- Reuses exact two original DCS byte writes,25us apart; no guest RAM writes.
dofile('mk3_friendship_isolated_time_v772.lua')
local frame=0
emu.register_frame(function()
 frame=frame+1
 if frame==1500 then print('MK3_LAUNCH_ORACLE_TERMINAL frame='..frame..' seconds='..string.format('%.12f',emu.time()));manager.machine:exit()end
end)
emu.register_sound_update(function()
 local now=emu.time()
 if now>=20 then
  local raw=manager.machine.sound:get_samples()
  print(string.format('MK3_LAUNCH_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,now,#raw,
   raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
end)
