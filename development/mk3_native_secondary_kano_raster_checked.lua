-- Compatible raster observation and attainable physical attack spacing.
-- The original failed controller is frozen; game state is never written.
local filename='mk3_native_secondary_kano_reference.lua'
local file=assert(io.open(filename,'r'))
local source=file:read('a');file:close()
local before="local raw,w,h=machine.screens[':screen']:pixels()"
local after="local screen=machine.screens[':screen'];local raw=screen:pixels();local w,h=screen.width,screen.height"
local at=assert(source:find(before,1,true))
assert(not source:find(before,at+#before,true))
source=source:sub(1,at-1)..after..source:sub(at+#before)
local close_before='if gap>45 then press(forward)'
local close_after='if gap>65 then press(forward)'
local close_at=assert(source:find(close_before,1,true))
assert(not source:find(close_before,close_at+#close_before,true))
source=source:sub(1,close_at-1)..close_after..source:sub(close_at+#close_before)
assert(load(source,'@'..filename..'::only_raster_ABI_checked'))()
