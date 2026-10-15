-- Read-only actual DMA packets at the three reference scene fields.
local file=assert(io.open('mk2ks_native_subzero_reference_pcm_v4961.lua','rb'))
local source=file:read('a');file:close()
local first,last=source:find('local pcm_index=0',1,true)
assert(first and not source:find('local pcm_index=0',last+1,true))
local observer=[=[local pcm_index=0
taps[#taps+1]=p:install_write_tap(0x01a80010,0x01a8001f,'readonly actual native ice DMA',function(at,data,mask)
 if at~=0x01a80010 or data&0x8000==0 or not deep then return end
 if not(frame-deep==100 or (fracture and frame-fracture==20)or (wrap and frame-wrap==150))then return end
 local registers={}
 for _,i in ipairs({0,2,3,4,5,6,7,8,9,10,11,12,13,14,15})do registers[i]=p:read_u16(0x01a80000+i*16)end
 log('DMA',string.format('command=%04X mask=%04X source=%08X x=%d y=%d width=%d height=%d palette=%04X color=%04X xscale=%04X yscale=%04X lrskip=%04X pc=%08X',
  data&0xffff,mask,registers[2]|(registers[3]<<16),registers[4],registers[5],registers[6],registers[7],registers[8],registers[9],registers[10],registers[11],registers[0],cpu.PC.value))
end)
]=]
source=source:sub(1,first-1)..observer..source:sub(last+1)
assert(load(source,'@actual_native_ice_DMA_and_PCM_v4965','t',_ENV))()
