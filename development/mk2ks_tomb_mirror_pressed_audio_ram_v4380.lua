-- Exact4342 fifteen native taps and full PCM/guest RAM sinks, new driver chain.
local f=assert(io.open('mk2ks_tomb_mirror_audio_ram_v4342.lua','rb'))
local source=f:read('a');f:close()
local old="dofile('mk2ks_tomb_mirror_provenance_ram_v4341.lua')"
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1).."dofile('mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua')"..source:sub(last+1)
assert(not source:find('set_value(',1,true)and not source:find('write_u%d+'))
assert(load(source,'@complete4342_native_pressed_mirror_audio_4380','t',_ENV))()
