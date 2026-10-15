-- Whole native parser diagnostic, no gameplay callback or guest write.
local native_load=load
emu.register_frame=function()end
emu.register_frame_done=function()end
emu.register_stop=function()end
local seen={}
local function emit(tag,source)
 assert(not seen[tag]);seen[tag]=true
 print(string.format('MK2_CS_PARSE_SOURCE kind=%s bytes=%d hex=%s',tag,#source,
  source:gsub('.',function(c)return string.format('%02x',c:byte())end)))
end
_G.load=function(source,name,mode,environment)
 local compiled,err=native_load(source,name,mode,environment);assert(compiled,err)
 if name=='@entire_original_nineteen_channel_observer'then emit('channels',source);return compiled end
 if name=='@entire_original_cpu_choke_wrapper'then emit('wrapper',source);return compiled end
 if name=='@mk2ks_cpu_recovery_probe_v1438.lua'then emit('physical',source);return function()end end
 if name=='@isolated_original_body_shadow_CPU_observer_v5328'then
  emit('body_shadow',source)
  local marker='-- BEGIN v1763 read-only consecutive move-phase observer'
  local at=assert(source:find(marker,1,true));assert(not source:find(marker,at+1,true))
  assert(native_load(source:sub(1,at-1),'@cpu_parser_prefix_only','t',environment))()
  return function()end
 end
 error('Unexpected actual compiler expansion '..tostring(name))
end
local file=assert(io.open('mk2ks_native_kano_laser_cpu_leg_repeat_p2.lua','rb'))
local root=file:read('*a');file:close()
assert(native_load(root,'@current_cpu_leg_repeat_p2_root','t',_G))()
assert(seen.channels and seen.wrapper and seen.physical and seen.body_shadow)
print('MK2_CS_PARSE_RESULT gameplay_callbacks_executed=0 guest_writes=0')
manager.machine:exit()
