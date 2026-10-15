-- Readonly root/cursor/group provenance; corrected native SP state name.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
assert(cpu.SP and cpu.A14 and cpu.ST,'Native CPU register names required')
local frame,busy,bad_frame,records=0,false,nil,0
local taps={}
local ring,ring_size,flushed={},1200,false
local function flush()
 if flushed then return end
 flushed=true
 for serial=math.max(1,records-ring_size+1),records do
  local item=ring[(serial-1)%ring_size+1]
  if item and (item.kind=='group_next' or item.kind=='descriptor')then print(item.line)end
 end
end
local function rom32(address)
 if address>=0xfe800000 and address<=0xffffffc0 then return p:read_u32(address)end
 return 0
end
local function own()
 local a=cpu.A8.value
 return a>=0x01000000 and a<0x01100000 and p:read_u16(a+0x1f0)==18 and
  p:read_u32(0x01060220)==a and p:read_u16(0x01060280)==18
end
local function record(kind,address,data,mask)
 if busy or frame<107500 or frame>108270 or not own()then return end
 busy=true
 local ok,line=pcall(function()
 local a,m=cpu.A8.value,cpu.A13.value
 return string.format('MK2_SUBZERO_CACHE_TRACE frame=%d kind=%s entry=%08X pc=%08X value=%04X mask=%04X id=18 roster=%d actor=%08X main=%08X main_owner=%08X health=%d,%d human_state=%d cpu_roster=%d cpu_actor=%08X mode=%d stage=%d pose=%08X cache=%08X action=%04X a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X a5=%08X a6=%08X a9=%08X a14=%08X sp=%08X a0_rom32=%08X a5_rom32=%08X a9_rom32=%08X writes=0 assistance=none',
  frame,kind,address,cpu.PC.value,data&0xffff,mask,p:read_u16(0x01060280),a,m,
  m>=0x01000000 and m<0x01100000 and p:read_u32(m+0xc0)or 0,
  p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(0x010601f0),p:read_u16(0x01060e50),p:read_u32(0x01060df0),
  p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),
  m>=0x01000000 and m<0x01100000 and p:read_u16(m+0x1f0)or 0,
  cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A4.value,cpu.A5.value,cpu.A6.value,cpu.A9.value,
  cpu.A14.value,cpu.SP.value,rom32(cpu.A0.value),rom32(cpu.A5.value),rom32(cpu.A9.value))
 end)
 busy=false
 if not ok then print('LUA ERROR readonly cache observer: '..tostring(line));manager.machine:exit();return end
 records=records+1
 ring[(records-1)%ring_size+1]={kind=kind,line=line}
 -- Always preserve the first lookup and cache entry, even if a bad group
 -- produces more loop records than the rolling RAM ring can hold.
 if kind~='group_next' and kind~='descriptor'then print(line)end
end
for _,entry in ipairs({{0xff906050,'self_lookup'},{0xff906090,'main_lookup'},
 {0xff906110,'root_loaded'},{0xff906130,'lookup_cell'},{0xff906140,'lookup_result'},
 {0xff838790,'cache_begin'},{0xff8387f0,'group_next'},{0xff838810,'descriptor'},
 {0xff838a30,'cache_end'}})do
 local address,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'readonly original native Sonya root/cursor/cache input',function(at,data,mask)
  if at==address and cpu.PC.value==address+16 then record(kind,address,data,mask)end
 end)
end
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'readonly first real original global-cache write',function(at,data,mask)
 if busy or bad_frame or cpu.PC.value~=0xff838860 or not own()then return end
 bad_frame=frame
 record('first_global_write',at,data,mask)
 flush()
end)
emu.register_frame_done(function()
 frame=frame+1
 if (bad_frame and frame>=bad_frame+2)or frame>=108270 then
  flush()
  print(string.format('MK2_SUBZERO_CACHE_TRACE_STOP frame=%d first_bad=%d records=%d diagnostic_only=true writes=0 assistance=none',frame,bad_frame or-1,records))
  manager.machine:exit()
 end
end)
emu.register_stop(function()
 print(string.format('MK2_SUBZERO_CACHE_TRACE_RESULT frame=%d first_bad=%d records=%d diagnostic_only=true writes=0 assistance=none',frame,bad_frame or-1,records))
 for _,tap in ipairs(taps)do tap:remove()end
end)
dofile('mk2ks_sonya_p1_jax_jump_guard_ram_v4807.lua')
