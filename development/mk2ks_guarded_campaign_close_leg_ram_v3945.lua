-- Original input-only campaign, closer physical leg attempt; RAM-only sinks.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
assert(fighter=='sonya','Specific ordinary leg physical-control trial only')
local path=assert(({kano='mk2ks_natural_campaign_shao_knife_retreat_v3510.lua',
 sonya='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'})[fighter])
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
-- Change only how close the human test controller walks before attempting
-- the original Down+LP+Block input. No action/health/AI/clock/schedule writes.
local old='leg_tactic and 85 or 70'
local start=assert(source:find(old,1,true))
assert(not source:find(old,start+#old,true),'One ordinary-leg threshold only')
source=source:sub(1,start-1)..'leg_tactic and 63 or 70'..source:sub(start+#old)
local adapted,count=source:gsub('screen:snapshot%(', '_campaign_emit(')
assert(count==6,'Exactly the six original PNG sinks, otherwise controls untouched')
local prefix=[[
local function _campaign_emit(name)
 local s=manager.machine.screens[':screen']
 local raw,width,height=s:pixels()
 assert(width==400 and height==254 and #raw==width*height*4)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=%s seconds=%.9f width=%d height=%d bytes=%d hex=%s',
  name,manager.machine.time:as_double(),width,height,#raw,hex))
end
]]
assert(load(prefix..adapted,'@'..path..'::PNG_sink_only','t',_ENV))()
