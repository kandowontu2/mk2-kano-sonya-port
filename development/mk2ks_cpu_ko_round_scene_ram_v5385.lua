-- Bind read-only transport functions explicitly across MAME Lua sandboxes.
local f=assert(io.open('mk2ks_cpu_ko_round_scene_ram_v5382.lua','rb'))
local source=f:read('*a'):gsub('\r\n','\n');f:close()
local before="assert(load(source,'@entire_original_physical_scene_KO_round_window_RAM_only_5382','t',_ENV))()"
local after=[[once('local environment=setmetatable({}, {__index=_G})',
 'local environment=setmetatable({}, {__index=_G});environment.MK2KS_TOMB_RAM_SAVE=assert(MK2KS_TOMB_RAM_SAVE);environment.MK2KS_TOMB_RAM_PIXELS=assert(MK2KS_TOMB_RAM_PIXELS)')
assert(load(source,'@entire_original_physical_scene_KO_round_window_RAM_only_5385','t',_ENV))()]]
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1)..after..source:sub(at+#before)
assert(load(source,'@whole_original_KO_round_RAM_recorder_explicit_sandbox_binding','t',_ENV))()
