-- Only ordinary Sonya test tactics against actual CPU Kano change.
-- Reuse the proven mirror guard/leg edges, not new game state or AI writes.
-- All other controller branches, tower/ending/fresh Kano join remain intact.
local base_path='mk2ks_sonya_extended_guard_base_ram_v5201.lua'
local function read(path)
 local file=assert(io.open(path,'rb'));local text=file:read('a');file:close();return text
end
local original=read(base_path)
local before="elseif strategy=='guard_punish' and other.roster==18 then"
local first=assert(original:find(before,1,true),'One existing mirror leg/guard branch')
assert(not original:find(before,first+#before,true),'Unique existing mirror leg/guard branch')
local last=assert(original:find("elseif strategy=='zoning' or strategy=='guard_punish' then",first,true))
local branch=original:sub(first,last-1)
local changed,count=branch:gsub('other%.roster==18','(other.roster==18 or other.roster==17)')
assert(count==5,'Only existing mirror branch eligibility/leg thresholds change for CPU Kano')
changed,count=changed:gsub('other_now%.roster~=18','other_now.roster~=18 and other_now.roster~=17')
assert(count==1,'One passive true-CPU action observer includes Kano')
local adapted=original:sub(1,first-1)..changed..original:sub(last)
local scoped_io=setmetatable({open=function(path,mode)
 if path==base_path then
  assert(mode=='rb' or mode=='r','Read-only whole original guard base')
  return {read=function(_,format)assert(format=='a' or format=='*a');return adapted end,
          close=function()return true end}
 end
 return io.open(path,mode)
end},{__index=io})
local environment=setmetatable({io=scoped_io},{__index=_ENV})
-- Lua's builtin dofile uses the global environment. Keep the explicit
-- read-only loader environment through the outer passive observer wrapper.
environment.dofile=function(path)
 return assert(load(read(path),'@'..path..'::scoped_read_only_loader','t',environment))()
end
local path='mk2ks_native_kano_laser_sonya_postending.lua'
assert(load(read(path),'@'..path..'::only_CPU_Kano_normal_guard_leg_inputs','t',environment))()
