-- Same whole campaign; replace only native Sub-Zero's failed Ring inputs.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path='mk2ks_native_paired_stumble_subzero_ring.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before="replacement=ranged..'\\n'..replacement"
local after=[====[
-- Copy the entire existing physical jump-kick feedback routine, not a guest
-- handler or a forced action. Native ground/flight/contact decide outcomes.
local common=read('mk2ks_natural_campaign_shao_ring_retreat_v3485.lua')
local native_begin=assert(common:find('    -- Read-only feedback: jump from actual grounded state',1,true))
local native_end=assert(common:find('    previous_y=human.y',native_begin,true))
assert(not common:find('    -- Read-only feedback: jump from actual grounded state',native_begin+1,true))
assert(not common:find('    previous_y=human.y',native_end+1,true))
local feedback=common:sub(native_begin,native_end+#'    previous_y=human.y'-1)
local input_begin=assert(ranged:find('    local forward=',1,true))
local input_end=assert(ranged:find("    log('RANGE_DECISION'",input_begin,true))
assert(not ranged:find('    local forward=',input_begin+1,true))
ranged=ranged:sub(1,input_begin-1).."    local reason='native_forward_jumpkick_feedback'\n"..feedback..'\n'..ranged:sub(input_end)
replacement=ranged..'\n'..replacement
]====]
local a,b=source:find(before,1,true)
assert(a and not source:find(before,b+1,true),'One entire native Sub-Zero-only physical decision block')
source=source:sub(1,a-1)..after..source:sub(b+1)
local old='original_Ring_routine=whole earlier_inputs=unchanged'
local first,last=source:find(old,1,true)
assert(first and not source:find(old,last+1,true))
source=source:sub(1,first-1)..'physical_feedback=whole_original_forward_jumpkick passive_observers=retained earlier_inputs=unchanged'..source:sub(last+1)
assert(load(source,'@'..path..'::only_SubZero_original_forward_jumpkick_inputs','t',_ENV))()
