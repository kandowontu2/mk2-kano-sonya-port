-- Full original two-human ground controller and native DMA observer.
-- Only its file sinks become bounded RAM transports. No gameplay writes.
local f=assert(io.open('mk2ks_ground_shadow_v815_probe.lua','rb'))
local source=f:read('*a');f:close()
local function replace(old,new,count)
 local result,n=source:gsub(old:gsub('([^%w])','%%%1'),function()return new end)
 assert(n==count,'Exact complete original sink boundary: '..old);source=result
end
replace('io.open(output..','_ground_ram_open(output..',3)
replace('screen:snapshot(file)','_ground_ram_rgb(file,frame)',1)
local helper=[[
local function _ground_hex(raw)return(raw:gsub('.',function(c)return string.format('%02X',c:byte())end))end
local function _ground_ram_open(path,mode)
 assert(mode=='wb','Only original binary evidence sinks')
 local name=assert(path:match('([^/\\]+)$'));local chunks={};local closed=false
 return {
  write=function(self,raw)assert(not closed and type(raw)=='string');chunks[#chunks+1]=raw;return self end,
  close=function(self)
   assert(not closed);closed=true;local raw=table.concat(chunks)
   print(string.format('MK2_GR_BUFFER filename=%s bytes=%d hex=%s',name,#raw,_ground_hex(raw)))
   return true
  end}
end
local function _ground_ram_rgb(filename,frame)
 local raw=manager.machine.video:snapshot_pixels()
 local width,height=manager.machine.video:snapshot_size()
 assert(width==400 and height==254 and #raw==400*254*4)
 print(string.format('MK2_GR_RGB frame=%d filename=%s width=%d height=%d bytes=%d hex=%s',
  frame,filename,width,height,#raw,_ground_hex(raw)))
end
]]
assert(load(helper..source,'@entire_original_ground_only_RAM_sinks','t',_G))()
local frame,channels,items=0,{},{}
local p=manager.machine.devices[':maincpu'].spaces.program
local function hex(raw)return(raw:gsub('.',function(c)return string.format('%02X',c:byte())end))end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local words={};for i=0,0xffffe,2 do words[#words+1]=string.pack('<I2',p:read_u16(0xff800000+i*8))end
  local raw=table.concat(words);print('MK2_GR_GUEST frame=1 bytes='..#raw..' hex='..hex(raw))
  local region=assert(manager.machine.memory.regions[':gfxrom']);local bytes={}
  for i=0,11943 do bytes[#bytes+1]=string.char(region:read_u8(0x1fa0000+i))end
  for i=0,7031 do bytes[#bytes+1]=string.char(region:read_u8(0x1fa4000+i))end
  raw=table.concat(bytes);assert(#raw==18976);print('MK2_GR_GFX frame=1 bytes=18976 hex='..hex(raw))
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for channel=0,18 do local c=assert(channels[channel]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)end
  for name,index in pairs(manager.machine.devices[':'].items)do
   local field=name:match('m_mk2ks_finish_audio_(.+)$')
   if field then assert(not items[field]);items[field]=emu.item(index)end
  end
  assert(items.actor and items.main and items.slot and items.priority and items.remaining)
 end
 for channel=0,18 do
  local c=channels[channel];local pos=string.unpack('<d',c.pos:read_block(0,8))
  print(string.format('MK2_GR_CHANNEL frame=%d channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0 assistance=none',
   frame,channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
 end
 local values={};for n=0,4 do values[#values+1]=string.format('%04X,%d',items.priority:read(n),items.remaining:read(n))end
 print(string.format('MK2_GR_FINISH_POOL frame=%d slot=%d actor=%08X main=%08X slots=%s writes=0 assistance=none',
  frame,items.slot:read(0),items.actor:read(0),items.main:read(0),table.concat(values,';')))
end)
