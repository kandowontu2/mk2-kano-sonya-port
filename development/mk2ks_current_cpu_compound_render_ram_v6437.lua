--Retain executed6432. Broaden only passive observation to precede native entry.
local file=assert(io.open('mk2ks_current_cpu_compound_render_ram_v6432.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local before="assert(not source:find('io.open',1,true)and not source:find(':snapshot',1,true))"
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
local inserted=[[
source=change(source,'local frame,command=0,nil','local frame,command=0,2918')
source=change(source,'origin=frame;command=frame','origin=frame')
source=change(source,'return command and command+204','return command and command+206')
]]
source=source:sub(1,first-1)..inserted..source:sub(first)
assert(load(source,'@whole6432_with_two_preentry_passive_fields','t',_G))()
