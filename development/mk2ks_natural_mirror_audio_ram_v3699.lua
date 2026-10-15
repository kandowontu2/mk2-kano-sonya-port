-- No new controls or game writes; original1166 drives selection/earned KOs.
dofile('mk2ks_natural_mirror_no_raster_v3698.lua')
local device=manager.machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,channels,taps=0,{},{}
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
   print(string.format('MK2_MAUDIO_CHANNEL frame=%d seconds=%.12f channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
    frame,emu.time(),n,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.loop:read(0),c.paused:read(0)))
  end
 end
end)
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual physical mirror sound commands',function(at,value,mask)
 if at==0x01d01030 and frame>=700 then
  print(string.format('MK2_MAUDIO_SOUND frame=%d seconds=%.12f word=%04X mask=%04X pc=%08X a8=%08X a13=%08X writes=0 assistance=none',
   frame,emu.time(),value,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 end
end)
emu.register_sound_update(function()
 if frame>=700 then
  local raw=manager.machine.sound:get_samples()
  print(string.format('MK2_BBAUDIO_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,emu.time(),#raw,
   raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
