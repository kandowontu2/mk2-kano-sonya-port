-- Whole completed34010 visible-scanout register order, Pit observer target only.
local f=assert(io.open('mk2ks_native_tomb_rejoin_scanout_display.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local old="io.open('mk2ks_native_tomb_rejoin_timing_display.lua','rb')"
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1).."io.open('mk2ks_native_pit_rejoin_timing_display.lua','rb')"..source:sub(last+1)
assert(load(source,'@whole_source_defined_completed_Pit_scanout','t',_ENV))()
