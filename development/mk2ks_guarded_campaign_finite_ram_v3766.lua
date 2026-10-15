-- Original input-only campaign; change only the six PNG output sinks.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local path=assert(({kano='mk2ks_natural_campaign_shao_knife_retreat_v3510.lua',
 sonya='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'})[fighter])
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local adapted,count=source:gsub('screen:snapshot%(', '_campaign_emit(')
assert(count==6,'Exactly the six original PNG sinks, controls untouched')
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
-- Only the host observation deadline changes. Exit before MAME's -str
-- fallback, which otherwise writes an automatic PNG (video.cpp). This does
-- not supply inputs, alter the game clock, health, roster, AI or a victory.
local limit=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_OBSERVER_LIMIT')))
assert(limit==5900,'Declared finite observation window only')
emu.register_frame_done(function()
 if manager.machine.time:as_double()>=limit then
  print(string.format('MK2_CAMPAIGN_HOST_DEADLINE seconds=%.9f limit=%d assistance=none writes=0',
   manager.machine.time:as_double(),limit))
  manager.machine:exit()
 end
end)
