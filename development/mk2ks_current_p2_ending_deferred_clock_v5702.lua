-- Whole original clock observer, same callbacks; only parent path changes.
local path='mk2ks_p1_ending_deferred_clock_ram_v5258.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local old='mk2ks_p1_ending_deferred_display_ram_v5257.lua'
local a,b=source:find(old,1,true)
assert(a and not source:find(old,b+1,true),'One exact deferred observer parent')
source=source:sub(1,a-1)..'mk2ks_current_p2_ending_deferred_display_v5701.lua'..source:sub(b+1)
assert(load(source,'@'..path..'::whole_clock_P2_observer_parent','t',_ENV))()
