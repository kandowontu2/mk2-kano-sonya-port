-- Whole original887 physical controller and904 passive art observer, RAM sinks.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local function read(name)
 local f=assert(io.open(root..'/'..name,'rb'));local raw=f:read('*a');f:close();return (raw:gsub('\r\n','\n'))
end
local function replace_once(source,before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 return source:sub(1,first-1)..after..source:sub(last+1)
end
function mk2_reptile_ram_emit(tag,raw,fields)
 print('MK2_CURRENT_REPTILE_RAM_'..tag..' '..fields..' bytes='..#raw..' hex='..
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
end
function mk2_reptile_ram_snapshot(filename)
 local raw=manager.machine.video:snapshot_pixels()
 local width,height=manager.machine.video:snapshot_size()
 assert(width==400 and height==254 and #raw==400*254*4)
 mk2_reptile_ram_emit('RGB',raw,'filename='..filename..' width='..width..' height='..height)
end
local controller=read('mk2ks_reptile_victim_v887.lua')
controller=replace_once(controller,
 "screen:snapshot(string.format('reptile_victim_%d_%03d.png',action_start,frame-action_start))",
 "mk2_reptile_ram_snapshot(string.format('reptile_victim_%d_%03d.png',action_start,frame-action_start))")
assert(load(controller,'@entire_original887_reptile_controller_only_RAM_snapshot_sink','t',_ENV))()
local observer=read('mk2ks_reptile_death_grounding_v904.lua')
observer=replace_once(observer,"dofile('mk2ks_reptile_victim_v887.lua')",'-- Entire original controller already registered above.')
observer=replace_once(observer,
 "local f=assert(io.open(output..'/'..file,'wb'));f:write(data);f:close()",
 "mk2_reptile_ram_emit('DATA',data,'filename='..file)")
observer=replace_once(observer,[=[  local f=assert(io.open(output..'/guest_maincpu.bin','wb'))
  for block=0,0xfffff,0x1000 do
   local bytes={}
   for at=0,0xfff do bytes[#bytes+1]=string.char(p:read_u8(0xff800000+(block+at)*8))end
   f:write(table.concat(bytes))
  end
  f:close()]=],[=[  local bytes={}
  for at=0,0xfffff do bytes[#bytes+1]=string.char(p:read_u8(0xff800000+at*8))end
  save('guest_maincpu.bin',table.concat(bytes))]=])
assert(load(observer,'@entire_original904_native_death_FIFO_DMA_only_RAM_file_sinks','t',_ENV))()
