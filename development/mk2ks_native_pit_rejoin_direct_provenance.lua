-- Complete original source-qualified stage provenance; unchanged paid-input
-- rejoin controller shared with Tomb. Arena6 is chosen by ordinary earned play.
local f=assert(io.open('mk2ks_current_stage_provenance_v3595.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
once("dofile('mk2ks_current_stage_ram_driver_v3594.lua')","dofile('mk2ks_native_pit_rejoin_direct_driver.lua')")
once('if at~=entry or p:read_u16(0x01061ac0)~=1','if at~=entry or cpu.PC.value~=at+16 or p:read_u16(0x01061ac0)~=1')
assert(not source:find(':write_',1,true))
assert(load(source,'@whole3595_Pit_source_PC_shared_ordinary_rejoin','t',_ENV))()
