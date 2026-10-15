-- Same full passive ladder object observer; actual fresh ordinary controls.
local f=assert(io.open('mk2ks_continue_ladder_positions_v6605.lua','rb'));local template=f:read('a');f:close()
local a,b=assert(template:find('local after=[=[',1,true));local stop=assert(template:find(']=]',b+1,true))
local additions=template:sub(b+1,stop-1)
f=assert(io.open('mk2ks_cross_continue_ordinary_presentation.lua','rb'));local source=f:read('a');f:close()
local before="assert(load(helper..source,'@whole_native_cross_continue_UI_ordinary_fresh_controls'))()"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..additions..source:sub(b+1)
assert(load(source,'@whole_cross_continue_ordinary_controls_and_native_ladder_observer'))()
