-- Preserve the actual Lua assertion multi-return failure. Keep both find
-- results before providing assert's message; all controller edits unchanged.
local f=assert(io.open('mk2ks_native_selector_sonya_cpu_air_approach_loaded.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local before='local first,last=assert(source:find(before,1,true),before)'
local after='local first,last=source:find(before,1,true);assert(first,before)'
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@whole_air_loader_two_real_find_results','t',_G))()
