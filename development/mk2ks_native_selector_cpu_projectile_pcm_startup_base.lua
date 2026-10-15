-- Retain every original current19-channel/PCM/DAC/ROM observer.
-- Arm on either actual owned first-round projectile entry, before its cue.
local file=assert(io.open('mk2ks_native_selector_cpu_projectile_pcm.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace("replace('0xff8bdfe0,0xff8bdfef','0xffffb000,0xffffb00f')",
 "replace('0xff8bdfe0,0xff8bdfef','0xffffb000,0xffffb40f')")
replace("replace('at~=0xff8bdfe0','at~=0xffffb000')",
 "replace('at~=0xff8bdfe0','(at~=0xffffb000 and at~=0xffffb400)')")
replace("'p:read_u16(a+0x1f0)~=17')",
 "'(p:read_u16(a+0x1f0)~=17 and p:read_u16(a+0x1f0)~=18)')")
assert(load(source,'@whole_original_PCM_both_owned_startup_entries','t',_G))()
