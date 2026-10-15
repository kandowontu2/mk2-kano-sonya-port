-- Read-only version3660 observer with CPU-fetch qualification added.
-- ROM dumps can read these addresses without executing the instructions.
local f=assert(io.open('mk2ks_current_tomb_audio_ram_v3660.lua','rb'))
local source=f:read('*a');f:close()
local count
source,count=source:gsub('if at==0xff8bdfe0 and not origin then',
 'if at==0xff8bdfe0 and cpu.PC.value==at+16 and frame>1 and not origin then')
assert(count==1)
source,count=source:gsub('if at~=entry or not active%(%)then return end',
 'if at~=entry or cpu.PC.value~=at+16 or not active()then return end')
assert(count==1)
assert(load(source,'@mk2ks_current_tomb_audio_ram_v3660_cpu_fetch_qualified'))()
