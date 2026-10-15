-- Preserve the actual failed wrapper. Its controller edits belong to the
-- defining pressure source, not the short-string-boundary loader wrapper.
local f=assert(io.open('mk2ks_native_selector_sonya_cpu_air_approach.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function replace(before,after)
 local first,last=assert(source:find(before,1,true),before)
 assert(not source:find(before,last+1,true),'Unique defining-source boundary')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace("io.open('mk2ks_native_selector_sonya_cpu_pressure_bound.lua','rb')",
        "io.open('mk2ks_native_selector_sonya_cpu_pressure.lua','rb')")
local marker=[[once("or approach=='pressure_hp'","or approach=='air_approach'")]]
local prefix=[==[
once("\n print('MK2_SONYA_OBSERVER_LOAD\n]====])",
     "\n]====]..\" print('MK2_SONYA_OBSERVER_LOAD\")")
]==]
replace(marker,prefix..marker)
assert(load(source,'@one_air_controller_actual_defining_source_and_boundary','t',_G))()
