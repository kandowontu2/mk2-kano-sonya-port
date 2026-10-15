-- Full current cold byte/channel/body collector, Sonya native controller only.
local file=assert(io.open('mk2ks_native_selector_cpu_blade_knife.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local before='mk2ks_current_cpu_blade_allocation_v6340.lua'
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1)..'mk2ks_native_selector_cpu_sonya_allocation.lua'..source:sub(at+#before)
assert(load(source,'@whole_current_body_cold_channel_Sonya_base','t',_G))()
