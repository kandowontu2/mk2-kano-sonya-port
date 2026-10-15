-- Reuse the previously executed physical campaign, changing only slot precondition.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='kano')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path='mk2ks_kano_current_p2_campaign_ram_v4472.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local before="assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')"
local at=assert(source:find(before,1,true))
assert(not source:find(before,at+#before,true),'Exactly one slot-only precondition')
source=source:sub(1,at-1).."assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')"..source:sub(at+#before)
assert(load(source,'@'..path..'::physical_slot_precondition_only','t',_ENV))()

