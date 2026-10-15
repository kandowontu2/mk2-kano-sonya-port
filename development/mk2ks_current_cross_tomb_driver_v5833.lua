-- Complete ordinary earned-stage controller, actual opposite-character victim.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a');f:close();return s
end
local source=read('mk2ks_current_stage_ram_driver_v3594.lua')
local function replace(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
replace("  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local f=assert(io.open(assert(os.getenv('MK2KS_STAGE_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()",
 "  -- The read-only audio observer sends the whole guest to verifier RAM.")
replace('if at~=entry or not window then return end','if at~=entry or cpu.PC.value~=at+16 or not window then return end')
assert(source:find('local victim_id=id==17 and 18 or 17',1,true))
assert(not source:find(':write_',1,true)and not source:find("'wb'",1,true))
assert(load(source,'@complete3594_actual_cross_ram_only_5833','t',_ENV))()
