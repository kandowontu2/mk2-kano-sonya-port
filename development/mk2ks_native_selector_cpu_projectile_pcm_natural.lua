-- Preserve the failed mirror-only observer and original physical controller.
-- Observe the real first live CPU opponent; do not prescribe its identity.
local file=assert(io.open('mk2ks_native_selector_cpu_projectile_pcm.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('and p:read_u16(0x01060e50)==17 then','and p:read_u16(0x01060e50)<=18 then')
replace('p:read_u16(a+0x1f0)==17 and p:read_u32(m+0xc0)==a then',
 'p:read_u16(a+0x1f0)==p:read_u16(0x01060e50) and p:read_u32(m+0xc0)==a then')
replace("origin=%d a8=%08X a13=%08X id=17',origin,a,m)",
 "origin=%d a8=%08X a13=%08X id=%d',origin,a,m,p:read_u16(a+0x1f0))")
assert(load(source,'@whole_original_current_PCM_actual_natural_opponent','t',_G))()
