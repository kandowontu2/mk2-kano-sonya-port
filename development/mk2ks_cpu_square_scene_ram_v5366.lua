-- Original scene/input observer; original snapshot render target, RAM only.
local f=assert(io.open('mk2ks_cpu_square_scene_ram_v5357.lua','rb'))
local source=f:read('*a'):gsub('\r\n','\n');f:close()
local before='local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400);save(file,raw)'
local after='local video=manager.machine.video;local w,h=video:snapshot_size();assert(w==400 and h==254);local raw=video:snapshot_pixels();assert(#raw==406400);save(file,raw)'
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1)..after..source:sub(at+#before)
assert(load(source,'@entire_original_RAM_scene_snapshot_render_target_5366','t',_ENV))()
