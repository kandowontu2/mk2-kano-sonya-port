-- Preserve the actual first IN0-only Low Kick controller failure unchanged.
-- MK2's compiled input map places Low Kick in IN2, not IN0.
local f=assert(io.open('mk2ks_native_selector_sonya_cpu_lowkick_owners.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(before,after)
 local first,last=source:find(before,1,true);assert(first,before)
 assert(not source:find(before,last+1,true),'Unique actual input binding boundary')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once([["if kicking then fields['P1 Low Kick']:set_value(1)end"]],
     [["if kicking then manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']:set_value(1)end"]])
local marker="once('local toward=eligible and gap>76',"
local addition=[====[
-- Extend only the original per-frame input-release list. Its callback runs
-- before the one original physical combat controller, including outside live.
once(" if path=='mk2ks_physical_p2_cpu_continuation_v3300.lua' then\n",[===[
 if path=='mk2ks_physical_p2_cpu_continuation_v3300.lua' then
  source=replace_once(source,"high['P1 Down'],high['P1 Block']}",
   "high['P1 Down'],high['P1 Block'],manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']}")
]===])
]====]
once(marker,addition..marker)
assert(load(source,'@same_one_controller_actual_IN2_lowkick_and_release','t',_G))()
