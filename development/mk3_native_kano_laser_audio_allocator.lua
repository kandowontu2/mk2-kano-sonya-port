-- Original laser, exactly the same earned physical controller and rasters.
-- Passive sound-record/allocator/packet/timer reads only; no audio injection.
local filename='mk3_native_kano_laser_burst_pipeline.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local boundary="assert(load(source,'@'..filename..'::burst_pipeline'))()"
local instrumentation=[==[
local additions={
 {"  for _,where in ipairs({0xffaa2880",[=[
  local function sound_slots()
   local slots={}
   for channel=0,4 do
    local at=0x010b8ba0+channel*64
    slots[#slots+1]=string.format('%04X,%04X,%08X',p:read_u16(at),p:read_u16(at+16),p:read_u32(at+32))
   end
   return table.concat(slots,';')
  end
  for _,where in ipairs({0xffaa8ca0,0xffaa4c80,0xffaa6c00,0xffaa6d00,0xffaa6e00,0xffaa7900,0xffaa87c0,0xffaa80d0})do
   local at=where
   taps[#taps+1]=p:install_read_tap(at,at+15,'passive original laser sound allocation',function(address)
    if address~=at or cpu.PC.value~=at+16 or not start or frame-start>300 then return end
    local actor=cpu.A8.value;local id=valid(actor)and p:read_u16(actor+0x1f0)or -1
    local flag=valid(actor)and p:read_u16(actor+0x1c0)or -1
    local record=(at==0xffaa6e00 and cpu.A0.value>=0xff800000)and p:read_u32(cpu.A0.value)or 0
    log('AUDIO_CODE',string.format('age=%d at=%08X actor=%08X id=%d flag=%d job=%08X a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X a5=%08X a14=%08X record=%08X slots=%s',frame-start,at,actor,id,flag,cpu.A13.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A4.value,cpu.A5.value,cpu.A14.value,record,sound_slots()))
   end)
  end
  for _,where in ipairs({0xffaa2880]=]}
}
for _,pair in ipairs(additions)do
 local at=assert(source:find(pair[1],1,true));assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::audio_allocator'))()
]==]
local at=assert(source:find(boundary,1,true));assert(not source:find(boundary,at+#boundary,true))
source=source:sub(1,at-1)..instrumentation..source:sub(at+#boundary)
assert(load(source,'@'..filename..'::audio_allocator_wrapper'))()
