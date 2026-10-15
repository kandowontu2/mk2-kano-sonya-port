-- Compile every whole actual expansion; execute no gameplay callbacks or taps.
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
 local names={['@whole_current_cpu_children_root']='root_children',['@whole_current_cpu_leg_p2_root']='root_p2',
  ['@entire_original_nineteen_channel_observer']='channels',['@entire_original_cpu_choke_wrapper']='wrapper'}
 if names[name]then emit(names[name],source);return compiled end
 if name=='@mk2ks_cpu_recovery_probe_v1438.lua'then emit('physical',source);return function()end end
 if name=='@isolated_original_body_shadow_CPU_observer_v5328'then
  emit('body_shadow',source)
  local marker='-- BEGIN v1763 read-only consecutive move-phase observer'
  local at=assert(source:find(marker,1,true));assert(not source:find(marker,at+1,true))
  assert(native_load(source:sub(1,at-1),'@cpu_parser_prefix_only','t',environment))()
  return function()end
 end
 local passive={['@whole_original_passive_child_overlap']='child_overlap',
  ['@whole_original_passive_child_guard']='child_guard',['@whole_original_passive_round_observer']='round_observer'}
 if passive[name]then emit(passive[name],source);return function()end end
 error('Unexpected full native compiler expansion '..tostring(name))
end
local f=assert(io.open('mk2ks_native_kano_laser_cpu_post_ko.lua','rb'));local source=f:read('*a');f:close()
assert(native_load(source,'@current_native_post_KO_root','t',_G))()
for _,tag in ipairs({'root_children','root_p2','channels','wrapper','physical','body_shadow','child_overlap','child_guard','round_observer'})do assert(seen[tag])end
print('MK2_CS_PARSE_RESULT gameplay_callbacks_executed=0 guest_writes=0')
manager.machine:exit()
