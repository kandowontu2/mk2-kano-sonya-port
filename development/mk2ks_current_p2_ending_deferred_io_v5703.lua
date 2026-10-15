-- Whole actual display IO observer; only declared clock parent changes.
local path='mk2ks_p1_ending_deferred_io_ram_v5259.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local old='mk2ks_p1_ending_deferred_clock_ram_v5258.lua'
local a,b=source:find(old,1,true)
assert(a and not source:find(old,b+1,true),'One exact deferred clock parent')
source=source:sub(1,a-1)..'mk2ks_current_p2_ending_deferred_clock_v5702.lua'..source:sub(b+1)
assert(load(source,'@'..path..'::whole_IO_P2_clock_parent','t',_ENV))()
