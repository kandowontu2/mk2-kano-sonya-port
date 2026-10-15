-- Run the whole original controller/audio/choices in one explicit environment.
-- Autoboot scripts are sandboxed; assigning their dofile does not change _G.
-- Nested wrappers deliberately load into _G, so bind that to the SAME table.
local file=assert(io.open('mk2ks_native_selector_sonya_choice_visual_audio.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local original_dofile=dofile',[[
local observer_env=setmetatable({}, {__index=_G})
observer_env._G=observer_env
local _G=observer_env
local loads={}
local original_dofile=function(path)
 local f=assert(io.open(path,'rb'));local text=f:read('a'):gsub('\r\n','\n');f:close()
 loads[path]=(loads[path]or 0)+1
 print('MK2_SONYA_OBSERVER_LOAD path='..path..' count='..loads[path]..' writes=0 assistance=none')
 return assert(load(text,'@explicit_bound_'..path,'t',observer_env))()
end
]])
replace('dofile=function(path)','observer_env.dofile=function(path)')
replace(" if path~='mk2ks_native_selector_cpu_guard_shadow.lua' then return original_dofile(path) end",[[
 if path~='mk2ks_native_selector_cpu_guard_shadow.lua' then return original_dofile(path) end
 loads[path]=(loads[path]or 0)+1
 assert(loads[path]==1,'Exactly one actual intercepted shadow root')
 print('MK2_SONYA_SHADOW_BIND count=1 human=17 cpu=18 writes=0 assistance=none')
]])
replace('dofile=original_dofile','observer_env.dofile=original_dofile')
assert(load(source,'@whole_original_sonya_observer_explicit_environment','t',_G))()

-- Independently record each actually executing native boundary position and
-- horizontal velocity store. Do not infer instruction execution from fields.
local p=manager.machine.devices[':maincpu'].spaces.program
local regs=manager.machine.devices[':maincpu'].state
local frame=0;local taps={};local count=0
emu.register_frame(function()frame=frame+1 end)
local function valid(a)return a>=0x01000000 and a<0x01100000 end
for slot,item in ipairs({{0x01060220,0x01060260},{0x01060df0,0x01060e30}})do
 -- Actors are allocated by the game. Install at their actual first live
 -- address, never at an injected fixture actor or assumed allocation.
 local installed=false
 emu.register_frame(function()
  if installed or p:read_u16(0x010601d0)~=2 then return end
  local a,m=p:read_u32(item[1]),p:read_u32(item[2])
  if not valid(a)or not valid(m)or p:read_u32(m+0xc0)~=a then return end
  installed=true
  for _,field in ipairs({{'x',0x80,32},{'vx',0x40,32}})do
   taps[#taps+1]=p:install_write_tap(a+field[2],a+field[2]+field[3]-1,'actual native boundary and horizontal physics',function(at,data,mask)
    local id=p:read_u16(a+0x1f0)
    if p:read_u16(0x010601d0)~=2 or (id~=17 and id~=18) or p:read_u32(m+0xc0)~=a then return end
    count=count+1
    print(string.format('MK2_SONYA_HORIZONTAL_STORE frame=%d slot=%d kind=%s at=%08X before=%08X data=%08X mask=%08X pc=%08X actor=%08X main=%08X owner=%08X id=%d action=%04X xraw=%08X yraw=%08X vx=%08X left=%d right=%d a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X a5=%08X a8=%08X a13=%08X writes=0 assistance=none',
     frame,slot,field[1],at,p:read_u32(at),data,mask,regs.PC.value,a,m,p:read_u32(m+0xc0),id,p:read_u16(m+0x1f0),
     p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_i16(0x0105ecf0)+0x3a,p:read_i16(0x0105ed00)+0x15f,
     regs.A0.value,regs.A1.value,regs.A2.value,regs.A3.value,regs.A4.value,regs.A5.value,regs.A8.value,regs.A13.value))
   end)
  end
 end)
end
emu.register_stop(function()
 for _,tap in ipairs(taps)do tap:remove()end
 print('MK2_SONYA_HORIZONTAL_RESULT stores='..count..' writes=0 assistance=none')
end)
