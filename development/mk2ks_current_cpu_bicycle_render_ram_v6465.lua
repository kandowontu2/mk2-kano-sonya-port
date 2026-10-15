-- Whole original5324 physical sequence and2014 renderer; passive Bicycle window.
local f=assert(io.open('mk2ks_current_cpu_compound_render_ram_v6432.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function replace(before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
replace("local move='leg'", "local move='bicycle'")
replace("'if not origin and #shots==3 then'", "'if not origin then'")
replace("'return command and command+204'", "'return command and command+136'")
replace('move=leg side=2 attempt=3','move=bicycle side=2 attempt=1')
local before="assert(not source:find('io.open',1,true)and not source:find(':snapshot',1,true))"
replace(before,[[
source=change(source,'local frame,command=0,nil','local frame,command=0,2661')
source=change(source,'origin=frame;command=frame','origin=frame')
]]..before)
assert(load(source,'@whole6432_passive_Bicycle_preentry_through_both_recoveries','t',_G))()
