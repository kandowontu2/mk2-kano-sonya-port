-- Native parser diagnostic only; no game or observer callbacks executed.
local actual=manager.machine;local native_load=load;local compiled=nil
_G.emu={register_frame=function()end}
_G.load=function(source,name,mode,environment)
 local fn,err=native_load(source,name,mode,environment or _G);assert(fn,err)
 if name=='@entire_original_special_shadow_controller'then
  assert(not compiled);compiled=source
  print(string.format('MK2_SS_PARSE_PHYSICAL bytes=%d hex=%s',#source,source:gsub('.',function(c)return string.format('%02X',c:byte())end)))
  return function()end
 end
 return fn
end
dofile('mk2ks_native_kano_laser_special_shadow.lua')
assert(compiled)
print('MK2_SS_PARSE_RESULT gameplay_callbacks_executed=0 guest_writes=0')
actual:exit()
