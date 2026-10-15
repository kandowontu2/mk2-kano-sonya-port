-- Entire proven native audio/DAC/ROM/PCM/14channel and Main140 observer.
dofile('mk2ks_current_subzero_pit_audio_v5941.lua')
-- Additional passive source-PC snapshots; never change RNG or queue state.
do
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,origin=0,nil
local taps={}
local function active()return origin and frame<=origin+1100 end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,entry,extra)
 local a,m=cpu.A8.value,cpu.A13.value
 print(string.format('MK2_PQR_%s frame=%d seconds=%.12f writes=0 assistance=none entry=%08X a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X a8=%08X a13=%08X sp=%08X top=%08X next=%08X id=%d owner140=%08X seed=%08X p0=%04X d0=%04X p1=%04X d1=%04X p2=%04X d2=%04X %s',
  tag,frame,emu.time(),entry,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A4.value,a,m,
  cpu.SP.value,p:read_u32(cpu.SP.value),p:read_u32(cpu.SP.value+32),valid(a)and p:read_u16(a+0x1f0)or -1,
  valid(m)and p:read_u32(m+0x140)or 0,p:read_u32(0x0105b950),
  p:read_u16(0x010b8100),p:read_u16(0x010b8110),p:read_u16(0x010b8140),p:read_u16(0x010b8150),
  p:read_u16(0x010b8180),p:read_u16(0x010b8190),extra or ''))
end
emu.register_frame(function()frame=frame+1 end)
taps[#taps+1]=p:install_read_tap(0xff8bdde0,0xff8bddef,'real current Pit PQR origin',function(at)
 if at~=0xff8bdde0 or cpu.PC.value~=at+16 then return end
 assert(not origin);origin=frame;log('BEGIN',at,'arena='..p:read_u16(0x01061ac0))
end)
for _,item in ipairs({
 {'DISPATCH',0xffa12530},{'HEADER',0xffa12620},{'SELECT',0xffa126a0},
 {'QUEUE',0xffa12a10},{'QUEUE',0xffa12a80},{'QUEUE',0xffa12b00},
 {'SUPPRESS',0xffa129d0},{'FINISH',0xffa12b90},
 {'RNG_BEGIN',0xff80eae0},{'RNG_SEED',0xff80e990},{'RNG_STORE',0xff80ea40},
 {'RNG_ROTATE',0xff80ea60},{'RNG_WORD',0xff80eaa0},{'RNG_MULTIPLY',0xff80eb20},
 {'RNG_PRODUCT',0xff80eb30},{'RNG_RETURN',0xff80eb60},
 {'PACKED_BEGIN',0xffa12180},{'PACKED_RETURN',0xffa121e0},
 {'VOICE_BEGIN',0xffa123d0},{'VOICE_RETURN',0xffa12400}
})do
 local tag,entry=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'passive exact original queue/RNG '..tag,function(at)
  if not active()or at~=entry or cpu.PC.value~=at+16 then return end
  local extra=''
  if tag=='HEADER'then
   assert(cpu.A0.value>=0xffa0ef20 and cpu.A0.value<0xffa10ee0)
   extra=string.format('header=%04X base=%04X',p:read_u16(cpu.A0.value),p:read_u16(cpu.A0.value+16))
  end
  log(tag,entry,extra)
 end)
end
emu.register_stop(function()
 assert(origin and frame==origin+1101);log('RESULT',0,'origin='..origin..' raw_files=0')
 for _,tap in ipairs(taps)do tap:remove()end
end)
end
