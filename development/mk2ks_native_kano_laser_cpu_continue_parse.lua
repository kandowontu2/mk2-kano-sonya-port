-- Same actual installed-parser diagnostic, first-loss physical cutover.
local filename='mk2ks_native_kano_laser_cpu_parse.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local function once(before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
once("name and name:find('::kintaro_pressure_guard_inputs_and_RAM_sinks',1,true)",
 "source:find('local function postending_join()',1,true) and source:find('local function sample(',1,true)")
once("dofile('mk2ks_native_kano_laser_cpu_audio.lua')","dofile('mk2ks_native_kano_laser_cpu_continue_audio.lua')")
assert(load(source,'@'..filename..'::first_loss_continue_physical_parser','t',_G))()
