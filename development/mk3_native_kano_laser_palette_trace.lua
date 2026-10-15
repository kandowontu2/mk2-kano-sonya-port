-- Successor original reference: unchanged physical commands; continuous
-- native palette/ramp observations. No guest-memory/register/state writes.
local filename='mk3_native_secondary_kano_source_distance.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local boundary="assert(load(source,'@'..filename..'::original_source_distance'))()"
local instrumentation=[==[
local additions={
 {"  for _,where in ipairs({0xff9b5cd0", [=[
  for _,where in ipairs({0xff92b890,0xff92b990,0xff92bb80,0xff925320,0xff925460})do
   local at=where
   taps[#taps+1]=p:install_read_tap(at,at+15,'passive source laser palette lifecycle',function(address)
    if address==at and cpu.PC.value==at+16 and start and frame-start<=150 then
     log('RAMP_CODE',string.format('age=%d at=%08X a0=%08X a1=%08X a5=%08X a6=%08X a7=%08X a8=%08X a9=%08X a10=%08X a11=%08X a13=%08X',frame-start,at,cpu.A0.value,cpu.A1.value,cpu.A5.value,cpu.A6.value,cpu.A7.value,cpu.A8.value,cpu.A9.value,cpu.A10.value,cpu.A11.value,cpu.A13.value))
    end
   end)
  end
  taps[#taps+1]=p:install_write_tap(0x01880000,0x018fffff,'passive actual victim palette transfer',function(at,data,mask)
   if not start or frame-start>150 then return end
   local victim=p:read_u32(0x01061560);if not valid(victim)then return end
   local bank=p:read_u16(victim+0x140)&0x7f00
   local first=0x01880000+bank*16
   if at>=first and at<first+64*16 then
    log('RAMP_WRITE',string.format('age=%d at=%08X bank=%04X pen=%d data=%04X mask=%04X pc=%08X job=%08X',frame-start,at,bank,(at-first)//16,data&0xffff,mask,cpu.PC.value,cpu.A13.value))
   end
  end)
  for _,where in ipairs({0xff9b5cd0]=]},
 {"  geometry('FIELD')",[=[
  geometry('FIELD')
  if frame-start<=150 then
   for side,actor in ipairs({a,b})do
    local bank=p:read_u16(actor+0x140)&0x7f00;local colors={}
    for color=0,63 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01880000+(bank+color)*16))end
    log('PALETTE_FIELD',string.format('age=%d side=%d actor=%08X pose=%08X bank=%04X colors=%s',frame-start,side,actor,p:read_u32(actor+0x1d0),bank,table.concat(colors,',')))
   end
  end]=]},
 {'{1,24,60,120,180,300,450}', '{1,12,20,24,26,32,38,44,50,56,60,62,68,74,90,120,180,300,450}'}
}
for _,pair in ipairs(additions)do
 local at=assert(source:find(pair[1],1,true));assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::laser_palette_trace'))()
]==]
local at=assert(source:find(boundary,1,true));assert(not source:find(boundary,at+#boundary,true))
source=source:sub(1,at-1)..instrumentation..source:sub(at+#boundary)
assert(load(source,'@'..filename..'::laser_palette_trace_wrapper'))()
