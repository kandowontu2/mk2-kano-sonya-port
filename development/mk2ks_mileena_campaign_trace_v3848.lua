-- Read-only actual native swallowing path; no inputs, assistance or raw media.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,busy=0,false
local taps={}
local function victim()
 local a=cpu.A8.value
 if a<0x01000000 or a>=0x01100000 then return false end
 local id=p:read_u16(a+0x1f0)
 return id==17 or id==18
end
local function log(tag,detail)
 print(string.format('MK2_MILEENA_CAMPAIGN_%s frame=%d pc=%08X a0=%08X a1=%08X a8=%08X a9=%08X a13=%08X id=%d writes=0 assistance=none %s',
  tag,frame,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A9.value,cpu.A13.value,
  victim()and p:read_u16(cpu.A8.value+0x1f0)or -1,detail or''))
end
taps[#taps+1]=p:install_read_tap(0xff9e7d70,0xff9e7d7f,'campaign original eaten victim task',function(at)
 if busy or at~=0xff9e7d70 or not victim()then return end
 busy=true;log('EATEN_TASK');busy=false
end)
taps[#taps+1]=p:install_read_tap(0xffd61800+17*32,0xffd61800+19*32-1,'campaign native owned victim rows',function(at,data,mask)
 if busy or not victim()then return end
 busy=true;log('ROW',string.format('at=%08X data=%04X mask=%04X',at,data&0xffff,mask));busy=false
end)
taps[#taps+1]=p:install_read_tap(0xff8387a0,0xff8387af,'campaign native owned swallowing groups',function(at)
 if busy or at~=0xff8387a0 or cpu.A0.value<0xffd61000 or cpu.A0.value>=0xffd613c0 or not victim()then return end
 busy=true;log('GROUP',string.format('descriptor=%08X zero=%08X',p:read_u32(cpu.A0.value),p:read_u32(cpu.A0.value+32)));busy=false
end)
taps[#taps+1]=p:install_read_tap(0xff838f60,0xff838f6f,'campaign native swallowed victim removal',function(at)
 if busy or at~=0xff838f60 or not victim()or cpu.A9.value<0xffd61400 or cpu.A9.value>0xffd61620 then return end
 busy=true;log('DISAPPEAR');busy=false
end)
local stores=0
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'campaign any original-cache global overrun',function(at,data,mask)
 if busy or cpu.PC.value~=0xff838860 then return end
 busy=true;stores=stores+1
 if stores<=180 then log('OVERRUN',string.format('at=%08X data=%04X mask=%04X',at,data&0xffff,mask))end
 busy=false
end)
emu.register_frame(function()assert(#taps==5,'Every campaign tap retained');frame=frame+1 end)
emu.register_stop(function()log('RESULT','global_cache_stores='..stores);for _,tap in ipairs(taps)do tap:remove()end end)
