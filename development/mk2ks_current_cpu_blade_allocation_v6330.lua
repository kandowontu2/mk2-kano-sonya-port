-- Same physical native CPU trajectory; original allocation observer unchanged.
-- Read source only to reuse qualified taps. No guest/register/state writes.
dofile('mk2ks_current_kano_cpu_extended_ram_v6290.lua')
local file=assert(io.open('mk2ks_blade_allocation_v2892.lua','rb'))
local original=file:read('*a'):gsub('\r\n','\n');file:close()
local marker="local p=manager.machine.devices[':maincpu'].spaces.program"
local first=assert(original:find(marker,1,true))
assert(not original:find(marker,first+1,true),'One entire original allocation observer')
assert(load(original:sub(first),'@original_blade_allocation_v2892_current_CPU','t',_G))()
