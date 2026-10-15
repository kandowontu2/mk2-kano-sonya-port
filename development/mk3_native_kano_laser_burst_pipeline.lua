-- Original, physically earned laser. Observe the real flash/render pipeline.
-- Only passive taps, field reads, and full-raster capture ages are added.
local filename='mk3_native_secondary_kano_source_distance.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local boundary="assert(load(source,'@'..filename..'::original_source_distance'))()"
local instrumentation=[==[
local additions={
 {"  for _,where in ipairs({0xff9b5cd0", [=[
  for _,where in ipairs({0xffaa2880,0xffaa2990,0xffaa2a20,0xffaa2b20})do
   local at=where
   taps[#taps+1]=p:install_read_tap(at,at+15,'passive original burst helpers',function(address)
    if address==at and cpu.PC.value==at+16 and start and frame-start<=240 then
     log('BURST_CODE',string.format('age=%d at=%08X job=%08X actor=%08X a9=%08X a11=%08X bg=%04X palette=%04X y=%04X',frame-start,at,cpu.A13.value,cpu.A8.value,cpu.A9.value,cpu.A11.value,p:read_u16(0x0105d7e0),p:read_u16(0x0105d820),p:read_u16(0x0105d8a0)))
    end
   end)
  end
  for _,where in ipairs({0xff9b5cd0]=]},
 {"  geometry('FIELD')",[=[
  geometry('FIELD')
  if frame-start<=240 then
   log('BURST_FIELD',string.format('age=%d bg=%04X palette=%04X y=%04X',frame-start,p:read_u16(0x0105d7e0),p:read_u16(0x0105d820),p:read_u16(0x0105d8a0)))
  end]=]},
 {'{1,24,60,120,180,300,450}', '{1,24,60,120,162,164,165,166,167,168,169,170,171,172,173,174,175,176,177,180,196,217,218,219,220,240,300,450}'}
}
for _,pair in ipairs(additions)do
 local at=assert(source:find(pair[1],1,true));assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::burst_pipeline'))()
]==]
local at=assert(source:find(boundary,1,true));assert(not source:find(boundary,at+#boundary,true))
source=source:sub(1,at-1)..instrumentation..source:sub(at+#boundary)
assert(load(source,'@'..filename..'::burst_pipeline_wrapper'))()
