-- Keep the entire executed physical driver; restore its original roster guard.
local f=assert(io.open('mk2ks_native_tomb_rejoin_driver.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local old='if mode==4 and p:read_u16(slots[n].state)==3 then'
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1)..'if mode==4 and p:read_u16(slots[n].state)==3 and p:read_u16(slots[n].roster)<=18 then'..source:sub(last+1)
assert(load(source,'@whole_rejoin_physical_driver_original_valid_roster_guard','t',_ENV))()
