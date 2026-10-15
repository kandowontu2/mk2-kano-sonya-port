-- Preserve6422's executed failure; supply its extracted observer's read helper.
local file=assert(io.open('mk2ks_current_cpu_ring_miss_audio_v6422.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local before="assert(load(source,'@whole_native_current_missed_Ring_audio_RAM_only','t',_G))()"
local after="assert(load(source,'@whole_native_current_missed_Ring_audio_RAM_only','t',setmetatable({read=read},{__index=_G})))()"
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@whole6422_miss_audio_observer_with_local_read_dependency','t',_G))()
