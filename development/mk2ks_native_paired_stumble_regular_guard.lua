-- Ordinary test tactics only. Same repaired game, no state/CPU/health edits.
local late_path='mk2ks_native_kano_laser_sonya_postending_leg_guard_late.lua'
local function read(path)
 local file=assert(io.open(path,'rb'));local text=file:read('a');file:close();return text
end
local function once(text,before,after)
 local first,last=text:find(before,1,true)
 assert(first and not text:find(before,last+1,true),'One exact physical-policy boundary')
 return text:sub(1,first-1)..after..text:sub(last+1)
end
local adapted=read(late_path)
adapted=once(adapted,'(other.roster==18 or other.roster==17)',
 '((other.roster>=0 and other.roster<=11) or other.roster==14 or other.roster==17 or other.roster==18)')
adapted=once(adapted,'other_now.roster~=18 and other_now.roster~=17',
 '(other_now.roster<0 or other_now.roster>11) and other_now.roster~=14 and other_now.roster~=17 and other_now.roster~=18')
adapted=once(adapted,'target_cpu=17 eligibility_changes=5 observer_changes=1 timing_changes=0',
 'target_cpu=0..11,14,17,18 eligibility_changes=5 observer_changes=1 timing_changes=0')
local environment=setmetatable({},{__index=_ENV})
environment.dofile=function(path)
 local source=path==late_path and adapted or read(path)
 return assert(load(source,'@'..path..'::normal_Raiden_guard_leg_policy_only','t',environment))()
end
assert(load(read('mk2ks_native_paired_stumble_campaign.lua'),
 '@mk2ks_native_paired_stumble_campaign.lua::unchanged_passive_handoffs_and_native_rasters','t',environment))()
