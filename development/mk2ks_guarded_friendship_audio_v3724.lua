-- Entire3560 genuine physical Friendship/PCM controller unchanged.
-- Add only all14 channel records, full actual port words and ADSP latch reads.
dofile('mk2ks_current_friendship_ram_mix_v3560.lua')
local frame,channels,taps=0,{},{}
local main=manager.machine.devices[':maincpu']
local dsp=assert(manager.machine.devices[':dcs:dcs'])
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for n=0,13 do local c=assert(channels[n]);assert(c.source_len and c.source_num and c.pos and c.loop and c.paused)end
 end
 if frame>=700 then
  for n=0,13 do
   local c=channels[n]
   print(string.format('MK2_FAUDIO_CHANNEL frame=%d seconds=%.12f channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
    frame,emu.time(),n,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.loop:read(0),c.paused:read(0)))
  end
 end
end)
taps[#taps+1]=main.spaces.program:install_write_tap(0x01d01030,0x01d0103f,'all genuine Friendship sound words',function(at,value,mask)
 if at==0x01d01030 and frame>=700 then
  print(string.format('MK2_FAUDIO_SOUND frame=%d seconds=%.12f word=%04X mask=%04X pc=%08X a8=%08X a13=%08X writes=0 assistance=none',
   frame,emu.time(),value,mask,main.state.PC.value,main.state.A8.value,main.state.A13.value))
 end
end)
taps[#taps+1]=dsp.spaces.data:install_read_tap(0x3400,0x37ff,'actual original DCS input latch',function(at,value,mask)
 if frame>=700 then
  print(string.format('MK2_FAUDIO_DELIVERY frame=%d seconds=%.12f at=%04X word=%04X mask=%04X dsp_pc=%04X writes=0 assistance=none',
   frame,emu.time(),at,value,mask,dsp.state.PC.value))
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
