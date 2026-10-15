-- Existing physical earned freeze/shatter/next-CPU controls, unchanged.
dofile('mk2ks_native_subzero_legs_nextmatch_v5000.lua')
-- Preserve the entire native audio observer; change only origin/window scope.
local file=assert(io.open('mk2ks_current_tomb_winner_mix_observer_v5779.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique complete audio observer adapter')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin~=nil end')
replace('0xff8bdfe0,0xff8bdfef','0xff8c2320,0xff8c232f')
replace('at~=0xff8bdfe0','at~=0xff8c2320')
replace("os.getenv('MK2KS_STAGE_WINNER')","os.getenv('MK2KS_TEST_FIGHTER')")
replace("assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin and frame-origin>=2000 and frame-origin<2100,'Whole earned freeze/shatter and next-CPU terminal ROM checks')")
assert(load(source,'@whole_native_Subzero_audio_v6212','t',_ENV))()
