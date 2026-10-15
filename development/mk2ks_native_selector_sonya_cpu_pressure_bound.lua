-- Preserve the already preflight-pinned pressure source. Correct one generated
-- short-string newline boundary before loading; controller/observations intact.
local f=assert(io.open('mk2ks_native_selector_sonya_cpu_pressure.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local before="\n print('MK2_SONYA_OBSERVER_LOAD\n]====])"
local after="\n]====]..\" print('MK2_SONYA_OBSERVER_LOAD\")"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@whole_pressure_controller_short_string_boundary_bound','t',_G))()
