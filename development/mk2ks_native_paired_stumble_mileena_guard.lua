-- Same game and full campaign; disable only the last losing ranged priority.
local path='mk2ks_native_paired_stumble_scorpion_guard.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local function once(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'One exact late physical-policy boundary')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once('local range_after="elseif strategy==\'guard_punish\' and other.roster==5 then"',
     'local range_after="elseif strategy==\'guard_punish\' and false then"')
once('MK2_CURRENT_SCORPION_PHYSICAL_POLICY true_cpu=10 branch_priority_changes=1 timing_changes=0 writes=0 assistance=none',
     'MK2_CURRENT_MILEENA_PHYSICAL_POLICY true_cpu=5 preceding_scorpion_policy_preserved=1 branch_priority_changes=1 timing_changes=0 writes=0 assistance=none')
assert(load(source,'@'..path..'::only_Mileena_ranged_priority_removed','t',_ENV))()
