-- Same complete passive packed-victim observer; ordinary established Kano tower.
local path='mk2ks_native_paired_stumble_campaign.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local function once(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'One exact passive-observer route boundary')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("id==18 and p:read_u16(owner+0x1f0)==7",
     "id==17 and p:read_u16(owner+0x1f0)==7")
once("dofile('mk2ks_native_kano_laser_sonya_postending_leg_guard_late.lua')",
     "dofile('mk2ks_native_kano_paired_stumble_cache_guard.lua')")
assert(load(source,'@'..path..'::same_paired_handoff_observer_and_Kano_victim_rasters','t',_ENV))()
