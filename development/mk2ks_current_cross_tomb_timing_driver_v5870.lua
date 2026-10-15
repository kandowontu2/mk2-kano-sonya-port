-- Complete original earned cross controller; ordinary finishing-input delay.
-- No writes to RNG, health, IDs, palettes, actors, positions or CPU registers.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a');f:close();return s
end
local source=read('mk2ks_current_stage_ram_driver_v3594.lua')
local function replace(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
replace("  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local f=assert(io.open(assert(os.getenv('MK2KS_STAGE_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()",
 "  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  _tomb_timing_guest(raw)")
replace('if at~=entry or not window then return end','if at~=entry or cpu.PC.value~=at+16 or not window then return end')
assert(not source:find(':write_',1,true)and not source:find("'wb'",1,true))
local delay=assert(tonumber(os.getenv('MK2KS_TOMB_COMMAND_DELAY')))
assert(delay>=1 and delay<=80 and delay==math.floor(delay),'Declared physical command delay only')
replace('frame-window>=65 then','frame-window>='..(65+delay)..' then')
local prefix=[[
local function _tomb_timing_guest(raw)
 assert(#raw==1048576)
 print('MK2_TOMB_TIMING_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end))
end
]]
print(string.format('MK2_TOMB_TIMING_CONFIGURATION delay=%d writes=0 assistance=none',delay))
assert(load(prefix..source,'@complete3594_actual_cross_physical_command_delay_5870','t',_ENV))()
-- Failure-only host deadline, never a native terminal or successful branch.
emu.register_frame_done(function()
 if manager.machine.time:as_double()>=890 then
  print('MK2_TOMB_TIMING_HOST_DEADLINE assistance=none writes=0')
  manager.machine:exit()
 end
end)
