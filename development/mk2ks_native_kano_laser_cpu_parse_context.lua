-- Preserve first diagnostic; match final expanded controller by its real body.
local path='mk2ks_native_kano_laser_cpu_parse.lua'
local file=assert(io.open(path,'r'));local source=file:read('a');file:close()
local before="name and name:find('::kintaro_pressure_guard_inputs_and_RAM_sinks',1,true)"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1).."source:find('local function postending_join()',1,true) and source:find('local function sample(',1,true)"..source:sub(b+1)
assert(load(source,'@'..path..'::actual_full_controller_parse_context','t',_G))()
