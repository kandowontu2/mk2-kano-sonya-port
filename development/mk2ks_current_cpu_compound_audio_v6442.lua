-- Whole original5324 physical match and native5779 RAM-only sound observer.
local function read(name)
 local file=assert(io.open(name,'rb'));local source=file:read('a'):gsub('\r\n','\n');file:close();return source
end
local physical=read('mk2ks_current_cpu_ring_miss_audio_v6422.lua')
local stop=assert(physical:find("local source=read('mk2ks_current_cpu_ring_audio_v6383.lua')",1,true))
assert(load(physical:sub(1,stop-1),'@whole_original5324_physical_RAM_driver','t',_G))()
local source=read('mk2ks_current_cpu_ring_mirror_audio_v6393.lua')
local first=assert(source:find("local source=read('mk2ks_current_tomb_winner_mix_observer_v5779.lua')",1,true))
source=source:sub(first)
local before='p:read_u16(0x01060280)==18 and p:read_u16(0x01060e50)==18'
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..'p:read_u16(0x01060280)==17 and p:read_u16(0x01060e50)==18'..source:sub(b+1)
-- The extracted observer deliberately receives its read helper explicitly.
assert(load(source,'@whole_native_true_Kano_Sonya_compound_match_audio','t',setmetatable({read=read},{__index=_G})))()
