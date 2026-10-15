-- Preserve the confirmed P1-human/P2-CPU route and all physical inputs.
-- Only observation accounting/exit changes: two FULL pairs, then 30 fields.
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
once("local move,side,attempt,air='choke',2,1,false","local move,side,attempt,air='leg',2,1,false")
once("local expected={human=='kano'and 17 or 18,17}","local expected={human=='kano'and 17 or 18,18}")
once('local count\ndriver,count=driver:gsub',[[local function observation_once(before,after)
 local at=assert(driver:find(before,1,true));assert(not driver:find(before,at+1,true))
 driver=driver:sub(1,at-1)..after..driver:sub(at+#before)
end
observation_once('local frame,cycle,complete=0,0,nil','local frame,cycle,complete=0,0,nil\nlocal complete_count,last_complete=0,nil')
observation_once("state('COMPLETE',s,v);complete=frame","state('COMPLETE',s,v);complete=frame\n            complete_count=complete_count+1;last_complete=frame")
observation_once('local deadline=follow_regain and math.max(complete,follow_regain)+30 or complete+180\n        if frame>=deadline then manager.machine:exit()end','if complete_count>=2 and frame>=last_complete+30 then manager.machine:exit()end')
observation_once('schema=8 cycles=%d complete=%d follow_regain=%d','schema=9 cycles=%d complete_count=%d complete=%d follow_regain=%d')
observation_once('cycle,complete or -1,follow_regain or -1','cycle,complete_count,complete or -1,follow_regain or -1')
local count
driver,count=driver:gsub]])
assert(load(wrapper,'@entire_original_cpu_choke_wrapper','t',_G))()
