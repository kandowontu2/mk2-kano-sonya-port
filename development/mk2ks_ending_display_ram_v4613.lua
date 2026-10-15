-- Entire frozen4542 read-only observer, plus actual scanout registers only.
local h=assert(io.open('mk2ks_ending_display_ram_v4542.lua','r'))
local source=h:read('a');h:close()
local boundary="assert(not source:find('io.open',1,true)"
local insertion=[[once("log('FLOOR_DISPLAY',", "log('FLOOR_SCANOUT',string.format('epoch=1 start=%04X dpyadr=%04X control=%04X tap=%04X vcount=%d vsblnk=%d veblnk=%d',p:read_u16(0xc0000090),p:read_u16(0xc00001e0),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),p:read_u16(0xc00001d0),p:read_u16(0xc0000060),p:read_u16(0xc0000050)))\n log('FLOOR_DISPLAY',")
]]
local at=assert(source:find(boundary,1,true),'One original read-only observer boundary')
assert(not source:find(boundary,at+#boundary,true),'Unique original read-only observer boundary')
source=source:sub(1,at-1)..insertion..source:sub(at)
assert(load(source,'@entire4542_ending_with_actual_native_scanout_4613','t',_ENV))()
