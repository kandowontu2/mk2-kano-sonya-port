-- Native installed parser, never execute UI/game/observer callbacks.
local actual=manager.machine
manager={machine={devices={[':maincpu']={spaces={program={}},state={}}}}}
emu={register_frame=function()end,register_sound_update=function()end,register_stop=function()end}
local native_load=load
local physical,audio=nil,nil
load=function(source,name,mode,environment)
 local fn,err=native_load(source,name,mode,environment or _G);assert(fn,err)
 if name=='@entire_original_UI_only_actual_displayed_RAM_sink'then
  assert(not physical);physical=source
  print(string.format('MK2_UI_PARSE_PHYSICAL bytes=%d hex=%s',#source,source:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  return function()end
 elseif name=='@entire_UI_audio_only_snapshot_return_signature_corrected'then
  assert(not audio);audio=source
  print(string.format('MK2_UI_PARSE_AUDIO bytes=%d hex=%s',#source,source:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
 return fn
end
dofile('mk2ks_native_kano_laser_ui.lua')
assert(physical and audio)
print('MK2_UI_PARSE_RESULT gameplay_callbacks_executed=0 guest_writes=0')
actual:exit()
