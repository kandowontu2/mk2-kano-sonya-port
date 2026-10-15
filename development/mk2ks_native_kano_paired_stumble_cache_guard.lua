-- Preserve the whole established cache observer and all ordinary Kano inputs.
local path='mk2ks_native_kano_laser_sonya_postending.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before="dofile('mk2ks_native_sonya_p1_postending_kano.lua')"
local after="dofile('mk2ks_current_kano_p1_campaign_ram_v5194.lua')"
local first,last=source:find(before,1,true)
assert(first and not source:find(before,last+1,true),'One existing physical-driver boundary')
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@'..path..'::ordinary_Kano_driver_and_unchanged_passive_cache_guard','t',_ENV))()
