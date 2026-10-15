-- Actual physical P2 CPU/P1 human inputs remain the unchanged v1438 driver.
-- Observe ALL mode/state callbacks and original health resets across rounds.
-- No guest state, ROM, timers, RNG, characters, health or positions are written.
dofile('mk2ks_cpu_recovery_probe_v1438.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,live=0,false
local taps={}
local slots={{a=0x01060220,m=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {a=0x01060df0,m=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function common()
 return string.format(' mode=%d states=%d,%d ids=%d,%d stage=%d schedule=%08X winner=%d writes=0 assistance=none',
  p:read_u16(0x010601d0),p:read_u16(slots[1].state),p:read_u16(slots[2].state),
  p:read_u16(slots[1].id),p:read_u16(slots[2].id),p:read_u16(0x01061b30),
  p:read_u32(0x01061b10),p:read_u16(0x01061b00))
end
for n,s in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(s.hp,s.hp+15,'all original CPU-round health stores',function(at,data,mask)
  if live then
   print(string.format('MK2_CPU_ROUND_HEALTH frame=%d slot=%d at=%08X before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X op0=%04X op1=%04X op2=%04X',
    frame,n,at,p:read_u16(s.hp),data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,
    p:read_u16(cpu.PC.value-48),p:read_u16(cpu.PC.value-32),p:read_u16(cpu.PC.value-16))..common())
  end
 end)
end
emu.register_frame(function()
 frame=frame+1
 if not live and p:read_u16(0x010601d0)==2 and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==0 and
  (p:read_u16(slots[2].id)==17 or p:read_u16(slots[2].id)==18)then
  live=true;print('MK2_CPU_ROUND_BEGIN frame='..frame..common())
 end
 if not live then return end
 for n,s in ipairs(slots)do
  local a,m=p:read_u32(s.a),p:read_u32(s.m)
  local owned=valid(a)and valid(m)
  print(string.format('MK2_CPU_ROUND_FIELD frame=%d slot=%d hp=%d actor=%08X main=%08X valid=%d owner=%08X id=%d action=%04X y=%d floor=%d vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X trail=%08X',
   frame,n,p:read_u16(s.hp),a,m,owned and 1 or 0,owned and p:read_u32(m+0xc0)or 0,
   owned and p:read_u16(a+0x1f0)or 0,owned and p:read_u16(m+0x1f0)or 0,
   owned and p:read_i16(a+0xb0)or 0,owned and p:read_i16(m+0x200)or 0,
   owned and p:read_u32(a+0x40)or 0,owned and p:read_u32(a+0x60)or 0,
   owned and p:read_u32(a+0x20)or 0,owned and p:read_u16(m+0x210)or 0,
   owned and p:read_u16(a+0x160)or 0,owned and p:read_u32(m+0x190)or 0)..common())
 end
end)
emu.register_stop(function()
 print('MK2_CPU_ROUND_RESULT frame='..frame..common())
 for _,tap in ipairs(taps)do tap:remove()end
end)
