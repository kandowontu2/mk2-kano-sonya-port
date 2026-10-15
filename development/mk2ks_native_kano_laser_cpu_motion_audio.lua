local filename='mk2ks_native_kano_laser_cpu_continue_audio.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local before='mk2ks_native_kano_laser_cpu_continue.lua'
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..'mk2ks_native_kano_laser_cpu_motion.lua'..source:sub(b+1)
assert(load(source,'@'..filename..'::ordinary_motion_then_released_CPU_mirror','t',_G))()
