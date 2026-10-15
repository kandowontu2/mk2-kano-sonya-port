-- Same ordinary two-human Freeze command; victim holds physical Block.
local path='mk2ks_normal_subzero_freeze_v5031.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local before="   if age>=90 and age<93 then press(winner_side,'Down')end"
local a,b=source:find(before,1,true)
assert(a and not source:find(before,b+1,true),'One original ordinary input timeline')
local after="   if age>=70 and age<300 then press(side,'Block')end\n"..before
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@'..path..'::only_physical_victim_Block_added','t',_ENV))()
