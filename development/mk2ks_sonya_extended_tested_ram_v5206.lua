-- Exact actually executed5081 uppercut timing, not the old9/6comment.
-- Down0..23, HP10..12; all game state and all other input policies untouched.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path='mk2ks_sonya_extended_prime_ram_v5205.lua'
local file=assert(io.open(path,'rb'));local text=file:read('a');file:close()
local needle='subzero=subzero:sub(1,pa-1)..prime_after..subzero:sub(pb+1)\n'
local first,last=text:find(needle,1,true)
assert(first and not text:find(needle,last+1,true),'Exact existing prime-only assembly')
local addition=[====[
local function tested_once(before,after)
 local ta,tb=subzero:find(before,1,true)
 assert(ta and not subzero:find(before,tb+1,true),'Unique original uppercut sequence timing')
 subzero=subzero:sub(1,ta-1)..after..subzero:sub(tb+1)
end
tested_once('if sz_leg and frame-sz_leg<12 then',
 "if sz_leg and frame-sz_leg<(sz_move=='uppercut' and 26 or 12) then")
tested_once('if age<9 then press(\'Down\')end',
 "if age<24 then press('Down')end")
tested_once('if age>=6 and age<9 then press(\'High Punch\')end',
 "if age>=10 and age<13 then press('High Punch')end")
]====]
text=text:sub(1,last)..addition..text:sub(last+1)
assert(load(text,'@'..path..'::SubZero_actual5081_Down24_HP10_physical_only_5185','t',_ENV))()

