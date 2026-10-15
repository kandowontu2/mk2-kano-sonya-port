-- Unchanged physical selection, two earned KOs, stock commands and cleanup.
dofile('mk2ks_stock_extended_earned_ram_v3958.lua')
-- The entire source-qualified15tap/14channel/PCM/DAC/ROM observer is kept.
local entry=assert(tonumber(os.getenv('MK2KS_AUDIO_ENTRY')))
local killer=assert(tonumber(os.getenv('MK2KS_AUDIO_KILLER_ID')))
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local victim=assert(({kano=17,sonya=18})[os.getenv('MK2KS_TEST_FIGHTER')])
local file=assert(io.open('mk2ks_current_tomb_winner_mix_observer_v5779.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique complete stock audio scope adapter')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin and frame<=origin+750 end')
replace('0xff8bdfe0,0xff8bdfef',string.format('0x%x,0x%x',entry,entry+15))
replace('at~=0xff8bdfe0',string.format('at~=0x%x',entry))
replace("p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')])",
 string.format('p:read_u16(a+0x1f0)~=%d',killer))
replace('origin=frame;log(\'BEGIN\'',
 string.format("local va=p:read_u32(0x%x);local vm=p:read_u32(0x%x);if not valid(va)or not valid(vm)or p:read_u32(vm+0xc0)~=va or p:read_u16(va+0x1f0)~=%d or p:read_u16(0x%x)~=0 then return end\n origin=frame;log('BEGIN'",
 side==1 and 0x01060220 or 0x01060df0,side==1 and 0x01060260 or 0x01060e30,victim,
 side==1 and 0x010602f0 or 0x01060ec0))
replace("assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin and frame==origin+751,'Whole stock finisher750field action/completion/continue audio and terminal ROM checks')")
assert(load(source,'@whole_native_stock_finisher_audio_v6221','t',_ENV))()
