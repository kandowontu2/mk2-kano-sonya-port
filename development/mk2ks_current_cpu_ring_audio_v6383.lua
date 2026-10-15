-- The complete qualified physical Ring driver, without its visual collector.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local physical=read('mk2ks_current_cpu_ring_render_ram_v6375.lua')
local stop=assert(physical:find("local source=read('mk2ks_physical_p2_cpu_ring_display_v2014.lua')",1,true))
assert(load(physical:sub(1,stop-1),'@whole_qualified_physical_ring_RAM_driver','t',_G))()
-- Retain every original passive audio, DAC, packet, ADSP, precise-channel
-- and startup/terminal sound-ROM observation. No native state is written.
local source=read('mk2ks_current_tomb_winner_mix_observer_v5779.lua')
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin and frame<=origin+639 end')
replace('0xff8bdfe0,0xff8bdfef','0xffffb400,0xffffb40f')
replace('at~=0xff8bdfe0','at~=0xffffb400')
replace("p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')])",
 'p:read_u16(a+0x1f0)~=18')
replace("origin=frame;log('BEGIN'",
 "if p:read_u32(0x01060df0)~=a or p:read_u32(0x01060e30)~=m or p:read_u16(0x01060e50)~=18 or p:read_u16(0x01060dc0)~=0 or p:read_u16(0x010601d0)~=2 then return end\n origin=frame;log('BEGIN'")
replace("assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin==2077 and frame==3623,'Both complete sound ROM checks and unchanged physical Ring terminal; audio2077..2716')")
assert(load(source,'@whole_native_CPU_ring_audio_v6383','t',_G))()
