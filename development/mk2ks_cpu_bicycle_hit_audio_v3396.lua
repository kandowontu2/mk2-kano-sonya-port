-- Read-only native blocked move/channel/mixed-PCM observer. PCM is streamed to
-- the verifier's RAM; no audio file is opened or game/input state modified.
dofile('mk2ks_native_cpu_audio_mobility_v3395.lua')
local frame,channels,owners=0,{},{}
local cpu=manager.machine.devices[':maincpu']
local tap
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local rom={};for i=0,0xffffe,2 do rom[#rom+1]=string.pack('<I2',cpu.spaces.program:read_u16(0xff800000+i*8))end
  local file=assert(io.open(assert(os.getenv('MK2KS_FLOOR_OUT'))..'/guest_maincpu.bin','wb'))
  file:write(table.concat(rom));file:close()
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then
    channel=tonumber(channel,16)
    if channel>=10 and channel<=13 then
     channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)
    end
   end
  end
  for name,index in pairs(manager.machine.devices[':'].items)do
   local field=name:match('m_mk2ks_battle_(.+)$')
   if field then owners[field]=emu.item(index)end
  end
  assert(owners.actor and owners.main and owners.health)
  for channel=10,13 do
   local c=assert(channels[channel]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)
  end
  tap=cpu.spaces.program:install_write_tap(0x01d01030,0x01d0103f,'actual blocked audio port',function(at,data,mask)
   if at==0x01d01030 and mask==0xffff then
    print(string.format('MK2_BBAUDIO_SOUND frame=%d seconds=%.12f word=%04X mask=%04X pc=%08X a8=%08X a13=%08X writes=0 assistance=none',
     frame,emu.time(),data,mask,cpu.state.PC.value,cpu.state.A8.value,cpu.state.A13.value))
   end
  end)
 end
 if frame>=2600 and frame<=2930 then
  for slot=1,2 do
   print(string.format('MK2_BBAUDIO_OWNER frame=%d slot=%d actor=%08X main=%08X health=%d writes=0',
    frame,slot,owners.actor:read(slot-1),owners.main:read(slot-1),owners.health:read(slot-1)))
  end
  for channel=10,13 do
   local c=channels[channel];local pos=string.unpack('<d',c.pos:read_block(0,8))
   print(string.format('MK2_BBAUDIO_CHANNEL frame=%d seconds=%.12f channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
    frame,emu.time(),channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
  end
 end
end)
emu.register_sound_update(function()
 if frame>=2600 and frame<=2930 then
  local pcm=manager.machine.sound:get_samples()
  local hex=pcm:gsub('.',function(c)return string.format('%02X',c:byte())end)
  print(string.format('MK2_BBAUDIO_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,emu.time(),#pcm,hex))
 end
end)
emu.register_stop(function()
 print(string.format('MK2_BBAUDIO_RESULT frame=%d seconds=%.12f writes=0 assistance=none',frame,emu.time()))
 if tap then tap:remove()end
end)
