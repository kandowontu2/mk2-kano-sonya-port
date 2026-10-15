-- Read-only donor callees: action setup, launch voice helper and body flag.
local f=assert(io.open('mk3_cannonball_startup_source_v6622.lua','rb'));local source=f:read('*a');f:close()
local before="d.execution_state='run'"
local after=[[
d:command('dasm '..prefix..'startup_helpers.asm,FF9E8500,300')
d:command('dasm '..prefix..'compact_body.asm,FF959C00,400')
d.execution_state='run'
]]
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..after..source:sub(last+1)
source=source:gsub('audit_v6623_donor_ball_startup_source/','audit_v6626_donor_ball_startup_helpers/')
assert(load(source,'@mk3_cannonball_startup_source_v6622.lua::read_only_native_helpers'))()
