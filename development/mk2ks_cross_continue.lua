-- Whole original passive ladder objects, using the extended real controller.
local f=assert(io.open('mk2ks_continue_ladder_positions_v6605.lua','rb'))
local source=f:read('a');f:close()
local before="io.open('mk2ks_continue_presentation_v6602.lua','rb')"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1).."io.open('mk2ks_cross_continue_presentation.lua','rb')"..source:sub(b+1)
assert(load(source,'@whole_native_cross_character_continue_ladder_objects'))()
