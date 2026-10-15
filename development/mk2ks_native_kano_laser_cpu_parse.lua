-- Actual installed Lua parser; compile complete expansions, run no callbacks.
local actual=manager.machine
local noop=function()return {remove=function()end}end
manager={machine={devices={[':maincpu']={spaces={program={install_read_tap=noop,install_write_tap=noop}},state={}},
 [':screen']={},[':dcs:dcs']={spaces={data={}},state={}}},ioport={ports={[':IN0']={fields={}},[':IN1']={fields={}}}}}}
emu={register_frame=function()end,register_frame_done=function()end,register_sound_update=function()end,register_stop=function()end}
local native_load=load
local parsed={}
load=function(source,name,mode,environment)
 local fn,err=native_load(source,name,mode,environment or _G);assert(fn,err)
 local tag
 if name and name:find('::kintaro_pressure_guard_inputs_and_RAM_sinks',1,true)then tag='CAMPAIGN'
 elseif name and name:find('::full_native_laser_audio',1,true)then tag='AUDIO'end
 if tag then
  assert(not parsed[tag]);parsed[tag]=true
  print(string.format('MK2_CPU_PARSE_%s bytes=%d hex=%s',tag,#source,source:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  return function()end
 end
 return fn
end
dofile('mk2ks_native_kano_laser_cpu_audio.lua')
assert(parsed.CAMPAIGN and parsed.AUDIO)
print('MK2_CPU_PARSE_RESULT gameplay_callbacks_executed=0 guest_writes=0')
actual:exit()
