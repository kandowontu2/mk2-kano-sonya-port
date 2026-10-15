-- Measured earlier jump crossed above Bicycle before its flight intersected.
-- Jump seven fields later so the native kick meets the actual startup path.
-- Only physical inputs change; every old observer and transport remains.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local controller=change(read('mk2ks_launch_jump_interrupt_v6693.lua'),'ball=80,square=2,bicycle=9','ball=80,square=2,bicycle=16')
rawset(_G,'MK2PORT_LATE_JUMP_SOURCE',controller)
local source=read('mk2ks_launch_ground_io_v6706.lua')
source=change(source,"'extra..'+string.format","'extra..'..string.format")
source=change(source,"local adapter=read('mk2ks_launch_ground_counter_v6703.lua')",
 "local adapter=assert(rawget(_G,'MK2PORT_LATE_JUMP_SOURCE'))")
assert(load(source,'@whole_later_jump_counter_actual_IN0_IN2','t',_G))()
