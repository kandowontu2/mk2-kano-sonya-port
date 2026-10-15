-- Add read-only mixed PCM/channel observations, preserving the old physical
-- controller exactly. PCM goes directly to verifier RAM, never a WAV/log.
dofile('mk2ks_current_friendship_ram_wins_v3559.lua')
local frame,channels=0,{}
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then
    channel=tonumber(channel,16)
    if channel>=4 and channel<=9 then
     channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)
    end
   end
  end
  for channel=4,9 do
   local c=assert(channels[channel]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)
  end
 end
 if frame>=3500 then
  for channel=4,9 do
   local c=channels[channel];local pos=string.unpack('<d',c.pos:read_block(0,8))
   print(string.format('MK2_FRIEND_MIX_CHANNEL frame=%d seconds=%.12f channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
    frame,emu.time(),channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
  end
 end
end)
emu.register_sound_update(function()
 if frame>=700 then
  local pcm=manager.machine.sound:get_samples()
  local hex=pcm:gsub('.',function(c)return string.format('%02X',c:byte())end)
  print(string.format('MK2_BBAUDIO_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,emu.time(),#pcm,hex))
 end
end)
emu.register_stop(function()
 print(string.format('MK2_FRIEND_MIX_RESULT frame=%d seconds=%.12f writes=0 assistance=none',frame,emu.time()))
end)
