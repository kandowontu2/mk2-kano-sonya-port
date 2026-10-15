-- Whole5833 RAM-only normal paid controller; real original Sub-Zero8 opponent.
-- No proxy for either performer, no health/position/arena/CPU writes.
local f=assert(io.open('mk2ks_current_cross_tomb_driver_v5833.lua','rb'))
local source=f:read('a');f:close();source=source:gsub('\r\n','\n')
local before="assert(source:find('local victim_id=id==17 and 18 or 17',1,true))"
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1).."replace('local victim_id=id==17 and 18 or 17','local victim_id=8')"..source:sub(last+1)
assert(load(source,'@whole5833_physical_current_performer_original_SubZero8_victim','t',_ENV))()
