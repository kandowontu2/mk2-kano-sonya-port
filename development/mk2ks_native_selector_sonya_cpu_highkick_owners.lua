-- A distinct ordinary walk/high-kick trial. CPU and guest state untouched.
local f=assert(io.open('mk2ks_native_selector_sonya_cpu_lowkick_owners.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(before,after)
 local first,last=source:find(before,1,true);assert(first,before)
 assert(not source:find(before,last+1,true),'Unique original input boundary')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("\n print('MK2_SONYA_OBSERVER_LOAD\n]====])",
     "\n]====]..\" print('MK2_SONYA_OBSERVER_LOAD\")")
once([["if kicking then fields['P1 Low Kick']:set_value(1)end"]],
     [["if kicking then fields['P1 High Kick']:set_value(1)end"]])
local marker="once('local toward=eligible and gap>76',"
local addition=[====[
once(" if path=='mk2ks_physical_p2_cpu_continuation_v3300.lua' then\n",[===[
 if path=='mk2ks_physical_p2_cpu_continuation_v3300.lua' then
  source=replace_once(source,"high['P1 Down'],high['P1 Block']}",
   "high['P1 Down'],high['P1 Block'],high['P1 High Kick']}")
]===])
]====]
once(marker,addition..marker)
source=source:gsub('LOWKICK_INPUT','HIGHKICK_INPUT'):gsub('LOWKICK_BIND','HIGHKICK_BIND'):gsub('walk_lowkick','walk_highkick')
assert(not source:match(':write_[ui]%d+') and not source:match('%.value%s*=[^=]'))
assert(load(source,'@one_original_physical_walk_highkick_saved_owners','t',_G))()
