-- Original physical campaign: change only six PNG sinks and one guest-file sink.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
assert(fighter=='sonya','Actual unfinished Sonya player-two campaign only')
local path='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local guest_sink="local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()"
local start=assert(source:find(guest_sink,1,true))
assert(not source:find(guest_sink,start+#guest_sink,true),'Exactly one original initialized guest sink')
source=source:sub(1,start-1)..'_campaign_guest(raw)'..source:sub(start+#guest_sink)
local adapted,count=source:gsub('screen:snapshot%(', '_campaign_emit(')
assert(count==6,'Exactly six original PNG sinks; physical inputs untouched')
local prefix=[[
local function _campaign_guest(raw)
 assert(#raw==1048576)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print(string.format('MK2_CAMPAIGN_GUEST_RAM frame=1 bytes=%d hex=%s',#raw,hex))
end
local function _campaign_emit(name)
 local s=manager.machine.screens[':screen']
 local raw,width,height=s:pixels()
 assert(width==400 and height==254 and #raw==width*height*4)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=%s seconds=%.9f width=%d height=%d bytes=%d hex=%s',
  name,manager.machine.time:as_double(),width,height,#raw,hex))
end
]]
assert(load(prefix..adapted,'@'..path..'::native_output_sinks_only','t',_ENV))()
