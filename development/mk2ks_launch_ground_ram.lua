-- Preserve entire815 physical mobility and native shadow/DMA observer.
-- Only raster/VRAM/palette/GFX output sinks become RAM-only transports.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true))
 return s:sub(1,a-1)..after..s:sub(b+1)
end
local source=read('mk2ks_ground_shadow_v815_probe.lua')
local helper=[[
local function _ram(filename,raw,kind)
 print(string.format('MK2_GROUND_RAW filename=%s kind=%s bytes=%d hex=%s',filename,kind,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
local function _image(filename)
 local raw=manager.machine.video:snapshot_pixels();local w,h=manager.machine.video:snapshot_size()
 assert(w==400 and h==254 and #raw==406400);_ram(filename,raw,'RGB')
end
]]
source=change(source,[[  local dump=assert(io.open(output..'/'..file,'wb'));dump:write(vram:read_block(0,512*512*2));dump:close()]],[[  _ram(file,vram:read_block(0,512*512*2),'VRAM_PRE')]])
source=change(source,[[ local file=string.format('ground_%04d.png',frame);screen:snapshot(file)]],[[ local file=string.format('ground_%04d.png',frame);_image(file)]])
source=change(source,[[ local dump=assert(io.open(output..'/'..vram_file,'wb'));dump:write(latch.raw);dump:close()]],[[ _ram(vram_file,latch.raw,'VRAM')]])
source=change(source,[[ dump=assert(io.open(output..'/'..palette_file,'wb'));dump:write(table.concat(colors));dump:close()]],[[ _ram(palette_file,table.concat(colors),'PALETTE')]])
assert(not source:find("io.open(output",1,true)and not source:find('screen:snapshot(',1,true),'No raw filesystem sink survives')
assert(load(helper..source,'@entire815_native_mobility_shadow_RAM_sinks','t',_G))()
emu.register_frame(function()
 if rawget(_G,'MK2PORT_GROUND_GUEST_SENT')then return end
 rawset(_G,'MK2PORT_GROUND_GUEST_SENT',true)
 local p=manager.machine.devices[':maincpu'].spaces.program;local words={}
 for at=0xff800000,0xffffffe0,32 do words[#words+1]=string.pack('<I4',p:read_u32(at))end
 _ram=nil -- helper is lexical; separate exact inventory transport below.
 local raw=table.concat(words);assert(#raw==1048576)
 print('MK2_GROUND_RAW filename=guest kind=GUEST bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
end)
