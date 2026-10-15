-- All full actual native expansions; no gameplay callback or tap setup.
local native_load=load
emu.register_frame=function()end
emu.register_frame_done=function()end
emu.register_stop=function()end
local seen={}
local function emit(tag,s)
 assert(not seen[tag]);seen[tag]=true
 print(string.format('MK2_CS_PARSE_SOURCE kind=%s bytes=%d hex=%s',tag,#s,s:gsub('.',function(c)return string.format('%02x',c:byte())end)))
end
_G.load=function(s,name,mode,env)
 local compiled,err=native_load(s,name,mode,env);assert(compiled,err)
 local roots={['@whole_original_post_KO_root_adaptive_deadline']='root_post',
  ['@whole_current_cpu_children_root']='root_children',['@whole_current_cpu_leg_p2_root']='root_p2',
  ['@entire_original_nineteen_channel_observer']='channels',['@entire_original_cpu_choke_wrapper']='wrapper'}
 if roots[name]then emit(roots[name],s);return compiled end
 if name=='@mk2ks_cpu_recovery_probe_v1438.lua'then emit('physical',s);return function()end end
 if name=='@isolated_original_body_shadow_CPU_observer_v5328'then
  emit('body_shadow',s)
  local marker='-- BEGIN v1763 read-only consecutive move-phase observer'
  local at=assert(s:find(marker,1,true));assert(not s:find(marker,at+1,true))
  assert(native_load(s:sub(1,at-1),'@cpu_parser_prefix_only','t',env))()
  return function()end
 end
 local observers={['@whole_original_passive_child_overlap']='child_overlap',
  ['@whole_original_passive_child_guard']='child_guard',['@whole_original_passive_round_observer']='round_observer',
  ['@whole_original_adaptive_post_reset_human_controls']='post_controls'}
 if observers[name]then emit(observers[name],s);return function()end end
 error('Unexpected full native compiler expansion '..tostring(name))
end
local f=assert(io.open('mk2ks_native_kano_laser_post_reset_controls.lua','rb'));local s=f:read('*a');f:close()
assert(native_load(s,'@native_post_reset_adaptive_root','t',_G))()
for _,tag in ipairs({'root_post','root_children','root_p2','channels','wrapper','physical','body_shadow','child_overlap','child_guard','round_observer','post_controls'})do assert(seen[tag])end
print('MK2_CS_PARSE_RESULT gameplay_callbacks_executed=0 guest_writes=0')
manager.machine:exit()
