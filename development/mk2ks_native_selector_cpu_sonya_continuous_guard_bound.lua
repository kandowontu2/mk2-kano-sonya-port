-- Native dofile loads from its own file API, not Lua io.open. Bind exactly
-- the one driver load; preserve the failed pregame adapter and its receipt.
local file=assert(io.open('mk2ks_native_selector_cpu_sonya_continuous_guard.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local at=assert(source:find('local original_open=io.open',1,true))
assert(not source:find('local original_open=io.open',at+1,true))
source=source:sub(1,at-1)..[[
local original_dofile=dofile
local reads=0
dofile=function(path)
 if path=='mk2ks_native_selector_cpu_sonya_extended_ram.lua'then
  reads=reads+1;assert(reads==1)
  return assert(load(extended,'@whole_original_Sonya_controller_continuous_physical_Block','t',_G))()
 end
 return original_dofile(path)
end
original_dofile('mk2ks_native_selector_cpu_sonya_startup_guard_bound.lua')
dofile=original_dofile
assert(reads==1,'One original controller with continuous physical Block policy')
print('MK2_CONTINUOUS_GUARD_SOURCE policy=continuous_guard controllers=1 writes=0 assistance=none')
]]
assert(load(source,'@whole_continuous_guard_native_dofile_binding','t',_G))()
