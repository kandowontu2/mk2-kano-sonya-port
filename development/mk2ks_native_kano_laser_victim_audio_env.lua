-- Keep the failed wrapper; correct only its optional Lua load environment.
local name='mk2ks_native_kano_laser_victim_audio.lua'
local file=assert(io.open(name,'r'));local source=file:read('a');file:close()
local before='return native_load(source,name,mode,environment)'
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..'return native_load(source,name,mode,environment or _G)'..source:sub(last+1)
assert(load(source,'@'..name..'::explicit_environment_successor','t',_G))()
