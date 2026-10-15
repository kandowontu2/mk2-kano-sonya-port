-- Preserve the actually executed6706 lexical failure. Correct its one Lua
-- string-concatenation operator; no controller or observation window changes.
local f=assert(io.open('mk2ks_launch_ground_io_v6706.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local before="'extra..'+string.format"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1).."'extra..'..string.format"..source:sub(b+1)
assert(load(source,'@whole_ground_IO_observer_correct_Lua_concatenation','t',_G))()
