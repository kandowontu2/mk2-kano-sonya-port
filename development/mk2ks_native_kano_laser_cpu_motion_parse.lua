local filename='mk2ks_native_kano_laser_cpu_parse.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local function once(before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
once("name and name:find('::kintaro_pressure_guard_inputs_and_RAM_sinks',1,true)",
 "source:find('local function postending_join()',1,true) and source:find('local function sample(',1,true)")
once("dofile('mk2ks_native_kano_laser_cpu_audio.lua')","dofile('mk2ks_native_kano_laser_cpu_motion_audio.lua')")
once(' local tag\n',[=[ local tag
 if name and name:find('::first_loss_ordinary_paid_Kano_continue',1,true)then
  print(string.format('MK2_CPU_PARSE_CONTROL bytes=%d hex=%s',#source,source:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
]=])
assert(load(source,'@'..filename..'::ordinary_motion_source_parser','t',_G))()
