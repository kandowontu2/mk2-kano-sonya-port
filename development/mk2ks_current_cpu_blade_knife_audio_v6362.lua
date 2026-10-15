-- Original physical inputs and allocation observer; no gameplay writes.
dofile('mk2ks_current_cpu_blade_allocation_v6340.lua')
-- Reuse the complete native audio observer, including all channels, DAC,
-- original queue/packet/DSP taps and startup/terminal sound-ROM inventories.
local file=assert(io.open('mk2ks_current_tomb_winner_mix_observer_v5779.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique complete audio scope adapter')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin and frame<=origin+639 end')
replace('0xff8bdfe0,0xff8bdfef','0xfff8cc00,0xfff8cc0f')
replace('at~=0xff8bdfe0','at~=0xfff8cc00')
replace("p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')])",
 'p:read_u16(a+0x1f0)~=17')
replace("origin=frame;log('BEGIN'",
 "if p:read_u32(0x01060df0)~=a or p:read_u32(0x01060e30)~=m or p:read_u16(0x01060e50)~=17 or p:read_u16(0x01060dc0)~=0 or p:read_u16(0x010601d0)~=2 then return end\n origin=frame;log('BEGIN'")
replace("assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin==1871 and frame==3615,'Both complete sound ROM checks and original physical native terminal; audio window1871..2510')")
assert(load(source,'@whole_native_CPU_blade_knife_audio_v6362','t',_ENV))()
