-- Preserve every actual passive handoff/cache observer and whole Kano driver.
local function read(path)
 local file=assert(io.open(path,'rb'));local source=file:read('a');file:close();return source
end
local environment=setmetatable({},{__index=_ENV})
environment.dofile=function(path)
 local source=read(path)
 if path=='mk2ks_native_kano_paired_stumble_cache_guard.lua' then
  local before="local after=\"dofile('mk2ks_current_kano_p1_campaign_ram_v5194.lua')\""
  local after="local after=\"dofile('mk2ks_native_kano_kitana_reactive_driver.lua')\""
  local first,last=source:find(before,1,true)
  assert(first and not source:find(before,last+1,true),'One whole existing cache-guard driver route')
  source=source:sub(1,first-1)..after..source:sub(last+1)
 end
 return assert(load(source,'@'..path..'::whole_original_observers_and_Kano_driver','t',environment))()
end
assert(load(read('mk2ks_native_kano_paired_stumble_campaign.lua'),
 '@mk2ks_native_kano_paired_stumble_campaign.lua::unchanged_paired_victim_observer','t',environment))()
