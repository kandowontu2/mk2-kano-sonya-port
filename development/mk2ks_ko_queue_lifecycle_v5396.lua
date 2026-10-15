-- Original cold physical CPU driver, no old body/GFX/RGB transport callback.
-- Only read-only queue/reset observations are added; all native choices remain native.
local file=assert(io.open('mk2ks_cpu_square_shadow_v5341.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local before="assert(load(source,'@CPU_Square_original_input_chain_RAM_body_shadow_v5341','t',_G))()"
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
local after=[=[
change("assert(load(prefix..observer..callback..cleanup,'@isolated_original_body_shadow_CPU_observer_v5328','t',_G))()",
 "assert(load(prefix..cleanup,'@original_physical_CPU_no_old_media_observer_v5396','t',_G))()")
assert(load(source,'@CPU_Square_original_input_chain_without_unused_media_observer_v5396','t',_G))()
]=]
source=source:sub(1,at-1)..after..source:sub(at+#before)
assert(load(source,'@original_CPU_readonly_queue_lifecycle_v5396','t',_G))()
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,event=0,0
local taps={}
local function active()return frame>=3198 and frame<=3220 end
local function log(kind,text)
 event=event+1
 print(string.format('MK2_QUEUE_LIFECYCLE_%s frame=%d event=%d writes=0 assistance=none mode=%d p1=%08X p2=%08X queue=%08X b13=%08X b14=%08X b8=%08X a1=%08X %s',
  kind,frame,event,p:read_u16(0x010601d0),p:read_u32(0x01060220),p:read_u32(0x01060df0),p:read_u32(0x0101f700),
  cpu.B13.value,cpu.B14.value,cpu.B8.value,cpu.A1.value,text or''))
end
emu.register_frame(function()frame=frame+1;if active()then log('PRE')end end)
emu.register_frame_done(function()
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  print('MK2_QUEUE_LIFECYCLE_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02x',c:byte())end))
 end
 if active()then log('POST')end
end)
for _,address in ipairs({0xff818e30,0xff818e80,0xff83f410,0xff83f4c0,0xff808310,0xff8083b0,
 0xff808780,0xff808900,0xff808930,0xff808960,0xff808a40,0xff808b00,0xff808b10,0xff808b20,
 0xff804410,0xff804430,0xff8045d0,0xff8046b0})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'readonly native round queue lifecycle',function(at,data,mask)
  if active()and at==address and cpu.PC.value==address+16 then
   log('CODE',string.format('at=%08X pc=%08X opcode=%04X mask=%04X',at,cpu.PC.value,data&0xffff,mask))
  end
 end)
end
for _,address in ipairs({0x0101f700,0x01060220,0x01060df0})do
 taps[#taps+1]=p:install_write_tap(address,address+31,'readonly actual native queue/actor reset writer',function(at,data,mask)
  if active()and at==address then
   log('STORE',string.format('at=%08X before=%08X after=%08X mask=%08X pc=%08X',at,p:read_u32(address),data,mask,cpu.PC.value))
  end
 end)
end
emu.register_stop(function()log('STOP');for _,tap in ipairs(taps)do tap:remove()end end)
