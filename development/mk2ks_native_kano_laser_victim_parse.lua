-- Actual candidate Lua compiler; wrapper expansion only, no gameplay callbacks.
local actual_machine=manager.machine
manager={machine={devices={[':maincpu']={spaces={program={}},state={}}}}}
emu={register_frame=function()end,register_sound_update=function()end,register_stop=function()end}
local native_load=load
local parsed={}
load=function(source,name,mode,environment)
 local compiled,err=native_load(source,name,mode,environment or _G);assert(compiled,err)
 local tag
 if name and name:find('::allocation_epoch_successor',1,true)then tag='PHYSICAL'
 elseif name and name:find('::full_native_laser_audio',1,true)then tag='AUDIO'end
 if tag then
  assert(not parsed[tag]);parsed[tag]=true
  print(string.format('MK2_VARIANT_%s bytes=%d hex=%s',tag,#source,source:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  return function()end
 end
 return compiled
end
dofile('mk2ks_native_kano_laser_victim_audio.lua')
assert(parsed.PHYSICAL and parsed.AUDIO)
print('MK2_VARIANT_PARSE_RESULT gameplay_callbacks_executed=0 guest_writes=0')
actual_machine:exit()
