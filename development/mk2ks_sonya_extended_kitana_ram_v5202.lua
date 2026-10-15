-- Physical controller experiment only; original guest and all other policies retained.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path='mk2ks_sonya_extended_guard_base_ram_v5201.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local function once(before,after)
 local first,last=source:find(before,1,true)
 assert(first,'Exact original physical source boundary')
 assert(not source:find(before,last+1,true),'Unique original physical source boundary')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')",
 "assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')")
local first=assert(source:find("   elseif strategy=='guard_punish' and other.roster==18 then",1,true))
local last=assert(source:find("   elseif strategy=='zoning' or strategy=='guard_punish' then",first+1,true))
local kitana=source:sub(first,last-1)
kitana=kitana:gsub('gp_','kt_')
local count
kitana,count=kitana:gsub('other%.roster==18','other.roster==4')
assert(count==5,'Only the separate CPU Kitana context and its thresholds change')
local allowed="(other_now.roster~=5 and other_now.roster~=10 and other_now.roster~=18)"
local at,finish=kitana:find(allowed,1,true)
assert(at and not kitana:find(allowed,finish+1,true))
kitana=kitana:sub(1,at-1)..'(other_now.roster~=4)'..kitana:sub(finish+1)
kitana=kitana:gsub('GUARD_','KITANA_')
once([[local gp_action_taps={}\nlocal rs_last]],
 [[local gp_action_taps={}\nlocal kt_last,kt_leg,kt_last_leg,kt_upper,kt_guard=nil,nil,-1000,-1000,-1000\nlocal kt_move=nil\nlocal kt_action_taps={}\nlocal rs_last]])
once('local replacement=[[\n','local replacement=[[\n'..kitana)
assert(load(source,'@'..path..'::P1_physical_Kitana_guard_only_4793','t',_ENV))()

