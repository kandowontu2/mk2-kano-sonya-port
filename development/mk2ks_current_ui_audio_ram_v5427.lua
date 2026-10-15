-- Whole original physical UI controller; only PNG sink becomes actual native
-- displayed pixels in RAM. Added observers cannot mutate game/input state.
local file=assert(io.open('mk2ks_native_ui_flow_v2_probe.lua','rb'))
local source=file:read('*a');file:close()
local before='screen:snapshot(name)'
local first,last=assert(source:find(before,1,true))
assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..'_ui_emit(name,frame)'..source:sub(last+1)
local helper=[[
local function _ui_emit(filename,frame)
 local raw,width,height=manager.machine.video:snapshot_pixels()
 assert(width==400 and height==254 and #raw==400*254*4)
 print(string.format('MK2_UA_RGB frame=%d seconds=%.12f filename=%s width=%d height=%d bytes=%d hex=%s',
  frame,emu.time(),filename,width,height,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
]]
assert(load(helper..source,'@entire_original_UI_only_actual_displayed_RAM_sink'))()
local frame,channels,tap=0,{},nil
local cpu=manager.machine.devices[':maincpu']
local p=cpu.spaces.program
local side=assert(tonumber(os.getenv('MK2KS_UI_SIDE')))
local roster=side==1 and 0x01060280 or 0x01060e50
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local rom={};for i=0,0xffffe,2 do rom[#rom+1]=string.pack('<I2',p:read_u16(0xff800000+i*8))end
  local raw=table.concat(rom)
  print(string.format('MK2_UA_GUEST frame=1 bytes=%d hex=%s',#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for channel=0,13 do local c=assert(channels[channel]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)end
  tap=p:install_write_tap(0x01d01030,0x01d0103f,'actual combined UI audio port',function(at,data,mask)
   if at==0x01d01030 and mask==0xffff then
    print(string.format('MK2_UA_SOUND frame=%d seconds=%.12f word=%04X mask=%04X pc=%08X a8=%08X a13=%08X roster=%d mode=%d writes=0 assistance=none',
     frame,emu.time(),data,mask,cpu.state.PC.value,cpu.state.A8.value,cpu.state.A13.value,p:read_u16(roster),p:read_u16(0x010601d0)))
   end
  end)
 end
 for channel=0,13 do
  local c=channels[channel];local pos=string.unpack('<d',c.pos:read_block(0,8))
  print(string.format('MK2_UA_CHANNEL frame=%d seconds=%.12f channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
   frame,emu.time(),channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
 end
end)
emu.register_sound_update(function()
 if frame>0 then
  local pcm=manager.machine.sound:get_samples()
  print(string.format('MK2_UA_PCM frame=%d seconds=%.12f bytes=%d hex=%s',frame,emu.time(),#pcm,pcm:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
end)
emu.register_stop(function()if tap then tap:remove()end end)
