-- Correct only the initial read-only inventory listener, not physical inputs.
local f=assert(io.open('mk2ks_native_sonya_cpu_finisher.lua','rb'))
local source=f:read('a');f:close()
local before='emu.register_frame(function()\n if frame==0 then\n'
local after='local guest_sent=false\nemu.register_frame(function()\n if not guest_sent then\n  guest_sent=true\n'
local first,last=source:find(before,1,true)
assert(first and not source:find(before,last+1,true),'Exact single initial inventory callback boundary')
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@mk2ks_native_sonya_cpu_finisher.lua::only_first_inventory_listener_corrected','t',_ENV))()
