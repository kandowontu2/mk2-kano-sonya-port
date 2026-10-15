-- Same natural-opponent observer plus both genuine startup entry taps.
local file=assert(io.open('mk2ks_native_selector_cpu_projectile_pcm_natural.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local before="io.open('mk2ks_native_selector_cpu_projectile_pcm.lua','rb')"
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1).."io.open('mk2ks_native_selector_cpu_projectile_pcm_startup_base.lua','rb')"..source:sub(last+1)
assert(load(source,'@whole_current_natural_CPU_startup_PCM','t',_G))()
