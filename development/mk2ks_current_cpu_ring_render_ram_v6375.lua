-- Whole original cold selection/retreat/guard/child observers, RAM-only sinks.
local function read(name)
 local file=assert(io.open(name,'rb'));local source=file:read('a'):gsub('\r\n','\n');file:close();return source
end
local sink=read('mk2ks_native_tomb_ram_v3624.lua')
local stop=assert(sink:find("local handle=assert(io.open('mk2ks_native_tomb_display_v2062.lua'",1,true))
assert(load(sink:sub(1,stop-1),'@whole_original_RAM_render_transport','t',_G))()
local frame=0
emu.register_frame(function()frame=frame+1 end)
local env=setmetatable({}, {__index=_G})
local counts={['mk2ks_physical_p2_cpu_continuation_v1997.lua']=6,
 ['mk2ks_physical_p2_cpu_round_trace_v1998.lua']=0,
 ['mk2ks_physical_p2_cpu_overlap_trace_v1999.lua']=1,
 ['mk2ks_physical_p2_cpu_ring_trace_v2013.lua']=0}
-- The legacy host transport tag is reused; labels retain actual CPU snapshots.
env.current_ring_snapshot=function(label)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',frame,label,w,h,#raw,
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
env.dofile=function(name)
 assert(counts[name]~=nil,'Only unchanged qualified original physical observer chain')
 local source=read(name);local count
 source,count=source:gsub("manager.machine.screens%[':screen'%]:snapshot",'current_ring_snapshot')
 assert(count==counts[name])
 assert(not source:find(':snapshot',1,true)and not source:find("'wb'",1,true))
 return assert(load(source,'@'..name,'t',env))()
end
env.dofile('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')
emu.register_frame(function()
 if frame~=1 then return end
 local p=manager.machine.devices[':maincpu'].spaces.program;local bytes={}
 for at=0xff800000,0xfffffff0,16 do bytes[#bytes+1]=string.pack('<I2',p:read_u16(at))end
 local raw=table.concat(bytes);assert(#raw==1048576)
 print('MK2_KNIFE_RAM_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
end)
local source=read('mk2ks_physical_p2_cpu_ring_display_v2014.lua')
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace("dofile('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')",'-- Whole original physical chain already loaded above.')
replace("local output=assert(os.getenv('MK2KS_FLOOR_OUT'))","local output='RAM_ONLY'")
replace("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)')
replace('screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)')
assert(not source:find('io.open',1,true)and not source:find('screen:snapshot',1,true))
assert(load(source,'@whole_original_current_CPU_ring_scene_RAM_v6375','t',_G))()
