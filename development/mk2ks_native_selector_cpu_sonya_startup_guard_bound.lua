-- Independent ungated startup observer, corrected full native base layout.
local file=assert(io.open('mk2ks_native_selector_cpu_sonya_startup_guard.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local before='mk2ks_native_selector_cpu_sonya_guard.lua'
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1)..'mk2ks_native_selector_cpu_sonya_guard_bound.lua'..source:sub(at+#before)
assert(load(source,'@whole_current_Sonya_startup_observer_layout_repair','t',_G))()
