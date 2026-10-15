-- Extend only the passive owned-GFX interval to the actual corrected head art.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_reptile_ram_v5467.lua','rb'))
local source=f:read('*a');f:close()
local before="assert(load(observer,'@entire_original904_native_death_FIFO_DMA_only_RAM_file_sinks','t',_ENV))()"
local after=[=[
local donor=assert(manager.machine.memory.regions[':mk3data'])
local count=0
for i=0,3 do count=count|(donor:read_u8(0x160008+i)<<(i*8))end
assert(count>=49228 and count<0x1c000)
local upper=string.format('0x%08x',(0x1ec0000+count)*8)
local occurrences=0
observer=observer:gsub('0x0f660260',function()occurrences=occurrences+1;return upper end)
assert(occurrences==2,'Only the two passive owned-art FIFO/DMA interval bounds change')
observer=replace_once(observer,'local count=0xc04c -- Exact v894 packed allocation, including alignment.',
 'local count='..count..' -- Whole actual corrected native-death GFX allocation.')
assert(load(observer,'@entire_original904_native_death_FIFO_DMA_current_owned_GFX_RAM_span','t',_ENV))()
]=]
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@whole5467_RAM_observer_only_current_corrected_head_GFX_span','t',_ENV))()
