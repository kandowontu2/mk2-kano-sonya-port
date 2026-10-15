-- Extra read-only actual guard and every live actor field. Physical inputs,
-- original labels and stop condition remain the original v1438 driver's.
dofile('mk2ks_physical_p2_cpu_overlap_trace_v1942.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame=0
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function live()
 return p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and p:read_u16(0x01060e50)==17
end
local function log(tag,text)
 print(string.format('MK2_KNIFE_PAIR_%s frame=%d %s writes=0 assistance=none',tag,frame,text))
end
taps[#taps+1]=p:install_read_tap(0xff837d40,0xff837d4f,'actual victim Main guard bit',function(at)
 if at~=0xff837d40 or cpu.PC.value~=0xff837d50 or not live()then return end
 local v,a,m=cpu.A0.value,cpu.A8.value,cpu.A13.value
 if not(valid(v)and valid(a)and valid(m))then return end
 -- Stock FF837D40 reads *A13(170), not the victim object.
 local vm=p:read_u32(m+0x170)
 if not valid(vm)then return end
 log('GUARD',string.format('entry=FF837D40 pc=%08X actor=%08X main=%08X owner=%08X parent=%08X victim=%08X vmain=%08X vowner=%08X vid=%d vflags=%04X vbody=%04X vxraw=%08X vyraw=%08X xraw=%08X yraw=%08X id=%d',
  cpu.PC.value,a,m,p:read_u32(m+0xc0),p:read_u32(m+0x230),v,vm,p:read_u32(vm+0xc0),p:read_u16(v+0x1f0),
  p:read_u16(vm+0x210),p:read_u16(v+0x160),p:read_u32(v+0x80),p:read_u32(v+0xa0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u16(a+0x1f0)))
end)
taps[#taps+1]=p:install_read_tap(0xff837d90,0xff837d9f,'actual tested guard flags before native branch',function(at)
 if at~=0xff837d90 or cpu.PC.value~=0xff837da0 or not live()then return end
 local a,m=cpu.A8.value,cpu.A13.value
 if not(valid(a)and valid(m))then return end
 local vm=p:read_u32(m+0x170)
 if not valid(vm)then return end
 log('TESTED',string.format('entry=FF837D90 pc=%08X actor=%08X main=%08X owner=%08X parent=%08X vmain=%08X loaded_main=%08X tested_flags=%08X vflags=%04X',
  cpu.PC.value,a,m,p:read_u32(m+0xc0),p:read_u32(m+0x230),vm,cpu.A0.value,cpu.A4.value,p:read_u16(vm+0x210)))
end)
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for _,range in ipairs({{0xffffb000,0xffffb080},{0xfffc5800,0xfffc6000}})do
   local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
 if not live()then return end
 for n,s in ipairs({{a=0x01060220,m=0x01060260},{a=0x01060df0,m=0x01060e30}})do
  local a,m=p:read_u32(s.a),p:read_u32(s.m)
  if valid(a)and valid(m)then
   log('FIELD',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d pose=%08X action=%04X xraw=%08X yraw=%08X floor=%d stage_floor=%d facing=%04X flags=%04X body=%04X vx=%08X vy=%08X gravity=%08X trail=%08X',
    n,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u32(a+0x1d0),p:read_u16(m+0x1f0),p:read_u32(a+0x80),p:read_u32(a+0xa0),
    p:read_i16(m+0x200),p:read_i16(0x0105ecd0),p:read_u16(a+0xf0),p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20),p:read_u32(m+0x190)))
  end
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end;log('RESULT','scope=knife_actor_fields_actual_guard_not_full_port')end)
