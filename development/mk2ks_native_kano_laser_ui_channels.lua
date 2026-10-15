-- Original full UI physical callback/snapshot sink, now observing all19 voices.
local filename='mk2ks_current_ui_audio_ram_v5430.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a'):gsub('\r\n','\n');file:close()
local before="local source=file:read('*a');file:close()"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
local after=before.."\nlocal expanded_count;source,expanded_count=source:gsub('for channel=0,13 do','for channel=0,18 do');assert(expanded_count==2)"
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@'..filename..'::all19channels_original_physical_UI','t',_G))()
