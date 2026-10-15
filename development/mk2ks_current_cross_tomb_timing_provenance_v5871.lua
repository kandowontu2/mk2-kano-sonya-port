-- Complete original read-only PC-qualified provenance; actual cross driver.
local f=assert(io.open('mk2ks_current_stage_provenance_v3595.lua','rb'))
local source=f:read('a');f:close()
local function replace(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
replace("dofile('mk2ks_current_stage_ram_driver_v3594.lua')","dofile('mk2ks_current_cross_tomb_timing_driver_v5870.lua')")
replace('if at~=entry or p:read_u16(0x01061ac0)~=1','if at~=entry or cpu.PC.value~=at+16 or p:read_u16(0x01061ac0)~=1')
assert(not source:find(':write_',1,true))
assert(load(source,'@complete3595_actual_cross_pc_qualified_command_delay_5871','t',_ENV))()
