-- Full unchanged19channel/nativeDAC/ROM window only for the true CPU mirror.
local filename='mk2ks_native_kano_laser_cpu_audio.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local before="once(\"dofile('mk2ks_native_kano_laser_burst.lua')\",\"dofile('mk2ks_native_kano_laser_cpu_campaign.lua')\")"
local after="once(\"dofile('mk2ks_native_kano_laser_burst.lua')\",\"dofile('mk2ks_native_kano_laser_cpu_continue.lua')\")"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..after..source:sub(b+1)
-- Scope the final base audio expansion without altering its native observations.
local native_load=load
local environment=setmetatable({load=function(text,name,mode,env)
 if name and name:find('::full_native_laser_audio',1,true)then
  local before='or frame<=1 or origin then return end'
  local a,b=assert(text:find(before,1,true));assert(not text:find(before,b+1,true))
  text=text:sub(1,a-1)..'or frame<=1 or origin or not _mk2_cpu_laser_started then return end'..text:sub(b+1)
 end
 return native_load(text,name,mode,env or _G)
end},{__index=_G})
-- Propagate scoped load when the audio adapter explicitly requests_G.
environment._G=environment
assert(native_load(source,'@'..filename..'::owned_CPU_mirror_origin_only','t',environment))()
