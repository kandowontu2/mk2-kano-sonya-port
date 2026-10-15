-- Complete original2062 CPU/FIFO/DMA/shift/scanout observer, unchanged reads.
-- Original3624 RAM-only sinks; only its driver target becomes true mirrors.
local handle=assert(io.open('mk2ks_native_tomb_ram_v3624.lua','rb'))
local source=handle:read('a');handle:close()
local old="dofile('mk2ks_current_stage_provenance_v3595.lua')"
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1).."dofile('mk2ks_tomb_mirror_provenance_ram_v4341.lua')"..source:sub(last+1)
assert(not source:find(':write_',1,true)and not source:find('set_value',1,true))
assert(load(source,'@complete3624_native_mirror_scene_RAM_sinks_4359','t',_ENV))()
