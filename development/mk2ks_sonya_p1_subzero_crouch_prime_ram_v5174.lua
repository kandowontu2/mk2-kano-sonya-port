-- Correct only ordinary anti-air input timing; keep native game untouched.
-- The real5084 basic-move test needs Down preparation, then HP at6..8.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path='mk2ks_sonya_p1_subzero_guard_ram_v5159.lua'
local file=assert(io.open(path,'rb'));local text=file:read('a');file:close()
local needle='subzero=subzero:sub(1,a-1)..after..subzero:sub(b+1)\n'
local first,last=text:find(needle,1,true)
assert(first and not text:find(needle,last+1,true),'Exact existing freeze-guard assembly')
local addition=[===[
local prime_before="reason='anti_air_attempt';press('High Punch');sz_upper=frame"
local prime_after="reason='anti_air_attempt';sz_move='uppercut';sz_leg=frame;sz_upper=frame"
local pa,pb=subzero:find(prime_before,1,true)
assert(pa and not subzero:find(prime_before,pb+1,true),'Exact ordinary simultaneous anti-air HP attempt')
-- Down is already pressed on this setup field. The unchanged original
-- uppercut_sequence branch holds Down9fields and presses HP at6..8.
subzero=subzero:sub(1,pa-1)..prime_after..subzero:sub(pb+1)
]===]
text=text:sub(1,last)..addition..text:sub(last+1)
assert(load(text,'@'..path..'::SubZero_physical_crouch_prime_only_5174','t',_ENV))()
