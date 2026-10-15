-- Entire native1800-field controller/round/choice chain, true Sonya router.
local file=assert(io.open('mk2ks_current_kano_cpu_extended_ram_v6290.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local first=assert(source:find(" if path=='mk2ks_physical_p2_cpu_choice_trace_v3303.lua'then",1,true))
local last=assert(source:find(' local n;source,n=source:gsub("manager.machine.screens',first,true))
-- Original v3303 is already Sonya: do not relocate its actual native AI entries.
source=source:sub(1,first-1)..[[
 if path=='mk2ks_physical_p2_cpu_choice_trace_v3303.lua'then
  source=replace_once(source,"dofile('mk2ks_physical_p2_cpu_overlap_trace_v3302.lua')",
                      "dofile('mk2ks_physical_p2_cpu_knife_trace_v1955.lua')")
 elseif path=='mk2ks_physical_p2_cpu_knife_trace_v1955.lua'then
  local rf=assert(io.open('mk2ks_physical_p2_cpu_ring_trace_v2013.lua','rb'))
  source=rf:read('*a'):gsub('\r\n','\n');rf:close()
  source=replace_once(source,"dofile('mk2ks_physical_p2_cpu_overlap_trace_v1999.lua')",
                      "dofile('mk2ks_physical_p2_cpu_overlap_trace_v1942.lua')")
 end
]]..source:sub(last)
assert(load(source,'@whole_native_extended_Sonya_control_choice_guard','t',_G))()
