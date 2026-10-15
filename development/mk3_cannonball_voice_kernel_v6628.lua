-- Read-only genuine donor launch voice routing, typed table and sound queue.
local f=assert(io.open('mk3_cannonball_startup_source_v6622.lua','rb'));local source=f:read('*a');f:close()
local before="d.execution_state='run'"
local after=[[
d:command('dasm '..prefix..'voice_kernel.asm,FFAA8A00,E00')
d:command('dasm '..prefix..'sound_queue.asm,FFAA6C00,500')
d:command('dasm '..prefix..'startup_helpers.asm,FF9E8500,190')
d.execution_state='run'
]]
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..after..source:sub(last+1)
source=source:gsub('audit_v6623_donor_ball_startup_source/','audit_v6629_donor_ball_voice_kernel/')
assert(load(source,'@mk3_cannonball_startup_source_v6622.lua::native_voice_kernel'))()
