-- Passive provenance only; SAME original full physical campaign and deadline.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,busy,first_bad,records=0,false,nil,0
local taps,ring={},{}
local ring_size=1800
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function peek(a)
 if a>=0xfe800000 and a<=0xffffffc0 then return p:read_u32(a)end
 return 0
end
local function own()
 local actor=cpu.A8.value
 local other=p:read_u32(0x01060df0)
 return valid(actor) and valid(other) and p:read_u32(0x01060220)==actor and
  p:read_u16(actor+0x1f0)==18 and p:read_u16(0x01060280)==18 and
  p:read_u16(other+0x1f0)==7 and p:read_u16(0x01060e50)==7
end
local function record(kind,at,data,mask)
 if busy or frame<32000 or not own()then return end
 busy=true
 local actor,main=cpu.A8.value,cpu.A13.value
 local human_main,cpu_main=p:read_u32(0x01060260),p:read_u32(0x01060e30)
 records=records+1
 ring[(records-1)%ring_size+1]=string.format('MK2_SONYA_RAIDEN_CACHE_CAUSE frame=%d seconds=%.12f kind=%s pc=%08X at=%08X data=%04X mask=%04X actor=%08X main=%08X main_owner=%08X victim_main=%08X cpu_main=%08X cpu_actor=%08X id=18 roster=%d cpu_roster=%d health=%d,%d state=%d,%d mode=%d stage=%d winner=%d action=%04X pose=%08X cache=%08X flags=%04X bank=%04X a0=%08X a1=%08X a5=%08X a6=%08X a7=%08X a9=%08X a14=%08X sp=%08X a0_rom=%08X a5_rom=%08X a9_rom=%08X stack0=%08X stack1=%08X stack2=%08X writes=0 assistance=none',
  frame,emu.time(),kind,cpu.PC.value,at,data&0xffff,mask,actor,main,valid(main)and p:read_u32(main+0xc0)or 0,
  human_main,cpu_main,p:read_u32(0x01060df0),p:read_u16(0x01060280),p:read_u16(0x01060e50),
  p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(0x010601f0),p:read_u16(0x01060dc0),
  p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u16(0x01061b00),
  valid(main)and p:read_u16(main+0x1f0)or 0,p:read_u32(actor+0x1d0),p:read_u32(actor+0x1a0),
  valid(main)and p:read_u16(main+0x210)or 0,p:read_u16(actor+0x140),
  cpu.A0.value,cpu.A1.value,cpu.A5.value,cpu.A6.value,cpu.A7.value,cpu.A9.value,cpu.A14.value,cpu.SP.value,
  peek(cpu.A0.value),peek(cpu.A5.value),peek(cpu.A9.value),
  p:read_u32(cpu.SP.value),p:read_u32(cpu.SP.value+32),p:read_u32(cpu.SP.value+64))
 busy=false
end
for _,entry in ipairs({{0xff906090,'main_lookup'},{0xff906110,'root_loaded'},
 {0xff906130,'lookup_cell'},{0xff906140,'lookup_result'},
 {0xff83c870,'animation_loop'},{0xff838790,'cache_begin'},
 {0xff8387f0,'group_next'},{0xff838810,'descriptor'},{0xff838a30,'cache_end'}})do
 local at,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'passive actual Sonya-victim Raiden animation cache provenance',function(address,data,mask)
  if address==at and cpu.PC.value==at+16 then record(kind,address,data,mask)end
 end)
end
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'passive first actual Sonya-victim global corruption',function(at,data,mask)
 if busy or first_bad or cpu.PC.value~=0xff838860 or not own()then return end
 first_bad=frame;record('first_global_write',at,data,mask)
 for serial=math.max(1,records-ring_size+1),records do print(ring[(serial-1)%ring_size+1])end
end)
emu.register_frame_done(function()
 frame=frame+1;assert(#taps==10,'All exact passive provenance taps retained')
end)
emu.register_stop(function()
 print(string.format('MK2_SONYA_RAIDEN_CACHE_CAUSE_RESULT frame=%d first_bad=%d records=%d writes=0 assistance=none',frame,first_bad or-1,records))
 for _,tap in ipairs(taps)do tap:remove()end
end)
dofile('mk2ks_native_kano_laser_sonya_postending_leg_guard_late.lua')
