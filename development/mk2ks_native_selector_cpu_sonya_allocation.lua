-- Preserve whole passive free-list store observer; only the real driver differs.
local file=assert(io.open('mk2ks_current_cpu_blade_allocation_v6340.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local before="dofile('mk2ks_current_kano_cpu_extended_ram_v6290.lua')"
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1).."dofile('mk2ks_native_selector_cpu_sonya_extended_ram.lua')"..source:sub(at+#before)
assert(load(source,'@whole_original_native_pool_observer_Sonya_controller','t',_G))()
