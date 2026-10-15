-- Same native cold controllers, with only the physical-slot precondition changed.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
assert(fighter=='kano' or fighter=='sonya')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path,before,after
if fighter=='kano' then
 path='mk2ks_kano_current_p2_campaign_ram_v4472.lua'
 before="assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')"
 after="assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')"
else
 path='mk2ks_kintaro_pressure_guard_long_campaign_ram_v4436.lua'
 before="assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')"
 after="assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')"
end
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local first,last=source:find(before,1,true)
assert(first,'Exact original physical-slot precondition')
assert(not source:find(before,last+1,true),'Only one physical-slot precondition changes')
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@'..path..'::player_one_precondition_only_4771','t',_ENV))()
