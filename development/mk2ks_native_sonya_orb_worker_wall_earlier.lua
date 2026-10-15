-- Preserve the actual expired-window trial; only physical retreat starts
--20fields earlier. Game parser, timing, coordinates and health untouched.
local filename='mk2ks_native_sonya_orb_worker_wall.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local old='frame-finish>=65';local at=assert(source:find(old,1,true))
assert(not source:find(old,at+#old,true))
source=source:sub(1,at-1)..'frame-finish>=45'..source:sub(at+#old)
assert(load(source,'@'..filename..'::earlier_physical_retreat'))()
