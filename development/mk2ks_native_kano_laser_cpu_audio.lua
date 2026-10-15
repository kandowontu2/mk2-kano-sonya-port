-- Same complete original audio/DAC/ROM observers; naturally chosen CPU origin.
local path='mk2ks_native_kano_laser_audio.lua'
local file=assert(io.open(path,'r'));local source=file:read('a'):gsub('\r\n','\n');file:close()
local function once(before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
once("dofile('mk2ks_native_kano_laser_burst.lua')","dofile('mk2ks_native_kano_laser_cpu_campaign.lua')")
local count;source,count=source:gsub('if frame>=2800 then','if _mk2_cpu_laser_started and frame<=_mk2_cpu_laser_started+750 then');assert(count==2)
assert(load(source,'@'..path..'::same_full_audio_natural_CPU_laser','t',_G))()
