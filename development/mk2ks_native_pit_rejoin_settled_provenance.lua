-- Whole proven provenance; only the later physical route-planning driver changes.
local f=assert(io.open('mk2ks_native_pit_rejoin_provenance.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local old="dofile('mk2ks_native_tomb_rejoin_guarded_driver.lua')"
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1).."dofile('mk2ks_native_pit_rejoin_settled_driver.lua')"..source:sub(last+1)
assert(load(source,'@whole_Pit_provenance_actual_initialized_cursor_driver','t',_ENV))()
