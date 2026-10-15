-- Read-only live sample-channel ledger. No save-state loading or item writes.
dofile('mk2ks_native_grab_audio_v1412.lua')
local frame,items,channels=0,nil,{}
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  items=manager.machine.devices[':mk2ksvoices'].items
  for name,index in pairs(items)do
   print(string.format('MK2_LAUNCH_CHANNEL_ITEM name=%s index=%d',name,index))
   local channel,field=name:match('^(%d+)/chan%.(.+)$')
   if channel then
    channel=tonumber(channel)
    if channel>=10 and channel<=13 then
     channels[channel]=channels[channel]or{}
     channels[channel][field]=emu.item(index)
    end
   end
  end
  for channel=10,13 do
   assert(channels[channel] and channels[channel].source_len and channels[channel].pos and
    channels[channel].source_num and channels[channel].loop and channels[channel].paused,'Actual channel item naming')
  end
 end
 if frame>=1450 then
  for channel=10,13 do
   local c=channels[channel]
   local pos=string.unpack('<d',c.pos:read_block(0,8))
   print(string.format('MK2_LAUNCH_CHANNEL frame=%d seconds=%.12f channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
    frame,emu.time(),channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
  end
 end
end)
