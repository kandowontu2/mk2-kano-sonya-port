-- Entire original physical CPU driver plus isolated original read-only body/shadow observer.
-- No human-special controller is loaded; CPU identity and choices remain native.
local file=assert(io.open('mk2ks_special_shadow_v5131.lua','rb'))
local original=file:read('*a'):gsub('\r\n','\n');file:close()
local function slice(first,last)
 local a=assert(original:find(first,1,true));assert(not original:find(first,a+1,true))
 local b=assert(original:find(last,a+#first,true));return original:sub(a,b-1)
end
local prefix=slice('local p=manager.machine.devices', 'local high,low,system=')
prefix=prefix..[[
local move,side,attempt,air='choke',2,1,false
local human=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local victim_name=human
local expected={human=='kano'and 17 or 18,17}
local frame,ready,command,recovered=0,nil,nil,nil
local marks,taps={},{}
]]
prefix=prefix..slice('local function valid(a)','local function pair_live(a,b)')
prefix=prefix..[[
local function pair_live(a,b)
 return a and b and p:read_u16(0x010601d0)==2 and a.id==expected[1]and b.id==expected[2]
  and a.roster==a.id and b.roster==b.id and a.state==1 and b.state==0 and a.owner==a.actor and b.owner==b.actor
end
emu.register_frame(function()
 frame=frame+1
 if not ready and pair_live(sample(1),sample(2))then ready=frame end
end)
local environment=setmetatable({}, {__index=_G})
environment.snapshot_ram=function(label)marks[frame]=label:gsub('%.png$','')end
local file=assert(io.open('mk2ks_cpu_recovery_probe_v1438.lua','rb'))
local driver=file:read('*a'):gsub('\r\n','\n');file:close()
local count
driver,count=driver:gsub("manager.machine.screens%[':screen'%]:snapshot",'snapshot_ram')
assert(count==6,'Exact original physical driver media transport substitutions')
assert(not driver:find(':snapshot',1,true),'No original media file writes')
assert(load(driver,'@mk2ks_cpu_recovery_probe_v1438.lua','t',environment))()
]]
local observer=slice('-- BEGIN v1763 read-only consecutive move-phase observer','local function snapshot_ram(label)')
local callback=slice('emu.register_frame_done(function()','-- END v1763 read-only consecutive move-phase observer')
local cleanup=[[
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
]]
assert(load(prefix..observer..callback..cleanup,'@isolated_original_body_shadow_CPU_observer_v5328','t',_G))()
