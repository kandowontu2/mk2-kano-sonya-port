-- Two full natural CPU Sonya grabs; unchanged original physical P2 controller.
-- The original RAM-only body/shadow observer is rebound to physical CPU P1.
local file=assert(io.open('mk2ks_native_kano_laser_special_shadow.lua','rb'))
local source=file:read('*a');file:close()
local marker='-- Passive current nineteen-channel/private-finisher-pool observer only.'
local at=assert(source:find(marker,1,true));assert(not source:find(marker,at+1,true))
assert(load(source:sub(at),'@entire_original_nineteen_channel_observer','t',_G))()
local file=assert(io.open('mk2ks_cpu_choke_shadow_v5328.lua','rb'))
local wrapper=file:read('*a'):gsub('\r\n','\n');file:close()
local function once(before,after)
 local at=assert(wrapper:find(before,1,true));assert(not wrapper:find(before,at+1,true))
 wrapper=wrapper:sub(1,at-1)..after..wrapper:sub(at+#before)
end
once("local move,side,attempt,air='choke',2,1,false","local move,side,attempt,air='leg',1,1,false")
once("local expected={human=='kano'and 17 or 18,17}","local expected={18,human=='kano'and 17 or 18}")
once('a.state==1 and b.state==0','a.state==0 and b.state==1')
-- Both the file read and compiler label must bind the same entire controller.
local count
wrapper,count=wrapper:gsub('mk2ks_cpu_recovery_probe_v1438.lua','mk2ks_cpu_recovery_probe_v1459.lua')
assert(count==2)
assert(load(wrapper,'@entire_original_cpu_choke_wrapper','t',_G))()
