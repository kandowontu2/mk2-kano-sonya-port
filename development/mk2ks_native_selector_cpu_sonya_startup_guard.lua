-- Original ungated child observer, with one native Sonya controller root.
local file=assert(io.open('mk2ks_native_selector_cpu_startup_guard.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local before="dofile('mk2ks_native_selector_cpu_guard_shadow.lua')"
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1).."dofile('mk2ks_native_selector_cpu_sonya_guard.lua')"..source:sub(at+#before)
assert(load(source,'@whole_current_Sonya_ungated_projectile_startup','t',_G))()
