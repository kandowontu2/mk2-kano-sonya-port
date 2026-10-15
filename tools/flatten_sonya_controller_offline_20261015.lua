-- Standalone Lua source transformation only. No emulator objects exist here.
local real_io,real_load=io,load
local trace={}
local output='video_sonya_full_20261015_preparation/expanded_historical_controller.lua'
local captured=false
io.open=function(path,mode)
 assert((mode=='r'or mode=='rb')and type(path)=='string'and path:match('^mk2ks_[%w_]+%.lua$'),'Only named source reads allowed')
 trace[#trace+1]=path;assert(#trace<=32)
 local f=assert(real_io.open(path,mode));return f
end
local env={MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='2',MK2KS_CAMPAIGN_STRATEGY='guard_punish',MK2KS_TEST_BOOT_FRAME='600',MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'}
os={getenv=function(k)return env[k]end}
dofile=function()error('Unexpected dofile before source captured')end
load=function(source,name,mode,environment)
 assert(type(source)=='string'and #source<1024*1024,'Bounded source strings')
 if source:find('local function _campaign_guest(raw)',1,true)and source:find('-- Cold campaign, genuine losses/paid continues.',1,true)then
  assert(not captured);captured=true
  local f=assert(real_io.open(output,'wb'));f:write(source);f:close()
  local t=assert(real_io.open('video_sonya_full_20261015_preparation/offline_read_trace.txt','wb'))
  t:write(table.concat(trace,'\n'));t:close()
  return function()error('SOURCE_CAPTURED_BEFORE_ANY_GUEST_EXECUTION')end
 end
 return real_load(source,name,mode,environment)
end
local first=assert(io.open('mk2ks_sonya_p2_verified_subzero_campaign_v5687.lua','rb'))
local source=first:read('a');first:close()
local ok,err=pcall(assert(load(source,'@historical_entry','t',_ENV)))
assert(not ok and captured and tostring(err):find('SOURCE_CAPTURED_BEFORE_ANY_GUEST_EXECUTION',1,true),tostring(err))
print('OFFLINE_SOURCE_CAPTURED reads='..#trace..' no_emulator=true no_guest_execution=true')
