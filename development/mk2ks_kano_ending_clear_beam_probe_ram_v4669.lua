-- Same earned cold campaign; bounded second-page clear/beam diagnosis only.
local file=assert(io.open('mk2ks_kano_ending_latch_probe_ram_v4599.lua','rb'))
local source=file:read('a');file:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true))
 assert(not source:find(before,last+1,true),'Unique bounded clear/beam adapter')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once('frame-origin<1095 or frame-origin>1145','frame-origin<1877 or frame-origin>1897')
once('frame-origin>=1095 and frame-origin<=1145','frame-origin>=1877 and frame-origin<=1897')
once('frame-origin<1100 or frame-origin>1140','frame-origin<1877 or frame-origin>1897')
once('assert(#taps==3)','assert(#taps==4)')
once('emu.register_frame(function()',[[
local buckets={}
taps[#taps+1]=p:install_write_tap(0,0x001fffff,'read-only actual second-page CPU clear beam timing',function(at,data,mask)
 if not origin or frame-origin<1877 or frame-origin>1897 then return end
 local beam,address,pc=p:read_u16(0xc00001d0),p:read_u16(0xc00001e0),cpu.PC.value
 local key=string.format('%d_%04X_%08X_%04X_%04X',beam,address,pc,data,mask)
 local bucket=buckets[key]
 if not bucket then
  bucket={count=0,beam=beam,address=address,pc=pc,value=data,mask=mask,first=at,last=at}
  buckets[key]=bucket
 end
 bucket.count=bucket.count+1;bucket.last=at
end)
emu.register_frame(function()
]])
once('emu.register_frame_done(function()',[[
emu.register_frame_done(function()
 if not origin or frame-origin<1877 or frame-origin>1897 then return end
 local keys={};for key in pairs(buckets)do keys[#keys+1]=key end;table.sort(keys)
 local total=0
 for _,key in ipairs(keys)do
  local b=buckets[key];total=total+b.count
  log('CPU_BUCKET',string.format('age=%d count=%d beam=%d dpyadr=%04X pc=%08X value=%04X mask=%04X first=%08X last=%08X',
   frame-origin,b.count,b.beam,b.address,b.pc,b.value,b.mask,b.first,b.last))
 end
 log('CPU_TOTAL',string.format('age=%d writes_observed=%d buckets=%d',frame-origin,total,#keys))
 buckets={}
end)
emu.register_frame_done(function()
]])
assert(load(source,'@whole4599_cold_policy_second_page_beam_RAM_only_4669','t',_ENV))()
