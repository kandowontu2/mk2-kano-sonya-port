-- Preserve6465/6467; add the whole original3395 passive contact/state observer.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
assert(load(read('mk2ks_current_cpu_bicycle_render_ram_v6465.lua'),'@whole6465_Bicycle_RAM_scene','t',_G))()
local source=read('mk2ks_native_cpu_audio_mobility_v3395.lua')
local dependency="dofile('mk2ks_physical_p2_cpu_square_trace_v3304.lua')"
local a,b=assert(source:find(dependency,1,true));assert(not source:find(dependency,b+1,true))
source=source:sub(1,a-1)..'-- Whole physical input/choice/Square chain already installed once.'..source:sub(b+1)
assert(not source:find('write_u',1,true)and not source:find(':snapshot',1,true)and not source:find('io.open',1,true))
assert(load(source,'@whole3395_passive_actual_Bicycle_contact_and_health_provenance','t',_G))()
