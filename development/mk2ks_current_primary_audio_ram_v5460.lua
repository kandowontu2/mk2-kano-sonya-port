-- Preserve whole qualified native channels/owners/sound/tail observer.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_natural_mirror_audio_ram_v3708.lua','rb'))
local source=f:read('*a');f:close()
local before="dofile(root..'/mk2ks_natural_mirror_no_raster_v3712.lua')"
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1).."dofile(root..'/mk2ks_current_primary_controller_ram_v5460.lua')"..source:sub(last+1)
assert(load(source,'@original_complete_native_audio_observer_only_controller_RAM_sinks','t',_ENV))()
