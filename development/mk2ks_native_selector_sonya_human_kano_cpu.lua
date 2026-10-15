-- Opposite real role pairing; one existing physical-input controller.
-- Bind nested loaders to one environment so passive drawing/audio filters
-- actually apply. CPU character/AI/RNG/HP/positions are never supplied.
local env=setmetatable({}, {__index=_G});env._G=env
local loads={}
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
env.dofile=function(path)
 local file=assert(io.open(path,'rb'));local source=file:read('a'):gsub('\r\n','\n');file:close()
 loads[path]=(loads[path]or 0)+1
 print('MK2_OPPOSITE_OBSERVER_LOAD path='..path..' count='..loads[path]..' writes=0 assistance=none')
 if path=='mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua' then
  local marker="assert(load(source,'@whole_current_natural_startup_PCM_direct_source','t',_G))()"
  source=change(source,marker,
   "replace('p:read_u16(0x01060280)==17','p:read_u16(0x01060280)==18')\n"..marker)
 elseif path=='mk2ks_native_selector_cpu_guard_shadow.lua' then
  assert(loads[path]==1)
  source=change(source,'a.id==17 and b.id==17 and','a.id==18 and b.id==17 and')
  source=change(source,'a.roster==17 and b.roster==17 and','a.roster==18 and b.roster==17 and')
  local marker=']==]\nroot=root:sub(1,first-1)'
  source=change(source,marker,[==[
change('a.id==17 and b.id==17 and a.roster==17 and b.roster==17',
       'a.id==18 and b.id==17 and a.roster==18 and b.roster==17')
]==]..'\n'..marker)
  print('MK2_OPPOSITE_SHADOW_BIND count=1 human=18 cpu=17 writes=0 assistance=none')
 end
 return assert(load(source,'@whole_opposite_role_'..path,'t',env))()
end
env.dofile('mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua')
