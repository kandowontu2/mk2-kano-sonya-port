-- Whole established passive cache observer, only physical driver leaf changes.
local path='mk2ks_native_kano_laser_sonya_postending.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before="dofile('mk2ks_native_sonya_p1_postending_kano.lua')"
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1).."dofile('mk2ks_native_kano_raiden_victim_driver.lua')"..source:sub(last+1)
assert(load(source,'@'..path..'::same_cache_observer_actual_Kano_Raiden_victim_driver','t',_ENV))()
