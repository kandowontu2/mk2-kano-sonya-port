-- Passive native root/sequence/group provenance with the SAME physical inputs.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,busy,first_bad,records=0,false,nil,0
local taps,ring={},{}
local ring_size=1800
local function peek(a)
 if a>=0xfe800000 and a<=0xffffffc0 then return p:read_u32(a) end
 return 0
end
local function own()
 local a=cpu.A8.value
 return a>=0x01000000 and a<0x01100000 and p:read_u16(a+0x1f0)==17 and
  p:read_u32(0x01060df0)==a and p:read_u16(0x01060e50)==17
end
local function record(kind,at,data,mask)
 if busy or frame<35000 or not own() then return end
 busy=true
 local a,m=cpu.A8.value,cpu.A13.value
 records=records+1
 ring[(records-1)%ring_size+1]=string.format('MK2_KANO_CACHE_CAUSE frame=%d kind=%s pc=%08X at=%08X data=%04X mask=%04X actor=%08X main=%08X owner=%08X id=17 roster=%d health=%d,%d state=%d mode=%d action=%04X pose=%08X cache=%08X a0=%08X a1=%08X a5=%08X a6=%08X a7=%08X a9=%08X a14=%08X sp=%08X a0_rom=%08X a5_rom=%08X a9_rom=%08X stack0=%08X stack1=%08X writes=0 assistance=none',
 frame,kind,cpu.PC.value,at,data&0xffff,mask,a,m,
 m>=0x01000000 and m<0x01100000 and p:read_u32(m+0xc0)or 0,
 p:read_u16(0x01060e50),p:read_u16(0x010602f0),p:read_u16(0x01060ec0),
 p:read_u16(0x01060dc0),p:read_u16(0x010601d0),
 m>=0x01000000 and m<0x01100000 and p:read_u16(m+0x1f0)or 0,
 p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),
 cpu.A0.value,cpu.A1.value,cpu.A5.value,cpu.A6.value,cpu.A7.value,cpu.A9.value,cpu.A14.value,cpu.SP.value,
 peek(cpu.A0.value),peek(cpu.A5.value),peek(cpu.A9.value),p:read_u32(cpu.SP.value),p:read_u32(cpu.SP.value+32))
 busy=false
end
for _,entry in ipairs({{0xff906090,'main_lookup'},{0xff906110,'root_loaded'},
 {0xff906130,'lookup_cell'},{0xff906140,'lookup_result'},
 {0xff83c870,'animation_loop'},{0xff838790,'cache_begin'},
 {0xff8387f0,'group_next'},{0xff838810,'descriptor'},{0xff838a30,'cache_end'}})do
 local at,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'readonly CPU Kano cache provenance',function(address,data,mask)
  if address==at and cpu.PC.value==at+16 then record(kind,address,data,mask)end
 end)
end
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'readonly first native global corruption',function(at,data,mask)
 if busy or first_bad or cpu.PC.value~=0xff838860 or not own()then return end
 first_bad=frame;record('first_global_write',at,data,mask)
 for serial=math.max(1,records-ring_size+1),records do print(ring[(serial-1)%ring_size+1])end
end)
emu.register_frame_done(function()
 frame=frame+1
 assert(#taps==10,'All exact passive native taps retained')
 if first_bad and frame>=first_bad+2 then
  print(string.format('MK2_KANO_CACHE_CAUSE_STOP frame=%d first_bad=%d records=%d writes=0 assistance=none',frame,first_bad,records))
  manager.machine:exit()
 end
end)
emu.register_stop(function()
 print(string.format('MK2_KANO_CACHE_CAUSE_RESULT frame=%d first_bad=%d records=%d writes=0 assistance=none',frame,first_bad or -1,records))
 for _,tap in ipairs(taps)do tap:remove()end
end)
dofile('mk2ks_native_sonya_p1_postending_kano.lua')
