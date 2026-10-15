-- Compose original read-only ladder additions into the actual UI edit block.
-- The previous wrapper's quoted search text caused a pre-game syntax failure.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a');f:close();return s
end
local template=read('mk2ks_continue_ladder_positions_v6605.lua')
local a,b=assert(template:find('local after=[=[',1,true))
local stop=assert(template:find(']=]',b+1,true))
local additions=template:sub(b+1,stop-1)
local source=read('mk2ks_cross_continue_presentation.lua')
local before="assert(load(helper..source,'@whole_native_continue_UI_then_ordinary_controls'))()"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..additions..source:sub(b+1)
assert(load(source,'@whole_original_paid_continue_UI_controls_and_passive_ladder'))()
