-- Keep the original controller and snapshot extension in the same Lua ENV.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_reptile_ram_v5480.lua','rb'))
local source=f:read('*a');f:close()
local before="dofile(root..'/mk2ks_current_reptile_ram_v5470.lua')"
local after=[=[
local controller_file=assert(io.open(root..'/mk2ks_current_reptile_ram_v5470.lua','rb'))
local controller_source=controller_file:read('*a');controller_file:close()
assert(load(controller_source,'@whole5470_controller_same_snapshot_environment','t',_ENV))()
]=]
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@whole5480_passive_scene_observer_shared_controller_ENV','t',_ENV))()
