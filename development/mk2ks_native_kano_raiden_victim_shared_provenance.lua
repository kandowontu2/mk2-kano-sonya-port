-- Whole original paired observer; explicitly share the passive Lua notification.
local path='mk2ks_native_paired_stumble_campaign.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once('id==18 and p:read_u16(owner+0x1f0)==7','id==17 and p:read_u16(owner+0x1f0)==7')
once('pending={frame=frame}',"pending={frame=frame};rawset(_G,'MK2KS_KANO_PAIRED_CALLBACK',frame)")
once("dofile('mk2ks_native_kano_laser_sonya_postending_leg_guard_late.lua')",
 "dofile('mk2ks_native_kano_raiden_victim_approach_cache.lua')")
assert(load(source,'@'..path..'::whole_original_paired_handoff_true_Kano_victim','t',_ENV))()
