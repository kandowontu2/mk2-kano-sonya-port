-- Same actual physical D,F,LP/thaw/control test; every live shadow field.
-- No guest/register/health/cache/state writes or artificial transitions.
local file=assert(io.open('mk2ks_normal_subzero_freeze_projection_v5043.lua','rb'))
local source=file:read('a');file:close()
local before='not first_live or not marks[frame-first_live]'
local count
source,count=source:gsub(before:gsub('([%(%)%.%%%+%-%*%?%[%]%^%$])','%%%1'),function()
 return 'not first_live or frame-first_live<0 or frame-first_live>700'
end)
assert(count==2,'Both actual DMA and projection observations span complete701live fields')
source,count=source:gsub('marks%[frame%-first_live%]',function()return "(marks[frame-first_live]or'live')"end)
assert(count==3,'Actual unmarked DMA/projection/part fields retain explicit live label')
assert(load(source,'@current_complete_normal_freeze_native_shadow_fields','t',_ENV))()
