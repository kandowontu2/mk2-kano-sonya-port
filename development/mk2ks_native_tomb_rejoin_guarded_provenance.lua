-- Full original passive provenance, with only the guarded driver target changed.
local f=assert(io.open('mk2ks_native_tomb_rejoin_provenance.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local old="dofile('mk2ks_native_tomb_rejoin_driver.lua')"
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1).."dofile('mk2ks_native_tomb_rejoin_guarded_driver.lua')"..source:sub(last+1)
assert(load(source,'@whole_rejoin_provenance_guarded_driver_target','t',_ENV))()
