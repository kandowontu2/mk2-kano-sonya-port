-- Same physical Kano guard/leg tactic, applied after unchanged opponent clones.
local base_path='mk2ks_sonya_extended_guard_base_ram_v5201.lua'
local function read(path)
 local file=assert(io.open(path,'rb'));local text=file:read('a');file:close();return text
end
local original=read(base_path)
local hook=[==[
-- The original Kitana/Jax/Subzero loaders have assembled replacement now.
local before="elseif strategy=='guard_punish' and other.roster==18 then"
local first=assert(replacement:find(before,1,true),'One assembled mirror leg/guard branch')
assert(not replacement:find(before,first+#before,true),'Unique assembled mirror leg/guard branch')
local last=assert(replacement:find("elseif strategy=='zoning' or strategy=='guard_punish' then",first,true))
local branch=replacement:sub(first,last-1)
local changed,count=branch:gsub('other%.roster==18','(other.roster==18 or other.roster==17)')
assert(count==5,'Only mirror branch eligibility/leg thresholds include CPU Kano')
changed,count=changed:gsub('other_now%.roster~=18','other_now.roster~=18 and other_now.roster~=17')
assert(count==1,'One passive true-CPU action observer includes Kano')
replacement=replacement:sub(1,first-1)..changed..replacement:sub(last)
print('MK2_CURRENT_CAMPAIGN_PHYSICAL_POLICY player=sonya slot=1 target_cpu=17 eligibility_changes=5 observer_changes=1 timing_changes=0 writes=0 assistance=none')
]==]
local needle='once(original,replacement)'
local first,last=original:find(needle,1,true)
assert(first and not original:find(needle,last+1,true),'One late assembled replacement boundary')
local adapted=original:sub(1,first-1)..hook..'\n'..needle..original:sub(last+1)
local scoped_io=setmetatable({open=function(path,mode)
 if path==base_path then
  assert(mode=='rb' or mode=='r')
  return {read=function(_,format)assert(format=='a' or format=='*a');return adapted end,
          close=function()return true end}
 end
 return io.open(path,mode)
end},{__index=io})
local environment=setmetatable({io=scoped_io},{__index=_ENV})
environment.dofile=function(path)
 return assert(load(read(path),'@'..path..'::scoped_read_only_late_loader','t',environment))()
end
local path='mk2ks_native_kano_laser_sonya_postending.lua'
assert(load(read(path),'@'..path..'::late_CPU_Kano_normal_guard_leg_inputs','t',environment))()
