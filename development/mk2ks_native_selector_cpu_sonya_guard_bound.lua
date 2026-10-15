-- Repair only the observer's base layout; preserve actual role/source checks.
local file=assert(io.open('mk2ks_native_selector_cpu_sonya_guard.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local before='mk2ks_native_selector_cpu_sonya_base.lua'
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1)..'mk2ks_native_selector_cpu_sonya_base_expanded.lua'..source:sub(at+#before)
assert(load(source,'@whole_current_Sonya_shadow_adapter_layout_repair','t',_G))()
