-- Additional read-only provenance for the naturally chosen P2 Square Wave.
-- Physical selection, human buttons, CPU RNG and the v1997 exit are unchanged.
dofile('mk2ks_physical_p2_cpu_choice_trace_v2035.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,taps=0,{}
local function owned()
 local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 return p:read_u16(0x010601d0)==2 and p:read_u16(0x01060dc0)==0 and
 p:read_u16(0x010601f0)==1 and p:read_u16(0x01060e50)==18 and
 a>=0x01000000 and a<0x01100000 and m>=0x01000000 and m<0x01100000 and
 cpu.A8.value==a and cpu.A13.value==m and p:read_u32(m+0xc0)==a
end
local function log(tag,s)
 print(string.format('MK2_SQUARE_NATIVE_%s frame=%d %s writes=0 assistance=none',tag,frame,s))
end
taps[#taps+1]=p:install_read_tap(0xff876660,0xff87666f,'original native Square fall',function(at,data,mask)
 if at~=0xff876660 or cpu.PC.value~=at+16 or not owned()then return end
 local a,m=cpu.A8.value,cpu.A13.value
 log('FALL',string.format('entry=%08X pc=%08X opcode=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d action=%04X xraw=%08X yraw=%08X floor=%d a0=%08X a1=%08X a2=%08X a3=%08X vx=%08X vy=%08X gravity=%08X',
 at,cpu.PC.value,data,mask,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(m+0x1f0),
 p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_i16(m+0x200),cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,
 p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20)))
end)
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for _,range in ipairs({{0xffffca00,0xffffd200},{0xff876420,0xff876b60}})do
   local words={}
   for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
