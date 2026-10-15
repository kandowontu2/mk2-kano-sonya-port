-- Whole original nineteen-channel observer, followed by whole original CPU wrapper.
-- Only physical human inputs; CPU identity, choice, health and RNG remain native.
local file=assert(io.open('mk2ks_native_kano_laser_special_shadow.lua','rb'))
local source=file:read('*a');file:close()
local marker='-- Passive current nineteen-channel/private-finisher-pool observer only.'
local at=assert(source:find(marker,1,true));assert(not source:find(marker,at+1,true))
assert(load(source:sub(at),'@entire_original_nineteen_channel_observer','t',_G))()
local file=assert(io.open('mk2ks_cpu_choke_shadow_v5328.lua','rb'))
local source=file:read('*a');file:close()
assert(load(source,'@entire_original_cpu_choke_wrapper','t',_G))()
