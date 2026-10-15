-- Different genuine human movement, one original physical controller.
-- No attacks supplied to the CPU; its decisions and outcomes remain native.
local f=assert(io.open('mk2ks_native_selector_sonya_cpu_pressure_bound.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("or approach=='pressure_hp'","or approach=='air_approach'")
once("if approach=='pressure_hp' then","if approach=='air_approach' then")
once('local toward=eligible and gap>76','local toward=eligible and gap>90')
once('local punch=eligible and (frame-first_live)%24<4','local jumping=eligible and (frame-first_live)%84<8')
once("fields['P1 Up']:set_value(0);fields['P1 Down']:set_value(0)",
     "fields['P1 Up']:set_value(jumping and 1 or 0);fields['P1 Down']:set_value(0)")
once("if punch then fields['P1 High Punch']:set_value(1)end",'-- No human attack supplied in this movement trial.')
once("log('PRESSURE_INPUT',string.format('policy=pressure_hp eligible=%d gap=%d toward=%d punch=%d',\n            eligible and 1 or 0,gap,toward and 1 or 0,punch and 1 or 0))",
     "log('AIR_INPUT',string.format('policy=air_approach eligible=%d gap=%d toward=%d jumping=%d',\n            eligible and 1 or 0,gap,toward and 1 or 0,jumping and 1 or 0))")
once('MK2_PRESSURE_BIND count=1 controller=original_physical_P1 inputs=walk_high_punch',
     'MK2_AIR_APPROACH_BIND count=1 controller=original_physical_P1 inputs=walk_periodic_jump')
assert(not source:match(':write_[ui]%d+')and not source:match('%.value%s*=[^=]'))
assert(load(source,'@one_original_controller_distinct_real_air_approach','t',_G))()

-- Retain the entire original dense renderer/display observer, replacing only
-- its already-loaded controller root. Native captures stay RAM-only.
f=assert(io.open('mk2ks_native_selector_sonya_pressure_snapshot.lua','rb'))
source=f:read('a'):gsub('\r\n','\n');f:close()
once("dofile('mk2ks_native_selector_sonya_cpu_pressure_bound.lua')",
     '-- Original physical air-approach controller already loaded once above.')
assert(load(source,'@whole_dense_display_distinct_real_air_approach','t',_G))()
