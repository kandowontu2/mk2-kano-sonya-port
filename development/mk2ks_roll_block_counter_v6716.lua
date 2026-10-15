-- Real stock defense/counter: block the high roll, release guard, uppercut
-- its native rebound while the startup source is still active. This is not
-- an initial-flight interruption claim. No guest, actor or HP assignments.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local controller=read('mk2ks_launch_ground_counter_v6703.lua')
controller=change(controller,[[if not entry and age>=79 then press('Down')end]],[[if not entry and age>=79 then press('Block')end]])
controller=change(controller,[[if live>=1 and live<delay+9 then press('Down')end
    if live>=delay and live<delay+5 then press('Low Kick')end]],[[if live>=1 and live<18 then press('Block')end
    if live>=delay-6 and live<delay+8 then press('Down')end
    if live>=delay and live<delay+5 then press('High Punch')end]])
rawset(_G,'MK2PORT_BLOCK_COUNTER_SOURCE',controller)
local observer=read('mk2ks_launch_ground_io_v6706.lua')
observer=change(observer,"'extra..'+string.format","'extra..'..string.format")
observer=change(observer,"local adapter=read('mk2ks_launch_ground_counter_v6703.lua')",
 "local adapter=assert(rawget(_G,'MK2PORT_BLOCK_COUNTER_SOURCE'))")
assert(load(observer,'@whole_native_ports_actual_guard_release_counter_inputs','t',_G))()
