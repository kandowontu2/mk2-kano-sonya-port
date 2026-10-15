-- Distinct real human policy: hold Block throughout live play, including grabs.
-- Keep every original passive observer and the single original controller.
local file=assert(io.open('mk2ks_native_selector_cpu_sonya_extended_ram.lua','rb'))
local extended=file:read('*a'):gsub('\r\n','\n');file:close()
local function replace_once(source,before,after)
 local at=assert(source:find(before,1,true));assert(not source:find(before,at+#before,true))
 return source:sub(1,at-1)..after..source:sub(at+#before)
end
local before=[[                      "dofile('mk2ks_physical_p2_cpu_overlap_trace_v1942.lua')")
 end
]]
local after=[[                      "dofile('mk2ks_physical_p2_cpu_overlap_trace_v1942.lua')")
 elseif path=='mk2ks_physical_p2_cpu_continuation_v3300.lua'then
  source=replace_once(source,"    state('FIELD',s,v)\n",
   "    state('FIELD',s,v)\n    fields['P1 Block']:set_value(1)\n    log('CONTINUOUS_GUARD_INPUT',string.format('policy=continuous_guard buttons=Block actor=%08X main=%08X hp=%d',v.actor,v.main,v.hp))\n")
 end
]]
extended=replace_once(extended,before,after)
-- Only substitute this exact immutable Lua source read while loading the
-- synchronous observer chain. Restore the native file API before gameplay.
local original_open=io.open
local reads=0
io.open=function(path,mode)
 if path=='mk2ks_native_selector_cpu_sonya_extended_ram.lua'then
  assert(mode=='rb');reads=reads+1;assert(reads==1)
  return {read=function(_,kind)assert(kind=='*a');return extended end,close=function()end}
 end
 return original_open(path,mode)
end
dofile('mk2ks_native_selector_cpu_sonya_startup_guard_bound.lua')
io.open=original_open
assert(reads==1,'One original controller with continuous physical Block policy')
print('MK2_CONTINUOUS_GUARD_SOURCE policy=continuous_guard controllers=1 writes=0 assistance=none')
