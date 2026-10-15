-- The entire proven later timing transport, only its Pit observer target changes.
local f=assert(io.open('mk2ks_native_tomb_rejoin_timing_display.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
once("io.open('mk2ks_native_tomb_rejoin_display.lua','rb')","io.open('mk2ks_native_pit_rejoin_display.lua','rb')")
once("once(\"dofile('mk2ks_native_tomb_rejoin_provenance.lua')\",\"dofile('mk2ks_native_tomb_rejoin_guarded_provenance.lua')\")",
 "assert(source:find(\"dofile('mk2ks_native_pit_rejoin_provenance.lua')\",1,true))")
assert(load(source,'@whole_inherited_Pit_later_timing_transport','t',_ENV))()
