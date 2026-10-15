-- One ordinary-input policy change: approach/jump-kick native Subzero8
-- instead of repeatedly using the unsuccessful distant knife zoning plan.
local path='mk2ks_native_kano_p2_postending_sonya.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local before="one('-- Observe actual own special entries independently of intended button plans.',helper"
local at=assert(source:find(before,1,true))
assert(not source:find(before,at+#before,true),'One existing controller expansion')
local policy=[[one("elseif strategy=='zoning' then", "elseif strategy=='zoning' and other.roster~=8 then")
]]
source=source:sub(1,at-1)..policy..source:sub(at)
assert(load(source,'@'..path..'::ordinary_Subzero_reactive_buttons_only','t',_ENV))()
